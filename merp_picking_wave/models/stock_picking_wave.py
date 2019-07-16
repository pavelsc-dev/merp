# Copyright 2019 VentorTech OU
# Part of Ventor modules. See LICENSE file for full copyright and licensing details.

from odoo import models, api, _


class PickingWave(models.Model):
    _inherit = 'stock.picking.batch'

    @api.multi
    def done_outgoing(self):
        behavior = self.env.user.company_id.outgoing_wave_behavior_on_confirm
        message_obj = self.env['message.wizard']
        res = True
        # i.e. close pickings in wave with/without creating backorders
        if behavior in (0, 1):
            for wave in self:
                for picking in wave.picking_ids:
                    picking.check_behavior_0()
                    backorder_pick = self.env['stock.picking'].search([('backorder_id', '=', picking.id)])
                    if backorder_pick:
                        backorder_pick.write({'batch_id': False})
                        if behavior == 1:
                            # i.e. close pickings in wave without creating backorders
                            backorder_pick.action_cancel()
                            self.message_post(
                                body=_("Back order <em>%s</em> <b>cancelled</b>.") % (backorder_pick.name))
            res = super(PickingWave, self).done()

        # i.e. move wave to on hold if not all pickings are confirmed
        elif behavior == 2:
            for wave in self:
                for picking in wave.picking_ids:
                    on_hold = picking.check_behavior_2()
                    if on_hold:
                        wave.write({'state': 'on_hold'})
                        message = _('''
                        Not all products were found in wave pickings.
                        Wave is moved to "On Hold" for manual processing.
                        ''')
                        return message_obj.with_context(message=message).wizard_view()
                    self.write({'state': 'done'})
        return res

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.model
    def search_pickings_to_pick(self, name, warehouse_id):
        warehouse = self.env['stock.warehouse'].browse(warehouse_id)
        if warehouse.delivery_steps == 'ship_only':
            picking_type_id = warehouse.out_type_id.id
        else:
            picking_type_id = warehouse.pick_type_id.id
        return self.search_read(domain=[
            ('picking_type_id', '=', picking_type_id),
            ('state', 'in', ('assigned', 'partially_available')),
            '|',
            ('name', '=', name),
            ('origin', '=', name)])

    def check_behavior_0(self):
        self.ensure_one()
        remove_not_moved = self.env.user.company_id.outgoing_wave_remove_not_moved
        if self.state in ('cancel', 'done'):
            return
        picking_not_moved = all([x.qty_done == 0.0 for x in self.move_line_ids])
        if remove_not_moved and (self.state == 'draft' or picking_not_moved):
            # In draft or with no pack operations edited yet,
            # remove from wave
            self.batch_id = False
            return
        if self.state != 'assigned':
            self.action_assign()
        if self.state == 'assigned' and picking_not_moved:
            for move in self.move_lines.filtered(lambda m: m.state not in ['done', 'cancel']):
                for move_line in move.move_line_ids:
                    move_line.qty_done = move_line.product_uom_qty
        self.action_done()

    def check_behavior_2(self):
        on_hold = False
        if self.state in ('cancel', 'done'):
            on_hold = False
        elif self.state != 'assigned':
            on_hold = True
        else:
            if not self.move_line_ids:
                self.do_prepare_partial()
            if self.move_line_ids.filtered(lambda o: o.qty_done < o.product_qty):
                on_hold = True
            else:
                self.do_transfer()
        return on_hold

# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class GestionBatiment(models.Model):
    _name = 'gestion.batiment'
    _description = 'hotel_gestion.hotel_gestion'

    Bat_ID = fields.Char()
    Ville = fields.Char()
    batiment_proprie = fields.Char()
    description = fields.Text()

    def open_chbr_gestion(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Chambres',
            'view_mode': 'tree,form',
            'res_model': 'chbr.gestion',
            'target': 'current',
        }

    def open_client_gestion(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Clients',
            'view_mode': 'tree,form',
            'res_model': 'client.gestion',
            'target': 'current',
        }
    def open_gestion_comodite(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Commodités',
            'view_mode': 'tree,form',
            'res_model': 'comodite.gestion',
            'target': 'current',
        }

    def open_reservation_gestion(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Réservations',
            'view_mode': 'tree,form',
            'res_model': 'reserve.gestion',
            'target': 'current',
        }

class ChambreGestion(models.Model):
    _name = 'chbr.gestion'
    _description = 'hotel_gestion.hotel_gestion'

    nbr_pieces = fields.Integer()
    numro_chambre = fields.Integer()
    chmabre_type = fields.Selection([
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
        ('deluxe', 'Deluxe')
    ], string="Type de Chambre")
    statut = fields.Selection([
        ('libre', 'Libre'),
        ('occupe', 'Occupé')
    ], string="Statut")
    description = fields.Text()
    batiment_chambre = fields.Many2many('gestion.batiment', string='Bâtiment de la chambre', required=True)
    prix = fields.Float(string='Prix')

    @api.onchange('chmabre_type')
    def _onchange_chmabre_type(self):
        if self.chmabre_type == 'single':
            self.prix = 50000
        elif self.chmabre_type == 'double':
            self.prix = 100000
        elif self.chmabre_type == 'suite':
            self.prix = 150000
        elif self.chmabre_type == 'deluxe':
            self.prix = 200000

class ComoditeGestion(models.Model):
     _name = 'comodite.gestion'
     _description = 'comodite_gest'

     room_service = fields.Char()

class ClientsGestion(models.Model):
     _name = 'client.gestion'
     _description = 'aaaaaa'

     nom = fields.Char()
     prenom = fields.Char()
     id_numero = fields.Char(required=True)
     nbr_reservation = fields.Integer()
     numero_de_chambre = fields.Many2many('chbr.gestion', string='Numéro de chambre', required=True)

class ReservationGestion(models.Model):
    _name = 'reserve.gestion'
    _description = 'aaaaaa'

    type_de_chambre = fields.Char()
    date_debut = fields.Datetime(string='Date de début', required=True)
    date_fin = fields.Datetime(string='Date de fin', required=True)
    numero_de_chambre = fields.Many2many('chbr.gestion', string='Numéro de chambre', required=True)
    clients = fields.Many2many('client.gestion', string='Client', required=True)
    comodite = fields.Many2many('comodite.gestion', string='Service')
    payement = fields.Many2many('payement.gestion', string='Type de paiement')

    @api.constrains('date_debut', 'date_fin', 'numero_de_chambre')
    def _check_chambre_reservation(self):
        for reservation in self:
            if reservation.date_debut >= reservation.date_fin:
                raise ValidationError("La date de début doit être avant la date de fin.")

            existing_reservations = self.env['reserve.gestion'].search([
                ('numero_de_chambre', 'in', reservation.numero_de_chambre.ids),
                ('id', '!=', reservation.id),
                ('date_debut', '<=', reservation.date_fin),
                ('date_fin', '>=', reservation.date_debut),
            ])

            if existing_reservations:
                raise ValidationError("La chambre est déjà réservée pour cette période.")

class PayementGestion(models.Model):
    _name = 'payement.gestion'
    _description = 'Gestion des paiements'

    type_de_payement = fields.Selection([
        ('carte_credit', 'Carte de Crédit'),
        ('virement', 'Virement Bancaire'),
        ('especes', 'Espèces'),
        ('cheque', 'Chèque')
    ], string='Type de paiement', required=True)

    statut_de_payement = fields.Selection([
        ('paye', 'Payé'),
        ('non_paye', 'Non Payé')
    ], string='Statut de paiement', required=True)

    montant = fields.Selection([
        ('50000', '50 000'),
        ('200000', '200 000'),
        ('25000', '25 000'),
        ('150000', '150 000')
    ], string='Montant', required=True)

class EspacesGestion(models.Model):
     _name = 'epaces.gestion'
     _description = 'aaaaaa'

     type_de_d_espace = fields.Char()
     statut_de_espace = fields.Char()

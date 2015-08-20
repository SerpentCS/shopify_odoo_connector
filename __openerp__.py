# -*- coding: utf-8 -*-
##############################################################################
#
#    Author: David BEAL, Copyright Akretion, 2014
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{'name': 'Shopify Connector',
 'version': '1.0',
 'author': "Openerp Connector Core Editors,Odoo Community Association (OCA)",
 'website': 'http://odoo-connector.com',
 'license': 'AGPL-3',
 'category': 'Connector',
 'description': """
Connector Base Product
======================

Add 'Connector' tab to product view
""",
 'depends': [
     'connector',
     'sale',
     'account',
     'sale_stock',
     'delivery',
 ],
 'data': [
          'views/shopify_model_view.xml',
          'views/shopifyodooconnect_menu.xml',
 ],
 'installable': True,
 }

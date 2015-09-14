# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011-Till Today Serpent Consulting Services PVT LTD (<http://www.serpentcs.com>)
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
############################################################################

import shopify
import urllib
import os
import base64#file encode
import urllib2 #file download from url
from openerp import models, fields, api, _
from openerp.exceptions import Warning
from openerp.addons.connector.session import ConnectorSession
from datetime import datetime


class Shopify(models.Model):
    _name = 'shopify.backend'

    @api.model
    def _get_stock_field_id(self):
        field = self.env['ir.model.fields'].search(
            [('model', '=', 'product.product'),
             ('name', '=', 'virtual_available')],
            limit=1)
        return field
    
    name = fields.Char("Name", required = True)
    shopify_url = fields.Char("Shopify Url", required = True)
    connection = fields.Boolean("synchronize")
    default_lang_id = fields.Many2one(
        comodel_name='res.lang',
        string='Default Language',
        help="If a default language is selected, the records "
             "will be imported in the translation of this language.\n"
             "Note that a similar configuration exists "
             "for each storeview.",
    )
    default_category_id = fields.Many2one(
        comodel_name='product.category',
        string='Default Product Category',
        help='If a default category is selected, products imported '
             'without a category will be linked to it.',
    )
    
    api_key = fields.Char("Api Key", required = True)
    password = fields.Char("Password", required = True)
    warehouse_id = fields.Many2one(
        comodel_name='stock.warehouse',
        string='Warehouse',
        required=True,
        help='Warehouse used to compute the '
             'stock quantities.',
    )
    sale_prefix = fields.Char(
        string='Sale Prefix',
        help="A prefix put before the name of imported sales orders.\n"
             "For instance, if the prefix is 'mag-', the sales "
             "order 100000692 in Magento, will be named 'mag-100000692' "
             "in OpenERP.",
    )
    product_stock_field_id = fields.Many2one(
        comodel_name='ir.model.fields',
        string='Stock Field',
        default=_get_stock_field_id,
        domain="[('model', 'in', ['product.product', 'product.template']),"
               " ('ttype', '=', 'float')]",
        help="Choose the field of the product which will be used for "
             "stock inventory updates.\nIf empty, Quantity Available "
             "is used.",
    )
    import_products_from_date = fields.Datetime("Import product from")
    import_categories_from_date = fields.Datetime("Import category from")

    @api.multi
    def test_connection(self):
        for backend in self:
            try:
                shop_url = backend.shopify_url % (backend.api_key , backend.password)
                shopify.ShopifyResource.set_site(shop_url)
                shop = shopify.Shop.current()
                backend.write({'connection': 'TRUE'})
            except Exception:
                raise Warning(_('UnauthorizedAccess: "[API] Invalid API key or access token (unrecognized login or wrong password)'))

    @api.one
    def import_product_categories(self):
        self.import_categories_from_date = datetime.now()
        if self.search([('connection','=',True), ('id','=',self.id)]):
            shopify_collection = shopify.CustomCollection.find()
            if shopify_collection:
                for category in shopify_collection:
                    dict_category = category.__dict__['attributes']
                    vals = {'name': dict_category['title'],
                            'write_uid': self.env.uid,
                            'parent_id': 2,
                            'shopify_product_cate_id': dict_category['id'],}
                    session = ConnectorSession(self.env.cr, self.env.uid,
                           context=self.env.context)
                    product_cate_id = self.env['product.category'].search([('shopify_product_cate_id',
                                                                            '=',dict_category['id'])])
                    if not product_cate_id:
                        session.create('product.category', vals)
                    else:
                        session.write('product.category',product_cate_id.id, vals)
        else:
            raise Warning(_('Please enter proper shopify store details!'))

    @api.multi
    def import_product_product(self):
        try:
            shop_url = self.shopify_url % (self.api_key , self.password)
            shopify.ShopifyResource.set_site(shop_url)
            shop = shopify.Shop.current()
        except Exception:
            raise Warning(_('UnauthorizedAccess: "[API] Invalid API key or access token (unrecognized login or wrong password)"}'))
        
        products = shopify.Product.find()
        product_tmpl_env = self.env['product.template']
        product_product_env = self.env['product.product']
        product_cate_env = self.env['product.category']
        for product in products:
            vals_product_tmpl = {}
            vals_product_product = {}
            dict_attr = product.__dict__['attributes']
            list_variant = dict_attr['variants']
            dict_variant = list_variant[0].__dict__['attributes']
            
            product_odoo = product_tmpl_env.search([('shopify_product_id', '=', dict_attr['id'])])
            if not product_odoo:
                image_urls = [getattr(i, 'src') for i in product.images]
                if len(image_urls)>0:
                    photo = base64.encodestring(urllib2.urlopen(image_urls[0]).read())
                    vals_product_tmpl.update({'image_medium':photo})
                
                custom_collection = shopify.CustomCollection.find(product_id = dict_attr['id'])
                if custom_collection:
                    for categ in custom_collection:
                        product_cate_obj = product_cate_env.search([('shopify_product_cate_id','=',categ.__dict__['attributes']['id'])])
                        if product_cate_obj:
                            vals_product_tmpl.update({'categ_id':product_cate_obj.id})
                            
                vals_product_tmpl.update({'name':dict_attr['title'],
                            'type':'consu',
                            'shopify_product_id':dict_attr['id'],
                            'description':dict_attr['body_html'],
                            'state':'add',
                            'list_price':dict_variant['price'],
                            'standard_price':dict_variant['compare_at_price'],
                            'volume':dict_variant['inventory_quantity']})
                
                product_tid = product_tmpl_env.create(vals_product_tmpl)
                
                for i in list_variant:
                    dict_vari = {}
                    dict_vari = i.__dict__
                    vals_product_product.update({'product_tmpl_id':product_tid.id,
                                                 'product_sfy_variant_id':dict_vari['attributes']['id'],})
                    product_product_env.create(vals_product_product)

    @api.multi
    def update_product_stock_qty(self):
        print "======"
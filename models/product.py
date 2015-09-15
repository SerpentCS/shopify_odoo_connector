from openerp import models, fields, api, _
import shopify

class product_template(models.Model):
    _inherit = 'product.template'

    state = fields.Selection([('draft','Draft'),('add','Add To Shopify'),('update','Update To Shopify')], "Status", default='draft')
    shopify_product_id = fields.Char('Shopify Product')
#     @api.one
#     def add_product(self):
#         self.state='add'
#         print "-------===-----",self.id,self.name,self.type,self.list_price,"Weight",self.weight,"vol",self.volume,"SKU",self.default_code
#         shop_url = "https://%s:%s@bipin-10.myshopify.com/admin" % ("313d144e627109997936e29461f1b941" , "4b102ac422007609308eef325c6ebda7")
#         shopify.ShopifyResource.set_site(shop_url)
#         
#         shop = shopify.Shop.current()
#         
#         new_product = shopify.Product()
#         new_product.title = self.name
#         new_product.body_html = self.description
#         if self.type == 'consu':
#             new_product.product_type = "Consumable"
#         if self.type == 'service':
#             new_product.product_type = "Service"
#         variant1 = shopify.Variant(dict(price=self.list_price, weight=self.weight, compare_at_price=self.standard_price )) # attributes can     be set at creation
#         new_product.variants = [variant1]
#         success = new_product.save() #returns false if the record is invalid
#         print "\n\n----------success",success,"NEW PRODUCR ID::::",new_product.id
#         self.shopify_product_id = new_product.id
#         product_obj = self.env['product.product']
#         product_obj.create({'product_sfy_variant_id':'1111111'})
#         
#     @api.multi
#     def update_product(self):
#         product_product_env = self.env['product.product']
#         products = product_product_env.search([('product_tmpl_id', '=', self.id)])
#         for product in products:
#             print "\n=====",product.product_sfy_variant_id
#         
#         shop_url = "https://%s:%s@bipin-10.myshopify.com/admin" % ("313d144e627109997936e29461f1b941" , "4b102ac422007609308eef325c6ebda7")
#         shopify.ShopifyResource.set_site(shop_url)
#         shop = shopify.Shop.current()
#         product_shopify = shopify.Product(dict(id=self.shopify_product_id))
#         
#         product_shopify.title = self.name
#         product_shopify.body_html = self.description
#         if self.type == 'consu':
#             product_shopify.product_type = "Consumable"
#         if self.type == 'service':
#             product_shopify.product_type = "Service"
#         success = product_shopify.save() #returns false if the record is invalid
#         print "\n\n----------successsssss",success
#         
#         '''product_obj = i.env['product.product']
#         product_odoo = product_obj.search([('product_tmpl_id', '=', self.id)])
#         print "SSSSSS",product_odoo
#         for p_line in product_odoo:
#             for p_line_attr in p_line.attribute_value_ids:
#                 print p_line_attr.name'''
class product_product(models.Model):
    _inherit = 'product.product' 
    
    product_sfy_variant_id = fields.Char("Shopify Product Variant")
    
class product_category(models.Model):
    _inherit = 'product.category'

    description = fields.Text('Description')
    shopify_product_cate_id = fields.Char('Shopify Product Category')

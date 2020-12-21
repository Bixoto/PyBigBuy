# -*- coding: utf-8 -*-

"""
bigbuy.endpoints
~~~~~~~~~~~~~~~~~

This module provides a mixin for a :class:`Bigbuy <Bigbuy>` instance.
Parameters that need to be embedded in the API url just need to be passed
as a keyword argument.


Official documentation for Bigbuy API endpoints can be found at:
https://api.bigbuy.eu/doc
"""


class EndpointsMixin(object):
    def get(self, *args, **kwargs):
        raise NotImplementedError()

    def post(self, *args, **kwargs):
        raise NotImplementedError()

    # catalog
    def get_attribute(self, attribute_id, **params):
        """Get a single attribute.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-attribute-{id}.{_format}

        """
        return self.get('catalog/attribute/%s' % attribute_id, params=params)

    def get_attribute_all_languages(self, attribute_id, **params):
        """Get a single attribute.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-attributealllanguages-{id}.{_format}

        """
        return self.get('catalog/attributealllanguages/%s' % attribute_id, params=params)

    def get_attribute_group(self, attribute_group_id, **params):
        """Get a single attribute group.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-attributegroup-{id}.{_format}

        """
        return self.get('catalog/attributegroup/%s' % attribute_group_id, params=params)

    def get_attribute_group_all_languages(self, attribute_group_id, **params):
        """Get a single attribute group.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-attributegroupalllanguages-{id}.{_format}

        """
        return self.get('catalog/attributegroupalllanguages/%s' % attribute_group_id, params=params)

    def get_attribute_groups(self, **params):
        """Lists all attribute groups.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-attributegroups.{_format}

        """
        return self.get('catalog/attributegroups', params=params)

    def get_attributes(self, **params):
        """Lists all attributes.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-attributes.{_format}

        """
        return self.get('catalog/attributes', params=params)

    def get_categories(self, **params):
        """Lists all categories.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-categories.{_format}

        """
        return self.get('catalog/categories', params=params)

    def get_category(self, category_id, **params):
        """Returns the selected category.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-category-{id}.{_format}

        """
        return self.get('catalog/category/%s' % category_id, params=params)

    def get_category_all_languages(self, category_id, **params):
        """Returns the selected category.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-categoryalllanguages-{id}.{_format}

        """
        return self.get('catalog/categoryalllanguages/%s' % category_id, params=params)

    def get_languages(self, **params):
        """Returns all languages

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-languages.{_format}

        """
        return self.get('catalog/languages', params=params)

    def get_manufacturer(self, manufacturer_id, **params):
        """Get a single manufacturer.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-manufacturer-{id}.{_format}

        """
        return self.get('catalog/manufacturer/%s' % manufacturer_id, params=params)

    def get_manufacturers(self, **params):
        """Lists all manufacturers.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-manufacturers.{_format}

        """
        return self.get('catalog/manufacturers', params=params)

    def get_product(self, product_id, **params):
        """Get a single product.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-product-{id}.{_format}

        """
        return self.get('catalog/product/%s' % product_id, params=params)

    def get_product_categories(self, product_id, **params):
        """Get product categories.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-productcategories-{id}.{_format}

        """
        return self.get('catalog/productcategories/%s' % product_id, params=params)

    def get_product_images(self, product_id, **params):
        """Get a single product images.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-productimages-{id}.{_format}

        """
        return self.get('catalog/productimages/%s' % product_id, params=params)

    def get_product_information(self, product_id, **params):
        """Get a single product information.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-productinformation-{id}.{_format}

        """
        return self.get('catalog/productinformation/%s' % product_id, params=params)

    def get_product_information_all_languages(self, product_id, **params):
        """Get a single product.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-productinformationalllanguages-{id}.{_format}

        """
        return self.get('catalog/productinformationalllanguages/%s' % product_id, params=params)

    def get_product_information_by_sku(self, sku, **params):
        """Get a single product by sku.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-productinformationbysku-{sku}.{_format}

        """
        return self.get('catalog/productinformationbysku/%s' % sku, params=params)

    def get_products(self, **params):
        """Returns all products.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-products.{_format}

        """
        return self.get('catalog/products', params=params)

    def get_products_categories(self, **params):
        """Returns all products categories.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-productscategories.{_format}

        """
        return self.get('catalog/productscategories', params=params)

    def get_products_images(self, **params):
        """Returns all products images.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-productsimages.{_format}

        """
        return self.get('catalog/productsimages', params=params)

    def get_products_information(self, **params):
        """Returns all products products information.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-productsproductsinformation.{_format}

        """
        return self.get('catalog/productsinformation', params=params)

    def get_products_stock(self, **params):
        """Returns all products stock.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-productsstock.{_format}

        """
        return self.get('catalog/productsstock', params=params)

    def get_products_stock_available(self, **params):
        """Returns all products with available stock.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-productsstockavailable.{_format}

        """
        return self.get('catalog/productsstockavailable', params=params)

    def get_products_stock_by_reference(self, **params):
        """TODO
        Not implemented.
        """
        return

    def get_products_tags(self, **params):
        """Lists all product tags.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-productstags.{_format}

        """
        return self.get('catalog/productstags', params=params)

    def get_product_stock(self, product_id, **params):
        """Get a single product stock.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-productstock-{id}.{_format}

        """
        return self.get('catalog/productstock/%s' % product_id, params=params)

    def get_products_variations(self, **params):
        """Returns all products variations.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-productsvariations.{_format}

        """
        return self.get('catalog/productsvariations', params=params)

    def get_products_variations_stock(self, **params):
        """Returns all products variations stock.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-productsvariationsstock.{_format}

        """
        return self.get('catalog/productsvariationsstock', params=params)

    def get_products_variations_stock_available(self, **params):
        """Returns all products variations stock available.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-productsvariationsstockavailable.{_format}

        """
        return self.get('catalog/productsvariationsstockavailable', params=params)

    def get_product_tags(self, product_id, **params):
        """Get a single ProductTag.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-producttags-{id}.{_format}

        """
        return self.get('catalog/producttags/%s' % product_id, params=params)

    def get_product_variations(self, product_id, **params):
        """Get a single Product variations.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-productvariations-{id}.{_format}

        """
        return self.get('catalog/productvariations/%s' % product_id, params=params)

    def get_product_variations_stock(self, product_id, **params):
        """Get a single product variation stock.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-productvariationsstock-{id}.{_format}

        """
        return self.get('catalog/productvariationsstock/%s' % product_id, params=params)

    def get_tag(self, tag_id, **params):
        """Get a single Tag.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-tag-{id}.{_format}

        """
        return self.get('catalog/tag/%s' % tag_id, params=params)

    def get_tag_all_languages(self, tag_id, **params):
        """Get a single Tag.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-tagalllanguages-{id}.{_format}

        """
        return self.get('catalog/tagalllanguages/%s' % tag_id, params=params)

    def get_tags(self, **params):
        """Lists all tags.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-tags.{_format}

        """
        return self.get('catalog/tags', params=params)

    def get_variation(self, variation_id, **params):
        """Get a single variation.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-variation-{id}.{_format}

        """
        return self.get('catalog/variation/%s' % variation_id, params=params)

    def get_variations(self, **params):
        """Lists all variations.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-variations.{_format}

        """
        return self.get('catalog/variations', params=params)

    # shipping
    def get_carriers(self, **params):
        """Get a single variation.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-catalog-variation-{id}.{_format}

        """
        return self.get('shipping/carriers', params=params)

    def get_shipping_order(self, order, **params):
        """Get the list of available shipping options with the calculated weight and cost in Kg and € respectively,
        for the given order.

        Docs:
        https://api.bigbuy.eu/doc#post--rest-shipping-orders.{_format}
        Example order:
            {"order":{"delivery":{"isoCountry":"ES","postcode":"46005"},"products":[{"reference":"V1300179","quantity":1}]}}
        """
        #
        return self.post('shipping/orders', order, **params)

    # order
    def get_order_addresses(self, **params):
        """Get order shipping address structure.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-order-addresses-new.{_format}
        """
        return self.get('order/addresses/new', **params)

    def get_order_carriers(self, **params):
        """Get order shipping address structure.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-order-carriers-new.{_format}
        """
        return self.get('order/carriers/new', **params)

    def check_order(self, order, **params):
        """Check/simulate an order and return the total order to paid.

        Docs:
        https://api.bigbuy.eu/doc#post--rest-order-check.{_format}
        Example order
        order = {
          "order": {
            "internalReference": "123456",
            "language": "es",
            "paymentMethod": "moneybox",
            "carriers": [
              {
                "name": "correos"
              },
              {
                "name": "chrono"
              }
            ],
            "shippingAddress": {
              "firstName": "John",
              "lastName": "Doe",
              "country": "ES",
              "postcode": "46005",
              "town": "Valencia",
              "address": "C/ Altea",
              "phone": "664869570",
              "email": "john@email.com",
              "comment": ""
            },
            "products": [
              {
                "reference": "F1505138",
                "quantity": 4
              }
            ]
          }
        }
        """
        return self.post('order/check', order, **params)

    def create_order(self, order, **params):
        """
        Submit an order.

        Docs:
        https://api.bigbuy.eu/doc#post--rest-order-create.{_format}
        Example order
        order = {
          "order": {
            "internalReference": "123456",
            "language": "es",
            "paymentMethod": "moneybox",
            "carriers": [
              {
                "name": "correos"
              },
              {
                "name": "chrono"
              }
            ],
            "shippingAddress": {
              "firstName": "John",
              "lastName": "Doe",
              "country": "ES",
              "postcode": "46005",
              "town": "Valencia",
              "address": "C/ Altea",
              "phone": "664869570",
              "email": "john@email.com",
              "comment": ""
            },
            "products": [
              {
                "reference": "F1505138",
                "quantity": 4
              }
            ]
          }
        }
        """
        return self.post('order/create', order, **params)

    def get_order_by_custref(self, reference, **params):
        """Get order information by customer reference.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-order-carriers-new.{_format}
        """
        return self.get(f'order/reference/{reference}', **params)

    def get_order_by_id(self, order_id, **params):
        """Get order information.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-order-{idOrder}.{_format}
        """
        return self.get(f'order/{order_id}', **params)

    # tracking
    def get_tracking_carriers(self, **params):
        """Get the list of available carriers.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-order-{idOrder}.{_format}
        """
        return self.get('tracking/carriers', **params)

    def get_tracking_order(self, order_id, **params):
        """Get the list of available trackings.

        Docs:
        https://api.bigbuy.eu/doc#get--rest-tracking-order-{idOrder}.{_format}
        """
        return self.get(f'tracking/order/{order_id}', **params)

    def get_trackings_orders(self, orders, **params):
        """
        Get the list of available trackings for the passed orders.

        Docs:
        https://api.bigbuy.eu/doc#post--rest-tracking-orders.{_format}
        Example order
        order = {
          "track":{
            "orders":[
              {
                "id":"66666"
              },
              {
                "id":"66667"
              }
            ]
          }
        }
        """
        return self.post('tracking/orders', orders, **params)


# from https://developer.twitter.com/en/docs/ads/general/guides/response-codes
HTTP_STATUS_CODE = {
    200: ('OK', 'Success!'),
    304: ('Not Modified', 'There was no new data to return.'),
    400: ('Bad Request', 'The request was invalid. An accompanying \
          error message will explain why. This is the status code \
          will be returned during rate limiting.'),
    401: ('Unauthorized', 'Authentication credentials were missing \
          or incorrect.'),
    403: ('Forbidden', 'The request is understood, but it has been \
          refused. An accompanying error message will explain why. \
          This code is used when requests are being denied due to \
          update limits.'),
    404: ('Not Found', 'The URI requested is invalid or the resource \
          requested, such as a user, does not exists.'),
    406: ('Not Acceptable', 'Returned by the Search API when an \
          invalid format is specified in the request.'),
    410: ('Gone', 'This resource is gone. Used to indicate that an \
          API endpoint has been turned off.'),
    422: ('Unprocessable Entity', 'Returned when an image uploaded to \
          POST account/update_profile_banner is unable to be processed.'),
    429: ('Too Many Requests', 'Returned in API v1.1 when a request cannot \
          be served due to the application\'s rate limit having been \
          exhausted for the resource.'),
    500: ('Internal Server Error', 'Something is broken. Please post to the \
          group so the Twitter team can investigate.'),
    502: ('Bad Gateway', 'Twitter is down or being upgraded.'),
    503: ('Service Unavailable', 'The Twitter servers are up, but overloaded \
          with requests. Try again later.'),
    504: ('Gateway Timeout', 'The Twitter servers are up, but the request \
          couldn\'t be serviced due to some failure within our stack. Try \
          again later.'),
}

import json


class ProductSerializer(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                'id': o.id,
                'name': o.name,
                'description': o.description,
                'price': o.price,
                'enabled': o.enabled,
            }
            return to_serialize
        except AttributeError:
            return super().default(o)


class ShippingSerializer(json.JSONEncoder):
    def default(self, o):
        try:
            to_serialize = {
                'id': o.id,
                'name': o.name,
                'price': o.price,
            }
            return to_serialize
        except AttributeError:
            return super().default(o)

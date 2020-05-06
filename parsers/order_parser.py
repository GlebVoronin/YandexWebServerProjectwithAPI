from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('id', required=True, type=int)
parser.add_argument('items_id', required=True)
parser.add_argument('is_finished', required=True, type=bool)
parser.add_argument('status', required=True)

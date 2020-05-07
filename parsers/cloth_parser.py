from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('id', required=False, type=int)
parser.add_argument('title', required=True)
parser.add_argument('description', required=True)
parser.add_argument('images_links', required=True)
parser.add_argument('colors')
parser.add_argument('length', required=True, type=float)
parser.add_argument('price', required=True, type=int)
parser.add_argument('date', required=True)
parser.add_argument('country_id', required=True)

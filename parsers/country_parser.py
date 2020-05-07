from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('id', required=False, type=int)
parser.add_argument('title', required=True, type=str)

from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('id', required=False, type=int)
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('middle_name', required=True)
parser.add_argument('email', required=True)
parser.add_argument('phone_number', required=True)
parser.add_argument('address', required=True)
parser.add_argument('postal_code', required=True)
parser.add_argument('hashed_password', required=True)
parser.add_argument('register_date', required=True)
parser.add_argument('order_id', required=True, type=int)
parser.add_argument('favourite_id', required=True, type=int)
parser.add_argument('account_type', required=True)

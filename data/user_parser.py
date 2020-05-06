from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('middle_name', required=False)
parser.add_argument('email', required=True)
parser.add_argument('phone_number', required=False)
parser.add_argument('address', required=False)
parser.add_argument('postal_code', required=False)
parser.add_argument('hashed_password', required=True)
parser.add_argument('hashed_password_repeat', required=True)

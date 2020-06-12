"""Constant for application."""
import os

JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_MINUTES = 30
JWT_EXP_DELTA_DAYS = 60
JWT_SECRET = os.getenv('JWT_SECRET', 'secret')

standart_port = 8080
mongo_port = 27017

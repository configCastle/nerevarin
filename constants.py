"""Constant for application."""
import os

standart_jwt_minutes = 30
standart_jwt_days = 60

JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_MINUTES = os.getenv('LIFE_MINUTE', standart_jwt_minutes)
JWT_EXP_DELTA_DAYS = os.getenv('LIFE_DAYS', standart_jwt_days)
JWT_SECRET = os.getenv('JWT_SECRET', 'secret')

standart_port = 8080
mongo_port = 27017

import asyncio

from environs import Env

from db import DataBase

# read env
env = Env()
env.read_env()

db_user = env.str('db_user')
db_password = env.str('db_password')
IP = env.str('IP')
db_port = env.int('db_port')
db_name = env.str('db_name')

db = DataBase(
    db_user, db_password, IP, db_port, db_name
)

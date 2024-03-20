from dotenv import load_dotenv
import os


load_dotenv()


#   Bot Settings
TOKEN = os.getenv("BOT_TOKEN")
description = "Hi! I'm here to make ordering easier!"

#   Connecting db
DB = os.getenv("DB")
USER = os.getenv("USER")
HOST = os.getenv("HOST")
PASSWD = os.getenv("PASSWD")
DB_NAME = os.getenv("DB_NAME")
PORT = os.getenv("PORT")

url = f'{DB}://{USER}:{PASSWD}@{HOST}:{PORT}/{DB_NAME}'

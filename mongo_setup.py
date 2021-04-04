import urllib
import mongoengine
from dotenv import load_dotenv
import os

load_dotenv()

def global_init():
    mongoengine.register_connection(alias="core", name="uniques")
    username = urllib.parse.quote_plus(os.getenv('MONGODB_USERNAME'))
    password = urllib.parse.quote_plus(os.getenv('MONGODB_PASSWORD'))
    mongoengine.connect(host = "mongodb+srv://%s:%s@discord-bots.3ipfn.mongodb.net/uniques?retryWrites=true&w=majority" %(username, password))
    print("MongoDB connection successful")
    
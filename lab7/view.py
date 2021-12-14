import sys
import click
import base64
import colorama
from pymongo import MongoClient
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import config


colorama.init()

client = MongoClient(config.MONGODB_URL)

db = client.get_database()
collection = db.users
click.clear()

try:
    master_key = click.prompt("Please enter master password", hide_input=True)

except click.exceptions.Abort as e:
    print("Aborting...")
    sys.exit(1)

for item in collection.find({}):
    userkey = bytes(item["userkey"].encode())
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=userkey, iterations=390000)
    key = base64.urlsafe_b64encode(kdf.derive(master_key.encode()))
    fernet = Fernet(key)
    try:
        d_memberof = fernet.decrypt(item["memberof"].encode())
        d_email = fernet.decrypt(item["email"].encode())
    except:
        print("Wrong master password. Aborting...")
        sys.exit()
    
    click.secho(f"ID: {item['_id']}", fg="green")
    click.secho(f"Name: {item['firstname']} {item['lastname']}")
    click.secho(f"Age: {item['age']}")
    click.secho(f"Height: {item['height']}")
    click.secho(f"Username: {item['username']}", fg="green")
    click.secho(f"Email (🔐): {d_email.decode()}", fg="red")
    click.secho(f"Address: {item['address']}")
    click.secho(f"City: {item['city']}")
    click.secho(f"Postal Code: {item['postalcode']}")
    click.secho(f"Country: {item['country']}")
    click.secho(f"Member of (🔐): {d_memberof.decode()}", fg="red")
    click.secho("-----------------------------------------------------------------------------------")
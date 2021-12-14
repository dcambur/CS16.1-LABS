# CS Lab 7

## Aims

- Create a MongoDB database which would contain some secured sensitive data (protected via 2-way encryption);
- Create an application which would display the data contained in the database (both common data and the decrypted sensitive data);
- Make sure that the sensitive data can only be accessed via your application (i.e. it is secure).

## Encryption libraries and methods used

Encryption/Decryption is accomplished by using python "cryptography" library.

### Algorithms and methods used

- AES in CBC mode with a 128-bit key for encryption; using PKCS7 padding.
- HMAC using SHA256 for authentication.
- Initialization vectors are generated using os.urandom().
- Encryption key is composed from userkey stored in db (salt) and password entered by user. Userkey (salt) was generated for every user. Every user should have his/her own password but for keeping this lab simple the same password is used for all users - `j969sfaidsA6ZWxE`.


## How to run


### Create a python virtaul environment and install necessary python modules

```bash
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

### Start MongoDB

Fetch official MongoDB docker image and start it:

```bash
$ docker run -d --name mongo -e MONGO_INITDB_ROOT_USERNAME=mongoadmin -e MONGO_INITDB_ROOT_PASSWORD=secret -p 27017:27017 mongo
```

Import database:

```bash
$ docker cp ./dump mongo:/dump
$ docker exec -i mongo /usr/bin/mongorestore --username mongoadmin --password secret --authenticationDatabase admin --db lab7 /dump/lab7
```

Run data viewer

```bash
$ python ./view.py
```

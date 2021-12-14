# CS Lab 8

## Aims

- Create an application that could register a new user;
- Perform email confirmation (via a one time password / code or via a link);
- Output on the screen whether a user confirmed their email or did not confirm it yet.

## Workflow Logic

1) User registers account, email link is being sent.
2) User logs into an unconfirmed account. (it is active for 3 minutes)
3) User opens his/her mailbox and clicks on the provided link.
4) Now user can enter on the email exclusive endpoint "/confirmed/welcome"

## How to run


### Create a python virtual environment and install necessary python modules

```bash
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

### Initialize and Migrate DB

```bash
$ flask db init # if not initialized migrations folder
$ flask db migrate -m "Any_Message" 
$ flask db upgrade
```

Run app.py

```bash
$ python app.py
```

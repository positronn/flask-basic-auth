# flask-basic-auth
A simple rest-api protected with simple http authentication using `jwt`.
This is an api template or example made by [miguelgrinberg](https://github.com/miguelgrinberg) on his repo [ miguelgrinberg /
REST-auth ](https://github.com/miguelgrinberg/REST-auth) as of April 19 2023 (latest commit: [82749ef](https://github.com/miguelgrinberg/REST-auth/commit/82749efcacb81be979ae1e185e385e284ccb97f7))

I did some minor changes, like structuring the api as a factory (`create_app` approach), updated the libraries to latest versions (as of April 19 2023) and fix minor bugs due to the updates.

The whole intellectual property belongs to  [miguelgrinberg](https://github.com/miguelgrinberg), I just rewrote his code
for self-learning purpouses. Thank you, Miguel.

## Setting up environment
```
$ python3 -m venv env
$ source env/bin/activate
(env) $ python -m pip install -r requirements.txt
```

Then create a `.env` file named `.env` on the root directory which contains these lines:
```
FLASK_APP=authy.py

```


## Setting up the database
Set up the database migration and recognize models
```
flask --env-file=.env db init
```

Migrate the current Model
```
flask --env-file=.env db migrate
```

Upgrade the database to build changes
```
flask --env-file=.env db upgrade 
```

## Run the server
Run the server on debug mode
```
flask --env-file=.env run --port=5000 --debug
```


## Example (same as in miguel's repo)
The following `curl` command registers a new user with username miguel and password python:
```
$ curl -i -X POST -H "Content-Type: application/json" -d '{"username":"miguel","password":"python"}' http://127.0.0.1:5000/api/users
HTTP/1.0 201 CREATED
Content-Type: application/json
Content-Length: 27
Location: http://127.0.0.1:5000/api/users/1
Server: Werkzeug/0.9.4 Python/2.7.3
Date: Thu, 28 Nov 2013 19:56:39 GMT

{
  "username": "miguel"
} 
```

These credentials can now be used to access protected resources:
```
$ curl -u miguel:python -i -X GET http://127.0.0.1:5000/api/resource
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 30
Server: Werkzeug/0.9.4 Python/2.7.3
Date: Thu, 28 Nov 2013 20:02:25 GMT

{
  "data": "Hello, miguel!"
}
```

Using the wrong credentials the request is refused:
```
$ curl -u miguel:ruby -i -X GET http://127.0.0.1:5000/api/resource
HTTP/1.0 401 UNAUTHORIZED
Content-Type: text/html; charset=utf-8
Content-Length: 19
WWW-Authenticate: Basic realm="Authentication Required"
Server: Werkzeug/0.9.4 Python/2.7.3
Date: Thu, 28 Nov 2013 20:03:18 GMT

Unauthorized Access
```

Finally, to avoid sending username and password with every request an authentication token can be requested:
```
$ curl -u miguel:python -i -X GET http://127.0.0.1:5000/api/token
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 139
Server: Werkzeug/0.9.4 Python/2.7.3
Date: Thu, 28 Nov 2013 20:04:15 GMT

{
  "duration": 600,
  "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4NTY2OTY1NSwiaWF0IjoxMzg1NjY5MDU1fQ.eyJpZCI6MX0.XbOEFJkhjHJ5uRINh2JA1BPzXjSohKYDRT472wGOvjc"
}
```

And now during the token validity period there is no need to send username and password to authenticate anymore:
```
$ curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTM4NTY2OTY1NSwiaWF0IjoxMzg1NjY5MDU1fQ.eyJpZCI6MX0.XbOEFJkhjHJ5uRINh2JA1BPzXjSohKYDRT472wGOvjc:x -i -X GET http://127.0.0.1:5000/api/resource
HTTP/1.0 200 OK
Content-Type: application/json
Content-Length: 30
Server: Werkzeug/0.9.4 Python/2.7.3
Date: Thu, 28 Nov 2013 20:05:08 GMT

{
  "data": "Hello, miguel!"
}
```

Once the token expires it cannot be used anymore and the client needs to request a new one. Note that in this last example the password is arbitrarily set to x, since the password isn't used for token authentication.

An interesting side effect of this implementation is that it is possible to use an unexpired token as authentication to request a new token that extends the expiration time. This effectively allows the client to change from one token to the next and never need to send username and password after the initial token was obtained.
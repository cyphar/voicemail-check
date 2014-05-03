Acma API
========

Because Fuck Logic. ;)

### Usage ###
For maximum hackerage:

```
$ tar xvfz data.tar.gz
# => Extract ACMA database.
$ ./acma-conv data.csv
# => Hopefully no errors.
$ ./acma-api.py [-H host] [-p port] [-D]
# => Run the goddamn server.
```

To access the API, navigate to this URL:

```
http://<host>:<port>/api/<number>
```

You'll get a response like this:

```
{"code": 200, "body": {"telco": <the telco>, "number": <number>, "vulnerable": <is it vulnerable?>}}
```

... or the world will explode. Who knows?

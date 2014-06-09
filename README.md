Optus Voicemail Check
=====================

A simple web app to check if your (Australian) voicemail is vulnerable to information disclosure.
For more information, see [this article](http://shubh.am/how-i-bypassed-2-factor-authentication-on-google-yahoo-linkedin-and-many-others/).

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

### Data Integrity ###
The [data](data.csv) used for this project is provided by ACMA, and no
guarantees are made for the integrity of the data provided (except any which
are provided by ACMA)

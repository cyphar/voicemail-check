#!/usr/bin/env python3

# acma: finds the telco for a number (and tells you if it is vuln to voicemail attacks)
# Copyright (C) 2014, Cyphar All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its contributors
#    may be used to endorse or promote products derived from this software without
#    specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import argparse
import sqlite3
import flask
import functools
import json

app = flask.Flask(__name__)
app.config.from_object(__name__)
dbfile = "acma.db"

def number_cache(func):
	pure = {}

	def wrapper(number):
		if number in pure:
			return pure[number]

		val = func(number)
		pure[number] = val

		return val

	return wrapper

def access_control(origins, methods=None, max_age=21600, headers=None):
	if methods:
		methods = ",".join(methods)
	if headers:
		headers = ",".join(headers)
	if not isinstance(origins, str):
		origins = ",".join(origins)

	def get_methods():
		if methods is not None:
			return methods

		resp = flask.current_app.make_default_options_response()
		return resp.headers.get("Allow")

	def decorator(func):
		@functools.wraps(func)
		def wrapper(*args, **kwargs):
			if flask.request.method == "OPTIONS":
				return flask.current_app.make_default_options_response()

			resp = flask.make_response(func(*args, **kwargs))

			resp.headers["Access-Control-Allow-Origin"] = origins

			resp.headers["Access-Control-Max-Age"] = str(max_age)

			if get_methods():
				resp.headers["Access-Control-Allow-Methods"] = get_methods()

			if headers:
				resp.headers["Access-Control-Allow-Headers"] = headers

			return resp
		return wrapper
	return decorator

@app.before_request
def getdb():
	if not getattr(flask.g, "conn", None):
		flask.g.conn = sqlite3.connect(dbfile)
		flask.g.conn.row_factory = sqlite3.Row

@app.teardown_appcontext
def cleardb(exception):
	conn = getattr(flask.g, "conn", None)

	if conn:
		conn.close()

	flask.g.conn = None

def is_vuln(telco):
	# Well ... basically...
	return "Optus" in telco

@app.route("/api/<number>")
@access_control(origins="*")
@number_cache
def lookup_number(number):
	cur = flask.g.conn.execute("SELECT telco FROM acma_registered WHERE number_length=? AND (? >= lower_bound AND ? <= upper_bound) LIMIT 1", (len(number), number, number))
	row = cur.fetchone()

	telco = None
	vuln = None

	if row:
		telco = row["telco"]
		vuln = is_vuln(telco)

	out = json.dumps({
		"code": 200,
		"body": {
			"number": number,
			"telco": telco,
			"vulnerable": vuln
		}
	})

	return flask.Response(response=out, mimetype="application/json")

@app.route("/")
def index():
	return flask.render_template("index.html")

@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(410)
@app.errorhandler(500)
@access_control(origins="*")
def what(exception):
	out = json.dumps({
		"code": exception.code,
		"body": {
			"message": "what?"
		}
	})

	return flask.Response(response=out, mimetype="application/json", status=exception.code)

def run_server(host, port, debug=False):
	app.debug = debug
	app.run(host=host, port=port)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Runs the magical ACMA API for shits and giggles.")
	parser.add_argument("-d", "--dbfile", type=str, default="acma.db")
	parser.add_argument("-D", "--debug", action="store_true", help="Debugging intensifies.")
	parser.add_argument("-H", "--host", type=str, default="0.0.0.0")
	parser.add_argument("-p", "--port", type=int, default=8888)

	args = parser.parse_args()

	dbfile = args.dbfile
	run_server(args.host, args.port, args.debug)

#!/usr/bin/env python3

# acma-api: finds the telco for a number (and tells you if it is vuln to voicemail attacks)
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
import json

app = flask.Flask(__name__)
app.config.from_object(__name__)
dbfile = "acma.db"

def number_cache(func):
	pure = {}

	def wrapper(number):
		if number in pure:
			print("[+] Cache'd that sucker! %s" % number)
			return pure[number]

		val = func(number)
		pure[number] = val

		return val

	return wrapper

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

@app.route("/api/v42/<number>")
@number_cache
def lookup_number(number):
	_conn = flask.g.conn

	cur = _conn.execute("SELECT telco FROM acma_registered WHERE number_length=? AND (? >= lower_bound AND ? <= upper_bound) LIMIT 1", (len(number), number, number))
	row = cur.fetchone()

	telco = row["telco"]
	vuln = is_vuln(telco)

	out = json.dumps({
		"number": number,
		"telco": telco,
		"vulnerable": vuln
	})

	return flask.Response(response=out, mimetype="application/json")

@app.errorhandler(401)
@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(410)
@app.errorhandler(500)
def what(e):
	out = json.dumps({
		"message": "what?"
	})

	return flask.Response(response=out, mimetype="application/json")

def run_server(host, port, debug=False):
	app.debug = debug
	app.run(host=host, port=port)

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Runs the magical ACMA API for shits and giggles.")
	parser.add_argument("-D", "--debug", action="store_true", help="Debugging intensifies.")
	parser.add_argument("-H", "--host", type=str, default="0.0.0.0")
	parser.add_argument("-p", "--port", type=int, default=8888)

	args = parser.parse_args()

	run_server(args.host, args.port, args.debug)

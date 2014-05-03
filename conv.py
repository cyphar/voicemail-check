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
import csv
import sqlite3

parser = argparse.ArgumentParser(description="Convert ACMA data into an SQLite3 Database, bitch.")
parser.add_argument("-d", "--dbfile", type=str, default="acma.db")
parser.add_argument("files", nargs="+", type=str)

args = parser.parse_args()

'''
def find_carrier(number, rows):
	for row in rows:
		if len(row["From"]) != len(row["To"]):
			continue

		ndigits = len(row["From"])

		if len(number) != ndigits:
			continue

		lower = int(row["From"])
		upper = int(row["To"])

		if int(number) >= lower and int(number) <= upper:
			return row["Allocatee"]
'''

def initdb(db_file):
	script = """
		CREATE TABLE IF NOT EXISTS acma_registered (
			id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,

			lower_bound INTEGER UNIQUE NOT NULL,
			upper_bound INTEGER UNIQUE NOT NULL,
			number_length INTEGER NOT NULL,

			allocatee TEXT NOT NULL,
			telco TEXT NOT NULL,
			service TEXT NOT NULL
		);
	"""

	with sqlite3.connect(db_file) as conn:
		conn.executescript(script)
		conn.commit()

def main():
	csv_files = args.files
	db_fname = args.dbfile

	initdb(db_fname)

	with sqlite3.connect(db_fname) as conn:
		for csv_fname in csv_files:
			with open(csv_fname, newline="") as f:
				reader = csv.DictReader(f)
				for row in reader:
					ins = "INSERT INTO acma_registered (lower_bound, upper_bound, number_length, allocatee, telco, service) VALUES (?, ?, ?, ?, ?, ?)"
					conn.execute(ins, (row["From"], row["To"], row["Number Length"], row["Allocatee"], row["Latest Holder"], row["Service Type"]))

		conn.commit()

if __name__ == "__main__":
	main()

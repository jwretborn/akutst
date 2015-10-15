#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from sqlalchemy import create_engine, schema
from sqlalchemy.sql import text

eng = create_engine(os.environ['DATABASE_URL'])
con = eng.connect()

# Read file
codes = []
insert_data = []
f = open('scripts/retts_codes.csv')
for line in f:
	entry = {}
	l = line.split(';');
	if line[0] :
		entry['type'] = l[0]
	if line[1] :
		entry['code'] = l[1]
		for i in range(2, len(l)) :
			if l[i] and len(l[i]) > 2 :
				insert_data.append({'type':l[0], 'code':l[1], 'name':unicode(l[i], "utf-8")})

# Fetch all existing entries from the db
rs = con.execute('''SELECT code, name, id FROM "retts_codes"''')
existing_data = rs.fetchall()
missing_data = []

# Insert missing value
for row in existing_data :
	found = False
	for entry in insert_data :
		# Check and remove data that already exists
		if row[0] == int(entry['code']) and row[1] == entry['name'] :
			insert_data.remove(entry)
			found = True
			break

	# Data that exists in the db but not in the file
	if not found :
		missing_data.append(row)

# Delete
metadata = schema.MetaData()
retts_table = schema.Table('retts_codes', metadata, autoload=True, autoload_with=eng)
for remove in missing_data :
	d = retts_table.delete(retts_table.c.id == remove[2])
	con.execute(d)

# Hack to get a correct max value for the auto-inc in postgres that might
con.execute("""SELECT setval('retts_codes_id_seq', MAX(id)) FROM retts_codes""")

#Insert
for add in insert_data :
	i = retts_table.insert().values(add)
	con.execute(i)

con.close()
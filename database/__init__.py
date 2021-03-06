#!/usr/bin/python3
# (c) Daniel Córdova A. <danesc87@gmail.com>, GPL v2
import os
from config import config_reader

db_path = config_reader.get('DataBase', 'path')
db_file = os.path.expanduser(os.path.join(db_path, 'ssemDB'))
exist_db_file = os.path.exists(db_file)

if not exist_db_file:
    try:
        open(db_file, 'a').close()
    except:
        print('Can not create database file!')
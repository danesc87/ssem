#!/usr/bin/python3
# (c) Daniel Córdova A. <danesc87@gmail.com>, GPL v2
import os
from config import config_reader

time_file = config_reader.get('Connection', 'executiontime')
ssh_file_path = config_reader.get('Secure Shell', 'path')
ssh_file_name = config_reader.get('Secure Shell', 'name')
ssh_file = os.path.expanduser(os.path.join(ssh_file_path, ssh_file_name))

if not os.path.exists(ssh_file):
    raise FileNotFoundError('File ' + ssh_file_name + ' does not exists in ' + os.path.expanduser(ssh_file_path) +
                            ' path!')
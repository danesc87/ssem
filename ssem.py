#!/usr/bin/python3
#SSEM file that allows do tasks with sqlite3 database or execute some command on remote server
# (c) Daniel Córdova A. <danesc87@gmail.com>, GPL v2

import argparse

from database import db_connection
from secure_shell.connection_factory import ConnectionFactory
from secure_shell.executor_command import ExecutorOnServer

class ServerScriptExecutorMonitor(object):
    '''Class that receives arguments from shell and do tasks with sqlite3 database or execute some command on ssh
    server'''
    def __init__(self):
        self.script_to_execute = None
        self.script_id = None
        self.exec_time = None
        self.arguments = None
        self.chosen_host = None

    def arguments_to_be_parsed(self):
        parser = argparse.ArgumentParser(description='Arguments for SSEM')
        parser.add_argument('--remotehost','-r', nargs='*', help='Connection to remote host')
        parser.add_argument('--remoteexecute','-x',nargs='*', help='Execute command on remote host')
        parser.add_argument('--addscript','-a',nargs=2, help='Add script to data base')
        parser.add_argument('--deletescript','-d', help='Delete script on data base')
        return parser.parse_args()

    def execution_time(self, argsObject, parameterNumber):
        timeForExecution = None
        if len(argsObject) < parameterNumber:
            timeForExecution = 0
        else:
            timeForExecution = argsObject[parameterNumber-1]
        return int(timeForExecution)

    def print_list_of_scripts(self, list_of_scripts):
        for specific_script in list_of_scripts:
            print(specific_script)

    def start_functions(self):
        self.arguments = self.arguments_to_be_parsed()
        new_connection = ConnectionFactory()
        if self.arguments.remotehost:
            self.print_list_of_scripts(db_connection.DataBaseConnector().show_all_scripts())
            self.exec_time = self.execution_time(self.arguments.remotehost, 2)
            self.script_id = input('Seleccione el ID del script a ejecutar: ')
            self.script_to_execute = db_connection.DataBaseConnector().select_script(self.script_id)[0][0]
            self.chosen_host = self.arguments.remotehost[0]
            opened_connection = new_connection.create_connection(self.chosen_host)
            command = ExecutorOnServer(opened_connection)
            command.execute_command_on_server(self.script_to_execute, self.exec_time)
        elif self.arguments.remoteexecute:
            self.execTime = self.execution_time(self.arguments.remoteexecute, 3)
            self.script_to_execute = self.arguments.remoteexecute[1]
            self.chosen_host = self.arguments.remoteexecute[0]
            opened_connection = new_connection.create_connection(self.chosen_host)
            command = ExecutorOnServer(opened_connection)
            command.execute_command_on_server(self.script_to_execute, self.exec_time)
        elif self.arguments.addscript:
            script_itself = self.arguments.addscript[0]
            script_description = self.arguments.addscript[1]
            db_connection.DataBaseConnector().insert_on_database(script_itself, script_description)
        elif self.arguments.deletescript:
            self.script_id = self.arguments.deletescript
            db_connection.DataBaseConnector().delete_from_database(self.script_id)
        else:
            print('SSEM necesita argumentos, mira ssem -h')


ssem = ServerScriptExecutorMonitor()
ssem.start_functions()
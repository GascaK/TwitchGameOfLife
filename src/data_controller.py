import sqlite3
import time
from datetime import datetime

class DataController:
    def __init__(self, db):
        if(db.lower() == "viewers"):
            self.con = sqlite3.connect("data/viewers.db")
        else:
            self.con = sqlite3.connect(":memory:")

        self.c = self.con.cursor()
        self.command_list = ['!POINTS']

    def command_controller(self, command, *args):
        '''command_controller(command, *args)
        Activate certain commands available in DataController.

        Noteable Variables
        ---------------------------------------------
        command - str
        Command to be executed.

        *args - Variable non keyword argument
        Information needed to execute command.
        ---------------------------------------------
        '''
        if(command == '!POINTS'):
            return self.get_points(args[0])

    def create_table(self, table_name):
        '''create_table(table_name)
        Create table if table does not already exist with table_name.

        Noteable Variables
        ---------------------------------------------
        table_name - string
        Escaped if value is able to be split, to help in preventing sql
        injections. TODO: Delete this.
        ---------------------------------------------

        returns - None
        '''
        if len(table_name.split()) > 1:
            raise sqlite3.ProgrammingError

        self.c.execute(f'''CREATE TABLE IF NOT EXISTS 
        {table_name}(ID text PRIMARY KEY UNIQUE, points integer, first_visit text)''')

    def add_column(self, table_name, data):
        '''add_column(table_name, data)
        Add a column to set table name with input data.

        Noteable Variables
        ---------------------------------------------
        table_name - string
        Table name to be altered. Escaped if value is able to be split, to
        help with sql injections.

        data - dict
        Dictionary with which to add values to TABLE. Dict must include 
        'col_name' and 'col_type' to funciton correctly.
        ---------------------------------------------

        returns - None

        TODO: Delete this function.
        '''
        if len(table_name.split()) > 1:
            raise sqlite3.ProgrammingError
        if len(data['col_name'].split()) > 1:
            raise sqlite3.ProgrammingError
        if len(data['col_type'].split()) > 1:
            raise sqlite3.ProgrammingError

        self.c.execute(f'''ALTER TABLE {table_name} 
        ADD COLUMN {data['col_name']} {data['col_type']}''')

    def add_points(self, viewer, points_added):
        '''add_points(viewer, points_added)
        Add set points to viewer. Will create a new database entry if user is
        not found.

        Noteable Variables
        ---------------------------------------------
        viewer - str
        Viewer name one at a time.
        TODO: Convert to loop. Learn sql idk.

        points_added - int
        Points to be added to table:viewer points.

        timestamp - time
        A timestamp of the time when user was input into system.
        ---------------------------------------------

        returns - connection . rowcount()
        '''
        self.c.execute(f'''SELECT * FROM viewers
        WHERE ID = ?''',(viewer,))
        entry = self.c.fetchone()

        if entry is None:
            print(entry)
            timestamp = datetime.fromtimestamp(time.time())
            self.c.execute(f'''INSERT INTO viewers(ID, points, first_visit)
            VALUES(?,?,?);''',(viewer,300,timestamp,))
            self.con.commit()
        else:
            print(entry)
            self.c.execute(f'''UPDATE viewers SET points = ?
            WHERE ID = ?''',(entry[1]+points_added,viewer,))
            self.con.commit()
        
        #return self.con.rowcount()

    def get_points(self, viewer):
        '''get_points(viewer)
        Get available points for user.

        Noteable Variables
        ---------------------------------------------
        viewer - str
        Viewer to be retrieved.
        ---------------------------------------------

        returns entry['POINTS']
        '''
        self.c.execute('''SELECT * FROM viewers
        WHERE ID = ?''',(viewer,))
        entry = self.c.fetchone()

        if entry is not None:
            return entry[1], f'{entry[1]} points avaiable to spend!'
        else:
            return 0, 'Unable to locate.'

    def get_user(self, viewer):
        '''get_user(viewer)
        Get viewer information from db.

        Noteable Variables
        ---------------------------------------------
        viewer - str
        Viewer to be retrieved.
        ---------------------------------------------

        returns cursor . fetchone()
        '''
        self.c.execute(f'''SELECT * FROM viewers
        WHERE ID = ?''',(viewer,))
        return self.c.fetchone()

    def get_commands(self):
        '''get_commands()
        Returns the command list available.

        returns command_list
        '''
        return self.command_list

    def spend_points(self, viewer, amount):
        '''spend_points(viewer, amount)
        Spend a viewers points.

        Noteable Variables
        ---------------------------------------------
        viewer - str
        Viewer to subtract points from.

        amount - int
        Amount of points to be subtracted.
        ---------------------------------------------
        '''
        self.c.execute(f'''SELECT * FROM viewers
        WHERE ID = ?''',(viewer,))

        entry = self.c.fetchone()

        if entry is not None and (entry[1] - amount >= 0):
            self.c.execute(f'''UPDATE viewers SET points = ?
            WHERE ID = ?''',(entry[1]-amount, viewer,))
            self.con.commit()
        else:
            print('Unable to spend points')
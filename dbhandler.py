import sqlite3
import tools as tool



class DbHandler:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.session = None


    def connect(self):
        """Connects to database"""
        
        try:
            self.session = sqlite3.connect(self.db_path)
            
        except sqlite3.Error as error:
            print(f"An error occurred:\n{error}")
            
    def close(self):
        """Closes the connection"""
        
        if self.session:
            self.session.close()
        else:
            print("No active connection to close.")



    def create_base(self):
        """Creates Basic tables of database"""
        
        self.connect()
        
        qry_table_capital_cities = """
        CREATE TABLE IF NOT EXISTS capital_cities (
            cc_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            lat REAL NOT NULL,
            lon REAL NOT NULL
        );
        """
        tool.handle_sql_execute(self.session, qry_table_capital_cities)
            
        self.close()
            
            
    def clean_db(self):
        
        """Cleans every record"""
        
        self.connect()
        
        qry_delete_cc = "DELETE FROM capital_cities;"
        qry_delete_ss = "DELETE FROM sqlite_sequence;"
        tool.handle_sql_execute(self.session, qry_delete_cc, qry_delete_ss)
        
        self.close()
       
                    
    def execute(self, query, parameters=None, mode=""):

        try:
            self.connect()
            
            cursor = self.session.cursor()
            
            if parameters:
                cursor.execute(query, parameters)
            else:
                cursor.execute(query)
            
            if mode == "table":
                result = []
                for item in cursor:
                    result.append(item)
                    
                self.close()
                return result
            else:
                self.session.commit()
                self.close()
                        
        except sqlite3.Error as error:
            print(f"An error occurred:\n{error}")
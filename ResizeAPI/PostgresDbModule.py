import psycopg2
from psycopg2 import Error

class PostgresDbModule:
    @staticmethod
    def getDbConnection():
        try:
            
            return connection
        except (Exception, Error) as error:
            print("Error while connecting to PostgreSQL", error)
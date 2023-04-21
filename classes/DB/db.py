import json

import pandas as pd
from sqlalchemy import create_engine, text

from classes.DB.db_conf import connection_uri
from classes.logger.logger_init import logger
from classes.sql_queries.manage_tables_queries import *


class Database:
    def __init__(self):
        self.connection_pd = None

    def connect(self):
        db = create_engine(connection_uri)
        try:
            self.connection_pd = db.connect()
            logger.info("Database connection successful.")
        except Exception as e:
            logger.error("Failed to connect to database: %s", str(e))

    def close(self):
        try:
            self.connection_pd.close()
            logger.info("Database connection closed successfully.")
        except Exception as e:
            logger.error("Failed to close database connection: %s", str(e))

    def get_data_json(self, sql_query):
        try:
            df = pd.read_sql(sql_query, con=self.connection_pd)
            result = df.to_json(orient="records")
            json_string = json.loads(result)
            logger.info("Retrieved data from database and converted to JSON.")
            return json_string
        except Exception as e:
            logger.error("Failed to retrieve data from database: %s", str(e))
            return None

    def get_data_xml(self, sql_query):
        try:
            df = pd.read_sql(sql_query, con=self.connection_pd)
            xml_string = df.to_xml(index=False)
            logger.info("Retrieved data from database and converted to XML.")
            return xml_string
        except Exception as e:
            logger.error("Failed to retrieve data from database: %s", str(e))
            return None

    def load_json(self, file, table_name):
        try:
            df = pd.read_json(file)
            df.to_sql(table_name, con=self.connection_pd, if_exists="append", index=False)
            logger.info("Loaded data from JSON file into database table '%s'.", table_name)
        except Exception as e:
            logger.error("Failed to load data from JSON file into database: %s", str(e))

    def check_if_tables_exist(self, table_names):
        try:
            tables_exist = True
            for table_name in table_names:
                query = f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name='{table_name}');"
                result = self.connection_pd.execute(text(query)).scalar()
                if not result:
                    tables_exist = False
                    break
                else:
                    logger.info("Table '%s' exists in database.", table_name)
            return tables_exist
        except Exception as e:
            logger.error("Failed to check tables: %s", str(e))

    def create_tables(self):
        try:
            self.connection_pd.execute(text(create_table_rooms_query))
            logger.info("Rooms table created successfully")
            self.connection_pd.execute(text(create_table_students_query))
            logger.info("Students table created successfully")
            self.connection_pd.commit()
        except Exception as e:
            logger.error("Failed to create tables: %s", str(e))

    def drop_tables(self):
        try:
            self.connection_pd.execute(text(drop_table_students_query))
            logger.info("Students table dropped successfully")
            self.connection_pd.execute(text(drop_table_rooms_query))
            logger.info("Rooms table dropped successfully")
            self.connection_pd.commit()
        except Exception as e:
            logger.error("Failed to drop tables: %s", str(e))

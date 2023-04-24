import json

import click

from classes.DB.db import Database
from classes.DB.db_conf import DB_TABLES_NAMES, connection_uri
from classes.sql_queries.retrieve_data_queries import retrieve_data_queries

FORMATS = ["xml", "json"]


@click.group
def commands():
    pass


@click.command()
@click.argument("students", type=click.Path(exists=True), default="./data/raw/students.json")
@click.argument("rooms", type=click.Path(exists=True), default="./data/raw/rooms.json")
def load(students, rooms):
    database = Database(connection_uri)
    database.connect()
    if not database.check_if_tables_exist(DB_TABLES_NAMES):
        database.create_tables()
    else:
        choice = input(
            "There are tables with this names already. Do you want to proceed and overwrite tables? " "Y/any other key"
        )
        if choice == "Y":
            database.drop_tables()
            database.create_tables()
        else:
            return
    database.load_json(rooms, DB_TABLES_NAMES[0])
    database.load_json(students, DB_TABLES_NAMES[1])
    database.close()


@click.command()
@click.argument("format", type=click.Choice(FORMATS), default="json")
def execute_queries(format):
    database = Database(connection_uri)
    database.connect()
    counter = 1
    if format == "json":
        for query in retrieve_data_queries:
            data_json = database.get_data_json(query)
            with open(f"./data/output/query_{counter}.json", "w", encoding="utf-8") as file:
                json.dump(data_json, file, indent="")
            counter += 1
    else:
        for query in retrieve_data_queries:
            data_xml = database.get_data_xml(query)
            with open(f"./data/output/query_{counter}.xml", "w", encoding="utf-8") as file:
                file.write(data_xml)
            counter += 1
    database.close()


commands.add_command(load)
commands.add_command(execute_queries)

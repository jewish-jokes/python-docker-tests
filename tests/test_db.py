import json
import os
import tempfile
from unittest.mock import MagicMock

import sqlalchemy as db
from sqlalchemy import DATE, INTEGER, VARCHAR, text

import tests.test_db_config as conf
from classes.DB.db import Database


def test_db_connection_with_correct_credits():
    database = Database(conf.correct_connection_uri)
    database.connect()
    assert database.connection_pd is not None


def test_db_connection_with_invalid_host():
    database = Database(conf.connection_uri_with_invalid_host)
    database.connect()
    assert database.connection_pd is None


def test_db_connection_with_invalid_password():
    database = Database(conf.connection_uri_with_invalid_password)
    database.connect()
    assert database.connection_pd is None


def test_db_connection_with_invalid_user():
    database = Database(conf.connection_uri_with_invalid_user)
    database.connect()
    assert database.connection_pd is None


def test_close_connection_function():
    connection_mock = MagicMock()
    database = Database(conf.correct_connection_uri)
    database.connect()
    database.connection_pd = connection_mock
    database.close()
    connection_mock.close.assert_called_once()


def test_get_data_json_function():
    engine = db.create_engine(conf.correct_connection_uri)
    connection = engine.connect()
    connection.execute(text("CREATE TABLE rooms (id INTEGER PRIMARY KEY, name VARCHAR(20));"))
    connection.execute(text("INSERT INTO rooms VALUES (0, 'Room #0');"))
    connection.execute(text("INSERT INTO rooms VALUES (1, 'Room #1');"))
    connection.execute(text("INSERT INTO rooms VALUES (2, 'Room #2');"))
    connection.commit()
    sql_query = "SELECT * FROM rooms;"
    database = Database(conf.correct_connection_uri)
    database.connect()
    result = database.get_data_json(sql_query)
    expected_json = '[{"id":0,"name":"Room #0"},{"id":1,"name":"Room #1"},{"id":2,"name":"Room #2"}]'
    assert result == json.loads(expected_json)
    database.close()
    connection.execute(text("DROP TABLE rooms;"))
    connection.commit()
    connection.close()


def test_get_data_xml_function():
    engine = db.create_engine(conf.correct_connection_uri)
    connection = engine.connect()
    connection.execute(text("CREATE TABLE rooms (id INTEGER PRIMARY KEY, name VARCHAR(20));"))
    connection.execute(text("INSERT INTO rooms VALUES (0, 'Room #0');"))
    connection.execute(text("INSERT INTO rooms VALUES (1, 'Room #1');"))
    connection.execute(text("INSERT INTO rooms VALUES (2, 'Room #2');"))
    connection.commit()
    # Call the get_data_json method with a SQL query and assert that it returns the expected JSON string
    sql_query = "SELECT * FROM rooms;"
    database = Database(conf.correct_connection_uri)
    database.connect()
    result = database.get_data_xml(sql_query)
    expected_xml = """<?xml version='1.0' encoding='utf-8'?>
<data>
  <row>
    <id>0</id>
    <name>Room #0</name>
  </row>
  <row>
    <id>1</id>
    <name>Room #1</name>
  </row>
  <row>
    <id>2</id>
    <name>Room #2</name>
  </row>
</data>"""
    assert result == expected_xml
    database.close()
    connection.execute(text("DROP TABLE rooms;"))
    connection.commit()
    connection.close()


def test_load_json_function():
    engine = db.create_engine(conf.correct_connection_uri)
    connection = engine.connect()
    connection.execute(text("CREATE TABLE rooms (id INTEGER PRIMARY KEY, name VARCHAR(20));"))
    connection.commit()
    data = [{"id": 0, "name": "Room #0"}, {"id": 1, "name": "Room #1"}]
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        json.dump(data, f)
    sql_query = "SELECT * FROM rooms;"
    database = Database(conf.correct_connection_uri)
    database.connect()
    database.load_json(f.name, "rooms")
    result = database.get_data_json(sql_query)
    expected_json = '[{"id":0,"name":"Room #0"},{"id":1,"name":"Room #1"}]'
    assert result == json.loads(expected_json)
    os.unlink(f.name)
    database.close()
    connection.execute(text("DROP TABLE rooms;"))
    connection.commit()
    connection.close()


def test_create_tables_function(db_connection):
    db_connection.create_tables()

    engine = db.create_engine(conf.correct_connection_uri)
    connection = engine.connect()

    rooms_table_columns = db.inspect(connection.engine).get_columns("rooms")
    assert len(rooms_table_columns) == 2
    assert rooms_table_columns[0]["name"] == "id"
    assert str(rooms_table_columns[0]["type"]) == str(INTEGER())
    assert rooms_table_columns[1]["name"] == "name"
    assert str(rooms_table_columns[1]["type"]) == str(VARCHAR(20))

    students_table_columns = db.inspect(connection.engine).get_columns("students")
    assert len(students_table_columns) == 5
    assert students_table_columns[0]["name"] == "id"
    assert str(students_table_columns[0]["type"]) == str(INTEGER())
    assert students_table_columns[1]["name"] == "name"
    assert str(students_table_columns[1]["type"]) == str(VARCHAR(50))
    assert students_table_columns[2]["name"] == "birthday"
    assert str(students_table_columns[2]["type"]) == str(DATE())
    assert students_table_columns[3]["name"] == "sex"
    assert str(students_table_columns[3]["type"]) == str(VARCHAR(1))
    assert students_table_columns[4]["name"] == "room"
    assert str(students_table_columns[4]["type"]) == str(INTEGER())

    db_connection.drop_tables()
    connection.close()


def test_drop_tables_function(db_connection):
    db_connection.create_tables()
    db_connection.drop_tables()

    engine = db.create_engine(conf.correct_connection_uri)
    connection = engine.connect()

    assert not db.inspect(connection.engine).has_table("rooms")
    assert not db.inspect(connection.engine).has_table("students")

    connection.close()

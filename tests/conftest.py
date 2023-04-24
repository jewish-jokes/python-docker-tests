import pytest

import tests.test_db_config as conf
from classes.DB.db import Database


@pytest.fixture()
def db_connection():
    db = Database(conf.correct_connection_uri)
    db.connect()
    yield db
    db.close()

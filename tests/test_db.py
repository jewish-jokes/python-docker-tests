def test_db_connection_with_correct_credits(database_instance):
    assert database_instance.connection


# def test_database_if_provided_wrong_config():
#     with pytest.raises(SystemExit):
#         Database(DatabaseConfig(pg_connection_dict_invalid))
#
#
# def test_query_returns_data_from_db(db_session):
#     assert len(db_session.query("""SELECT pid FROM pg_stat_activity""")) != 0

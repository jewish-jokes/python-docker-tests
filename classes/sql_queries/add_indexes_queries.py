add_indexes_to_rooms_table_query = """
    CREATE INDEX room_id_idx ON rooms (id);
"""

add_indexes_to_students_table_query = """
    CREATE INDEX student_room_birthday_idx ON students (room, birthday);
"""

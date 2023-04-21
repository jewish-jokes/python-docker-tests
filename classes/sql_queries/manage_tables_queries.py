create_table_rooms_query = """
    CREATE TABLE IF NOT EXISTS rooms (
      id INTEGER PRIMARY KEY,
      name VARCHAR(20)
    );
"""

create_table_students_query = """
    CREATE TABLE IF NOT EXISTS students (
      id INTEGER PRIMARY KEY,
      name VARCHAR(50),
      birthday DATE,
      sex VARCHAR(1),
      room INTEGER REFERENCES rooms(id)
    );
"""

drop_table_rooms_query = """
    DROP TABLE rooms;
"""

drop_table_students_query = """
    DROP TABLE students;
"""

check_if_students_table_exists_query = """SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema = 
'python_task' AND table_name = 'students');"""

check_if_rooms_table_exists_query = """
    SELECT EXISTS(SELECT 1 FROM information_schema.tables WHERE table_schema = 'python_task' AND table_name = 'rooms');
"""

list_of_rooms_and_number_of_students_query = """
    SELECT r.id, COUNT(*) AS students_pre_room
    FROM rooms r                                           
    LEFT JOIN students s ON r.id = s.room                       
    GROUP BY r.id;
"""

five_rooms_with_lowest_avg_age_query = """
    SELECT r.id
    FROM rooms r                                           
    JOIN students s ON r.id = s.room    
    GROUP BY r.id
    ORDER BY AVG(AGE(CURRENT_DATE, s.birthday)) ASC
    LIMIT 5;
"""

five_rooms_with_highest_age_diff_query = """
    SELECT r.id
    FROM rooms r                                           
    JOIN students s ON r.id = s.room    
    GROUP BY r.id
    ORDER BY MAX(s.birthday)-MIN(s.birthday) DESC
    LIMIT 5;
"""

list_of_rooms_with_different_genders_query = """
    SELECT id
    FROM
      (
        SELECT rooms.id, students.sex
        FROM rooms
        JOIN students ON rooms.id = students.room
        GROUP BY rooms.id,students.sex
      ) temp
    GROUP BY id
    HAVING COUNT(id) = 2;
"""

retrieve_data_queries = [
    list_of_rooms_and_number_of_students_query,
    list_of_rooms_with_different_genders_query,
    five_rooms_with_lowest_avg_age_query,
    five_rooms_with_highest_age_diff_query,
]

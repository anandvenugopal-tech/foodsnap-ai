from database.db import get_db

def get_nutrition(food_name):
    db = get_db()
    cursor = db.cursor(dictionary = True)

    query = "SELECT * FROM food_nutrition WHERE LOWER(food_name)=LOWER(%s)"
    cursor.execute(query, (food_name,))
    data = cursor.fetchone()

    cursor.close()
    db.close()

    return data



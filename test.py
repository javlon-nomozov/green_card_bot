from loader import db
user_id = 1559808420

user_info = db.select_user(id=user_id)
if user_info:
    print(user_info[3])
else:
    db.add_user(id=user_id, language='uz', name='Joe')


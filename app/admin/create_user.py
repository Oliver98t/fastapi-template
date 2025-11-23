from auth.encrypt import get_password_hash
from database.base_schemas import UserInput
from database.base_orm import user_orm
from database.connection import get_db
from getpass import getpass

while True:
    username = input("enter username: ")
    email = input("enter email: ")
    privilege = input("enter privilege: ")
    password = getpass("enter password: ")
    create_check = input("Create user (y/n): ")

    if create_check == 'y':
        hashed_password = get_password_hash(password)
        user_input = UserInput( username=username,
                                email=email,
                                privilege=privilege,
                                hashed_password=hashed_password)

        # Create a database session and use it with the ORM
        db = next(get_db())
        try:
            new_user = user_orm()
            new_user.create(db=db,obj=user_input)
            print(f"User '{username}' created successfully!")
        finally:
            db.close()

    continue_check = input("Create another user (y/n): ")
    if continue_check != 'y':
        break
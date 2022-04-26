from bson import ObjectId
from pymongo import MongoClient, ReturnDocument
from datetime import datetime
import re

client = MongoClient('localhost:27017')
mydb = client['user_crud']

mycol = mydb['user_data']

def get_user_id():
    try:
        user_id = input("\nEnter user ID: ")
    except:
        print("Invalid ID type")
    return user_id

def get_user_object():
    print(' call one '.center(100, '*'))
    while True:
        user_id = get_user_id()
        result = mycol.find_one({'_id':ObjectId(user_id)})
        if result:
            user = {
                "id": str(result['_id']),
                "name": result['name'],
                "email": result['email'],
                "age": result['age'],
                "access_time": result['access_time']
            }
            break

        else:
            print('User Not found')
            option = input('Do you wanna try again (y/n): ')
            if option in ('y', 'Y'):
                pass
            elif option in ('n', 'N'):
                user = None
                break
            else:
                print('Invalid option.')
    return user

def get_user_name():
    name = input("\nEnter user name: ")
    return name

def get_user_email():
    email = input("\nEnter user email: ")
    return email

def get_user_age():
    age = int(input("\nEnter user\'s age: "))
    return age

def get_user_details():
    name = get_user_name()
    email = get_user_email()
    age = get_user_age()

    access_time = None
    user = {
        "name": name,
        "email": email,
        "age": age,
        "access_time": access_time
    }

    return user

#insert document into the collection
def create_user(user):
    print("Creating user.")
    id = mycol.insert_one(user)
    print("""
    Created user successfull.
    user ID: 
    """, id.inserted_id)

#query document
def access_user(user):
    date_format = "%d %m %y, %H:%M:%S"

    date_str = datetime.now().strftime(date_format)
    date_obj = datetime.strptime(date_str, date_format)
    access_time = date_obj

    print(f"User {user['id']} details: ")
    print(f"""
    Name: {user['name']}
    Emial: {user['email']}
    Age: {user['age']}
    Last access time: {access_time}
    """)

    updated_user = mycol.find_one_and_update({'_id':ObjectId(user['id'])}, {'$set': {'access_time': access_time}}, return_document=ReturnDocument.AFTER)

#update document
def update_input(id, field, value):
    new_user = mycol.find_one_and_update({'_id': ObjectId(id)}, {'$set': {field: value}}, return_document=ReturnDocument.AFTER)
    if new_user is None:
        return 'User not found'
    return new_user

def update_user():
    user_id = get_user_id()

    props = {
            1: {
                'field': 'name',
                'caller': get_user_name
            },
            2: {
                'field': 'email',
                'caller': get_user_email
            },
            3: {
                'field': 'age',
                'caller': get_user_age
            },
            
        }

    while True:
        choice = int(input("""
        Which user data would you like to modify?
        1) Name
        2) Email
        3) Age
        4) Quit
        Input: """))

        if choice in (1, 2, 3):
            updated_user = update_input(user_id, props[choice]['field'], props[choice]['caller']())
            print(updated_user)

        elif choice == 4:
            break;

        else:
            print('Invalid input')

#delete document
def remove_user():
    user_id = get_user_id()
    while True:
        confirm = int(input(f"""
        Are you sure you want to delete user ID {user_id}
        1) Yes
        2) No
        Input: """))

        if confirm == 1:
            mycol.delete_one(
                {'_id': ObjectId(user_id)}
            )
            print(f"Successfully deleted usere ID: {user_id}.")
            break

        elif confirm ==2:
            break

        print("Invalid operation.")

def main():
    while True:
        operation = int(input("""
        What operation would you like to perform?
        1) Create User
        2) Access User
        3) Modify User
        4) Delete User
        5) Exit
        Input: """))

        if operation == 1:
            user = get_user_details()
            create_user(user)

        elif operation == 2:
            user = get_user_object()
            if user:
                access_user(user)

        elif operation == 3:
            update_user()

        elif operation == 4:
            remove_user()

        elif operation == 5:
            print("Exiting".center(100, ('*')))
            break

        else:
            print("Invalid Operation.")

if __name__ == "__main__":
    main()


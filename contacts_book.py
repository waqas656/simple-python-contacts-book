import POSTGRES_CONNECTION
import configparser


def initiate_db():
    # reading properties from 'db.properties' file
    config = configparser.ConfigParser()
    config.read('db.properties')

    db_name = config.get("db", "db_name")
    user = config.get("db", "user")
    password = config.get("db", "password")
    host = config.get("db", "host")
    port = config.get("db", "port")

    global pg_connection
    pg_connection = POSTGRES_CONNECTION.create_connection(
        db_name, user, password, host, port
    )

    if pg_connection is not None:
        try:
            create_database_query = "CREATE DATABASE contacts_book"
            POSTGRES_CONNECTION.create_database(pg_connection, create_database_query)
        except BaseException as e:
            print("Error : " + str(e))

        create_contacts_table = """
        CREATE TABLE IF NOT EXISTS contacts (
          id SERIAL PRIMARY KEY,
          name TEXT NOT NULL, 
          phone_num TEXT NOT NULL,
          email TEXT
        )
        """

        print("Creating table in database ...")
        POSTGRES_CONNECTION.execute_query(pg_connection, create_contacts_table)

    else:
        print("Error: Connection to database was not successful")


def retrieve_and_save_contact_details():
    c_name = input("Please enter contact name: ")
    c_phone = input("Please enter contact phone number: ")
    c_email = input("Please enter contact email: ")

    # creating a tuple for contact details
    contact = (c_name, c_phone, c_email)

    insert_query = (
        f"INSERT INTO contacts (name, phone_num, email) VALUES {contact}"
    )

    print(insert_query)
    POSTGRES_CONNECTION.execute_query(pg_connection, insert_query)


def view_all_contacts():
    all_contacts_query = 'select name, phone_num, email from contacts'
    try:
        cursor = POSTGRES_CONNECTION.execute_query(pg_connection, all_contacts_query)
        contacts_list = cursor.fetchall()

        print(" *** CONTACTS LIST ***")
        if len(contacts_list) > 0:
            for contact in contacts_list:
                print(f"| Name: {contact[0]}    Phone: {contact[1]}     Email: {contact[2]}")
        else:
            print("No contacts saved.")

    except BaseException as e:
        print("ERROR: " + str(e))


def find_contact():
    name_to_find = input("Enter contact name to find: ")
    find_contact_query = f"select name, phone_num, email from contacts where name = '{name_to_find}'"

    try:
        cursor = POSTGRES_CONNECTION.execute_query(pg_connection, find_contact_query)
        contact = cursor.fetchone()
        if contact is not None:
            print("Search Result:")
            print(f"| Name: {contact[0]}    Phone: {contact[1]}     Email: {contact[2]}")
        else:
            print(f"No record found with name : {name_to_find}")

    except BaseException as e:
        print("ERROR: " + str(e))


def delete_contact():
    name_to_delete = input("Enter contact name to delete: ")
    delete_contact_query = f"delete from contacts where name = '{name_to_delete}'"

    try:
        cursor = POSTGRES_CONNECTION.execute_query(pg_connection, delete_contact_query)
        rows_deleted = cursor.rowcount  # gets the number of rows updated

        print(f"{rows_deleted} record(s) deleted") if rows_deleted > 0 else print(f"No records exists with name: {name_to_delete}")

    except BaseException as e:
        print("ERROR: " + str(e))


# flow of app starts here
pg_connection = None
initiate_db()

while True:
    user_choice = input(
        """
Press:  
     y to end program
     v to view all contacts
     f to find a contact
     a to add a contact
     d to delete a contact
     Enter choice: 
""").lower()

    if user_choice == 'y':
        break
    elif user_choice == 'v':
        view_all_contacts()
    elif user_choice == 'f':
        find_contact()
    elif user_choice == 'a':
        retrieve_and_save_contact_details()
    elif user_choice == 'd':
        delete_contact()
    else:
        print("Please enter a key from the above choices ..")

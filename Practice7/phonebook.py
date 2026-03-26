# Task 1
import psycopg2
import csv
from connect import connect

def create_table():
    """ Create the phonebook table if it doesn't exist """
    command = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        phone VARCHAR(20) NOT NULL
    )
    """
    conn = None
    try:
        conn = connect()
        if conn:
            cur = conn.cursor()
            cur.execute(command)
            conn.commit()
            cur.close()
            print("Table 'phonebook' is ready.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error creating table: {error}")
    finally:
        if conn:
            conn.close()

def insert_from_csv(filename):
    create_table() # Ensure table exists
    sql = "INSERT INTO phonebook(name, phone) VALUES(%s, %s)"
    conn = None
    try:
        conn = connect()
        if conn:
            cur = conn.cursor()
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    cur.execute(sql, (row[0], row[1]))
            conn.commit()
            cur.close()
            print("Data imported from CSV successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            conn.close()

def insert_from_console():
    create_table() # Ensure table exists
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    sql = "INSERT INTO phonebook(name, phone) VALUES(%s, %s)"
    conn = None
    try:
        conn = connect()
        if conn:
            cur = conn.cursor()
            cur.execute(sql, (name, phone))
            conn.commit()
            cur.close()
            print("Contact added successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            conn.close()

def update_contact():
    create_table() # Ensure table exists
    print("1. Update Name\n2. Update Phone")
    choice = input("Choose option: ")
    
    if choice == '1':
        old_name = input("Enter current name: ")
        new_name = input("Enter new name: ")
        sql = "UPDATE phonebook SET name = %s WHERE name = %s"
        val = (new_name, old_name)
    elif choice == '2':
        name = input("Enter contact name: ")
        new_phone = input("Enter new phone: ")
        sql = "UPDATE phonebook SET phone = %s WHERE name = %s"
        val = (new_phone, name)
    else:
        print("Invalid choice")
        return

    conn = None
    try:
        conn = connect()
        if conn:
            cur = conn.cursor()
            cur.execute(sql, val)
            conn.commit()
            cur.close()
            print("Contact updated successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            conn.close()

def query_contacts():
    create_table() # Ensure table exists
    print("1. Search by Name\n2. Search by Phone Prefix")
    choice = input("Choose option: ")
    
    if choice == '1':
        name = input("Enter name: ")
        sql = "SELECT * FROM phonebook WHERE name ILIKE %s"
        val = ('%' + name + '%',)
    elif choice == '2':
        prefix = input("Enter phone prefix: ")
        sql = "SELECT * FROM phonebook WHERE phone LIKE %s"
        val = (prefix + '%',)
    else:
        print("Invalid choice")
        return

    conn = None
    try:
        conn = connect()
        if conn:
            cur = conn.cursor()
            cur.execute(sql, val)
            rows = cur.fetchall()
            for row in rows:
                print(row)
            cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            conn.close()

def delete_contact():
    create_table() # Ensure table exists
    print("1. Delete by Name\n2. Delete by Phone")
    choice = input("Choose option: ")
    
    if choice == '1':
        name = input("Enter name: ")
        sql = "DELETE FROM phonebook WHERE name = %s"
        val = (name,)
    elif choice == '2':
        phone = input("Enter phone: ")
        sql = "DELETE FROM phonebook WHERE phone = %s"
        val = (phone,)
    else:
        print("Invalid choice")
        return

    conn = None
    try:
        conn = connect()
        if conn:
            cur = conn.cursor()
            cur.execute(sql, val)
            conn.commit()
            cur.close()
            print("Contact deleted successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn:
            conn.close()

def main():
    while True:
        print("\n--- PhoneBook Menu ---")
        print("1. Insert from CSV")
        print("2. Insert from Console")
        print("3. Update Contact")
        print("4. Query Contacts")
        print("5. Delete Contact")
        print("6. Exit")
        choice = input("Select an option: ")
        
        if choice == '1':
            insert_from_csv('contacts.csv')
        elif choice == '2':
            insert_from_console()
        elif choice == '3':
            update_contact()
        elif choice == '4':
            query_contacts()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            break
        else:
            print("Invalid choice, try again.")

if __name__ == '__main__':
    main()

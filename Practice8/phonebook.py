import psycopg2
from connect import connect


def create_table():
    conn = connect()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS phonebook (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                phone VARCHAR(20) NOT NULL
            )
        """)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        conn.close()


def create_functions_and_procedures():
    """Read .sql files and register them in the database."""
    conn = connect()
    if not conn:
        return
    try:
        cur = conn.cursor()
        with open('functions.sql', 'r') as f:
            cur.execute(f.read())
        with open('procedures.sql', 'r') as f:
            cur.execute(f.read())
        conn.commit()
        cur.close()
        print("Functions and procedures created successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error creating functions/procedures: {error}")
    finally:
        conn.close()


# calls the search_contacts() function from functions.sql
def search_by_pattern():
    pattern = input("Enter search pattern: ")
    conn = connect()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM search_contacts(%s)", (pattern,))
        rows = cur.fetchall()
        if rows:
            print(f"\n{'ID':<5} {'Name':<20} {'Phone':<15}")
            print("-" * 40)
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<20} {row[2]:<15}")
        else:
            print("No contacts found.")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        conn.close()


# calls upsert_contact() procedure — CALL instead of SELECT
def upsert_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    conn = connect()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("CALL upsert_contact(%s, %s)", (name, phone))
        conn.commit()
        cur.close()
        print("Contact upserted successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        conn.close()


# collects names/phones into lists, sends them as arrays to postgres
# the function validates phones and returns any bad entries
def bulk_insert():
    names = []
    phones = []
    print("Enter contacts (empty name to finish):")
    while True:
        name = input("  Name: ")
        if not name:
            break
        phone = input("  Phone: ")
        names.append(name)
        phones.append(phone)

    if not names:
        print("No contacts to insert.")
        return

    conn = connect()
    if not conn:
        return
    try:
        cur = conn.cursor()
        # psycopg2 converts python lists to postgres arrays automatically
        cur.execute("SELECT * FROM bulk_insert_contacts(%s, %s)", (names, phones))
        invalid = cur.fetchall()
        conn.commit()
        if invalid:
            print("\nInvalid entries:")
            print(f"{'Name':<20} {'Phone':<15} {'Reason'}")
            print("-" * 55)
            for row in invalid:
                print(f"{row[0]:<20} {row[1]:<15} {row[2]}")
        else:
            print("All contacts inserted successfully.")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        conn.close()


# limit = how many to show, offset = how many to skip
def query_paginated():
    try:
        limit = int(input("Enter page size (limit): "))
        offset = int(input("Enter offset: "))
    except ValueError:
        print("Invalid input. Please enter numbers.")
        return

    conn = connect()
    if not conn:
        return
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
        rows = cur.fetchall()
        if rows:
            print(f"\n{'ID':<5} {'Name':<20} {'Phone':<15}")
            print("-" * 40)
            for row in rows:
                print(f"{row[0]:<5} {row[1]:<20} {row[2]:<15}")
        else:
            print("No contacts on this page.")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        conn.close()


# pass name or phone, the other one goes as NULL
def delete_contact():
    print("1. Delete by Name")
    print("2. Delete by Phone")
    choice = input("Choose option: ")

    conn = connect()
    if not conn:
        return
    try:
        cur = conn.cursor()
        if choice == '1':
            name = input("Enter name: ")
            cur.execute("CALL delete_contact(%s, NULL)", (name,))
        elif choice == '2':
            phone = input("Enter phone: ")
            cur.execute("CALL delete_contact(NULL, %s)", (phone,))
        else:
            print("Invalid choice.")
            return
        conn.commit()
        cur.close()
        print("Contact deleted successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Error: {error}")
    finally:
        conn.close()


def main():
    create_table()
    create_functions_and_procedures()

    while True:
        print("\n--- PhoneBook Menu (Practice 8) ---")
        print("1. Search by pattern")
        print("2. Upsert contact (insert or update)")
        print("3. Bulk insert contacts")
        print("4. Query with pagination")
        print("5. Delete contact")
        print("6. Exit")
        choice = input("Select an option: ")

        if choice == '1':
            search_by_pattern()
        elif choice == '2':
            upsert_contact()
        elif choice == '3':
            bulk_insert()
        elif choice == '4':
            query_paginated()
        elif choice == '5':
            delete_contact()
        elif choice == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid choice, try again.")


if __name__ == '__main__':
    main()

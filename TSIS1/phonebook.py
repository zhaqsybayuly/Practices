import csv
import json
from connect import connect


def init_db():
    conn = connect()
    if not conn:
        return
    with conn, conn.cursor() as cur:
        with open("schema.sql") as f:
            cur.execute(f.read())
        with open("procedures.sql") as f:
            cur.execute(f.read())
    conn.close()
    print("Schema and procedures created.")


def import_csv(filename="contacts.csv"):
    conn = connect()
    if not conn:
        return
    with conn, conn.cursor() as cur, open(filename, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # find or create group
            cur.execute("SELECT id FROM groups WHERE name=%s", (row["group"],))
            r = cur.fetchone()
            if r:
                gid = r[0]
            else:
                cur.execute("INSERT INTO groups(name) VALUES(%s) RETURNING id", (row["group"],))
                gid = cur.fetchone()[0]
            # insert contact
            cur.execute("""INSERT INTO phonebook(name, phone, email, birthday, group_id)
                           VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                        (row["name"], row["phone"], row["email"], row["birthday"], gid))
            cid = cur.fetchone()[0]
            # also add a row to phones table
            cur.execute("INSERT INTO phones(contact_id, phone, type) VALUES (%s, %s, %s)",
                        (cid, row["phone"], row["phone_type"]))
    conn.close()
    print(f"Imported contacts from {filename}.")


def filter_by_group():
    group = input("Group name: ")
    conn = connect()
    with conn, conn.cursor() as cur:
        cur.execute("""SELECT pb.id, pb.name, pb.phone, pb.email
                       FROM phonebook pb JOIN groups g ON g.id = pb.group_id
                       WHERE g.name = %s""", (group,))
        for row in cur.fetchall():
            print(row)
    conn.close()


def search_by_email():
    q = input("Email pattern: ")
    conn = connect()
    with conn, conn.cursor() as cur:
        cur.execute("SELECT id, name, phone, email FROM phonebook WHERE email ILIKE %s",
                    (f"%{q}%",))
        for row in cur.fetchall():
            print(row)
    conn.close()


def sort_results():
    print("Sort by: 1) name  2) birthday  3) date added")
    choice = input("Choose: ")
    column = {"1": "name", "2": "birthday", "3": "created_at"}.get(choice)
    if not column:
        print("Invalid")
        return
    conn = connect()
    with conn, conn.cursor() as cur:
        cur.execute(f"SELECT id, name, phone, email, birthday FROM phonebook ORDER BY {column} NULLS LAST")
        for row in cur.fetchall():
            print(row)
    conn.close()


def paginate():
    page_size = 5
    offset = 0
    conn = connect()
    while True:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (page_size, offset))
            rows = cur.fetchall()
        if not rows:
            print("No more results.")
        else:
            print(f"\n--- offset {offset} ---")
            for r in rows:
                print(r)
        cmd = input("[next/prev/quit]: ").strip().lower()
        if cmd == "next":
            offset += page_size
        elif cmd == "prev":
            offset = max(0, offset - page_size)
        else:
            break
    conn.close()


def export_json(filename="export.json"):
    conn = connect()
    with conn, conn.cursor() as cur:
        cur.execute("""SELECT pb.id, pb.name, pb.email, pb.birthday, g.name AS gname
                       FROM phonebook pb LEFT JOIN groups g ON g.id = pb.group_id""")
        contacts = []
        for row in cur.fetchall():
            cid, name, email, birthday, group = row
            cur2 = conn.cursor()
            cur2.execute("SELECT phone, type FROM phones WHERE contact_id=%s", (cid,))
            phones = [{"phone": p, "type": t} for p, t in cur2.fetchall()]
            cur2.close()
            contacts.append({
                "id": cid, "name": name, "email": email,
                "birthday": str(birthday) if birthday else None,
                "group": group, "phones": phones,
            })
    with open(filename, "w") as f:
        json.dump(contacts, f, indent=2, ensure_ascii=False)
    conn.close()
    print(f"Exported {len(contacts)} contacts to {filename}.")


def import_json(filename="export.json"):
    with open(filename) as f:
        data = json.load(f)
    conn = connect()
    with conn, conn.cursor() as cur:
        for c in data:
            cur.execute("SELECT id FROM phonebook WHERE name=%s", (c["name"],))
            existing = cur.fetchone()
            if existing:
                action = input(f"{c['name']} exists. [s]kip / [o]verwrite? ").lower()
                if action == "s":
                    continue
                cur.execute("DELETE FROM phonebook WHERE id=%s", (existing[0],))
            # insert group if needed
            gid = None
            if c.get("group"):
                cur.execute("SELECT id FROM groups WHERE name=%s", (c["group"],))
                r = cur.fetchone()
                gid = r[0] if r else cur.execute(
                    "INSERT INTO groups(name) VALUES(%s) RETURNING id", (c["group"],)
                ) or cur.fetchone()[0]
            # primary phone (first one or empty)
            primary = c["phones"][0]["phone"] if c.get("phones") else ""
            cur.execute("""INSERT INTO phonebook(name, phone, email, birthday, group_id)
                           VALUES (%s, %s, %s, %s, %s) RETURNING id""",
                        (c["name"], primary, c.get("email"), c.get("birthday"), gid))
            cid = cur.fetchone()[0]
            for p in c.get("phones", []):
                cur.execute("INSERT INTO phones(contact_id, phone, type) VALUES (%s, %s, %s)",
                            (cid, p["phone"], p["type"]))
    conn.close()
    print(f"Imported {len(data)} contacts from {filename}.")


def add_phone():
    name = input("Contact name: ")
    phone = input("Phone: ")
    type_ = input("Type [home/work/mobile]: ")
    conn = connect()
    with conn, conn.cursor() as cur:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, type_))
    conn.close()
    print("Phone added.")


def move_to_group_action():
    name = input("Contact name: ")
    group = input("Group name: ")
    conn = connect()
    with conn, conn.cursor() as cur:
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
    conn.close()
    print("Contact moved.")


def search_contacts():
    q = input("Search query: ")
    conn = connect()
    with conn, conn.cursor() as cur:
        cur.execute("SELECT * FROM search_contacts(%s)", (q,))
        for row in cur.fetchall():
            print(row)
    conn.close()


def main():
    init_db()
    actions = {
        "1": ("Filter by group",  filter_by_group),
        "2": ("Search by email",  search_by_email),
        "3": ("Sort results",     sort_results),
        "4": ("Paginate",         paginate),
        "5": ("Add phone",        add_phone),
        "6": ("Move to group",    move_to_group_action),
        "7": ("Search contacts",  search_contacts),
        "8": ("Import CSV",       import_csv),
        "9": ("Export JSON",      export_json),
        "10": ("Import JSON",     import_json),
        "0": ("Quit",             None),
    }
    while True:
        print("\n=== TSIS1 PhoneBook ===")
        for k, (label, _) in actions.items():
            print(f"{k}. {label}")
        choice = input("Choose: ").strip()
        if choice == "0":
            break
        action = actions.get(choice)
        if action and action[1]:
            try:
                action[1]()
            except Exception as e:
                print("Error:", e)
        else:
            print("Invalid choice")


if __name__ == "__main__":
    main()

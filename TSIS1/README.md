# TSIS1 — PhoneBook Extended

Extends Practice 7-8 phonebook with:
- `groups` table + `phones` table (1-to-many)
- `email`, `birthday`, `created_at` columns
- New procedures: `add_phone`, `move_to_group`
- Extended `search_contacts` covers name + email + all phones
- Console: filter by group, search by email, sort, paginate
- JSON export / import (with duplicate prompt)
- Extended CSV import (email, birthday, group, phone type)

## Run
```bash
python phonebook.py
```
The first run executes `schema.sql` and `procedures.sql` automatically.

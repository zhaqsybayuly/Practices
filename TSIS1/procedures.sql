-- add a new phone for an existing contact
CREATE OR REPLACE PROCEDURE add_phone(p_contact_name VARCHAR, p_phone VARCHAR, p_type VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    cid INT;
BEGIN
    SELECT id INTO cid FROM phonebook WHERE name = p_contact_name LIMIT 1;
    IF cid IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;
    INSERT INTO phones(contact_id, phone, type) VALUES (cid, p_phone, p_type);
END;
$$;

-- move contact to a different group; create the group if it doesn't exist
CREATE OR REPLACE PROCEDURE move_to_group(p_contact_name VARCHAR, p_group_name VARCHAR)
LANGUAGE plpgsql AS $$
DECLARE
    gid INT;
BEGIN
    SELECT id INTO gid FROM groups WHERE name = p_group_name;
    IF gid IS NULL THEN
        INSERT INTO groups(name) VALUES (p_group_name) RETURNING id INTO gid;
    END IF;
    UPDATE phonebook SET group_id = gid WHERE name = p_contact_name;
END;
$$;

-- drop any older version (Practice 8 may have left a function with a different return type)
DROP FUNCTION IF EXISTS search_contacts(TEXT);
DROP FUNCTION IF EXISTS get_contacts_paginated(INT, INT);

-- extended pattern search across name, email and all phones from the phones table
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR, email VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT pb.id, pb.name, pb.phone, pb.email
    FROM phonebook pb
    LEFT JOIN phones ph ON ph.contact_id = pb.id
    WHERE pb.name  ILIKE '%' || p_query || '%'
       OR pb.phone ILIKE '%' || p_query || '%'
       OR pb.email ILIKE '%' || p_query || '%'
       OR ph.phone ILIKE '%' || p_query || '%';
END;
$$ LANGUAGE plpgsql;

-- pagination function (kept from Practice 8 — required for console navigation)
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR, email VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT pb.id, pb.name, pb.phone, pb.email
    FROM phonebook pb
    ORDER BY pb.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

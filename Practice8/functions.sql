-- find contacts where name or phone matches the given pattern
-- using ILIKE so it's case-insensitive
CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.name, p.phone
    FROM phonebook p
    WHERE p.name ILIKE '%' || pattern || '%'
       OR p.phone ILIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- return contacts in chunks instead of all at once
-- page_limit = how many rows, page_offset = how many to skip
CREATE OR REPLACE FUNCTION get_contacts_paginated(page_limit INT, page_offset INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id, p.name, p.phone
    FROM phonebook p
    ORDER BY p.id
    LIMIT page_limit OFFSET page_offset;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- Procedure 1: Upsert contact
-- If name exists -> update phone, else -> insert new
-- ============================================
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE name = p_name;
        RAISE NOTICE 'Updated phone for %', p_name;
    ELSE
        INSERT INTO phonebook(name, phone) VALUES(p_name, p_phone);
        RAISE NOTICE 'Inserted new contact %', p_name;
    END IF;
END;
$$;

-- ============================================
-- Procedure 2: Bulk insert contacts with phone validation
-- Phone must be digits only and 11 characters long
-- Returns table of invalid entries
-- ============================================
CREATE OR REPLACE FUNCTION bulk_insert_contacts(
    p_names TEXT[],
    p_phones TEXT[]
)
RETURNS TABLE(invalid_name TEXT, invalid_phone TEXT, reason TEXT) AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(p_names, 1) LOOP
        -- Validate phone: must be digits only and 11 characters
        IF p_phones[i] !~ '^\d{11}$' THEN
            invalid_name := p_names[i];
            invalid_phone := p_phones[i];
            reason := 'Phone must be exactly 11 digits';
            RETURN NEXT;
        ELSE
            -- Check if contact exists, then upsert
            IF EXISTS (SELECT 1 FROM phonebook WHERE name = p_names[i]) THEN
                UPDATE phonebook SET phone = p_phones[i] WHERE name = p_names[i];
            ELSE
                INSERT INTO phonebook(name, phone) VALUES(p_names[i], p_phones[i]);
            END IF;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- ============================================
-- Procedure 3: Delete contact by name or phone
-- ============================================
CREATE OR REPLACE PROCEDURE delete_contact(p_name VARCHAR DEFAULT NULL, p_phone VARCHAR DEFAULT NULL)
LANGUAGE plpgsql AS $$
BEGIN
    IF p_name IS NOT NULL THEN
        DELETE FROM phonebook WHERE name = p_name;
        RAISE NOTICE 'Deleted contact with name: %', p_name;
    ELSIF p_phone IS NOT NULL THEN
        DELETE FROM phonebook WHERE phone = p_phone;
        RAISE NOTICE 'Deleted contact with phone: %', p_phone;
    ELSE
        RAISE EXCEPTION 'Either name or phone must be provided';
    END IF;
END;
$$;

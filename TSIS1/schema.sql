-- TSIS1 schema: extends Practice 7-8 phonebook with groups, phones, email, birthday

CREATE TABLE IF NOT EXISTS groups (
    id   SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

-- seed default groups
INSERT INTO groups(name) VALUES ('Family'), ('Work'), ('Friend'), ('Other')
    ON CONFLICT (name) DO NOTHING;

-- base contacts table from Practice 7
CREATE TABLE IF NOT EXISTS phonebook (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(255) NOT NULL,
    phone      VARCHAR(20)  NOT NULL,
    email      VARCHAR(100),
    birthday   DATE,
    group_id   INTEGER REFERENCES groups(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- add the new columns if the table already existed without them
ALTER TABLE phonebook ADD COLUMN IF NOT EXISTS email      VARCHAR(100);
ALTER TABLE phonebook ADD COLUMN IF NOT EXISTS birthday   DATE;
ALTER TABLE phonebook ADD COLUMN IF NOT EXISTS group_id   INTEGER REFERENCES groups(id);
ALTER TABLE phonebook ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT NOW();

-- 1-to-many phones table: each contact can have many phones with a type
CREATE TABLE IF NOT EXISTS phones (
    id         SERIAL PRIMARY KEY,
    contact_id INTEGER REFERENCES phonebook(id) ON DELETE CASCADE,
    phone      VARCHAR(20) NOT NULL,
    type       VARCHAR(10) CHECK (type IN ('home', 'work', 'mobile'))
);

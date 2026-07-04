CREATE OR REPLACE PROCEDURE upsert_contact(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM contacts
        WHERE first_name = p_first_name
          AND last_name = p_last_name
    ) THEN

        UPDATE contacts
        SET phone = p_phone
        WHERE first_name = p_first_name
          AND last_name = p_last_name;

    ELSE

        INSERT INTO contacts(first_name, last_name, phone)
        VALUES (p_first_name, p_last_name, p_phone);

    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_first_names TEXT[],
    p_last_names TEXT[],
    p_phones TEXT[]
)
LANGUAGE plpgsql
AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1..array_length(p_first_names, 1) LOOP

        IF p_phones[i] ~ '^87[0-9]{9}$' THEN

            INSERT INTO contacts(first_name, last_name, phone)
            VALUES (
                p_first_names[i],
                p_last_names[i],
                p_phones[i]
            );

        ELSE
            RAISE NOTICE 'Invalid phone: %', p_phones[i];
        END IF;

    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(
    p_value VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN
    DELETE FROM contacts
    WHERE first_name = p_value
       OR phone = p_value;
END;
$$;
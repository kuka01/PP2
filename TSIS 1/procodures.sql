CREATE OR REPLACE PROCEDURE upsert_contact(
    p_first_name VARCHAR,
    p_last_name VARCHAR,
    p_phone VARCHAR
)
LANGUAGE plpgsql
AS $$
BEGIN

    IF EXISTS(
        SELECT 1
        FROM contacts
        WHERE first_name=p_first_name
        AND last_name=p_last_name
    )

    THEN

        UPDATE contacts
        SET phone=p_phone
        WHERE first_name=p_first_name
        AND last_name=p_last_name;

    ELSE

        INSERT INTO contacts(first_name,last_name,phone)
        VALUES(p_first_name,p_last_name,p_phone);

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

FOR i IN 1..array_length(p_first_names,1)

LOOP

    IF p_phones[i] ~ '^87[0-9]{9}$'

    THEN

        INSERT INTO contacts(first_name,last_name,phone)

        VALUES(

            p_first_names[i],
            p_last_names[i],
            p_phones[i]

        );

    ELSE

        RAISE NOTICE 'Invalid phone: %',p_phones[i];

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

WHERE first_name=p_value

OR phone=p_value;

END;

$$;

-- ==========================================
-- TSIS 1 Procedures
-- ==========================================

-- Добавление нового номера существующему контакту
CREATE OR REPLACE PROCEDURE add_phone(
    p_contact_name VARCHAR,
    p_phone VARCHAR,
    p_type VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INT;
BEGIN

    SELECT id
    INTO v_contact_id
    FROM contacts
    WHERE first_name = p_contact_name;

    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact % not found', p_contact_name;
    END IF;

    INSERT INTO phones(contact_id, phone, type)
    VALUES(v_contact_id, p_phone, p_type);

END;
$$;


-- Перемещение контакта в другую группу
CREATE OR REPLACE PROCEDURE move_to_group(
    p_contact_name VARCHAR,
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_group_id INT;
BEGIN

    -- Если группы нет — создаем
    INSERT INTO groups(name)
    VALUES(p_group_name)
    ON CONFLICT(name) DO NOTHING;

    SELECT id
    INTO v_group_id
    FROM groups
    WHERE name = p_group_name;

    UPDATE contacts
    SET group_id = v_group_id
    WHERE first_name = p_contact_name;

END;
$$;
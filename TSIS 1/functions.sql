CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p_pattern TEXT)
RETURNS TABLE(
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.last_name, c.phone
    FROM contacts c
    WHERE c.first_name ILIKE '%' || p_pattern || '%'
       OR c.last_name ILIKE '%' || p_pattern || '%'
       OR c.phone ILIKE '%' || p_pattern || '%';
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_limit INT,
    p_offset INT
)
RETURNS TABLE(
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    phone VARCHAR
)
AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.last_name, c.phone
    FROM contacts c
    ORDER BY c.id
    LIMIT p_limit
    OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

-- ==========================================
-- TSIS 1 Functions
-- ==========================================

CREATE OR REPLACE FUNCTION search_contacts(
    p_query TEXT
)
RETURNS TABLE(
    id INT,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    birthday DATE,
    group_name VARCHAR,
    phone VARCHAR,
    phone_type VARCHAR
)
LANGUAGE plpgsql
AS
$$
BEGIN

RETURN QUERY

SELECT DISTINCT

    c.id,
    c.first_name,
    c.last_name,
    c.email,
    c.birthday,
    g.name,
    p.phone,
    p.type

FROM contacts c

LEFT JOIN groups g
ON c.group_id = g.id

LEFT JOIN phones p
ON c.id = p.contact_id

WHERE

      c.first_name ILIKE '%' || p_query || '%'
   OR c.last_name  ILIKE '%' || p_query || '%'
   OR c.email      ILIKE '%' || p_query || '%'
   OR p.phone      ILIKE '%' || p_query || '%';

END;
$$;
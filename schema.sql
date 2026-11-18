-- Run this once in psql to create the database:
-- psql -U postgres -c "CREATE DATABASE alumni_db;"

-- Then connect and run db.py (init_db()) via Python, OR paste the DDL below:

CREATE TABLE IF NOT EXISTS alumni (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(150) UNIQUE NOT NULL,
    phone       VARCHAR(20),
    batch_year  INTEGER,
    course      VARCHAR(50),
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS employment (
    id              SERIAL PRIMARY KEY,
    alumni_id       INTEGER REFERENCES alumni(id) ON DELETE CASCADE,
    company         VARCHAR(150),
    designation     VARCHAR(100),
    city            VARCHAR(80),
    start_year      INTEGER,
    end_year        INTEGER,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS mentorship (
    id           SERIAL PRIMARY KEY,
    mentor_id    INTEGER REFERENCES alumni(id) ON DELETE CASCADE,
    topic        VARCHAR(200),
    availability VARCHAR(50),
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

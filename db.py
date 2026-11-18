"""
Database configuration and initialization for Alumni Management System.
Update DB_CONFIG with your PostgreSQL credentials before running.
"""
import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "host": "localhost",
    "database": "alumni_db",
    "user": "postgres",
    "password": "postgres123",
    "port": 5432,
}


def get_connection():
    """Return a new database connection."""
    return psycopg2.connect(**DB_CONFIG)


def init_db():
    """Create all tables if they do not exist."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS alumni (
            id          SERIAL PRIMARY KEY,
            name        VARCHAR(100) NOT NULL,
            email       VARCHAR(150) UNIQUE NOT NULL,
            phone       VARCHAR(20),
            batch_year  INTEGER,
            course      VARCHAR(50),
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS employment (
            id              SERIAL PRIMARY KEY,
            alumni_id       INTEGER REFERENCES alumni(id) ON DELETE CASCADE,
            company         VARCHAR(150),
            designation     VARCHAR(100),
            city            VARCHAR(80),
            start_year      INTEGER,
            end_year        INTEGER,       -- NULL means current job
            created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS mentorship (
            id          SERIAL PRIMARY KEY,
            mentor_id   INTEGER REFERENCES alumni(id) ON DELETE CASCADE,
            topic       VARCHAR(200),
            availability VARCHAR(50),   -- e.g. 'Weekends', 'Evenings'
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("Database initialised successfully.")


if __name__ == "__main__":
    init_db()

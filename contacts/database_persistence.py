from contextlib import contextmanager

import os
import logging
import psycopg2
from psycopg2.extras import DictCursor

LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

class DatabasePersistence:
    def __init__(self):
        self._setup_schema()

    @contextmanager
    def _database_connect(self):
        if os.environ.get('FLASK_ENV') == 'production':
            connection = psycopg2.connect(os.environ['DATABASE_URL'])
        else:
            connection = psycopg2.connect(dbname='contacts')
        try:
            with connection:
                yield connection
        finally:
            connection.close()
    
    def _setup_schema(self):
        with self._database_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_name = 'users';
                """)
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                        CREATE TABLE users (
                            id serial PRIMARY KEY,
                            username text NOT NULL UNIQUE,
                            password_hash text NOT NULL
                        );
                    """)
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_name = 'categories';
                """)
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                        CREATE TABLE categories(
                        id serial PRIMARY KEY,
                        name text NOT NULL,
                        user_id int NOT NULL REFERENCES users (id) ON DELETE CASCADE,
                        CONSTRAINT unique_category_per_user UNIQUE (name, user_id)
                        );
                    """)
                cursor.execute("""
                    SELECT COUNT(*)
                    FROM information_schema.tables
                    WHERE table_schema = 'public' AND table_name = 'contacts';
                """)
                if cursor.fetchone()[0] == 0:
                    cursor.execute("""
                        CREATE TABLE contacts (
                        id serial PRIMARY KEY,
                        first_name text NOT NULL,
                        last_name text NOT NULL,
                        phone_number text NOT NULL,
                        email text,
                        category_id int NOT NULL REFERENCES categories (id),
                        user_id int NOT NULL REFERENCES users (id) ON DELETE CASCADE,
                        CONSTRAINT unique_name_per_user UNIQUE (first_name, last_name, user_id)
                        );
                    """)
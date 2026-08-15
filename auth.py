import sqlite3
import bcrypt
from pathlib import Path


DB_PATH = Path(__file__).parent / "data" / "users.db"


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:

        # USERS TABLE
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL
            )
            """
        )

        # CAMPAIGNS TABLE
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS campaigns (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )

        # LEADS TABLE
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                campaign_id INTEGER NOT NULL,
                name TEXT,
                company TEXT,
                position TEXT,
                industry TEXT,
                email TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
            )
            """
        )

        conn.commit()


def create_user(email, password):
    email = email.strip().lower()

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    )

    try:
        with sqlite3.connect(DB_PATH) as conn:

            conn.execute(
                """
                INSERT INTO users (email, password_hash)
                VALUES (?, ?)
                """,
                (email, password_hash),
            )

            conn.commit()

        return True, "Account created successfully."

    except sqlite3.IntegrityError:
        return False, "An account with this email already exists."


def authenticate_user(email, password):
    email = email.strip().lower()

    with sqlite3.connect(DB_PATH) as conn:

        user = conn.execute(
            """
            SELECT id, email, password_hash
            FROM users
            WHERE email = ?
            """,
            (email,),
        ).fetchone()

    if not user:
        return False, None

    user_id, user_email, password_hash = user

    if bcrypt.checkpw(
        password.encode("utf-8"),
        password_hash,
    ):
        return True, {
            "id": user_id,
            "email": user_email,
        }

    return False, None


def create_campaign(user_id, campaign_name):
    with sqlite3.connect(DB_PATH) as conn:

        cursor = conn.execute(
            """
            INSERT INTO campaigns (user_id, name)
            VALUES (?, ?)
            """,
            (user_id, campaign_name),
        )

        conn.commit()

        return cursor.lastrowid


def get_user_campaigns(user_id):
    with sqlite3.connect(DB_PATH) as conn:

        campaigns = conn.execute(
            """
            SELECT id, name, created_at
            FROM campaigns
            WHERE user_id = ?
            ORDER BY created_at DESC
            """,
            (user_id,),
        ).fetchall()

    return campaigns


def save_lead(campaign_id, lead):
    with sqlite3.connect(DB_PATH) as conn:

        cursor = conn.execute(
            """
            INSERT INTO leads (
                campaign_id,
                name,
                company,
                position,
                industry,
                email
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                campaign_id,
                lead.name,
                lead.company,
                lead.position,
                lead.industry,
                lead.email,
            ),
        )

        conn.commit()

        return cursor.lastrowid


def get_campaign_leads(campaign_id):
    with sqlite3.connect(DB_PATH) as conn:

        leads = conn.execute(
            """
            SELECT
                id,
                name,
                company,
                position,
                industry,
                email
            FROM leads
            WHERE campaign_id = ?
            ORDER BY created_at DESC
            """,
            (campaign_id,),
        ).fetchall()

    return leads
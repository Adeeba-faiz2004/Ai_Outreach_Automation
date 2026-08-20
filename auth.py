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
                status TEXT NOT NULL DEFAULT 'Active',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
            """
        )

        # Migration safety: if the campaigns table already existed from
        # before this feature was added, it won't have a `status` column
        # yet. ALTER TABLE has no "IF NOT EXISTS" in SQLite, so we try
        # and simply ignore the error if the column is already there.
        try:
            conn.execute(
                "ALTER TABLE campaigns ADD COLUMN status TEXT NOT NULL DEFAULT 'Active'"
            )
        except sqlite3.OperationalError:
            pass

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
                status TEXT DEFAULT 'pending',
                subject TEXT,
                body TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (campaign_id) REFERENCES campaigns(id)
            )
            """
        )

        # Migration safety for pre-existing databases that were created
        # before status/subject/body/updated_at existed on this table.
        for column, definition in [
            ("status", "TEXT DEFAULT 'pending'"),
            ("subject", "TEXT"),
            ("body", "TEXT"),
            ("updated_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"),
        ]:
            try:
                conn.execute(
                    f"ALTER TABLE leads ADD COLUMN {column} {definition}"
                )
            except sqlite3.OperationalError:
                pass

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
            INSERT INTO campaigns (user_id, name, status)
            VALUES (?, ?, 'Active')
            """,
            (user_id, campaign_name),
        )

        conn.commit()

        return cursor.lastrowid


def update_campaign_status(campaign_id, status):
    """
    Update a campaign's status.

    Allowed values: 'Active', 'Paused', 'Completed'
    """
    valid_statuses = ("Active", "Paused", "Completed")

    if status not in valid_statuses:
        raise ValueError(
            f"Invalid status '{status}'. Must be one of {valid_statuses}."
        )

    with sqlite3.connect(DB_PATH) as conn:

        conn.execute(
            """
            UPDATE campaigns
            SET status = ?
            WHERE id = ?
            """,
            (status, campaign_id),
        )

        conn.commit()


def get_user_campaigns(user_id):
    with sqlite3.connect(DB_PATH) as conn:

        campaigns = conn.execute(
            """
            SELECT id, name, status, created_at
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


def update_lead_status(lead_id, status, subject=None, body=None):
    """
    Update a lead's outreach status (e.g. "sent", "failed", "generated")
    and optionally store the latest subject/body that was generated or
    sent for that lead.

    This is a no-op-safe function: if the leads table doesn't yet have
    the status/subject/body columns (older databases), they are added
    automatically the first time this module is imported (see the
    migration block in init_db()).
    """
    with sqlite3.connect(DB_PATH) as conn:

        conn.execute(
            """
            UPDATE leads
            SET status = ?,
                subject = ?,
                body = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (status, subject, body, lead_id),
        )

        conn.commit()
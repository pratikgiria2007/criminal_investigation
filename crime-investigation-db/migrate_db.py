import os
from db.connection import get_db_connection
from werkzeug.security import generate_password_hash

def migrate():
    conn = get_db_connection()
    if not conn:
        print("Failed to connect to database.")
        return

    try:
        cursor = conn.cursor()
        
        # 1. Create Users Table
        print("Creating Users table...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                user_id         INT AUTO_INCREMENT PRIMARY KEY,
                username        VARCHAR(50) UNIQUE NOT NULL,
                password_hash   VARCHAR(255) NOT NULL,
                role            ENUM('Official', 'Casual') DEFAULT 'Casual',
                officer_id      INT NULL,
                FOREIGN KEY (officer_id) REFERENCES Officers(officer_id) ON DELETE SET NULL
            );
        """)
        
        # 2. Insert default 'admin' user (Official)
        print("Inserting 'admin' user...")
        admin_hash = generate_password_hash("admin123")
        cursor.execute("""
            INSERT INTO Users (username, password_hash, role)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE password_hash=VALUES(password_hash), role=VALUES(role)
        """, ('admin', admin_hash, 'Official'))
        
        # 3. Insert default 'guest' user (Casual)
        print("Inserting 'guest' user...")
        guest_hash = generate_password_hash("guest123")
        cursor.execute("""
            INSERT INTO Users (username, password_hash, role)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE password_hash=VALUES(password_hash), role=VALUES(role)
        """, ('guest', guest_hash, 'Casual'))
        
        conn.commit()
        print("Migration completed successfully.")
        
    except Exception as e:
        conn.rollback()
        print(f"Migration failed: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

if __name__ == '__main__':
    migrate()

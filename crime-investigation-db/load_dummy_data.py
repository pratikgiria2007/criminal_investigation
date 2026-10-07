"""
Load dummy data from dummy_data.sql into the crime_db database.
Run from the crime-investigation-db directory.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.connection import get_db_connection

DUMMY_SQL = os.path.join(os.path.dirname(__file__), '..', 'dummy_data.sql')


def split_sql_statements(sql):
    """Split SQL on semicolons outside quoted strings and comments."""
    statements = []
    current = []
    quote = None
    index = 0

    while index < len(sql):
        char = sql[index]
        next_char = sql[index + 1] if index + 1 < len(sql) else ''

        if quote:
            current.append(char)
            if char == '\\' and quote in ("'", '"') and next_char:
                current.append(next_char)
                index += 2
                continue
            if char == quote:
                if next_char == quote:
                    current.append(next_char)
                    index += 2
                    continue
                quote = None
            index += 1
            continue

        if char in ("'", '"', '`'):
            quote = char
            current.append(char)
            index += 1
            continue

        if char == '#' or (
            char == '-' and next_char == '-' and
            (index + 2 == len(sql) or sql[index + 2].isspace())
        ):
            newline = sql.find('\n', index)
            end = len(sql) if newline == -1 else newline + 1
            current.append(sql[index:end])
            index = end
            continue

        if char == '/' and next_char == '*':
            end_comment = sql.find('*/', index + 2)
            end = len(sql) if end_comment == -1 else end_comment + 2
            current.append(sql[index:end])
            index = end
            continue

        if char == ';':
            statement = ''.join(current).strip()
            if statement:
                statements.append(statement)
            current = []
        else:
            current.append(char)
        index += 1

    statement = ''.join(current).strip()
    if statement:
        statements.append(statement)
    return statements


def load_dummy_data():
    conn = get_db_connection()
    if not conn:
        print("ERROR: Database connection failed.")
        return

    cursor = None
    try:
        cursor = conn.cursor()
        with open(DUMMY_SQL, 'r', encoding='utf-8') as f:
            sql = f.read()

        statements = split_sql_statements(sql)
        loaded = 0
        errors = 0
        for statement_number, stmt in enumerate(statements, start=1):
            if not stmt:
                continue
            try:
                cursor.execute(stmt)
                loaded += 1
            except Exception as e:
                if 'Duplicate entry' in str(e):
                    print(f"  [SKIP] Duplicate: {str(e)[:80]}")
                else:
                    print(f"  [ERR ] Statement {statement_number}: {e}")
                    errors += 1

        if errors:
            conn.rollback()
            print("Changes rolled back because one or more statements failed.")
        else:
            conn.commit()
        print(f"\nDone. {loaded} statements executed. {errors} errors.")
    except FileNotFoundError:
        print(f"dummy_data.sql not found at: {DUMMY_SQL}")
    except Exception as e:
        conn.rollback()
        print(f"Fatal error: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

if __name__ == '__main__':
    load_dummy_data()

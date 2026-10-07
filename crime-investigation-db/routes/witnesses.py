from flask import Blueprint, render_template, jsonify, request
from db.connection import get_db_connection

witnesses_bp = Blueprint('witnesses', __name__)

# ── Page ──────────────────────────────────────────────────────────────────────
@witnesses_bp.route('/witnesses', methods=['GET'])
def list_witnesses():
    return render_template('witnesses.html')

# ── API: List all witnesses (optionally filter by case) ───────────────────────
@witnesses_bp.route('/api/witnesses', methods=['GET'])
def api_get_witnesses():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        case_id = request.args.get('case_id')
        if case_id:
            cursor.execute("""
                SELECT w.*, cw.statement, cw.case_id
                FROM Witnesses w
                JOIN Case_Witnesses cw ON w.witness_id = cw.witness_id
                WHERE cw.case_id = %s
                ORDER BY w.witness_id DESC
            """, (case_id,))
        else:
            cursor.execute("""
                SELECT w.*,
                       COUNT(cw.case_id) AS case_count
                FROM Witnesses w
                LEFT JOIN Case_Witnesses cw ON w.witness_id = cw.witness_id
                GROUP BY w.witness_id
                ORDER BY w.witness_id DESC
            """)
        results = cursor.fetchall()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Get single witness with statements ───────────────────────────────────
@witnesses_bp.route('/api/witnesses/<int:witness_id>', methods=['GET'])
def api_get_witness(witness_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Witnesses WHERE witness_id = %s", (witness_id,))
        witness = cursor.fetchone()
        if not witness:
            return jsonify({"error": "Witness not found"}), 404

        cursor.execute("""
            SELECT cw.case_id, c.case_title, cw.statement
            FROM Case_Witnesses cw
            JOIN Cases c ON cw.case_id = c.case_id
            WHERE cw.witness_id = %s
        """, (witness_id,))
        witness['cases'] = cursor.fetchall()
        return jsonify(witness)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Create witness ───────────────────────────────────────────────────────
@witnesses_bp.route('/api/witnesses', methods=['POST'])
def api_create_witness():
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Witnesses (name, contact_info, address, is_anonymous, protection_status)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data.get('name'),
            data.get('contact_info'),
            data.get('address'),
            data.get('is_anonymous', 0),
            data.get('protection_status', 'None')
        ))
        witness_id = cursor.lastrowid

        # If case_id and statement provided, link immediately
        case_id = data.get('case_id')
        statement = data.get('statement')
        if case_id and statement:
            cursor.execute("""
                INSERT INTO Case_Witnesses (case_id, witness_id, statement)
                VALUES (%s, %s, %s)
            """, (case_id, witness_id, statement))

        conn.commit()
        return jsonify({"message": "Witness created", "witness_id": witness_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Update witness ───────────────────────────────────────────────────────
@witnesses_bp.route('/api/witnesses/<int:witness_id>', methods=['PUT'])
def api_update_witness(witness_id):
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Witnesses
            SET name=%s, contact_info=%s, address=%s, is_anonymous=%s, protection_status=%s
            WHERE witness_id=%s
        """, (
            data.get('name'),
            data.get('contact_info'),
            data.get('address'),
            data.get('is_anonymous', 0),
            data.get('protection_status', 'None'),
            witness_id
        ))
        conn.commit()
        return jsonify({"message": "Witness updated"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Delete witness ───────────────────────────────────────────────────────
@witnesses_bp.route('/api/witnesses/<int:witness_id>', methods=['DELETE'])
def api_delete_witness(witness_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Witnesses WHERE witness_id = %s", (witness_id,))
        conn.commit()
        return jsonify({"message": "Witness deleted"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Link witness to case (with statement) ────────────────────────────────
@witnesses_bp.route('/api/cases/<int:case_id>/witnesses', methods=['POST'])
def api_link_witness(case_id):
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Case_Witnesses (case_id, witness_id, statement)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE statement = VALUES(statement)
        """, (case_id, data.get('witness_id'), data.get('statement')))
        conn.commit()
        return jsonify({"message": "Witness linked to case"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

from flask import Blueprint, render_template, jsonify, request
from db.connection import get_db_connection

officers_bp = Blueprint('officers', __name__)

# ── Page ──────────────────────────────────────────────────────────────────────
@officers_bp.route('/officers', methods=['GET'])
def list_officers():
    return render_template('officers.html')

# ── API: List all officers ────────────────────────────────────────────────────
@officers_bp.route('/api/officers', methods=['GET'])
def api_get_officers():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        # View_Officer_Performance columns from DB: officer_id, name, total_cases, solved_cases
        cursor.execute("""
            SELECT o.*,
                   vp.total_cases,
                   vp.solved_cases
            FROM Officers o
            LEFT JOIN View_Officer_Performance vp ON o.officer_id = vp.officer_id
            ORDER BY o.officer_id DESC
        """)
        results = cursor.fetchall()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Get single officer ───────────────────────────────────────────────────
@officers_bp.route('/api/officers/<int:officer_id>', methods=['GET'])
def api_get_officer(officer_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Officers WHERE officer_id = %s", (officer_id,))
        officer = cursor.fetchone()
        if not officer:
            return jsonify({"error": "Officer not found"}), 404

        # Cases led by this officer
        cursor.execute("""
            SELECT case_id, case_title, status, date_opened
            FROM Cases WHERE lead_officer_id = %s
            ORDER BY date_opened DESC
        """, (officer_id,))
        officer['cases'] = cursor.fetchall()

        # Interrogations conducted
        cursor.execute("""
            SELECT i.interrogation_id, i.session_date,
                   s.name AS suspect_name, c.case_title
            FROM Interrogations i
            JOIN Suspects s ON i.suspect_id = s.suspect_id
            JOIN Cases    c ON i.case_id    = c.case_id
            WHERE i.officer_id = %s
            ORDER BY i.session_date DESC
            LIMIT 10
        """, (officer_id,))
        officer['interrogations'] = cursor.fetchall()

        return jsonify(officer)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Create officer ───────────────────────────────────────────────────────
@officers_bp.route('/api/officers', methods=['POST'])
def api_create_officer():
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Officers (name, badge_number, officer_rank, department, phone, join_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data.get('name'),
            data.get('badge_number'),
            data.get('rank'),
            data.get('department'),
            data.get('contact_email'),   # maps to phone
            data.get('date_joined')      # maps to join_date
        ))
        conn.commit()
        return jsonify({"message": "Officer created", "officer_id": cursor.lastrowid}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Update officer ───────────────────────────────────────────────────────
@officers_bp.route('/api/officers/<int:officer_id>', methods=['PUT'])
def api_update_officer(officer_id):
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Officers
            SET name=%s, badge_number=%s, officer_rank=%s, department=%s, phone=%s
            WHERE officer_id=%s
        """, (
            data.get('name'),
            data.get('badge_number'),
            data.get('rank'),
            data.get('department'),
            data.get('contact_email'),
            officer_id
        ))
        conn.commit()
        return jsonify({"message": "Officer updated"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Delete officer ───────────────────────────────────────────────────────
@officers_bp.route('/api/officers/<int:officer_id>', methods=['DELETE'])
def api_delete_officer(officer_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Officers WHERE officer_id = %s", (officer_id,))
        conn.commit()
        return jsonify({"message": "Officer deleted"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Officer performance (View) ──────────────────────────────────────────
@officers_bp.route('/api/officers/performance', methods=['GET'])
def api_officer_performance():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM View_Officer_Performance ORDER BY solved_cases DESC")
        results = cursor.fetchall()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

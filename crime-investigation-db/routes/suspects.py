from flask import Blueprint, render_template, jsonify, request
from db.connection import get_db_connection

suspects_bp = Blueprint('suspects', __name__)

# ── Page ──────────────────────────────────────────────────────────────────────
@suspects_bp.route('/suspects', methods=['GET'])
def list_suspects():
    return render_template('suspects.html')

# ── API: List all suspects (with case count) ──────────────────────────────────
@suspects_bp.route('/api/suspects', methods=['GET'])
def api_get_suspects():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.*,
                   COUNT(DISTINCT cs.case_id) AS case_count
            FROM Suspects s
            LEFT JOIN Case_Suspects cs ON s.suspect_id = cs.suspect_id
            GROUP BY s.suspect_id
            ORDER BY s.suspect_id DESC
        """)
        results = cursor.fetchall()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Get single suspect ───────────────────────────────────────────────────
@suspects_bp.route('/api/suspects/<int:suspect_id>', methods=['GET'])
def api_get_suspect(suspect_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Suspects WHERE suspect_id = %s", (suspect_id,))
        suspect = cursor.fetchone()
        if not suspect:
            return jsonify({"error": "Suspect not found"}), 404

        # Cases linked
        cursor.execute("""
            SELECT c.case_id, c.case_title, c.status, cs.role
            FROM Cases c
            JOIN Case_Suspects cs ON c.case_id = cs.case_id
            WHERE cs.suspect_id = %s
        """, (suspect_id,))
        suspect['cases'] = cursor.fetchall()

        # Evidence implicating this suspect
        cursor.execute("""
            SELECT e.evidence_id, e.description, e.type, e.date_collected
            FROM Evidence e
            JOIN Evidence_Suspects es ON e.evidence_id = es.evidence_id
            WHERE es.suspect_id = %s
        """, (suspect_id,))
        suspect['evidence'] = cursor.fetchall()

        # DNA matches
        cursor.execute("""
            SELECT d.dna_id, d.sample_type, d.profile_code, d.lab_result
            FROM DNA_Samples d
            WHERE d.match_suspect_id = %s
        """, (suspect_id,))
        suspect['dna_matches'] = cursor.fetchall()

        # Fingerprint matches
        cursor.execute("""
            SELECT f.fingerprint_id, f.pattern_type, f.match_reference
            FROM Fingerprints f
            WHERE f.matched_suspect_id = %s
        """, (suspect_id,))
        suspect['fingerprint_matches'] = cursor.fetchall()

        return jsonify(suspect)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Create suspect ───────────────────────────────────────────────────────
@suspects_bp.route('/api/suspects', methods=['POST'])
def api_create_suspect():
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Suspects (name, dob, gender, nationality, address, criminal_record)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data.get('name'),
            data.get('dob'),
            data.get('gender'),
            data.get('nationality'),
            data.get('address'),
            data.get('criminal_record', 0)
        ))
        conn.commit()
        return jsonify({"message": "Suspect created", "suspect_id": cursor.lastrowid}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Update suspect ───────────────────────────────────────────────────────
@suspects_bp.route('/api/suspects/<int:suspect_id>', methods=['PUT'])
def api_update_suspect(suspect_id):
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Suspects
            SET name=%s, dob=%s, gender=%s, nationality=%s, address=%s, criminal_record=%s
            WHERE suspect_id=%s
        """, (
            data.get('name'),
            data.get('dob'),
            data.get('gender'),
            data.get('nationality'),
            data.get('address'),
            data.get('criminal_record', 0),
            suspect_id
        ))
        conn.commit()
        return jsonify({"message": "Suspect updated"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Delete suspect ───────────────────────────────────────────────────────
@suspects_bp.route('/api/suspects/<int:suspect_id>', methods=['DELETE'])
def api_delete_suspect(suspect_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Suspects WHERE suspect_id = %s", (suspect_id,))
        conn.commit()
        return jsonify({"message": "Suspect deleted"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── Analytical Query 1: Repeat offenders ─────────────────────────────────────
@suspects_bp.route('/api/suspects/repeat-offenders', methods=['GET'])
def api_repeat_offenders():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.suspect_id, s.name, s.gender, s.criminal_record,
                   COUNT(cs.case_id) AS case_count
            FROM Suspects s
            JOIN Case_Suspects cs ON s.suspect_id = cs.suspect_id
            GROUP BY s.suspect_id, s.name, s.gender, s.criminal_record
            HAVING COUNT(cs.case_id) > 1
            ORDER BY case_count DESC;
        """)
        results = cursor.fetchall()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()


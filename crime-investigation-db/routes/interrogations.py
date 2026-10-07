from flask import Blueprint, render_template, jsonify, request
from db.connection import get_db_connection

interrogations_bp = Blueprint('interrogations', __name__)

# ── Page ──────────────────────────────────────────────────────────────────────
@interrogations_bp.route('/interrogations', methods=['GET'])
def list_interrogations():
    return render_template('interrogations.html')

# ── API: List interrogations ──────────────────────────────────────────────────
@interrogations_bp.route('/api/interrogations', methods=['GET'])
def api_get_interrogations():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        case_id = request.args.get('case_id')
        suspect_id = request.args.get('suspect_id')
        officer_id = request.args.get('officer_id')

        sql = """
            SELECT i.*,
                   s.name  AS suspect_name,
                   o.name  AS officer_name,
                   o.badge_number,
                   c.case_title
            FROM Interrogations i
            JOIN Suspects s ON i.suspect_id = s.suspect_id
            JOIN Officers o ON i.officer_id = o.officer_id
            JOIN Cases    c ON i.case_id    = c.case_id
        """
        filters, params = [], []
        if case_id:
            filters.append("i.case_id = %s"); params.append(case_id)
        if suspect_id:
            filters.append("i.suspect_id = %s"); params.append(suspect_id)
        if officer_id:
            filters.append("i.officer_id = %s"); params.append(officer_id)
        if filters:
            sql += " WHERE " + " AND ".join(filters)
        sql += " ORDER BY i.session_date DESC"

        cursor.execute(sql, params)
        results = cursor.fetchall()
        
        # map back to UI expected fields
        for r in results:
            r['date_time'] = r['session_date']
            r['notes'] = r['transcript_summary']
            # We don't have location and outcome in the DB schema
            r['location'] = 'Interrogation Room'
            r['outcome'] = 'Pending'

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Get single interrogation ─────────────────────────────────────────────
@interrogations_bp.route('/api/interrogations/<int:interrogation_id>', methods=['GET'])
def api_get_interrogation(interrogation_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT i.*,
                   s.name AS suspect_name,
                   o.name AS officer_name, o.badge_number,
                   c.case_title
            FROM Interrogations i
            JOIN Suspects s ON i.suspect_id = s.suspect_id
            JOIN Officers o ON i.officer_id = o.officer_id
            JOIN Cases    c ON i.case_id    = c.case_id
            WHERE i.interrogation_id = %s
        """, (interrogation_id,))
        result = cursor.fetchone()
        if not result:
            return jsonify({"error": "Interrogation not found"}), 404
            
        result['date_time'] = result['session_date']
        result['notes'] = result['transcript_summary']
        result['location'] = 'Interrogation Room'
        result['outcome'] = 'Pending'
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Create interrogation ─────────────────────────────────────────────────
@interrogations_bp.route('/api/interrogations', methods=['POST'])
def api_create_interrogation():
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        
        # Mapping UI fields to DB schema
        session_date = data.get('date_time')
        transcript = data.get('notes')
        
        cursor.execute("""
            INSERT INTO Interrogations
                (case_id, suspect_id, officer_id, session_date, transcript_summary)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            data.get('case_id'),
            data.get('suspect_id'),
            data.get('officer_id'),
            session_date,
            transcript
        ))
        conn.commit()
        return jsonify({"message": "Interrogation logged", "interrogation_id": cursor.lastrowid}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Update interrogation ─────────────────────────────────────────────────
@interrogations_bp.route('/api/interrogations/<int:interrogation_id>', methods=['PUT'])
def api_update_interrogation(interrogation_id):
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Interrogations
            SET session_date=%s, transcript_summary=%s
            WHERE interrogation_id=%s
        """, (
            data.get('date_time'),
            data.get('notes'),
            interrogation_id
        ))
        conn.commit()
        return jsonify({"message": "Interrogation updated"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Delete interrogation ─────────────────────────────────────────────────
@interrogations_bp.route('/api/interrogations/<int:interrogation_id>', methods=['DELETE'])
def api_delete_interrogation(interrogation_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Interrogations WHERE interrogation_id = %s", (interrogation_id,))
        conn.commit()
        return jsonify({"message": "Interrogation deleted"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

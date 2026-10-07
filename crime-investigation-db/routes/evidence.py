from flask import Blueprint, render_template, jsonify, request
from db.connection import get_db_connection

evidence_bp = Blueprint('evidence', __name__)

# ── Page ──────────────────────────────────────────────────────────────────────
@evidence_bp.route('/evidence', methods=['GET'])
def list_evidence():
    return render_template('evidence.html')

@evidence_bp.route('/api/evidence', methods=['GET'])
def api_get_evidence():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM Evidence")
        results = cursor.fetchall()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@evidence_bp.route('/api/evidence', methods=['POST'])
def api_log_evidence():
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO Evidence (case_id, scene_id, description, type, date_collected, storage_location)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            data.get('case_id'),
            data.get('scene_id'),
            data.get('description'),
            data.get('type', 'Physical'),
            data.get('date_collected'),
            data.get('storage_location')
        )
        cursor.execute(query, values)
        conn.commit()
        return jsonify({"message": "Evidence logged successfully", "evidence_id": cursor.lastrowid}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@evidence_bp.route('/api/evidence/<int:evidence_id>', methods=['PUT'])
def api_update_evidence(evidence_id):
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Evidence
            SET case_id=%s, scene_id=%s, description=%s, type=%s,
                date_collected=%s, storage_location=%s
            WHERE evidence_id=%s
        """, (
            data.get('case_id'),
            data.get('scene_id'),
            data.get('description'),
            data.get('type', 'Physical'),
            data.get('date_collected'),
            data.get('storage_location'),
            evidence_id
        ))
        conn.commit()
        return jsonify({"message": "Evidence updated successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@evidence_bp.route('/api/evidence/<int:evidence_id>', methods=['DELETE'])
def api_delete_evidence(evidence_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Evidence WHERE evidence_id = %s", (evidence_id,))
        conn.commit()
        return jsonify({"message": "Evidence deleted successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@evidence_bp.route('/api/evidence/<int:evidence_id>/suspects', methods=['POST'])
def api_link_evidence_suspect(evidence_id):
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor()
        query = "INSERT INTO Evidence_Suspects (evidence_id, suspect_id) VALUES (%s, %s)"
        cursor.execute(query, (evidence_id, data.get('suspect_id')))
        conn.commit()
        return jsonify({"message": "Evidence linked to suspect successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@evidence_bp.route('/api/fingerprints/cross-scene', methods=['GET'])
def api_cross_scene_fingerprints():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor(dictionary=True)
        # Query 2: Fingerprints found at more than one crime scene
        query = """
            SELECT f.match_reference, COUNT(DISTINCT f.scene_id) AS scene_count
            FROM Fingerprints f
            WHERE f.match_reference IS NOT NULL
            GROUP BY f.match_reference
            HAVING COUNT(DISTINCT f.scene_id) > 1;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

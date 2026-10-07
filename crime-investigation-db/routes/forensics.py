from flask import Blueprint, render_template, jsonify, request
from db.connection import get_db_connection

forensics_bp = Blueprint('forensics', __name__)

# ── Page ──────────────────────────────────────────────────────────────────────
@forensics_bp.route('/forensics', methods=['GET'])
def forensics_page():
    return render_template('forensics.html')

# ═══════════════════════════════════════════════════════════════════════════════
#  DNA SAMPLES
# ═══════════════════════════════════════════════════════════════════════════════

@forensics_bp.route('/api/dna-samples', methods=['GET'])
def api_get_dna_samples():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        evidence_id = request.args.get('evidence_id')
        if evidence_id:
            cursor.execute("""
                SELECT d.*, e.description AS evidence_desc
                FROM DNA_Samples d
                JOIN Evidence e ON d.evidence_id = e.evidence_id
                WHERE d.evidence_id = %s
            """, (evidence_id,))
        else:
            cursor.execute("""
                SELECT d.*,
                       e.description AS evidence_desc,
                       e.case_id,
                       c.case_title
                FROM DNA_Samples d
                JOIN Evidence e ON d.evidence_id = e.evidence_id
                JOIN Cases    c ON e.case_id = c.case_id
                ORDER BY d.dna_id DESC
            """)
        results = cursor.fetchall()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@forensics_bp.route('/api/dna-samples', methods=['POST'])
def api_create_dna_sample():
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO DNA_Samples
                (evidence_id, sample_type, profile_code, collected_by, lab_result, match_suspect_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data.get('evidence_id'),
            data.get('sample_type'),
            data.get('profile_code'),
            data.get('collected_by'),
            data.get('lab_result'),
            data.get('match_suspect_id')
        ))
        conn.commit()
        return jsonify({"message": "DNA sample logged", "dna_id": cursor.lastrowid}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@forensics_bp.route('/api/dna-samples/<int:dna_id>', methods=['PUT'])
def api_update_dna_sample(dna_id):
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE DNA_Samples
            SET sample_type=%s, profile_code=%s, collected_by=%s,
                lab_result=%s, match_suspect_id=%s
            WHERE dna_id=%s
        """, (
            data.get('sample_type'),
            data.get('profile_code'),
            data.get('collected_by'),
            data.get('lab_result'),
            data.get('match_suspect_id'),
            dna_id
        ))
        conn.commit()
        return jsonify({"message": "DNA sample updated"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@forensics_bp.route('/api/dna-samples/<int:dna_id>', methods=['DELETE'])
def api_delete_dna_sample(dna_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM DNA_Samples WHERE dna_id = %s", (dna_id,))
        conn.commit()
        return jsonify({"message": "DNA sample deleted"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ═══════════════════════════════════════════════════════════════════════════════
#  FINGERPRINTS
# ═══════════════════════════════════════════════════════════════════════════════
# Schema: fingerprint_id, evidence_id, scene_id, suspect_id, print_type, match_status, match_reference

@forensics_bp.route('/api/fingerprints', methods=['GET'])
def api_get_fingerprints():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        scene_id = request.args.get('scene_id')
        evidence_id = request.args.get('evidence_id')
        if scene_id:
            cursor.execute("""
                SELECT f.*, cs.location AS scene_location
                FROM Fingerprints f
                LEFT JOIN Crime_Scenes cs ON f.scene_id = cs.scene_id
                WHERE f.scene_id = %s
                ORDER BY f.fingerprint_id DESC
            """, (scene_id,))
        elif evidence_id:
            cursor.execute("""
                SELECT f.*
                FROM Fingerprints f
                WHERE f.evidence_id = %s
                ORDER BY f.fingerprint_id DESC
            """, (evidence_id,))
        else:
            cursor.execute("""
                SELECT f.*,
                       cs.location AS scene_location,
                       e.description AS evidence_desc
                FROM Fingerprints f
                LEFT JOIN Crime_Scenes cs ON f.scene_id  = cs.scene_id
                LEFT JOIN Evidence     e  ON f.evidence_id = e.evidence_id
                ORDER BY f.fingerprint_id DESC
            """)
        results = cursor.fetchall()
        for r in results:
            # Map back to UI
            r['pattern_type'] = r.get('print_type')
            r['matched_suspect_id'] = r.get('suspect_id')
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@forensics_bp.route('/api/fingerprints', methods=['POST'])
def api_create_fingerprint():
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        suspect_id = data.get('matched_suspect_id')
        match_status = "Matched" if suspect_id else "Unmatched"
        
        cursor.execute("""
            INSERT INTO Fingerprints
                (evidence_id, scene_id, suspect_id, print_type, match_status, match_reference)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data.get('evidence_id'),
            data.get('scene_id'),
            suspect_id,
            data.get('pattern_type'),
            match_status,
            data.get('match_reference')
        ))
        conn.commit()
        return jsonify({"message": "Fingerprint logged", "fingerprint_id": cursor.lastrowid}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@forensics_bp.route('/api/fingerprints/<int:fingerprint_id>', methods=['PUT'])
def api_update_fingerprint(fingerprint_id):
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        suspect_id = data.get('matched_suspect_id')
        match_status = "Matched" if suspect_id else "Unmatched"
        
        cursor.execute("""
            UPDATE Fingerprints
            SET print_type=%s, match_reference=%s,
                suspect_id=%s, match_status=%s
            WHERE fingerprint_id=%s
        """, (
            data.get('pattern_type'),
            data.get('match_reference'),
            suspect_id,
            match_status,
            fingerprint_id
        ))
        conn.commit()
        return jsonify({"message": "Fingerprint updated"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@forensics_bp.route('/api/fingerprints/<int:fingerprint_id>', methods=['DELETE'])
def api_delete_fingerprint(fingerprint_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Fingerprints WHERE fingerprint_id = %s", (fingerprint_id,))
        conn.commit()
        return jsonify({"message": "Fingerprint deleted"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── Analytical Query 2: Cross-scene fingerprint matches ───────────────────────
@forensics_bp.route('/api/fingerprints/cross-scene', methods=['GET'])
def api_cross_scene_fingerprints():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT f.match_reference,
                   COUNT(DISTINCT f.scene_id) AS scene_count,
                   GROUP_CONCAT(DISTINCT cs.location SEPARATOR ' | ') AS scenes
            FROM Fingerprints f
            JOIN Crime_Scenes cs ON f.scene_id = cs.scene_id
            WHERE f.match_reference IS NOT NULL
            GROUP BY f.match_reference
            HAVING COUNT(DISTINCT f.scene_id) > 1
        """)
        results = cursor.fetchall()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

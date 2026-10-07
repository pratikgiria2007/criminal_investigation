from flask import Blueprint, render_template, jsonify, request
from db.connection import get_db_connection

crime_scenes_bp = Blueprint('crime_scenes', __name__)

# Actual DB columns: scene_id, case_id, location, date_occurred, description

# ── Page ──────────────────────────────────────────────────────────────────────
@crime_scenes_bp.route('/crime-scenes', methods=['GET'])
def list_crime_scenes():
    return render_template('crime_scenes.html')

# ── API: List all crime scenes ────────────────────────────────────────────────
@crime_scenes_bp.route('/api/crime-scenes', methods=['GET'])
def api_get_crime_scenes():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        case_id = request.args.get('case_id')
        if case_id:
            cursor.execute("""
                SELECT cs.*, c.case_title
                FROM Crime_Scenes cs
                JOIN Cases c ON cs.case_id = c.case_id
                WHERE cs.case_id = %s
                ORDER BY cs.date_occurred DESC
            """, (case_id,))
        else:
            cursor.execute("""
                SELECT cs.*, c.case_title,
                       COUNT(e.evidence_id) AS evidence_count
                FROM Crime_Scenes cs
                JOIN Cases c ON cs.case_id = c.case_id
                LEFT JOIN Evidence e ON cs.scene_id = e.scene_id
                GROUP BY cs.scene_id
                ORDER BY cs.date_occurred DESC
            """)
        results = cursor.fetchall()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Get single crime scene ───────────────────────────────────────────────
@crime_scenes_bp.route('/api/crime-scenes/<int:scene_id>', methods=['GET'])
def api_get_crime_scene(scene_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT cs.*, c.case_title
            FROM Crime_Scenes cs
            JOIN Cases c ON cs.case_id = c.case_id
            WHERE cs.scene_id = %s
        """, (scene_id,))
        scene = cursor.fetchone()
        if not scene:
            return jsonify({"error": "Crime scene not found"}), 404

        cursor.execute("SELECT * FROM Evidence WHERE scene_id = %s", (scene_id,))
        scene['evidence'] = cursor.fetchall()

        cursor.execute("SELECT * FROM Fingerprints WHERE scene_id = %s", (scene_id,))
        scene['fingerprints'] = cursor.fetchall()

        return jsonify(scene)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Create crime scene ───────────────────────────────────────────────────
@crime_scenes_bp.route('/api/crime-scenes', methods=['POST'])
def api_create_crime_scene():
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Crime_Scenes (case_id, location, date_occurred, description)
            VALUES (%s, %s, %s, %s)
        """, (
            data.get('case_id'),
            data.get('location_description') or data.get('location'),
            data.get('timestamp') or data.get('date_occurred'),
            data.get('description', '')
        ))
        conn.commit()
        return jsonify({"message": "Crime scene created", "scene_id": cursor.lastrowid}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Update crime scene ───────────────────────────────────────────────────
@crime_scenes_bp.route('/api/crime-scenes/<int:scene_id>', methods=['PUT'])
def api_update_crime_scene(scene_id):
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Crime_Scenes
            SET location=%s, date_occurred=%s, description=%s
            WHERE scene_id=%s
        """, (
            data.get('location_description') or data.get('location'),
            data.get('timestamp') or data.get('date_occurred'),
            data.get('description', ''),
            scene_id
        ))
        conn.commit()
        return jsonify({"message": "Crime scene updated"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

# ── API: Delete crime scene ───────────────────────────────────────────────────
@crime_scenes_bp.route('/api/crime-scenes/<int:scene_id>', methods=['DELETE'])
def api_delete_crime_scene(scene_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Crime_Scenes WHERE scene_id = %s", (scene_id,))
        conn.commit()
        return jsonify({"message": "Crime scene deleted"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

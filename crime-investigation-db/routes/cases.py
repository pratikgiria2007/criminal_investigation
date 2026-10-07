from flask import Blueprint, render_template, jsonify, request
from db.connection import get_db_connection

cases_bp = Blueprint('cases', __name__)

@cases_bp.route('/cases', methods=['GET'])
def list_cases():
    return render_template('cases.html')

@cases_bp.route('/cases/<int:case_id>', methods=['GET'])
def case_detail(case_id):
    return render_template('case_detail.html', case_id=case_id)

@cases_bp.route('/api/cases', methods=['GET'])
def api_list_cases():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM View_Case_Summary ORDER BY case_id DESC")
        results = cursor.fetchall()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@cases_bp.route('/api/cases/<int:case_id>', methods=['GET'])
def api_case_detail(case_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor(dictionary=True)
        
        # We can call the stored procedure GetCaseDetails
        # but mysql.connector callproc with multiple result sets can be tricky
        # Let's just do individual queries for safety and clarity
        
        cursor.execute("SELECT * FROM Cases WHERE case_id = %s", (case_id,))
        case = cursor.fetchone()
        
        if not case:
            return jsonify({"error": "Case not found"}), 404
            
        # Get lead officer
        if case['lead_officer_id']:
            cursor.execute("SELECT name, badge_number FROM Officers WHERE officer_id = %s", (case['lead_officer_id'],))
            case['officer'] = cursor.fetchone()
            
        # Get suspects
        cursor.execute("""
            SELECT s.*, cs.role 
            FROM Suspects s 
            JOIN Case_Suspects cs ON s.suspect_id = cs.suspect_id 
            WHERE cs.case_id = %s
        """, (case_id,))
        case['suspects'] = cursor.fetchall()
        
        # Get evidence
        cursor.execute("SELECT * FROM Evidence WHERE case_id = %s", (case_id,))
        case['evidence'] = cursor.fetchall()
        
        # Mask sensitive data for Casual users
        from flask import session
        if session.get('role') == 'Casual':
            case['suspects'] = []
            case['evidence'] = []
            if 'officer' in case:
                case['officer'] = {'name': 'Classified', 'badge_number': '***'}
        
        # Get scenes
        cursor.execute("SELECT * FROM Crime_Scenes WHERE case_id = %s", (case_id,))
        case['scenes'] = cursor.fetchall()
        
        return jsonify(case)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@cases_bp.route('/api/cases', methods=['POST'])
def api_create_case():
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor()
        query = """
            INSERT INTO Cases (case_title, description, status, date_opened, lead_officer_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        values = (
            data.get('case_title'),
            data.get('description'),
            data.get('status', 'Open'),
            data.get('date_opened'),
            data.get('lead_officer_id')
        )
        cursor.execute(query, values)
        conn.commit()
        return jsonify({"message": "Case created successfully", "case_id": cursor.lastrowid}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@cases_bp.route('/api/cases/<int:case_id>', methods=['PUT'])
def api_update_case(case_id):
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor()
        query = """
            UPDATE Cases 
            SET case_title = %s, description = %s, status = %s, lead_officer_id = %s
            WHERE case_id = %s
        """
        values = (
            data.get('case_title'),
            data.get('description'),
            data.get('status'),
            data.get('lead_officer_id'),
            case_id
        )
        cursor.execute(query, values)
        conn.commit()
        return jsonify({"message": "Case updated successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@cases_bp.route('/api/cases/<int:case_id>', methods=['DELETE'])
def api_delete_case(case_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Cases WHERE case_id = %s", (case_id,))
        conn.commit()
        return jsonify({"message": "Case deleted successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@cases_bp.route('/api/cases/<int:case_id>/suspects', methods=['POST'])
def api_link_suspect(case_id):
    data = request.json
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor()
        cursor.callproc('AddSuspectToCase', (case_id, data.get('suspect_id'), data.get('role', 'Person of Interest')))
        conn.commit()
        return jsonify({"message": "Suspect linked to case successfully"})
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@cases_bp.route('/api/cases/no-evidence', methods=['GET'])
def api_cases_no_evidence():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor(dictionary=True)
        # Query 4: Cases with no forensic evidence at all
        query = """
            SELECT c.case_id, c.case_title
            FROM Cases c
            LEFT JOIN Evidence e ON c.case_id = e.case_id
            WHERE e.evidence_id IS NULL;
        """
        cursor.execute(query)
        results = cursor.fetchall()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

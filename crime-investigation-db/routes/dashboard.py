from flask import Blueprint, render_template, jsonify
from db.connection import get_db_connection

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    return render_template('dashboard.html')

@dashboard_bp.route('/api/stats/overview', methods=['GET'])
def overview_stats():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor(dictionary=True)
        stats = {}
        
        # Total cases
        cursor.execute("SELECT COUNT(*) as count FROM Cases")
        stats['total_cases'] = cursor.fetchone()['count']
        
        # Open cases
        cursor.execute("SELECT COUNT(*) as count FROM Cases WHERE status IN ('Open', 'Under Investigation')")
        stats['open_cases'] = cursor.fetchone()['count']
        
        # Solved cases
        cursor.execute("SELECT COUNT(*) as count FROM Cases WHERE status = 'Solved'")
        stats['solved_cases'] = cursor.fetchone()['count']
        
        # Total suspects
        cursor.execute("SELECT COUNT(*) as count FROM Suspects")
        stats['total_suspects'] = cursor.fetchone()['count']
        
        # Total evidence
        cursor.execute("SELECT COUNT(*) as count FROM Evidence")
        stats['total_evidence'] = cursor.fetchone()['count']
        
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@dashboard_bp.route('/api/stats/officer-leaderboard', methods=['GET'])
def officer_leaderboard():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT name, solved_cases, total_cases
            FROM View_Officer_Performance 
            ORDER BY solved_cases DESC 
            LIMIT 5
        """)
        results = cursor.fetchall()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@dashboard_bp.route('/api/stats/case-status', methods=['GET'])
def case_status():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
        
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT status, COUNT(*) as count 
            FROM Cases 
            GROUP BY status
        """)
        results = cursor.fetchall()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

@dashboard_bp.route('/api/stats/recent-cases', methods=['GET'])
def recent_cases():
    """Returns the 8 most recently opened cases for the activity feed."""
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT c.case_id, c.case_title, c.status, c.date_opened,
                   o.name AS lead_officer
            FROM Cases c
            LEFT JOIN Officers o ON c.lead_officer_id = o.officer_id
            ORDER BY c.date_opened DESC
            LIMIT 8
        """)
        results = cursor.fetchall()
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

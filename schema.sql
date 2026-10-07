-- ============================================================
-- CRIMINAL INVESTIGATION EVIDENCE DATABASE
-- MySQL Schema : Tables, Constraints, Views, Triggers, Procedures
-- ============================================================

CREATE DATABASE IF NOT EXISTS crime_db;
USE crime_db;

-- ------------------------------------------------------------
-- 1. OFFICERS
-- ------------------------------------------------------------
CREATE TABLE Officers (
    officer_id      INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    badge_number    VARCHAR(20) UNIQUE NOT NULL,
    officer_rank    VARCHAR(50),
    department      VARCHAR(100),
    join_date       DATE,
    phone           VARCHAR(15)
);

-- ------------------------------------------------------------
-- 2. CASES
-- ------------------------------------------------------------
CREATE TABLE Cases (
    case_id         INT AUTO_INCREMENT PRIMARY KEY,
    case_title      VARCHAR(150) NOT NULL,
    description     TEXT,
    status          ENUM('Open','Under Investigation','Solved','Closed','Cold Case') DEFAULT 'Open',
    date_opened     DATE NOT NULL,
    date_closed     DATE,
    lead_officer_id INT,
    FOREIGN KEY (lead_officer_id) REFERENCES Officers(officer_id)
        ON DELETE SET NULL
);

-- ------------------------------------------------------------
-- 3. SUSPECTS
-- ------------------------------------------------------------
CREATE TABLE Suspects (
    suspect_id      INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    dob             DATE,
    gender          ENUM('Male','Female','Other'),
    address         VARCHAR(200),
    phone           VARCHAR(15),
    criminal_record TEXT
);

-- ------------------------------------------------------------
-- 4. VICTIMS
-- ------------------------------------------------------------
CREATE TABLE Victims (
    victim_id       INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    dob             DATE,
    gender          ENUM('Male','Female','Other'),
    address         VARCHAR(200),
    contact_info    VARCHAR(100),
    case_id         INT,
    FOREIGN KEY (case_id) REFERENCES Cases(case_id)
        ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- 5. CRIME SCENES
-- ------------------------------------------------------------
CREATE TABLE Crime_Scenes (
    scene_id        INT AUTO_INCREMENT PRIMARY KEY,
    case_id         INT NOT NULL,
    location        VARCHAR(200) NOT NULL,
    date_occurred   DATETIME,
    description     TEXT,
    FOREIGN KEY (case_id) REFERENCES Cases(case_id)
        ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- 6. EVIDENCE
-- ------------------------------------------------------------
CREATE TABLE Evidence (
    evidence_id     INT AUTO_INCREMENT PRIMARY KEY,
    case_id         INT NOT NULL,
    scene_id        INT,
    description     VARCHAR(255) NOT NULL,
    type            ENUM('Physical','Digital','Document','Biological','Weapon','Other') DEFAULT 'Physical',
    date_collected  DATE,
    storage_location VARCHAR(100),
    FOREIGN KEY (case_id) REFERENCES Cases(case_id)
        ON DELETE CASCADE,
    FOREIGN KEY (scene_id) REFERENCES Crime_Scenes(scene_id)
        ON DELETE SET NULL
);

-- ------------------------------------------------------------
-- 7. WITNESSES
-- ------------------------------------------------------------
CREATE TABLE Witnesses (
    witness_id      INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    contact_info    VARCHAR(100),
    address         VARCHAR(200)
);

-- ------------------------------------------------------------
-- 8. INTERROGATIONS
-- ------------------------------------------------------------
CREATE TABLE Interrogations (
    interrogation_id INT AUTO_INCREMENT PRIMARY KEY,
    suspect_id      INT NOT NULL,
    officer_id      INT NOT NULL,
    case_id         INT NOT NULL,
    session_date    DATETIME,
    transcript_summary TEXT,
    FOREIGN KEY (suspect_id) REFERENCES Suspects(suspect_id) ON DELETE CASCADE,
    FOREIGN KEY (officer_id) REFERENCES Officers(officer_id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES Cases(case_id) ON DELETE CASCADE
);

-- ------------------------------------------------------------
-- 9. DNA SAMPLES
-- ------------------------------------------------------------
CREATE TABLE DNA_Samples (
    dna_id          INT AUTO_INCREMENT PRIMARY KEY,
    evidence_id     INT NOT NULL,
    suspect_id      INT,
    victim_id       INT,
    sample_type     VARCHAR(50),
    collection_date DATE,
    lab_result      ENUM('Pending','Match','No Match','Inconclusive') DEFAULT 'Pending',
    FOREIGN KEY (evidence_id) REFERENCES Evidence(evidence_id) ON DELETE CASCADE,
    FOREIGN KEY (suspect_id) REFERENCES Suspects(suspect_id) ON DELETE SET NULL,
    FOREIGN KEY (victim_id) REFERENCES Victims(victim_id) ON DELETE SET NULL
);

-- ------------------------------------------------------------
-- 10. FINGERPRINTS
-- ------------------------------------------------------------
CREATE TABLE Fingerprints (
    fingerprint_id  INT AUTO_INCREMENT PRIMARY KEY,
    evidence_id     INT NOT NULL,
    scene_id        INT,
    suspect_id      INT,
    print_type      VARCHAR(50),
    match_status    ENUM('Pending','Matched','Unmatched') DEFAULT 'Pending',
    match_reference VARCHAR(50), -- shared code across duplicate prints from same source
    FOREIGN KEY (evidence_id) REFERENCES Evidence(evidence_id) ON DELETE CASCADE,
    FOREIGN KEY (scene_id) REFERENCES Crime_Scenes(scene_id) ON DELETE SET NULL,
    FOREIGN KEY (suspect_id) REFERENCES Suspects(suspect_id) ON DELETE SET NULL
);

-- ============================================================
-- MANY-TO-MANY JUNCTION TABLES
-- ============================================================

-- A suspect can belong to multiple cases, a case can have multiple suspects
CREATE TABLE Case_Suspects (
    case_id     INT NOT NULL,
    suspect_id  INT NOT NULL,
    role        ENUM('Primary','Accomplice','Person of Interest') DEFAULT 'Person of Interest',
    PRIMARY KEY (case_id, suspect_id),
    FOREIGN KEY (case_id) REFERENCES Cases(case_id) ON DELETE CASCADE,
    FOREIGN KEY (suspect_id) REFERENCES Suspects(suspect_id) ON DELETE CASCADE
);

-- An evidence item can implicate multiple suspects, a suspect can be tied to multiple evidence items
CREATE TABLE Evidence_Suspects (
    evidence_id INT NOT NULL,
    suspect_id  INT NOT NULL,
    PRIMARY KEY (evidence_id, suspect_id),
    FOREIGN KEY (evidence_id) REFERENCES Evidence(evidence_id) ON DELETE CASCADE,
    FOREIGN KEY (suspect_id) REFERENCES Suspects(suspect_id) ON DELETE CASCADE
);

-- A witness may testify in several cases, a case can have multiple witnesses
CREATE TABLE Case_Witnesses (
    case_id     INT NOT NULL,
    witness_id  INT NOT NULL,
    statement   TEXT,
    PRIMARY KEY (case_id, witness_id),
    FOREIGN KEY (case_id) REFERENCES Cases(case_id) ON DELETE CASCADE,
    FOREIGN KEY (witness_id) REFERENCES Witnesses(witness_id) ON DELETE CASCADE
);

-- ============================================================
-- AUDIT LOG (supports the trigger below)
-- ============================================================
CREATE TABLE Interrogation_Audit (
    audit_id        INT AUTO_INCREMENT PRIMARY KEY,
    interrogation_id INT,
    action          VARCHAR(20),
    action_time     DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- SAMPLE QUERIES (the four asked for in the brief)
-- ============================================================

-- Q1: Suspects who appear in more than one investigation
SELECT s.suspect_id, s.name, COUNT(cs.case_id) AS case_count
FROM Suspects s
JOIN Case_Suspects cs ON s.suspect_id = cs.suspect_id
GROUP BY s.suspect_id, s.name
HAVING COUNT(cs.case_id) > 1;

-- Q2: Fingerprints (by match_reference) found at more than one crime scene
SELECT f.match_reference, COUNT(DISTINCT f.scene_id) AS scene_count
FROM Fingerprints f
WHERE f.match_reference IS NOT NULL
GROUP BY f.match_reference
HAVING COUNT(DISTINCT f.scene_id) > 1;

-- Q3: Officer who has solved/closed the highest number of cases
SELECT o.officer_id, o.name, COUNT(c.case_id) AS cases_solved
FROM Officers o
JOIN Cases c ON o.officer_id = c.lead_officer_id
WHERE c.status IN ('Solved','Closed')
GROUP BY o.officer_id, o.name
ORDER BY cases_solved DESC
LIMIT 1;

-- Q4: Cases with no forensic evidence at all
SELECT c.case_id, c.case_title
FROM Cases c
LEFT JOIN Evidence e ON c.case_id = e.case_id
WHERE e.evidence_id IS NULL;

-- ============================================================
-- VIEWS
-- ============================================================

-- View: Full case summary (title, officer, suspect count, evidence count)
CREATE VIEW View_Case_Summary AS
SELECT
    c.case_id,
    c.case_title,
    c.status,
    o.name AS lead_officer,
    (SELECT COUNT(*) FROM Case_Suspects cs WHERE cs.case_id = c.case_id) AS suspect_count,
    (SELECT COUNT(*) FROM Evidence e WHERE e.case_id = c.case_id) AS evidence_count
FROM Cases c
LEFT JOIN Officers o ON c.lead_officer_id = o.officer_id;

-- View: Officer performance (case load and solve rate)
CREATE VIEW View_Officer_Performance AS
SELECT
    o.officer_id,
    o.name,
    COUNT(c.case_id) AS total_cases,
    SUM(CASE WHEN c.status IN ('Solved','Closed') THEN 1 ELSE 0 END) AS solved_cases
FROM Officers o
LEFT JOIN Cases c ON o.officer_id = c.lead_officer_id
GROUP BY o.officer_id, o.name;

-- View: Suspects with case and role info (flattened for dashboard tables)
CREATE VIEW View_Suspect_Cases AS
SELECT
    s.suspect_id,
    s.name AS suspect_name,
    c.case_id,
    c.case_title,
    cs.role
FROM Case_Suspects cs
JOIN Suspects s ON cs.suspect_id = s.suspect_id
JOIN Cases c ON cs.case_id = c.case_id;

-- ============================================================
-- TRIGGERS
-- ============================================================

DELIMITER //

-- Trigger 1: Log every new interrogation into the audit table
CREATE TRIGGER trg_after_interrogation_insert
AFTER INSERT ON Interrogations
FOR EACH ROW
BEGIN
    INSERT INTO Interrogation_Audit (interrogation_id, action)
    VALUES (NEW.interrogation_id, 'CREATED');
END//

-- Trigger 2: Auto-close a case when its status is manually set to 'Solved'
-- (sets date_closed automatically so no one forgets to fill it in)
CREATE TRIGGER trg_before_case_update
BEFORE UPDATE ON Cases
FOR EACH ROW
BEGIN
    IF NEW.status = 'Solved' AND OLD.status <> 'Solved' THEN
        SET NEW.date_closed = CURDATE();
    END IF;
END//

-- Trigger 3: Prevent deletion of a suspect who still has a 'Matched' fingerprint on file
CREATE TRIGGER trg_before_suspect_delete
BEFORE DELETE ON Suspects
FOR EACH ROW
BEGIN
    DECLARE match_count INT;
    SELECT COUNT(*) INTO match_count
    FROM Fingerprints
    WHERE suspect_id = OLD.suspect_id AND match_status = 'Matched';

    IF match_count > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Cannot delete suspect: matched fingerprint evidence exists.';
    END IF;
END//

DELIMITER ;

-- ============================================================
-- STORED PROCEDURES
-- ============================================================

DELIMITER //

-- Procedure 1: Get full details of a case (info + suspects + evidence count)
CREATE PROCEDURE GetCaseDetails(IN p_case_id INT)
BEGIN
    SELECT * FROM Cases WHERE case_id = p_case_id;
    SELECT s.* FROM Suspects s
        JOIN Case_Suspects cs ON s.suspect_id = cs.suspect_id
        WHERE cs.case_id = p_case_id;
    SELECT * FROM Evidence WHERE case_id = p_case_id;
END//

-- Procedure 2: Link a suspect to a case (used by the "Add Suspect to Case" form)
CREATE PROCEDURE AddSuspectToCase(IN p_case_id INT, IN p_suspect_id INT, IN p_role VARCHAR(30))
BEGIN
    INSERT INTO Case_Suspects (case_id, suspect_id, role)
    VALUES (p_case_id, p_suspect_id, p_role)
    ON DUPLICATE KEY UPDATE role = p_role;
END//

-- Procedure 3: Count how many cases an officer has solved (used by dashboard leaderboard)
CREATE PROCEDURE CountCasesSolvedByOfficer(IN p_officer_id INT, OUT p_count INT)
BEGIN
    SELECT COUNT(*) INTO p_count
    FROM Cases
    WHERE lead_officer_id = p_officer_id AND status IN ('Solved','Closed');
END//

DELIMITER ;

-- ============================================================
-- USERS (For Authentication and Roles)
-- ============================================================
CREATE TABLE IF NOT EXISTS Users (
    user_id         INT AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(50) UNIQUE NOT NULL,
    password_hash   VARCHAR(255) NOT NULL,
    role            ENUM('Official', 'Casual') DEFAULT 'Casual',
    officer_id      INT NULL,
    FOREIGN KEY (officer_id) REFERENCES Officers(officer_id) ON DELETE SET NULL
);



USE crime_db;


INSERT IGNORE INTO Officers (name, badge_number, officer_rank, department, join_date, phone) VALUES
('James Harrington', 'B-1001', 'Inspector', 'Homicide', '2015-03-15', '9812345601'),
('Priya Mehra',      'B-1002', 'Sub-Inspector', 'Cyber Crime', '2018-07-22', '9812345602'),
('David Okonkwo',    'B-1003', 'Detective', 'Narcotics', '2016-11-05', '9812345603'),
('Sofia Reyes',      'B-1004', 'Inspector', 'Homicide', '2017-01-30', '9812345604'),
('Marcus Webb',      'B-1005', 'Constable', 'General', '2020-06-18', '9812345605'),
('Ananya Sharma',    'B-1006', 'Detective', 'Financial Crimes', '2019-09-09', '9812345606'),
('Liam Chen',        'B-1007', 'Inspector', 'Organized Crime', '2014-04-12', '9812345607'),
('Fatima Al-Sayed',  'B-1008', 'Sub-Inspector', 'Homicide', '2021-03-01', '9812345608'),
('Raj Patel',        'B-1009', 'Detective', 'Narcotics', '2018-08-25', '9812345609'),
('Elena Vasquez',    'B-1010', 'Inspector', 'Cyber Crime', '2016-05-17', '9812345610');


INSERT IGNORE INTO Cases (case_title, description, status, date_opened, date_closed, lead_officer_id) VALUES
('Operation Blackout',          'Series of armed robberies at night targeting jewelry stores.', 'Under Investigation', '2024-01-10', NULL, 1),
('The Harbor Murders',          'Three bodies found near the docks. Suspected organized crime.', 'Open', '2024-02-14', NULL, 4),
('Digital Ghost',               'Large-scale financial fraud via phishing networks.', 'Solved', '2023-06-01', '2024-01-20', 2),
('Phantom Smuggler',            'Narcotics trafficking through the city port.', 'Under Investigation', '2024-03-22', NULL, 3),
('Silhouette Killer',           'Serial killer targeting professionals; 4 victims identified.', 'Open', '2024-05-05', NULL, 1),
('Operation Cobweb',            'Dismantling a city-wide drug distribution network.', 'Solved', '2022-11-10', '2023-08-15', 9),
('The Missing Heiress',         'Disappearance of a wealthy industrialist''s daughter.', 'Cold Case', '2021-04-01', NULL, 4),
('Counterfeit Currency Ring',   'Fake bills flooding local markets.', 'Closed', '2023-02-18', '2023-12-01', 6),
('Blue Horizon Heist',          'Audacious bank robbery with sophisticated planning.', 'Under Investigation', '2024-04-10', NULL, 7),
('Market Massacre',             'Bombing at a local market. 2 dead, 9 injured.', 'Open', '2024-06-18', NULL, 1),
('Operation Nightfall',         'Money laundering through shell companies.', 'Solved', '2023-01-05', '2023-11-30', 6),
('The Arsonist',                'Suspicious fires in the industrial district.', 'Under Investigation', '2024-07-01', NULL, 5),
('Rooftop Sniper',              'Sniper attacks on government buildings.', 'Open', '2024-07-20', NULL, 7),
('Tax Evasion Syndicate',       'Coordinated tax fraud by corporate executives.', 'Solved', '2022-09-01', '2023-05-20', 6),
('Ghost Protocol',              'Unknown actor breaching law-enforcement databases.', 'Under Investigation', '2024-08-01', NULL, 2);


INSERT IGNORE INTO Suspects (name, dob, gender, address, phone, criminal_record) VALUES
('Victor Draine',       '1985-04-12', 'Male',   '12 Shadwell Lane, Eastport',  '9900001111', 'Prior convictions: armed robbery (2015), assault (2018)'),
('Nina Kowalski',       '1990-09-25', 'Female', '7 Birch Ave, Northgate',      '9900002222', 'Suspected identity fraud, no convictions'),
('Darius Cole',         '1978-12-01', 'Male',   '55 Harbor Road, Southbay',    '9900003333', 'Known associate of organized crime, 2 prior arrests'),
('Meera Joshi',         '1995-07-15', 'Female', '301 Palm Street, Midtown',    '9900004444', 'No criminal record'),
('Tyson Brack',         '1982-03-22', 'Male',   '88 Old Mill Road, Westside',  '9900005555', 'Drug trafficking (2019, acquitted), assault (2021)'),
('Renata Volkov',       '1988-11-09', 'Female', '14 Ice Street, Northgate',    '9900006666', 'Financial fraud conviction (2020, 2 years suspended)'),
('Omar Khalid',         '1975-06-30', 'Male',   '9 Crescent Blvd, Eastport',   '9900007777', 'Narcotics possession, served 18 months (2017)'),
('Lily Chang',          '1993-02-14', 'Female', '22 Tech Park, Downtown',      '9900008888', 'Charged with corporate espionage, case pending'),
('Sanjay Mirza',        '1980-08-05', 'Male',   '77 Old Town Square, Midtown', '9900009999', 'Multiple fraud cases, convicted once (2016)'),
('Carlos Fuentes',      '1987-01-19', 'Male',   '5 Riverside Lane, Southbay',  '9900010000', 'Armed robbery, served 3 years (2014-2017)'),
('Irina Petranova',     '1992-10-31', 'Female', '33 North Quay, Eastport',     '9900011111', 'Suspected money laundering, no convictions'),
('Felix Drummond',      '1970-05-27', 'Male',   '91 Highcliff Drive, Westside','9900012222', 'White-collar crime, corporate fraud (2010), acquitted');

INSERT IGNORE INTO Victims (name, dob, gender, address, contact_info, case_id) VALUES
('Alan Foster',    '1960-03-10', 'Male',   '45 Marina Blvd, Eastport',   'afoster@mail.com',  2),
('Sandra Bloom',   '1975-08-22', 'Female', '12 Clover Lane, Northgate',  '9811001101',        2),
('George Tran',    '1958-11-14', 'Male',   '8 Dock Road, Southbay',      '9811001102',        2),
('Rachel Kim',     '1988-05-01', 'Female', '302 City Park, Downtown',    'rkim@webmail.net',  5),
('Hassan Al-Amin', '1972-07-19', 'Male',   '19 Desert Rose, Midtown',    '9811001104',        5),
('Maria Santos',   '1990-12-25', 'Female', '7 Sunset Ave, Westside',     'msantos@corp.in',   5),
('Peter Novak',    '1965-04-04', 'Male',   '55 Oak Street, Northgate',   '9811001106',        10),
('Zara Hussain',   '1982-09-11', 'Female', '3 River Walk, Eastport',     '9811001107',        10),
('Eleanor Cross',  '1948-01-30', 'Female', '15 Meadow Lane, Westside',   'ecross@old.net',    7),
('Tom Bryce',      '1991-06-06', 'Male',   '44 High Street, Downtown',   '9811001109',        1);


INSERT IGNORE INTO Crime_Scenes (case_id, location, date_occurred, description) VALUES
(1,  'Goldman Jewelers, 8 Central Sq.',         '2024-01-08 22:30:00', 'Forced entry through back door, security camera disabled.'),
(1,  'Luxe Gems, 22 Market Street',             '2024-01-09 23:00:00', 'Second jewelry store hit same night. Similar MO.'),
(2,  'Dock 17, Southbay Harbor',                '2024-02-12 03:15:00', 'First body found by harbor police.'),
(2,  'Dock 9, Southbay Harbor',                 '2024-02-14 05:00:00', 'Two more bodies found. Execution-style.'),
(3,  'Tech Park Server Room, Downtown',         '2023-06-05 02:00:00', 'Physical access breach to install rogue access point.'),
(4,  'Container Yard, Port Area',               '2024-03-20 01:00:00', 'Narcotics hidden in imported cargo.'),
(5,  '14 Wellington Street (Office Building)',  '2024-05-03 19:00:00', 'Victim found in elevator. No signs of struggle.'),
(5,  'Northgate Parking Garage',                '2024-06-01 21:00:00', 'Second victim discovered in vehicle.'),
(6,  'Abandoned Warehouse 22, Southbay',        '2022-11-12 23:45:00', 'Raid location. Drug packaging materials found.'),
(9,  'First National Bank, City Centre',        '2024-04-10 10:30:00', 'Armed takeover robbery. Vault breached.'),
(10, 'Midtown Market, Vendor Square',           '2024-06-18 12:45:00', 'Improvised explosive device detonated in market.'),
(11, 'Shell Corp Offices, Financial District',  '2023-01-10 18:00:00', 'Covert entry to copy physical ledger books.'),
(12, 'Factory Shed 4, Industrial District',     '2024-07-01 02:00:00', 'Arson. Accelerant traces found.'),
(12, 'Warehouse 11, Port Rd',                   '2024-07-03 00:30:00', 'Second suspicious fire. Linked by MO.'),
(14, 'CEO Estate, 100 Hillview Dr',             '2022-09-05 20:00:00', 'Secret meeting location for tax fraud syndicate.'),
(15, 'Police HQ Server Room (remote intrusion)','2024-08-01 04:00:00', 'Unauthorized access via compromised credentials.');


INSERT IGNORE INTO Evidence (case_id, scene_id, description, type, date_collected, storage_location) VALUES
(1,  1,  'Bolt cutter found near back entrance',        'Physical',    '2024-01-09', 'Locker A-12'),
(1,  2,  'Partial boot print on floor',                 'Physical',    '2024-01-10', 'Locker A-13'),
(2,  3,  'Victim clothing sample',                      'Biological',  '2024-02-12', 'Bio Lab B-02'),
(2,  4,  'Shell casings .45 ACP (x3)',                  'Physical',    '2024-02-14', 'Locker A-20'),
(2,  4,  'Security camera footage (damaged)',           'Digital',     '2024-02-14', 'Digital Vault D-01'),
(3,  5,  'Rogue Wi-Fi Router left on site',             'Physical',    '2023-06-05', 'Locker B-10'),
(3,  NULL,'Email server logs showing phishing activity','Digital',     '2023-06-10', 'Digital Vault D-02'),
(4,  6,  '30kg cocaine in sealed containers',           'Physical',    '2024-03-22', 'Evidence Vault V-03'),
(5,  7,  'Victim personal effects (wallet, keys)',      'Physical',    '2024-05-04', 'Locker B-05'),
(5,  8,  'Tire marks at scene',                         'Physical',    '2024-06-02', 'Locker B-06'),
(6,  9,  'Scale and packaging baggies',                 'Physical',    '2022-11-13', 'Locker C-01'),
(6,  9,  'Burner phone with supplier contacts',         'Digital',     '2022-11-13', 'Digital Vault D-04'),
(9,  10, 'Broken vault drill bit',                      'Physical',    '2024-04-10', 'Locker A-31'),
(9,  10, 'Getaway vehicle (abandoned, 3km away)',       'Physical',    '2024-04-10', 'Vehicle Bay V-01'),
(10, 11, 'IED components recovered post-blast',         'Physical',    '2024-06-18', 'Bomb Disposal Bd-01'),
(10, 11, 'Witness video recording (mobile phone)',      'Digital',     '2024-06-18', 'Digital Vault D-03'),
(11, 12, 'Hidden USB drive with off-book transactions', 'Digital',     '2023-01-11', 'Digital Vault D-05'),
(11, NULL,'Shell company financial records (paper)',    'Document', '2023-01-15', 'Document Room DR-01'),
(12, 13, 'Accelerant sample (gasoline)',                'Biological',  '2024-07-01', 'Bio Lab B-03'),
(12, 14, 'Partial fingerprint on door frame',           'Physical',    '2024-07-04', 'Locker B-10'),
(14, 15, 'Audio recording of illicit tax meeting',      'Digital',     '2022-09-06', 'Digital Vault D-06'),
(14, 15, 'Shredded documents (reconstructed)',          'Document', '2022-09-10', 'Document Room DR-02'),
(15, 16, 'Server intrusion logs',                       'Digital',     '2024-08-02', 'Digital Vault D-05'),
(13, NULL,'Bullet casings from rooftop',                'Physical',    '2024-07-21', 'Locker A-40');


INSERT IGNORE INTO Witnesses (name, contact_info, address) VALUES
('Brian Lock',    '9801001101', '3 Hillcrest Rd, Northgate'),
('Sheila Bauer',  '9801001102', '17 Lake View, Eastport'),
('Tommy Yuen',    '9801001103', '54 West End Lane, Downtown'),
('Priti Nair',    '9801001104', '8 Garden Close, Midtown'),
('Ray Donovan',   '9801001105', '22 Canal Side, Southbay'),
('Monika Geller', '9801001106', '10 Central Park, Downtown'),
('Ian Frost',     '9801001107', '66 Pine Street, Westside'),
('Yuki Tanaka',   '9801001108', '11 Cherry Blossom Lane, Northgate'),
('Amir Hassan',   '9801001109', '39 Boulevard, Eastport'),
('Chloe Martin',  '9801001110', '2 Crescent Way, Midtown'),
('John Doe (Anon)','Hidden',    'Confidential'),
('Sarah Smith',   '9801001112', '88 Corporate Ave, Financial District'),
('Michael Ross',  '9801001113', '12 Bank St, City Centre'),
('Lisa Wong',     '9801001114', '40 Ocean Drive, Southbay'),
('Omar Little',   '9801001115', '99 Project Row, Westside');

INSERT IGNORE INTO Interrogations (suspect_id, officer_id, case_id, session_date, transcript_summary) VALUES
(1, 1, 1,  '2024-01-15 10:00:00', 'Suspect denies involvement. Claims he was home all night. No alibi witnesses.'),
(3, 4, 2,  '2024-02-20 14:00:00', 'Suspect lawyered up immediately. Provided no information.'),
(7, 9, 4,  '2024-03-25 09:30:00', 'Suspect admits knowledge of shipment but denies ownership. Implicates known crime figure.'),
(2, 2, 3,  '2023-06-15 11:00:00', 'Suspect cooperated fully. Provided email chain as evidence. Led to conviction.'),
(5, 3, 4,  '2024-04-01 15:00:00', 'Volatile interrogation. Suspect threatened officers. No useful intel obtained.'),
(6, 6, 11, '2023-01-25 10:00:00', 'Suspect initially denied. Confronted with financial records. Admitted to minor role.'),
(9, 6, 8,  '2023-03-01 13:00:00', 'Denied knowledge of counterfeiting operation. Evidence suggests otherwise.'),
(11,7, 9,  '2024-04-20 16:00:00', 'Claims to be a bystander. Eyewitness places her near the bank during the robbery.'),
(12,6, 14, '2022-09-15 09:00:00', 'Cornered by audio evidence, suspect confessed to orchestrating the tax fraud syndicate.'),
(5, 9, 6,  '2022-11-20 14:00:00', 'Admitted to packing the narcotics. Plea deal offered.'),
(2, 2, 15, '2024-08-05 10:00:00', 'Denies hacking police servers, claims her identity was stolen.'),
(8, 2, 3,  '2023-06-20 11:00:00', 'Accomplice turned state witness against Primary Suspect.');

INSERT IGNORE INTO DNA_Samples (evidence_id, suspect_id, victim_id, sample_type, collection_date, lab_result) VALUES
(3, NULL, 1, 'Blood',       '2024-02-13', 'Match'),
(3, 3,    NULL,'Hair',      '2024-02-13', 'Pending'),
(19,NULL, NULL,'Soil swab', '2024-07-02', 'No Match'),
(9, NULL, 4,  'Skin cells', '2024-05-05', 'Inconclusive'),
(2, 1,    NULL,'Blood',     '2024-01-11', 'No Match'),
(15,NULL, 7,  'Trace debris','2024-06-19', 'Pending'),
(11, 5,   NULL,'Hair',      '2022-11-14', 'Match'),
(21,12,   NULL,'Saliva',    '2022-09-07', 'Match');

INSERT IGNORE INTO Fingerprints (evidence_id, scene_id, suspect_id, print_type, match_status, match_reference) VALUES
(1,  1,  1,    'Loop',     'Matched',   'FP-REF-001'),
(2,  2,  1,    'Whorl',    'Matched',   'FP-REF-001'),
(4,  4,  3,    'Arch',     'Unmatched', NULL),
(20, 14, NULL, 'Loop',     'Pending',   'FP-REF-002'),
(13, 10, 10,   'Whorl',    'Matched',   'FP-REF-003'),
(9,  7,  4,    'Loop',     'Pending',   NULL),
(10, 8,  5,    'Arch',     'Unmatched', NULL),
(15, 11, NULL, 'Loop',     'Pending',   'FP-REF-004'),
(1, NULL,1,    'Whorl',    'Matched',   'FP-REF-001'),
(23, 16, 8,    'Loop',     'Pending',   'FP-REF-005'),
(6,  5,  2,    'Whorl',    'Matched',   'FP-REF-006'),
(11, 9,  5,    'Loop',     'Matched',   'FP-REF-007'),
(12, 9,  5,    'Arch',     'Matched',   'FP-REF-007'),
(17, 12, 6,    'Loop',     'Matched',   'FP-REF-008'),
(21, 15, 12,   'Whorl',    'Matched',   'FP-REF-009');

-- ============================================================
-- 11. CASE_SUSPECTS (junction: case <-> suspect)
-- ============================================================
INSERT IGNORE INTO Case_Suspects (case_id, suspect_id, role) VALUES
(1,  1,  'Primary'),
(1,  10, 'Accomplice'),
(2,  3,  'Primary'),
(2,  11, 'Person of Interest'),
(3,  2,  'Primary'),
(3,  8,  'Accomplice'),
(4,  7,  'Primary'),
(4,  5,  'Accomplice'),
(5,  1,  'Person of Interest'),
(5,  4,  'Person of Interest'),
(6,  5,  'Primary'),
(8,  9,  'Primary'),
(9,  10, 'Primary'),
(9,  11, 'Accomplice'),
(11, 6,  'Accomplice'),
(11, 12, 'Primary'),
(13, 1,  'Person of Interest'),
(14, 12, 'Primary'),
(15, 2,  'Primary'),
(15, 8,  'Person of Interest');


INSERT IGNORE INTO Evidence_Suspects (evidence_id, suspect_id) VALUES
(1,  1),
(2,  1),
(4,  3),
(6,  2),
(7,  7),
(11, 5),
(12, 5),
(13, 10),
(17, 6),
(21, 12),
(23, 8);


INSERT IGNORE INTO Case_Witnesses (case_id, witness_id, statement) VALUES
(1,  1, 'Saw two masked individuals near the alley at approx. 10:30pm.'),
(2,  2, 'Heard gunshots from Dock 9 area around 5am.'),
(2,  5, 'Saw a black van leaving the docks at high speed.'),
(3,  12, 'Provided access logs showing unauthorized entry into the system.'),
(4,  3, 'Noticed suspicious cargo being offloaded late at night.'),
(5,  4, 'Saw a man in a grey coat near the elevator around 7pm.'),
(6,  14, 'Reported suspicious activity and smells coming from Warehouse 22.'),
(9,  6, 'Was inside the bank. Saw two armed men wearing ski masks.'),
(9,  7, 'Witnessed getaway vehicle speeding off towards the east.'),
(10, 8, 'Was in the market when the explosion occurred. Severe trauma.'),
(11, 11, 'Anonymous tip providing the location of the hidden ledger.'),
(12, 9, 'Smelled petrol near Factory Shed 4 before the fire.'),
(13, 10, 'Heard a sharp crack like a gunshot from the rooftop.'),
(14, 13, 'Overheard the executives planning the offshore accounts layout.');

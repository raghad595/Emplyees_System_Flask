from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3, os
# ================== APP SETUP ==================
app = Flask(__name__)
app.secret_key = "change-me-please"

DB_NAME = os.path.join(os.path.dirname(__file__), "employees_system.db")

def get_conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

# ================== DB SETUP & SEED ==================
def init_db():
    conn = get_conn()
    c = conn.cursor()

    # Department
    c.execute("""
    CREATE TABLE IF NOT EXISTS Department (
        dep_id INTEGER PRIMARY KEY,
        name_employee TEXT,
        phone_numper INTEGER,
        location TEXT
    )""")

    # employee
    c.execute("""
    CREATE TABLE IF NOT EXISTS employee(
        emp_id INTEGER PRIMARY KEY,
        bdate TEXT,
        salary REAL,
        ssn TEXT,
        address TEXT NOT NULL,
        gender TEXT CHECK (gender IN ('M','F')),
        firt_name TEXT,
        last_name TEXT,
        dep_id INTEGER,
        FOREIGN KEY (dep_id) REFERENCES Department(dep_id)
    )""")

    # project
    c.execute("""
    CREATE TABLE IF NOT EXISTS project(
        project_id INTEGER PRIMARY KEY,
        employee_name TEXT,
        phone_numper INTEGER,
        location TEXT,
        dep_id INTEGER,
        FOREIGN KEY (dep_id) REFERENCES Department(dep_id)
    )""")

    # jop (jobs)
    c.execute("""
    CREATE TABLE IF NOT EXISTS jop(
        jop_id INTEGER PRIMARY KEY,
        title TEXT,
        description_jop TEXT,
        Salary REAL,
        Grade TEXT
    )""")

    # bonus
    c.execute("""
    CREATE TABLE IF NOT EXISTS bonus (
        bounis_id INTEGER PRIMARY KEY,
        amount REAL NOT NULL,
        _date TEXT,
        emp_id INTEGER,
        FOREIGN KEY (emp_id) REFERENCES employee(emp_id)
    )""")

    # dependant
    c.execute("""
    CREATE TABLE IF NOT EXISTS dependant (
        dependant_id INTEGER PRIMARY KEY,
        _name TEXT,
        gender TEXT CHECK (gender IN ('M','F')),
        Bdate TEXT,
        relationship TEXT NOT NULL,
        emp_id INTEGER,
        FOREIGN KEY (emp_id) REFERENCES employee(emp_id)
    )""")

    # training
    c.execute("""
    CREATE TABLE IF NOT EXISTS training(
        training_id INTEGER PRIMARY KEY,
        title TEXT,
        _description TEXT,
        start_date TEXT,
        end_date TEXT
    )""")

    # works_on (employee <-> project)
    c.execute("""
    CREATE TABLE IF NOT EXISTS works_on(
        emp_id INTEGER,
        project_id INTEGER,
        hours REAL,
        PRIMARY KEY (emp_id, project_id),
        FOREIGN KEY (emp_id) REFERENCES employee(emp_id),
        FOREIGN KEY (project_id) REFERENCES project(project_id)
    )""")

    # attends (employee <-> training)
    c.execute("""
    CREATE TABLE IF NOT EXISTS attends (
        emp_id INTEGER,
        training_id INTEGER,
        PRIMARY KEY (emp_id, training_id),
        FOREIGN KEY (emp_id) REFERENCES employee(emp_id),
        FOREIGN KEY (training_id) REFERENCES training(training_id)
    )""")

    # employee_Job (employee <-> jop)
    c.execute("""
    CREATE TABLE IF NOT EXISTS employee_Job (
        emp_id INTEGER,
        job_id INTEGER,
        PRIMARY KEY (emp_id, job_id),
        FOREIGN KEY (emp_id) REFERENCES employee(emp_id),
        FOREIGN KEY (job_id) REFERENCES jop(jop_id)
    )""")

    conn.commit()
    conn.close()

# Seed the database with initial data if empty
def seed_db_if_empty():
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) AS n FROM Department")
    if c.fetchone()["n"] > 0:
        conn.close()
        return  # already seeded

    # Departments
    departments = [
        (1, 'HR Department', 201234567, 'Cairo'),
        (2, 'IT Department', 201234568, 'Giza'),
        (3, 'Finance Department', 201234569, 'Alexandria'),
        (4, 'Marketing Department', 201234570, 'Cairo'),
        (5, 'Sales Department', 201234571, 'Giza'),
        (6, 'R&D Department', 201234572, 'Alexandria'),
        (7, 'Support Department', 201234573, 'Cairo'),
        (8, 'Logistics Department', 201234574, 'Giza'),
        (9, 'Operations Department', 201234575, 'Alexandria'),
        (10, 'Legal Department', 201234576, 'Cairo'),
        (11, 'HR Department 2', 201234577, 'Cairo'),
        (12, 'IT Department 2', 201234578, 'Giza'),
        (13, 'Finance Department 2', 201234579, 'Alexandria'),
        (14, 'Marketing Department 2', 201234580, 'Cairo'),
        (15, 'Sales Department 2', 201234581, 'Giza'),
        (16, 'R&D Department 2', 201234582, 'Alexandria'),
        (17, 'Support Department 2', 201234583, 'Cairo'),
        (18, 'Logistics Department 2', 201234584, 'Giza'),
        (19, 'Operations Department 2', 201234585, 'Alexandria'),
        (20, 'Legal Department 2', 201234586, 'Cairo'),
        (21, 'Department 21', 201234587, 'Cairo'),
        (22, 'Department 22', 201234588, 'Giza'),
        (23, 'Department 23', 201234589, 'Alexandria'),
        (24, 'Department 24', 201234590, 'Cairo'),
        (25, 'Department 25', 201234591, 'Giza'),
        (26, 'Department 26', 201234592, 'Alexandria'),
        (27, 'Department 27', 201234593, 'Cairo'),
        (28, 'Department 28', 201234594, 'Giza'),
        (29, 'Department 29', 201234595, 'Alexandria'),
        (30, 'Department 30', 201234596, 'Cairo'),
        (31, 'Department 31', 201234597, 'Cairo'),
        (32, 'Department 32', 201234598, 'Giza'),
        (33, 'Department 33', 201234599, 'Alexandria'),
        (34, 'Department 34', 201234600, 'Cairo'),
        (35, 'Department 35', 201234601, 'Giza'),
        (36, 'Department 36', 201234602, 'Alexandria'),
        (37, 'Department 37', 201234603, 'Cairo'),
        (38, 'Department 38', 201234604, 'Giza'),
        (39, 'Department 39', 201234605, 'Alexandria'),
        (40, 'Department 40', 201234606, 'Cairo'),
        (41, 'Department 41', 201234607, 'Cairo'),
        (42, 'Department 42', 201234608, 'Giza'),
        (43, 'Department 43', 201234609, 'Alexandria'),
        (44, 'Department 44', 201234610, 'Cairo'),
        (45, 'Department 45', 201234611, 'Giza'),
        (46, 'Department 46', 201234612, 'Alexandria'),
        (47, 'Department 47', 201234613, 'Cairo'),
        (48, 'Department 48', 201234614, 'Giza'),
        (49, 'Department 49', 201234615, 'Alexandria'),
        (50, 'Department 50', 201234616, 'Cairo')
    ]
    c.executemany("INSERT INTO Department (dep_id, name_employee, phone_numper, location) VALUES (?, ?, ?, ?)", departments)

    # Employees
    employees = [
        (1, '1990-05-12', 7000.00, 'SSN001', 'Cairo, Egypt', 'M', 'Ahmed', 'Hassan', 1),
        (2, '1985-03-22', 8500.00, 'SSN002', 'Giza, Egypt', 'F', 'Sara', 'Mohamed', 2),
        (3, '1992-11-02', 6200.00, 'SSN003', 'Alexandria, Egypt', 'M', 'Omar', 'Khaled', 3),
        (4, '1995-01-15', 5000.00, 'SSN004', 'Cairo, Egypt', 'F', 'Noura', 'Ali', 4),
        (5, '1988-07-19', 9000.00, 'SSN005', 'Giza, Egypt', 'M', 'Hassan', 'Mahmoud', 5),
        (6, '1993-04-05', 6500.00, 'SSN006', 'Alexandria, Egypt', 'F', 'Mai', 'Sami', 6),
        (7, '1991-06-12', 7200.00, 'SSN007', 'Cairo, Egypt', 'M', 'Mostafa', 'Youssef', 7),
        (8, '1986-09-18', 8800.00, 'SSN008', 'Giza, Egypt', 'F', 'Laila', 'Adel', 8),
        (9, '1994-02-21', 5500.00, 'SSN009', 'Alexandria, Egypt', 'M', 'Ehab', 'Ibrahim', 9),
        (10, '1989-08-14', 9300.00, 'SSN010', 'Cairo, Egypt', 'M', 'Mohamed', 'Reda', 10),
        (11, '1990-07-01', 7400.00, 'SSN011', 'Cairo, Egypt', 'M', 'Yasser', 'Hamdy', 11),
        (12, '1987-12-13', 8100.00, 'SSN012', 'Giza, Egypt', 'F', 'Amal', 'Rashad', 12),
        (13, '1992-05-27', 6600.00, 'SSN013', 'Alexandria, Egypt', 'M', 'Karim', 'Magdy', 13),
        (14, '1994-09-30', 5900.00, 'SSN014', 'Cairo, Egypt', 'F', 'Huda', 'Amin', 14),
        (15, '1985-11-16', 9700.00, 'SSN015', 'Giza, Egypt', 'M', 'Fadi', 'Tamer', 15),
        (16, '1991-01-08', 7200.00, 'SSN016', 'Alexandria, Egypt', 'F', 'Aya', 'Hany', 16),
        (17, '1993-03-10', 6800.00, 'SSN017', 'Cairo, Egypt', 'M', 'Sherif', 'Maher', 17),
        (18, '1988-06-25', 9100.00, 'SSN018', 'Giza, Egypt', 'F', 'Mona', 'Fouad', 18),
        (19, '1995-04-04', 5600.00, 'SSN019', 'Alexandria, Egypt', 'M', 'Tamer', 'Galal', 19),
        (20, '1990-10-12', 7500.00, 'SSN020', 'Cairo, Egypt', 'M', 'Rami', 'Zaki', 20),
        (21, '1992-12-22', 7000.00, 'SSN021', 'Cairo, Egypt', 'M', 'Adel', 'Saad', 21),
        (22, '1986-05-14', 8600.00, 'SSN022', 'Giza, Egypt', 'F', 'Reham', 'Farouk', 22),
        (23, '1991-08-08', 6400.00, 'SSN023', 'Alexandria, Egypt', 'M', 'Mahmoud', 'Sobhy', 23),
        (24, '1993-07-05', 5100.00, 'SSN024', 'Cairo, Egypt', 'F', 'Eman', 'Lotfy', 24),
        (25, '1989-01-01', 8900.00, 'SSN025', 'Giza, Egypt', 'M', 'Ahmed', 'Samir', 25),
        (26, '1994-11-09', 6700.00, 'SSN026', 'Alexandria, Egypt', 'F', 'Doaa', 'Anwar', 26),
        (27, '1990-02-20', 7100.00, 'SSN027', 'Cairo, Egypt', 'M', 'Wael', 'Shehata', 27),
        (28, '1987-10-19', 8400.00, 'SSN028', 'Giza, Egypt', 'F', 'Mervat', 'Rashwan', 28),
        (29, '1992-06-07', 6500.00, 'SSN029', 'Alexandria, Egypt', 'M', 'Ibrahim', 'Refaat', 29),
        (30, '1995-09-02', 5300.00, 'SSN030', 'Cairo, Egypt', 'M', 'Khaled', 'Selim', 30),
        (31, '1988-04-15', 8800.00, 'SSN031', 'Cairo, Egypt', 'F', 'Yasmin', 'Fekry', 31),
        (32, '1991-03-26', 6900.00, 'SSN032', 'Giza, Egypt', 'M', 'Omar', 'Shawky', 32),
        (33, '1985-12-17', 9500.00, 'SSN033', 'Alexandria, Egypt', 'F', 'Nesma', 'Hossam', 33),
        (34, '1993-07-13', 6000.00, 'SSN034', 'Cairo, Egypt', 'M', 'Youssef', 'Hegazy', 34),
        (35, '1989-05-29', 8700.00, 'SSN035', 'Giza, Egypt', 'F', 'Abeer', 'Salah', 35),
        (36, '1992-08-18', 6400.00, 'SSN036', 'Alexandria, Egypt', 'M', 'Othman', 'Saif', 36),
        (37, '1990-09-24', 7600.00, 'SSN037', 'Cairo, Egypt', 'M', 'Hady', 'Shaker', 37),
        (38, '1986-07-31', 8100.00, 'SSN038', 'Giza, Egypt', 'F', 'Manar', 'ElShazly', 38),
        (39, '1995-01-19', 5800.00, 'SSN039', 'Alexandria, Egypt', 'M', 'Sameh', 'Arafa', 39),
        (40, '1987-03-11', 9000.00, 'SSN040', 'Cairo, Egypt', 'F', 'Hager', 'Alaa', 40),
        (41, '1991-11-25', 7200.00, 'SSN041', 'Cairo, Egypt', 'M', 'Taha', 'Fekry', 41),
        (42, '1988-08-06', 8500.00, 'SSN042', 'Giza, Egypt', 'F', 'Mariam', 'Sayed', 42),
        (43, '1992-02-28', 6300.00, 'SSN043', 'Alexandria, Egypt', 'M', 'Younes', 'Sabry', 43),
        (44, '1994-04-14', 5200.00, 'SSN044', 'Cairo, Egypt', 'F', 'Shaimaa', 'Fouzy', 44),
        (45, '1989-09-01', 8800.00, 'SSN045', 'Giza, Egypt', 'M', 'Islam', 'Hussein', 45),
        (46, '1993-12-08', 6600.00, 'SSN046', 'Alexandria, Egypt', 'F', 'Farah', 'Mostafa', 46),
        (47, '1990-01-23', 7400.00, 'SSN047', 'Cairo, Egypt', 'M', 'Essam', 'Abbas', 47),
        (48, '1986-05-10', 8100.00, 'SSN048', 'Giza, Egypt', 'F', 'Rania', 'Ashraf', 48),
        (49, '1995-06-16', 5700.00, 'SSN049', 'Alexandria, Egypt', 'M', 'Sherif', 'Nasr', 49),
        (50, '1988-02-12', 8900.00, 'SSN050', 'Cairo, Egypt', 'F', 'Lobna', 'Ezzat', 50)

    ]
    c.executemany("""
        INSERT INTO employee (emp_id, bdate, salary, ssn, address, gender, firt_name, last_name, dep_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, employees)

    # Projects
    projects = [
        (1, 'Project Alpha', 201111111, 'Cairo', 1),
        (2, 'Project Beta', 201111112, 'Giza', 2),
        (3, 'Project Gamma', 201111113, 'Alexandria', 3),
        (4, 'Project Delta', 201111114, 'Cairo', 4),
        (5, 'Project Epsilon', 201111115, 'Giza', 5),
        (6, 'Project Zeta', 201111116, 'Alexandria', 6),
        (7, 'Project Eta', 201111117, 'Cairo', 7),
        (8, 'Project Theta', 201111118, 'Giza', 8),
        (9, 'Project Iota', 201111119, 'Alexandria', 9),
        (10, 'Project Kappa', 201111120, 'Cairo', 10),
        (11, 'Project Lambda', 201111121, 'Cairo', 11),
        (12, 'Project Mu', 201111122, 'Giza', 12),
        (13, 'Project Nu', 201111123, 'Alexandria', 13),
        (14, 'Project Xi', 201111124, 'Cairo', 14),
        (15, 'Project Omicron', 201111125, 'Giza', 15),
        (16, 'Project Pi', 201111126, 'Alexandria', 16),
        (17, 'Project Rho', 201111127, 'Cairo', 17),
        (18, 'Project Sigma', 201111128, 'Giza', 18),
        (19, 'Project Tau', 201111129, 'Alexandria', 19),
        (20, 'Project Upsilon', 201111130, 'Cairo', 20),
        (21, 'Project Phi', 201111131, 'Cairo', 21),
        (22, 'Project Chi', 201111132, 'Giza', 22),
        (23, 'Project Psi', 201111133, 'Alexandria', 23),
        (24, 'Project Omega', 201111134, 'Cairo', 24),
        (25, 'Project Orion', 201111135, 'Giza', 25),
        (26, 'Project Vega', 201111136, 'Alexandria', 26),
        (27, 'Project Sirius', 201111137, 'Cairo', 27),
        (28, 'Project Altair', 201111138, 'Giza', 28),
        (29, 'Project Deneb', 201111139, 'Alexandria', 29),
        (30, 'Project Rigel', 201111140, 'Cairo', 30),
        (31, 'Project Spica', 201111141, 'Cairo', 31),
        (32, 'Project Betelgeuse', 201111142, 'Giza', 32),
        (33, 'Project Antares', 201111143, 'Alexandria', 33),
        (34, 'Project Procyon', 201111144, 'Cairo', 34),
        (35, 'Project Aldebaran', 201111145, 'Giza', 35),
        (36, 'Project Fomalhaut', 201111146, 'Alexandria', 36),
        (37, 'Project Castor', 201111147, 'Cairo', 37),
        (38, 'Project Pollux', 201111148, 'Giza', 38),
        (39, 'Project Capella', 201111149, 'Alexandria', 39),
        (40, 'Project Arcturus', 201111150, 'Cairo', 40),
        (41, 'Project Andromeda', 201111151, 'Cairo', 41),
        (42, 'Project Pegasus', 201111152, 'Giza', 42),
        (43, 'Project Hercules', 201111153, 'Alexandria', 43),
        (44, 'Project Perseus', 201111154, 'Cairo', 44),
        (45, 'Project Orionis', 201111155, 'Giza', 45),
        (46, 'Project Cygnus', 201111156, 'Alexandria', 46),
        (47, 'Project Phoenix', 201111157, 'Cairo', 47),
        (48, 'Project Hydra', 201111158, 'Giza', 48),
        (49, 'Project Leo', 201111159, 'Alexandria', 49),
        (50, 'Project Virgo', 201111160, 'Cairo', 50)
    ]
    c.executemany("""
        INSERT INTO project (project_id, employee_name, phone_numper, location, dep_id)
        VALUES (?, ?, ?, ?, ?)
    """, projects)

    # Jobs (jop)
    jobs = [
        (1, 'Job_1', 'Description for Job 1', 3050.00, 'Grade_2'),
        (2, 'Job_2', 'Description for Job 2', 3100.00, 'Grade_3'),
        (3, 'Job_3', 'Description for Job 3', 3150.00, 'Grade_4'),
        (4, 'Job_4', 'Description for Job 4', 3200.00, 'Grade_5'),
        (5, 'Job_5', 'Description for Job 5', 3250.00, 'Grade_1'),
        (6, 'Job_6', 'Description for Job 6', 3300.00, 'Grade_2'),
        (7, 'Job_7', 'Description for Job 7', 3350.00, 'Grade_3'),
        (8, 'Job_8', 'Description for Job 8', 3400.00, 'Grade_4'),
        (9, 'Job_9', 'Description for Job 9', 3450.00, 'Grade_5'),
        (10, 'Job_10', 'Description for Job 10', 3500.00, 'Grade_1'),
        (11, 'Job_11', 'Description for Job 11', 3550.00, 'Grade_2'),
        (12, 'Job_12', 'Description for Job 12', 3600.00, 'Grade_3'),
        (13, 'Job_13', 'Description for Job 13', 3650.00, 'Grade_4'),
        (14, 'Job_14', 'Description for Job 14', 3700.00, 'Grade_5'),
        (15, 'Job_15', 'Description for Job 15', 3750.00, 'Grade_1'),
        (16, 'Job_16', 'Description for Job 16', 3800.00, 'Grade_2'),
        (17, 'Job_17', 'Description for Job 17', 3850.00, 'Grade_3'),
        (18, 'Job_18', 'Description for Job 18', 3900.00, 'Grade_4'),
        (19, 'Job_19', 'Description for Job 19', 3950.00, 'Grade_5'),
        (20, 'Job_20', 'Description for Job 20', 4000.00, 'Grade_1'),
        (21, 'Job_21', 'Description for Job 21', 4050.00, 'Grade_2'),
        (22, 'Job_22', 'Description for Job 22', 4100.00, 'Grade_3'),
        (23, 'Job_23', 'Description for Job 23', 4150.00, 'Grade_4'),
        (24, 'Job_24', 'Description for Job 24', 4200.00, 'Grade_5'),
        (25, 'Job_25', 'Description for Job 25', 4250.00, 'Grade_1'),
        (26, 'Job_26', 'Description for Job 26', 4300.00, 'Grade_2'),
        (27, 'Job_27', 'Description for Job 27', 4350.00, 'Grade_3'),
        (28, 'Job_28', 'Description for Job 28', 4400.00, 'Grade_4'),
        (29, 'Job_29', 'Description for Job 29', 4450.00, 'Grade_5'),
        (30, 'Job_30', 'Description for Job 30', 4500.00, 'Grade_1'),
        (31, 'Job_31', 'Description for Job 31', 4550.00, 'Grade_2'),
        (32, 'Job_32', 'Description for Job 32', 4600.00, 'Grade_3'),
        (33, 'Job_33', 'Description for Job 33', 4650.00, 'Grade_4'),
        (34, 'Job_34', 'Description for Job 34', 4700.00, 'Grade_5'),
        (35, 'Job_35', 'Description for Job 35', 4750.00, 'Grade_1'),
        (36, 'Job_36', 'Description for Job 36', 4800.00, 'Grade_2'),
        (37, 'Job_37', 'Description for Job 37', 4850.00, 'Grade_3'),
        (38, 'Job_38', 'Description for Job 38', 4900.00, 'Grade_4'),
        (39, 'Job_39', 'Description for Job 39', 4950.00, 'Grade_5'),
        (40, 'Job_40', 'Description for Job 40', 5000.00, 'Grade_1'),
        (41, 'Job_41', 'Description for Job 41', 5050.00, 'Grade_2'),
        (42, 'Job_42', 'Description for Job 42', 5100.00, 'Grade_3'),
        (43, 'Job_43', 'Description for Job 43', 5150.00, 'Grade_4'),
        (44, 'Job_44', 'Description for Job 44', 5200.00, 'Grade_5'),
        (45, 'Job_45', 'Description for Job 45', 5250.00, 'Grade_1'),
        (46, 'Job_46', 'Description for Job 46', 5300.00, 'Grade_2'),
        (47, 'Job_47', 'Description for Job 47', 5350.00, 'Grade_3'),
        (48, 'Job_48', 'Description for Job 48', 5400.00, 'Grade_4'),
        (49, 'Job_49', 'Description for Job 49', 5450.00, 'Grade_5'),
        (50, 'Job_50', 'Description for Job 50', 5500.00, 'Grade_1')
    ]
    c.executemany("""
        INSERT INTO jop (jop_id, title, description_jop, Salary, Grade)
        VALUES (?, ?, ?, ?, ?)
    """, jobs)

    # Bonus
    bonuses = [
        (1, 510.00, '2025-01-02', 1),
        (2, 520.00, '2025-01-03', 2),
        (3, 530.00, '2025-01-04', 3),
        (4, 540.00, '2025-01-05', 4),
        (5, 550.00, '2025-01-06', 5),
        (6, 560.00, '2025-01-07', 6),
        (7, 570.00, '2025-01-08', 7),
        (8, 580.00, '2025-01-09', 8),
        (9, 590.00, '2025-01-10', 9),
        (10, 600.00, '2025-01-11', 10),
        (11, 610.00, '2025-01-12', 11),
        (12, 620.00, '2025-01-13', 12),
        (13, 630.00, '2025-01-14', 13),
        (14, 640.00, '2025-01-15', 14),
        (15, 650.00, '2025-01-16', 15),
        (16, 660.00, '2025-01-17', 16),
        (17, 670.00, '2025-01-18', 17),
        (18, 680.00, '2025-01-19', 18),
        (19, 690.00, '2025-01-20', 19),
        (20, 700.00, '2025-01-21', 20),
        (21, 710.00, '2025-01-22', 21),
        (22, 720.00, '2025-01-23', 22),
        (23, 730.00, '2025-01-24', 23),
        (24, 740.00, '2025-01-25', 24),
        (25, 750.00, '2025-01-26', 25),
        (26, 760.00, '2025-01-27', 26),
        (27, 770.00, '2025-01-28', 27),
        (28, 780.00, '2025-01-01', 28),
        (29, 790.00, '2025-01-02', 29),
        (30, 800.00, '2025-01-03', 30),
        (31, 810.00, '2025-01-04', 31),
        (32, 820.00, '2025-01-05', 32),
        (33, 830.00, '2025-01-06', 33),
        (34, 840.00, '2025-01-07', 34),
        (35, 850.00, '2025-01-08', 35),
        (36, 860.00, '2025-01-09', 36),
        (37, 870.00, '2025-01-10', 37),
        (38, 880.00, '2025-01-11', 38),
        (39, 890.00, '2025-01-12', 39),
        (40, 900.00, '2025-01-13', 40),
        (41, 910.00, '2025-01-14', 41),
        (42, 920.00, '2025-01-15', 42),
        (43, 930.00, '2025-01-16', 43),
        (44, 940.00, '2025-01-17', 44),
        (45, 950.00, '2025-01-18', 45),
        (46, 960.00, '2025-01-19', 46),
        (47, 970.00, '2025-01-20', 47),
        (48, 980.00, '2025-01-21', 48),
        (49, 990.00, '2025-01-22', 49),
        (50, 1000.00, '2025-01-23', 50)
    ]
    c.executemany("INSERT INTO bonus (bounis_id, amount, _date, emp_id) VALUES (?, ?, ?, ?)", bonuses)

    # Dependants
    dependants = [
        (1, 'Dependant_1', 'F', '2001-02-15', 'Relation_2', 1),
        (2, 'Dependant_2', 'M', '2002-03-15', 'Relation_3', 2),
        (3, 'Dependant_3', 'F', '2003-04-15', 'Relation_4', 3),
        (4, 'Dependant_4', 'M', '2004-05-15', 'Relation_1', 4),
        (5, 'Dependant_5', 'F', '2005-06-15', 'Relation_2', 5),
        (6, 'Dependant_6', 'M', '2006-07-15', 'Relation_3', 6),
        (7, 'Dependant_7', 'F', '2007-08-15', 'Relation_4', 7),
        (8, 'Dependant_8', 'M', '2008-09-15', 'Relation_1', 8),
        (9, 'Dependant_9', 'F', '2009-01-15', 'Relation_2', 9),
        (10, 'Dependant_10', 'M', '2000-02-15', 'Relation_3', 10),
        (11, 'Dependant_11', 'F', '2001-03-15', 'Relation_4', 11),
        (12, 'Dependant_12', 'M', '2002-04-15', 'Relation_1', 12),
        (13, 'Dependant_13', 'F', '2003-05-15', 'Relation_2', 13),
        (14, 'Dependant_14', 'M', '2004-06-15', 'Relation_3', 14),
        (15, 'Dependant_15', 'F', '2005-07-15', 'Relation_4', 15),
        (16, 'Dependant_16', 'M', '2006-08-15', 'Relation_1', 16),
        (17, 'Dependant_17', 'F', '2007-09-15', 'Relation_2', 17),
        (18, 'Dependant_18', 'M', '2008-01-15', 'Relation_3', 18),
        (19, 'Dependant_19', 'F', '2009-02-15', 'Relation_4', 19),
        (20, 'Dependant_20', 'M', '2000-03-15', 'Relation_1', 20),
        (21, 'Dependant_21', 'F', '2001-04-15', 'Relation_2', 21),
        (22, 'Dependant_22', 'M', '2002-05-15', 'Relation_3', 22),
        (23, 'Dependant_23', 'F', '2003-06-15', 'Relation_4', 23),
        (24, 'Dependant_24', 'M', '2004-07-15', 'Relation_1', 24),
        (25, 'Dependant_25', 'F', '2005-08-15', 'Relation_2', 25),
        (26, 'Dependant_26', 'M', '2006-09-15', 'Relation_3', 26),
        (27, 'Dependant_27', 'F', '2007-01-15', 'Relation_4', 27),
        (28, 'Dependant_28', 'M', '2008-02-15', 'Relation_1', 28),
        (29, 'Dependant_29', 'F', '2009-03-15', 'Relation_2', 29),
        (30, 'Dependant_30', 'M', '2000-04-15', 'Relation_3', 30),
        (31, 'Dependant_31', 'F', '2001-05-15', 'Relation_4', 31),
        (32, 'Dependant_32', 'M', '2002-06-15', 'Relation_1', 32),
        (33, 'Dependant_33', 'F', '2003-07-15', 'Relation_2', 33),
        (34, 'Dependant_34', 'M', '2004-08-15', 'Relation_3', 34),
        (35, 'Dependant_35', 'F', '2005-09-15', 'Relation_4', 35),
        (36, 'Dependant_36', 'M', '2006-01-15', 'Relation_1', 36),
        (37, 'Dependant_37', 'F', '2007-02-15', 'Relation_2', 37),
        (38, 'Dependant_38', 'M', '2008-03-15', 'Relation_3', 38),
        (39, 'Dependant_39', 'F', '2009-04-15', 'Relation_4', 39),
        (40, 'Dependant_40', 'M', '2000-05-15', 'Relation_1', 40),
        (41, 'Dependant_41', 'F', '2001-06-15', 'Relation_2', 41),
        (42, 'Dependant_42', 'M', '2002-07-15', 'Relation_3', 42),
        (43, 'Dependant_43', 'F', '2003-08-15', 'Relation_4', 43),
        (44, 'Dependant_44', 'M', '2004-09-15', 'Relation_1', 44),
        (45, 'Dependant_45', 'F', '2005-01-15', 'Relation_2', 45),
        (46, 'Dependant_46', 'M', '2006-02-15', 'Relation_3', 46),
        (47, 'Dependant_47', 'F', '2007-03-15', 'Relation_4', 47),
        (48, 'Dependant_48', 'M', '2008-04-15', 'Relation_1', 48),
        (49, 'Dependant_49', 'F', '2009-05-15', 'Relation_2', 49),
        (50, 'Dependant_50', 'M', '2000-06-15', 'Relation_3', 50)
    ]
    c.executemany("""
        INSERT INTO dependant (dependant_id, _name, gender, Bdate, relationship, emp_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, dependants)

    # Trainings
    trainings = [
        (1, 'Training_1', 'Description for Training 1', '2025-02-02', '2025-03-02'),
        (2, 'Training_2', 'Description for Training 2', '2025-02-03', '2025-03-03'),
        (3, 'Training_3', 'Description for Training 3', '2025-02-04', '2025-03-04'),
        (4, 'Training_4', 'Description for Training 4', '2025-02-05', '2025-03-05'),
        (5, 'Training_5', 'Description for Training 5', '2025-02-06', '2025-03-06'),
        (6, 'Training_6', 'Description for Training 6', '2025-02-07', '2025-03-07'),
        (7, 'Training_7', 'Description for Training 7', '2025-02-08', '2025-03-08'),
        (8, 'Training_8', 'Description for Training 8', '2025-02-09', '2025-03-09'),
        (9, 'Training_9', 'Description for Training 9', '2025-02-10', '2025-03-10'),
        (10, 'Training_10', 'Description for Training 10', '2025-02-11', '2025-03-11'),
        (11, 'Training_11', 'Description for Training 11', '2025-02-12', '2025-03-12'),
        (12, 'Training_12', 'Description for Training 12', '2025-02-13', '2025-03-13'),
        (13, 'Training_13', 'Description for Training 13', '2025-02-14', '2025-03-14'),
        (14, 'Training_14', 'Description for Training 14', '2025-02-15', '2025-03-15'),
        (15, 'Training_15', 'Description for Training 15', '2025-02-16', '2025-03-16'),
        (16, 'Training_16', 'Description for Training 16', '2025-02-17', '2025-03-17'),
        (17, 'Training_17', 'Description for Training 17', '2025-02-18', '2025-03-18'),
        (18, 'Training_18', 'Description for Training 18', '2025-02-19', '2025-03-19'),
        (19, 'Training_19', 'Description for Training 19', '2025-02-20', '2025-03-20'),
        (20, 'Training_20', 'Description for Training 20', '2025-02-21', '2025-03-21'),
        (21, 'Training_21', 'Description for Training 21', '2025-02-22', '2025-03-22'),
        (22, 'Training_22', 'Description for Training 22', '2025-02-23', '2025-03-23'),
        (23, 'Training_23', 'Description for Training 23', '2025-02-24', '2025-03-24'),
        (24, 'Training_24', 'Description for Training 24', '2025-02-25', '2025-03-25'),
        (25, 'Training_25', 'Description for Training 25', '2025-02-26', '2025-03-26'),
        (26, 'Training_26', 'Description for Training 26', '2025-02-27', '2025-03-27'),
        (27, 'Training_27', 'Description for Training 27', '2025-02-28', '2025-03-28'),
        (28, 'Training_28', 'Description for Training 28', '2025-02-01', '2025-03-01'),
        (29, 'Training_29', 'Description for Training 29', '2025-02-02', '2025-03-02'),
        (30, 'Training_30', 'Description for Training 30', '2025-02-03', '2025-03-03'),
        (31, 'Training_31', 'Description for Training 31', '2025-02-04', '2025-03-04'),
        (32, 'Training_32', 'Description for Training 32', '2025-02-05', '2025-03-05'),
        (33, 'Training_33', 'Description for Training 33', '2025-02-06', '2025-03-06'),
        (34, 'Training_34', 'Description for Training 34', '2025-02-07', '2025-03-07'),
        (35, 'Training_35', 'Description for Training 35', '2025-02-08', '2025-03-08'),
        (36, 'Training_36', 'Description for Training 36', '2025-02-09', '2025-03-09'),
        (37, 'Training_37', 'Description for Training 37', '2025-02-10', '2025-03-10'),
        (38, 'Training_38', 'Description for Training 38', '2025-02-11', '2025-03-11'),
        (39, 'Training_39', 'Description for Training 39', '2025-02-12', '2025-03-12'),
        (40, 'Training_40', 'Description for Training 40', '2025-02-13', '2025-03-13'),
        (41, 'Training_41', 'Description for Training 41', '2025-02-14', '2025-03-14'),
        (42, 'Training_42', 'Description for Training 42', '2025-02-15', '2025-03-15'),
        (43, 'Training_43', 'Description for Training 43', '2025-02-16', '2025-03-16'),
        (44, 'Training_44', 'Description for Training 44', '2025-02-17', '2025-03-17'),
        (45, 'Training_45', 'Description for Training 45', '2025-02-18', '2025-03-18'),
        (46, 'Training_46', 'Description for Training 46', '2025-02-19', '2025-03-19'),
        (47, 'Training_47', 'Description for Training 47', '2025-02-20', '2025-03-20'),
        (48, 'Training_48', 'Description for Training 48', '2025-02-21', '2025-03-21'),
        (49, 'Training_49', 'Description for Training 49', '2025-02-22', '2025-03-22'),
        (50, 'Training_50', 'Description for Training 50', '2025-02-23', '2025-03-23')

    ]
    c.executemany("""
        INSERT INTO training (training_id, title, _description, start_date, end_date)
        VALUES (?, ?, ?, ?, ?)
    """, trainings)

    # works_on
    works = [
        (1,1,11.00),
        (2,2,12.00),
        (3,3,13.00),
        (4,4,14.00),
        (5, 5, 15.00),
        (6, 6, 16.00),
        (7, 7, 17.00),
        (8, 8, 18.00),
        (9, 9, 19.00),
        (10, 10, 20.00),
        (11, 11, 21.00),
        (12, 12, 22.00),
        (13, 13, 23.00),
        (14, 14, 24.00),
        (15, 15, 25.00),
        (16, 16, 26.00),
        (17, 17, 27.00),
        (18, 18, 28.00),
        (19, 19, 29.00),
        (20, 20, 10.00),
        (21, 21, 11.00),
        (22, 22, 12.00),
        (23, 23, 13.00),
        (24, 24, 14.00),
        (25, 25, 15.00),
        (26, 26, 16.00),
        (27, 27, 17.00),
        (28, 28, 18.00),
        (29, 29, 19.00),
        (30, 30, 20.00),
        (31, 31, 21.00),
        (32, 32, 22.00),
        (33, 33, 23.00),
        (34, 34, 24.00),
        (35, 35, 25.00),
        (36, 36, 26.00),
        (37, 37, 27.00),
        (38, 38, 28.00),
        (39, 39, 29.00),
        (40, 40, 10.00),
        (41, 41, 11.00),
        (42, 42, 12.00),
        (43, 43, 13.00),
        (44, 44, 14.00),
        (45, 45, 15.00),
        (46, 46, 16.00),
        (47, 47, 17.00),
        (48, 48, 18.00),
        (49, 49, 19.00),
        (50, 50, 20.00)
    ]
    c.executemany("INSERT INTO works_on (emp_id, project_id, hours) VALUES (?, ?, ?)", works)

    # attends
    attends = [
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12, 12),
        (13, 13),
        (14, 14),
        (15, 15),
        (16, 16),
        (17, 17),
        (18, 18),
        (19, 19),
        (20, 20),
        (21, 21),
        (22, 22),
        (23, 23),
        (24, 24),
        (25, 25),
        (26, 26),
        (27, 27),
        (28, 28),
        (29, 29),
        (30, 30),
        (31, 31),
        (32, 32),
        (33, 33),
        (34, 34),
        (35, 35),
        (36, 36),
        (37, 37),
        (38, 38),
        (39, 39),
        (40, 40),
        (41, 41),
        (42, 42),
        (43, 43),
        (44, 44),
        (45, 45),
        (46, 46),
        (47, 47),
        (48, 48),
        (49, 49),
        (50, 50)
    ]
    c.executemany("INSERT INTO attends (emp_id, training_id) VALUES (?, ?)", attends)

    # employee_Job
    employee_jobs = [
        (1,1),
        (2,2),
        (3,3),
        (4,4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
        (11, 11),
        (12, 12),
        (13, 13),
        (14, 14),
        (15, 15),
        (16, 16),
        (17, 17),
        (18, 18),
        (19, 19),
        (20, 20),
        (21, 21),
        (22, 22),
        (23, 23),
        (24, 24),
        (25, 25),
        (26, 26),
        (27, 27),
        (28, 28),
        (29, 29),
        (30, 30),
        (31, 31),
        (32, 32),
        (33, 33),
        (34, 34),
        (35, 35),
        (36, 36),
        (37, 37),
        (38, 38),
        (39, 39),
        (40, 40),
        (41, 41),
        (42, 42),
        (43, 43),
        (44, 44),
        (45, 45),
        (46, 46),
        (47, 47),
        (48, 48),
        (49, 49),
        (50, 50)
    ]
    c.executemany("INSERT INTO employee_Job (emp_id, job_id) VALUES (?, ?)", employee_jobs)

    conn.commit()
    conn.close()

init_db()
seed_db_if_empty()

# ================== ROUTES ==================
@app.route("/")
def index():
    conn = get_conn()
    c = conn.cursor()

    # Departments
    c.execute("SELECT * FROM Department ORDER BY dep_id")
    departments = c.fetchall()

    # Employees (include department name)
    c.execute("""
        SELECT e.*, d.name_employee AS dep_name
        FROM employee e
        LEFT JOIN Department d ON e.dep_id = d.dep_id
        ORDER BY e.emp_id
    """)
    employees = c.fetchall()

    # Projects + related Department name
    c.execute("""
        SELECT p.*, d.name_employee AS dep_name
        FROM project p
        LEFT JOIN Department d ON p.dep_id = d.dep_id
        ORDER BY p.project_id
    """)
    projects = c.fetchall()

    # Jobs + related employees (comma-separated)
    c.execute("""
        SELECT j.jop_id,
               j.title,
               j.description_jop,
               j.Salary AS salary,
               j.Grade AS grade,
               GROUP_CONCAT(e.firt_name || ' ' || e.last_name) AS employees
        FROM jop j
        LEFT JOIN employee_Job ej ON j.jop_id = ej.job_id
        LEFT JOIN employee e ON e.emp_id = ej.emp_id
        GROUP BY j.jop_id
        ORDER BY j.jop_id
    """)
    jobs = c.fetchall()

    conn.close()
    return render_template(
        "employees_system.html",
        departments=departments,
        employees=employees,
        projects=projects,
        jobs=jobs
    )

# ---------- Departments CRUD (existing) ----------
# Create a new department
@app.route("/create_department", methods=["POST"])
def create_department():
    dep_id = request.form["dep_id"]
    name_employee = request.form["name_employee"]
    phone_numper = request.form["phone_numper"] or None
    location = request.form["location"] or None
    conn = get_conn(); c = conn.cursor()
    try:
        c.execute("INSERT INTO Department (dep_id, name_employee, phone_numper, location) VALUES (?, ?, ?, ?)",
                  (dep_id, name_employee, phone_numper, location))
        conn.commit()
        flash("Department added successfully", "success")
    except sqlite3.IntegrityError:
        flash(f"Department with ID {dep_id} already exists.", "danger")
    finally:
        conn.close()
    return redirect(url_for("index"))

# Update an existing department
@app.route("/update_department/<int:dep_id>", methods=["POST"])
def update_department(dep_id):
    name_employee = request.form["name_employee"]
    phone_numper = request.form["phone_numper"] or None
    location = request.form["location"] or None
    conn = get_conn(); c = conn.cursor()
    c.execute("UPDATE Department SET name_employee=?, phone_numper=?, location=? WHERE dep_id=?",
              (name_employee, phone_numper, location, dep_id))
    conn.commit(); conn.close()
    flash("Department updated successfully", "success")
    return redirect(url_for("index"))

# Delete an existing department
@app.route("/delete_department/<int:dep_id>", methods=["POST"])
def delete_department(dep_id):
    conn = get_conn(); c = conn.cursor()
    c.execute("DELETE FROM Department WHERE dep_id=?", (dep_id,))
    conn.commit(); conn.close()
    flash("Department deleted successfully", "success")
    return redirect(url_for("index"))

# ---------- Employees CRUD (existing) ----------
# Create a new employee
@app.route("/create_employee", methods=["POST"])
def create_employee():
    emp_id = request.form["emp_id"]
    bdate = request.form["bdate"] or None
    salary = request.form["salary"] or None
    ssn = request.form["ssn"] or None
    address = request.form["address"]
    gender = request.form["gender"] or None
    dep_id = request.form["dep_id"] or None

    conn = get_conn(); c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO employee (emp_id, bdate, salary, ssn, address, gender, dep_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (emp_id, bdate, salary, ssn, address, gender, dep_id))
        conn.commit()
        flash("Employee added successfully", "success")
    except sqlite3.IntegrityError:
        flash(f"Employee with ID {emp_id} already exists.", "danger")
    finally:
        conn.close()
    return redirect(url_for("index"))

# Update an existing employee
@app.route("/update_employee/<int:emp_id>", methods=["POST"])
def update_employee(emp_id):
    bdate = request.form["bdate"] or None
    salary = request.form["salary"] or None
    ssn = request.form["ssn"] or None
    address = request.form["address"]
    gender = request.form["gender"] or None
    dep_id = request.form["dep_id"] or None

    conn = get_conn(); c = conn.cursor()
    c.execute("""
        UPDATE employee
        SET bdate=?, salary=?, ssn=?, address=?, gender=?, dep_id=?
        WHERE emp_id=?
    """, (bdate, salary, ssn, address, gender, dep_id, emp_id))
    conn.commit(); conn.close()
    flash("Employee updated successfully", "success")
    return redirect(url_for("index"))

# Delete an existing employee
@app.route("/delete_employee/<int:emp_id>", methods=["POST"])
def delete_employee(emp_id):
    conn = get_conn(); c = conn.cursor()
    c.execute("DELETE FROM employee WHERE emp_id=?", (emp_id,))
    conn.commit(); conn.close()
    flash("Employee deleted successfully", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
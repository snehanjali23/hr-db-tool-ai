import sqlite3

try:
    conn = sqlite3.connect("hr.db")
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS employees")

    cursor.execute("""
    CREATE TABLE employees (
        id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        designation TEXT,
        salary INTEGER,
        location TEXT,
        hire_date TEXT
    )
    """)

    employees = [
        (1, "Alice Johnson", "HR", "HR Manager", 75000, "New York", "2018-03-12"),
        (2, "Bob Smith", "IT", "Software Engineer", 90000, "San Francisco", "2019-06-21"),
        (3, "Carla James", "Finance", "Accountant", 70000, "Chicago", "2020-08-15"),
        (4, "David Lee", "Marketing", "Marketing Manager", 80000, "Los Angeles", "2021-04-10"),
        (5, "Eva Brown", "Operations", "Ops Manager", 85000, "Seattle", "2017-01-25"),
        (6, "Frank Wright", "HR", "Recruiter", 60000, "Austin", "2016-11-11"),
        (7, "Grace Kim", "IT", "DevOps Engineer", 95000, "Boston", "2015-09-05"),
        (8, "Henry Miller", "Finance", "Financial Analyst", 72000, "Miami", "2020-10-30"),
        (9, "Isla Davis", "Marketing", "SEO Specialist", 68000, "Denver", "2022-02-17"),
        (10, "Jack Wilson", "Operations", "Logistics Lead", 79000, "San Diego", "2019-12-14")
    ]

    cursor.executemany("""
    INSERT INTO employees (id, name, department, designation, salary, location, hire_date)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """, employees)

    conn.commit()
    print("✅ HR database created with 10 employees.")

except sqlite3.Error as e:
    print("❌ SQLite Error:", e)

finally:
    if conn:
        conn.close()

"""
Seed script – inserts realistic sample data into alumni_db.
Run once: python seed.py
"""
import random
from db import get_connection

alumni_data = [
    ("Aarav Sharma",    "aarav.sharma@gmail.com",    "9876543210", 2019, "MCA"),
    ("Priya Patel",     "priya.patel@gmail.com",     "9123456780", 2020, "MCA"),
    ("Rohit Verma",     "rohit.verma@gmail.com",     "9988776655", 2018, "MCA"),
    ("Sneha Joshi",     "sneha.joshi@gmail.com",     "9871234560", 2021, "MCA"),
    ("Karan Mehta",     "karan.mehta@gmail.com",     "9765432100", 2019, "MBA"),
    ("Ananya Gupta",    "ananya.gupta@gmail.com",    "9654321890", 2020, "M.Sc"),
    ("Vikram Singh",    "vikram.singh@gmail.com",    "9543218900", 2018, "MCA"),
    ("Deepika Nair",    "deepika.nair@gmail.com",    "9432109870", 2022, "MCA"),
    ("Amit Tiwari",     "amit.tiwari@gmail.com",     "9321098760", 2017, "MBA"),
    ("Pooja Yadav",     "pooja.yadav@gmail.com",     "9210987650", 2021, "M.Sc"),
    ("Arjun Reddy",     "arjun.reddy@gmail.com",     "9109876540", 2020, "MCA"),
    ("Meera Iyer",      "meera.iyer@gmail.com",      "9098765430", 2019, "MCA"),
    ("Suresh Kumar",    "suresh.kumar@gmail.com",    "8987654320", 2018, "MCA"),
    ("Kavita Desai",    "kavita.desai@gmail.com",    "8876543210", 2022, "MBA"),
    ("Nikhil Jain",     "nikhil.jain@gmail.com",     "8765432100", 2017, "MCA"),
]

employment_data = [
    (1,  "TCS",            "Software Engineer",        "Mumbai",    2019, None),
    (2,  "Infosys",        "Systems Analyst",          "Pune",      2020, None),
    (3,  "Wipro",          "Senior Developer",         "Bangalore", 2018, None),
    (4,  "HCL Technologies","Junior Developer",        "Noida",     2021, None),
    (5,  "Accenture",      "Business Analyst",         "Hyderabad", 2019, None),
    (6,  "Cognizant",      "Data Scientist",           "Chennai",   2020, None),
    (7,  "Tech Mahindra",  "Team Lead",                "Pune",      2018, 2022),
    (7,  "Google",         "Software Engineer III",    "Bangalore", 2022, None),
    (8,  "Amazon",         "SDE-1",                    "Hyderabad", 2022, None),
    (9,  "Microsoft",      "Program Manager",          "Bangalore", 2017, None),
    (10, "Flipkart",       "Data Analyst",             "Bangalore", 2021, None),
    (11, "Zomato",         "Backend Developer",        "Gurgaon",   2020, None),
    (12, "Swiggy",         "Full Stack Developer",     "Bangalore", 2019, None),
    (13, "Oracle",         "Database Administrator",   "Hyderabad", 2018, None),
    (14, "Deloitte",       "Consultant",               "Mumbai",    2022, None),
    (15, "IBM",            "Cloud Architect",          "Bangalore", 2017, None),
    (3,  "Wipro",          "Junior Developer",         "Bangalore", 2018, 2020),
]

mentorship_data = [
    (3,  "Machine Learning & AI",          "Weekends"),
    (7,  "System Design & Architecture",   "Evenings"),
    (9,  "Product Management",             "Weekends"),
    (13, "Database & Cloud Computing",     "Flexible"),
    (15, "DevOps & CI/CD",                "Weekdays"),
    (1,  "Web Development",               "Evenings"),
    (6,  "Data Science & Analytics",      "Weekends"),
]

def seed():
    conn = get_connection()
    cur = conn.cursor()

    # Clear existing data
    cur.execute("TRUNCATE mentorship, employment, alumni RESTART IDENTITY CASCADE")

    # Insert alumni
    for name, email, phone, batch, course in alumni_data:
        cur.execute(
            "INSERT INTO alumni (name, email, phone, batch_year, course) VALUES (%s,%s,%s,%s,%s)",
            (name, email, phone, batch, course)
        )

    # Insert employment
    for alumni_id, company, designation, city, start_yr, end_yr in employment_data:
        cur.execute(
            "INSERT INTO employment (alumni_id, company, designation, city, start_year, end_year) VALUES (%s,%s,%s,%s,%s,%s)",
            (alumni_id, company, designation, city, start_yr, end_yr)
        )

    # Insert mentorship
    for mentor_id, topic, availability in mentorship_data:
        cur.execute(
            "INSERT INTO mentorship (mentor_id, topic, availability) VALUES (%s,%s,%s)",
            (mentor_id, topic, availability)
        )

    conn.commit()
    cur.close()
    conn.close()
    print(f"✅ Seeded {len(alumni_data)} alumni, {len(employment_data)} employment records, {len(mentorship_data)} mentors.")

if __name__ == "__main__":
    seed()

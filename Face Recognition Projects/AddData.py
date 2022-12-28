import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL' : "https://real-time-attendance-56aee-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "21116091":
        {
            "name": "Emily Blunt",
            "major": "Drama",
            "starting_year": 2017,
            "total_attendance": 6,
            "Grade": 'A',
            "year": 5,
            "last_attendace_time": "2022-12-27 20:00:00"
        },
    "20111002":
        {
            "name": "Bill Gates",
            "major": "Computer Science & Engineering",
            "starting_year": 2018,
            "total_attendance": 9,
            "Grade": 'G',
            "year": 4,
            "last_attendace_time": "2022-12-27 20:00:00"
        },
    "20117901":
        {
            "name": "Aditya Kumar Dubey",
            "major": "Electrical Engineering",
            "starting_year": 2020,
            "total_attendance": 13,
            "Grade": 'A',
            "year": 4,
            "last_attendace_time": "2022-12-27 20:00:00"
        },
    "20118901":
        {
            "name": "Elon Musk",
            "major": "Rocket Science",
            "starting_year": 2016,
            "total_attendance": 10,
            "Grade": 'B',
            "year": 6,
            "last_attendace_time": "2022-12-27 20:00:00"
        },
    "20120901":
        {
            "name": "Ashish Dubey",
            "major": "DM/Nephrology",
            "starting_year": 2022,
            "total_attendance": 15,
            "Grade": 'G',
            "year": 1,
            "last_attendace_time": "2022-12-27 20:00:00"
        }
}

for key, value in data.items():
    ref.child(key).set(value)
from src.screen.database.config import supabase
import bcrypt



# hashing
def hash_pass(pswrd):
    return bcrypt.hashpw(pswrd.encode(),bcrypt.gensalt()).decode()    # .encode converts pswrd in binary form/bytes bcoz haspw take input as binary, gensalt is same as ranodm_state -> for particular salt it add random values to the password

# .decode() -> we use it to convert those bytes back into a normal Python string:
        # b'$2b$12$....'       →       '$2b$12$....'
        #    bytes                        string

def check_pass(pswrd,hash_pswrd):
  return bcrypt.checkpw(pswrd.encode(),hash_pswrd.encode())






def teacher_exists(username):
    # check for unique username and returns true or false
    response = supabase.table("teachers").select("username").eq("username",username).execute()  #this will give rows
    return len(response.data) > 0


def create_teacher(username, password, name):

    data = {"username" : username, "password" : hash_pass(password), "name" : name.upper()}   #{column_name:value}
    response = supabase.table("teachers").insert(data).execute()
    return response.data


def teacher_login(username,password):

    response = supabase.table("teachers").select("*").eq("username",username).execute()
    if response.data:   # we get response in array => [{....}]
        teacher = response.data[0]
        if check_pass(password,teacher['password']):
            return teacher
        return None


def get_all_students():

    response = supabase.table("students").select("*").execute()
    return response.data


def create_student(new_name,face_embedding=None,voice_embedding=None):
    data = {'name':new_name, 'face_embedding':face_embedding, 'voice_embedding':voice_embedding}
    response = supabase.table('students').insert(data).execute()
    return response.data


def create_subject(subject_code, name, section, teacher_id):
    data = {'subject_code':subject_code , 'name':name, 'section':section, 'teacher_id':teacher_id}
    response = supabase.table('subjects').insert(data).execute()
    return response.data


def get_teacher_subject(teacher_id):
    response = supabase.table("subjects").select("*, subject_students(count), attendance_logs(attendance_date)").eq('teacher_id',teacher_id).execute()  # join
    subjects = response.data    # response.data are always list of dictionary

    for sub in subjects:
        sub['total_students'] = sub.get("subject_students", [{}])[0].get("count",0) if  sub.get("subject_students") else 0
        attendance = sub.get("attendance_logs",[])
        unique_sessions = len(set(log['attendance_date'] for log in attendance))
        sub['total_classes']= unique_sessions

        sub.pop('subject_students',None)
        sub.pop('attendance_logs',None)

    return subjects    


# eg : how the  subjects = response.data will look like

"""
Here i just added new column to attendance log which is attendance_date, it contains the date when the student joins the class 
and also helps to find the total number of class for a particular teacher - different from the concept of the snapclass

"""

"""
subjects = [
    {
        "subject_id": 1,
        "subject_code": "ML101",
        "name": "Machine Learning",
        "section": "A",
        "teacher_id": 10,

        "subject_students": [
            {
                "count": 3
            }
        ],

        "attendance_logs": [
            {
                "attendance_date": "2026-08-01"
            },
            {
                "attendance_date": "2026-08-01"
            },
            {
                "attendance_date": "2026-08-03"
            },
            {
                "attendance_date": "2026-08-03"
            }
        ]
    },

    {
        "subject_id": 2,
        "subject_code": "PY101",
        "name": "Python",
        "section": "B",
        "teacher_id": 10,

        "subject_students": [
            {
                "count": 2
            }
        ],

        "attendance_logs": [
            {
                "attendance_date": "2026-08-02"
            },
            {
                "attendance_date": "2026-08-02"
            },
            {
                "attendance_date": "2026-08-05"
            }
        ]
    }
]

"""


def enroll_student_to_subject(student_id, subject_id):
    data = {'subject_id':subject_id, 'student_id':student_id}
    response = supabase.table('subject_students').insert(data).execute()
    return response.data


def unenroll_student_to_subject(student_id, subject_id):
    data = {'subject_id':subject_id, 'student_id':student_id}
    response = supabase.table('subject_students').delete().eq('student_id',student_id).eq('subject_id',subject_id).execute()
    return response.data

def get_student_subjects(student_id):
    response = supabase.table("subject_students").select("*, subjects(*)").eq('student_id',student_id).execute()
    return response.data

def get_student_attendance(student_id):
    response = supabase.table("attendance_logs").select("*,subjects(*)").eq('student_id',student_id).execute()
    return response.data

# how the result of get_student_attendance() will look like
"""
{
    student_id: 101,
    subject_id: 5,
    status: "Present",

    subjects: {
        subject_id: 5,
        name: "DAA"
    }
}

"""



def unenroll_student_to_subject(student_id, subject_id):
    data = {'subject_id':subject_id, 'student_id':student_id}
    response = supabase.table('subject_students').delete().eq('student_id',student_id).eq('subject_id',subject_id).execute()
    return response.data



def create_attendance(logs):
    try:
        response = (
            supabase
            .table("attendance_logs")
            .insert(logs)
            .execute()
        )

        return response.data

    except Exception as e:
        if "23505" in str(e):
            return []

        raise

"""
upsert = update + insert.

->on_conflict

    This tells Supabase: "How should I determine whether this attendance record already exists?"

    So it checks this combination: student_id + subject_id + attendance_date

    For example:

    Student 1 + Subject 6 + 2026-09-02

    If that combination already exists, it's considered a conflict.


Normally, upsert would update

        Suppose your database has:

        student_id | subject_id | date       | ispresent
        1          | 6          | 2026-09-02 | TRUE

        And you send:

        student_id | subject_id | date       | ispresent
        1          | 6          | 2026-09-02 | FALSE

        Normal upsert behavior is essentially:

        Already exists?
            ↓
            YES
            ↓
        UPDATE the existing row

        So it could change TRUE → FALSE.

        You don't want that for attendance.



-> That's why you have ignore_duplicates=True

    This tells Supabase: If there is already a record with that unique combination, don't update it and don't insert another one. Just ignore that record.
"""



def get_attendance_for_teacher(teacher_id):
    response = (
        supabase
        .table('attendance_logs')
        .select("*, subjects!inner(*)")
        .eq('subjects.teacher_id', teacher_id)
        .execute()
    )

    data = response.data

    unique_dates = set(
        row['attendance_date']
        for row in data
        if row.get('attendance_date')
    )

    total_classes = len(unique_dates)

    return data, total_classes
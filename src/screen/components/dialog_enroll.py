import streamlit as st
from src.screen.database.db import create_subject
from src.screen.database.config import supabase
from src.screen.database.db import enroll_student_to_subject


@st.dialog("ENROLL IN SUBJECT")
def enroll_dialog():
    st.space()
    st.write("Enter the subject code provided by teacher to enroll")
    join_code = st.text_input("Subject_code",placeholder="Eg. CS101")

    if st.button("Enroll Now",type='primary',width='stretch'):
        if join_code:
            response = supabase.table('subjects').select('subject_id', 'subject_code').eq('subject_code',join_code.upper()).execute()
            if response.data:
                subject = response.data[0]
                student_id = st.session_state.student_data['student_id']

                check = supabase.table("subject_students").select("*").eq('subject_id',subject['subject_id']).eq('student_id',student_id).execute()

                if check.data:
                    st.warning("Your are already enrolled in this program")

                else:
                    enroll_student_to_subject(student_id, subject['subject_id'])
                    st.success('Successfully Enrolled!')
                    import time
                    time.sleep(1)
                    st.rerun()    

            else:
                st.warning("Enter valid Code!")

        else:
            st.warning("Please enter a subject code")    
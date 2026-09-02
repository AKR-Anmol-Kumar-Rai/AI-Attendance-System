import streamlit as st
from src.screen.database.db import create_subject
from src.screen.database.config import supabase
from src.screen.database.db import enroll_student_to_subject
import time


@st.dialog("QUICK ENROLLMENT")
def auto_enroll_dialog(subject_code):
    st.space()
    student_id = st.session_state.student_data["student_id"]


    response = supabase.table("subjects").select('subject_id','name').eq('subject_code',subject_code).execute()
    if not response.data:
        st.error('Subject Code not found!')
        if st.button("Close"):
            st.query_params.clear()
            st.rerun()

        return
    subject = response.data[0]
 
    check = supabase.table('subject_students').select("*").eq('subject_id',subject['subject_id']).eq('student_id',student_id).execute()
    if check.data:
        if st.info("You are already enrolled"):
            if st.button("Got it!"):
                st.query_params.clear()
                st.rerun()
            return     

    st.markdown(f"Would you lie to enroll in **{subject['name']}?**")            

    col1 ,col2 = st.columns(2)

    with col1:
        if st.button("No Thanks"):
            st.query_params.clear()
            st.rerun()

    with col2:
        if st.button("Yes enroll now!",type='primary',width='stretch'):
            enroll_student_to_subject(student_id,subject['subject_id'])
            st.success("Joined Successfully!")
            st.query_params.clear()
            time.sleep(2)
            st.rerun()
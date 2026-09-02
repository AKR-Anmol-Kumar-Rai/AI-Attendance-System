import streamlit as st
from src.screen.database.db import create_subject
from src.screen.database.config import supabase
from src.screen.database.db import enroll_student_to_subject
import time
from src.screen.database.db import create_attendance

def show_attendance_result(df,logs):
        st.write("Please review attendance before confirming")
        st.dataframe(df,hide_index=True,width='stretch')  # earlier using width='stretch'

        col1 , col2 = st.columns(2)

        with col1:
            if st.button("Discard",width='stretch'):
                st.session_state.voice_attendance_results = None
                st.session_state.attendance_images = []
                st.rerun()

        with col2:
            if st.button("Confirm & Save",width='stretch',type='primary'):
                try:
                    result = create_attendance(logs)
                    if result:
                        st.toast("Attendance taken")
                        st.session_state.attendance_images = []
                        st.session_state.voice_attendance_results = None
                        st.rerun()
                    else:
                        st.warning("Attendance Already Marked!")
                except Exception as e:
                    st.error(f"Sync failed: {e}")

@st.dialog("ATTENDANCE REPORTS")
def attendance_result_dialog(df,logs):
    st.space()
    show_attendance_result(df,logs)
      
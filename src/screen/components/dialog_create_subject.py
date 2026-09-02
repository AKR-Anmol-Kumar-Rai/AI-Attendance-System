import streamlit as st
from src.screen.database.db import create_subject

@st.dialog('CREATE NEW SUBJECT')
def create_subject_dialog(teacher_id):
    st.space()
    st.write("Enter the details of subject")
    sub_id= st.text_input("Subject Code",placeholder="CS101")
    sub_name= st.text_input("Subject Name",placeholder='Introduction to DAA')
    sub_section= st.text_input("Section",placeholder='A')


    if st.button("Create Subjects Now", type='primary',width='stretch'):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(sub_id.upper(),sub_name.title(),sub_section.upper(),teacher_id)
                st.toast("Subject Created Successfully!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")

        else:
            st.warning("Please fill all the fields")         



import streamlit as st
from src.screen.components.header import header_dashboard
from src.screen.ui.base_layout import style_base_layout ,style_background_home, style_background_dashboard
from src.screen.components.footer import footer_dashboard
from PIL import Image
import numpy as np
from src.screen.pipelines.face_pipeline import predict_attendance, train_classifier, get_face_embedings
from src.screen.database.db import get_all_students, create_student, get_student_attendance, get_student_subjects
from src.screen.pipelines.voice_pipeline import get_voice_embeddings
import time
from src.screen.components.dialog_enroll import enroll_dialog
from src.screen.database.db import  unenroll_student_to_subject
from src.screen.components.subject_card import subject_card


def student_dashboard():

    student_data = st.session_state["student_data"]
    student_id = student_data['student_id']
    
    col1, col2 = st.columns(2,vertical_alignment='center',gap='xxlarge')

    with col1:
      header_dashboard()

    with col2:
       st.subheader(f"""WELCOME, {student_data['name']}""")
       if st.button("Logout",type='secondary',key='loginbackbtn',shortcut="control+backspace"):
          st.session_state["is_logged_in"]=False  
          del st.session_state.student_data
          st.rerun()

    c1, c2 = st.columns(2)

    with c1:
        st.header("YOUR ENROLLED SUBJECTS")

    with c2:
        st.markdown("""
                <style>
                          div[data-testid="stButton"] {
                           transform: translateY(-5px);
                                 }
                </style>
               """, unsafe_allow_html=True)
        if st.button("Enroll in Subject",width='stretch',type = 'primary'):
            enroll_dialog()


    with st.spinner("Loading your enrolled subjects.."):
        subjects = get_student_subjects(student_id)
        logs = get_student_attendance(student_id)

    #display logic 
    stats_map = {}
    for log in logs:
       sid = log['subject_id']

       if sid not in stats_map:
          stats_map[sid] = {'total':0, 'attendance':0}

       stats_map[sid]['total'] += 1

       if log.get('ispresent'):
          stats_map[sid]['attendance'] +=1

    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):   # i is index of the sub_node
       sub = sub_node['subjects']
       sid = sub['subject_id']


       stats = stats_map.get(sid,{'total':0, 'attendance':0})   # if sid not exist then {'total':0, 'attendance':0} will be displayed
       def unenroll_btn():
           if st.button('Unenroll from this course',type='tertiary',width='stretch',key=f"unenroll_{sid}"):
                  unenroll_student_to_subject(student_id, sid)
                  st.toast(f"Unenrolled from this {sub['name']} succesfully")
                  st.rerun()

       with cols[i % 2]:
          subject_card(
             name = sub['name'],
             code = sub['subject_code'],
             section = sub['section'],
             stats = [
                ('🗓️','Total',stats['total']),
                ('✅','Attendance',stats['attendance'])
             ],
             footer_callback= unenroll_btn
          )           


    st.divider()



    st.space()
    footer_dashboard()





def student_screen():

    style_background_dashboard()
    style_base_layout()



    if 'student_data' in st.session_state:
         student_dashboard()
         return

    c1 , c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')
    
    with c1:
        header_dashboard()
    
    with c2:
        # overwriting the position of the button using css
        st.markdown("""
            <style>
                div[data-testid="stButton"] {
                transform: translateY(-20px);
                }
            </style>
            """, unsafe_allow_html=True)
        if st.button('Go back to Home',type='secondary',width='content',shortcut="control+backspace"):
                 st.session_state['login_type']=None
                 st.rerun()  #whenever state changes make rerun


    st.header("LOGIN USING FACEID",text_alignment='center')


    # (overwritting) hepls to fix the size of the camera input
    st.markdown("""
        <style>

            # /* Remove page scrolling */
            # html, body, [data-testid="stAppViewContainer"] {
            # overflow: hidden !important;
            # }

            /* Center camera */
            div[data-testid="stCameraInput"] {
             width: 650px !important;
             margin:auto !important;
            }

        </style>
        """, unsafe_allow_html=True)

    show_registration = False
    photo_source = st.camera_input("Position Your face to the center")
    if photo_source:
         
        img = np.array(Image.open(photo_source))
        with st.spinner("AI is scanning.."):
            detected, all_ids, num_faces =  predict_attendance(img)

            if num_faces == 0:
                st.warning("Face not Found! ")

            elif num_faces > 1:
                 st.warning("Multiple faces found! ")

            else:
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()

                    student = next((s for s in all_students if s['student_id'] == student_id),None)

                    if student:
                        st.session_state.is_logged_in = True
                        st.session_state.user_role = 'student'
                        st.session_state.student_data = student
                        st.toast(f"Welcome Back {student['name']}👋")
                        import time
                        time.sleep(1)
                        st.rerun()

                else:
                    st.info("Face not recognized You might be a new student!")
                    show_registration = True

        if show_registration:
             with st.container(border=True):
                st.header('REGISTER NEW PROFILE')
                new_name = st.text_input('Enter your name',placeholder="e.g Anmol kumar rai")

                st.header('Optional : Voice Enrollement')
                st.info("Enroll for voice only attendance")

                audio_data = None

                try:
                    audio_data = st.audio_input("Record a short phrase like i am present, My name is Anmol")
                except Exception:
                    st.error("Audio data failed")

                    
                if st.button('Create Account',type='primary'):
                    if new_name:
                          with st.spinner("Creating Profile...."):
                             img1 = np.array(Image.open(photo_source))
                             encodings = get_face_embedings(img1)
                             if encodings:
                                face_emb = encodings[0].tolist()
       
                                voice_emb = None
                                if audio_data:
                                  voice_emb = get_voice_embeddings(audio_data.read())   #.read convert audio data into binary/bytes form
                                 
                                response_data = create_student(new_name,face_embedding=face_emb, voice_embedding=voice_emb)
       
                                if response_data:
                                   train_classifier()
                                   st.session_state.is_logged_in = True
                                   st.session_state.user_role = 'student'
                                   st.session_state.student_data = response_data[0]
                                   st.toast(f"profile created! Hi {new_name}")
                                   time.sleep(2)
                                   st.rerun()
       
                             else:
                                st.error("Could'nt capture ypur facial features for registration")      
       
                    else:
                          st.warning("Please enter your name")             
                       



    st.space()
    footer_dashboard()
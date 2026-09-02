import streamlit as st
from src.screen.components.header import header_dashboard
from src.screen.ui.base_layout import style_base_layout ,style_background_home, style_background_dashboard
from src.screen.components.footer import footer_dashboard
from src.screen.database.db import create_teacher,teacher_exists,teacher_login, get_teacher_subject,get_attendance_for_teacher
from src.screen.components.dialog_create_subject import create_subject_dialog
from src.screen.components.share_subject_dialog import share_subject_dialog
from src.screen.components.subject_card import subject_card
from src.screen.components.dialog_add_photos import add_photos_dialog
import numpy as np
from src.screen.pipelines.face_pipeline import predict_attendance
from src.screen.database.config import supabase
import pandas as pd
from src.screen.components.dialog_attendance_to_result import attendance_result_dialog
from datetime import date, datetime
from src.screen.components.dialog_voice_attendance import voice_attendance_dialog

def teacher_screen():

    style_background_dashboard()
    style_base_layout()

    if 'teacher_data' in st.session_state:
         teacher_dashboard()


    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type == 'login':
         
         teacher_screen_login()

    elif st.session_state.teacher_login_type =='register':

        teacher_screen_register()






def teacher_dashboard():


     teacher_data = st.session_state['teacher_data']

     c1 , c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')
         
     with c1:
          header_dashboard()
         
     with c2:
          st.subheader(f"""WELCOME, {teacher_data['name']}""")
          # overwriting the position of the button using css
          st.markdown("""
                <style>
                          div[data-testid="stButton"] {
                           transform: translateY(-20px);
                                 }
                </style>
               """, unsafe_allow_html=True)
          if st.button('Logout',type='secondary',width='content',shortcut="control+backspace"):
               st.session_state['is_logged_in']=False
               del st.session_state.teacher_data
               st.rerun()  #whenever state changes make rerun


     st.space()
     st.space()

     tab1, tab2, tab3 = st.columns(3)

     if 'current_teacher_tab' not in st.session_state:   #this session state will handle teacher tabs
        st.session_state.current_teacher_tab='take_attendance'

     with tab1:
          type1 = 'primary' if  st.session_state.current_teacher_tab =='take_attendance' else 'tertiary'
          if st.button('Take Attendance',width='stretch',type=type1,icon=':material/ar_on_you:'):
           st.session_state.current_teacher_tab='take_attendance'
           st.rerun()

     with tab2:
          type2 = 'primary' if st.session_state.current_teacher_tab =='manage_subjects' else 'tertiary'
          if st.button('Manage Subjects',width='stretch',type=type2,icon=':material/book_ribbon:'):
           st.session_state.current_teacher_tab='manage_subjects'
           st.rerun()

     with tab3:
          type3 = 'primary' if st.session_state.current_teacher_tab =='attendance_records' else 'tertiary'
          if st.button('Attendance Records',width='stretch',type=type3,icon=':material/cards_stack:'):
           st.session_state.current_teacher_tab='attendance_records'
           st.rerun()

     st.divider()

     if st.session_state.current_teacher_tab == 'take_attendance':
        teacher_tab_take_attendance()
     if st.session_state.current_teacher_tab == 'manage_subjects':
        teacher_tab_manage_subjects()
     if st.session_state.current_teacher_tab == 'attendance_records':
        teacher_tab_attendance_records()
     footer_dashboard()




def teacher_tab_take_attendance():
    teacher_id = st.session_state.teacher_data['teacher_id']
    st.header('TAKE AI ATTENDANCE')

    if 'attendance_images' not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subject(teacher_id)

    if not subjects:
        st.warning("You have'nt created any subject yet! Please create one to begin!")

    subject_options = {f"{s['subject_code']} - {s['name']}": s['subject_id'] for s in subjects}

    select_subject_label = st.selectbox('Select Subject',options=list(subject_options.keys()))  
    st.space()
    if st.button("Add Photos",type='primary',icon=':material/photo_prints:',width='content'):
            add_photos_dialog()

    selected_subject_id = subject_options[select_subject_label]

    st.space()
    
    st.divider()

    if st.session_state.attendance_images:
        st.header("ADDED PHOTOS")
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.attendance_images):
            with gallery_cols[idx % 4]:
                st.image(img,width='stretch',caption=f'Photo {idx +1}')

    has_photo = bool(st.session_state.attendance_images)
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("Clear all photos",type='tertiary',width='stretch',icon=":material/delete:",disabled= not has_photo):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        if st.button("Run Face Analysis",type='secondary',width='stretch',disabled= not has_photo):
            with st.spinner("Deep scanning classroom photos....."):

                all_detected_ids = {}

                for idx , img in enumerate(st.session_state.attendance_images):
                    img_np = np.array(img.convert('RGB'))  # .convert helps model to process images more smoothy processing
                    detected, _, _ = predict_attendance(img_np)   # detected_students ->{1: True, 3: True}
                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)

                            all_detected_ids.setdefault(student_id,[]).append(f"Photo {idx+1}")    #all_detected_ids.setdefault(student_id,[]) -> "If key 3 doesn't exist, create it with an empty list []. If it already exists, give me its existing list."
                            """
                            {
                              3: ["Photo 1"]
                            }
                                   """
                enroll_response = supabase.table("subject_students").select("*, students(*)").eq('subject_id',selected_subject_id).execute()
                enroll_students = enroll_response.data
               #  enroll students
                """
               [
                    {
                         "subject_id": 102,
                         "student_id": 1,
                         "students": {
                              "student_id": 1,
                              "name": "Anmol",
                              "face_embedding": [...],
                              "voice_embedding": [...]
                         }
                    },
                    {
                         "subject_id": 102,
                         "student_id": 3,
                         "students": {
                              "student_id": 3,
                              "name": "Rahul",
                              "face_embedding": [...],
                              "voice_embedding": [...]
                         }
                    }
                    ]
                    """               

                if not enroll_students:
                    st.warning("No students enrolled in this course") 
                    return           

                else:
                    results , attendance_to_log = [], []
                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")   

                    for node in enroll_students:
                        student = node['students']
                        source = all_detected_ids.get(int(student['student_id']),[])   # student aya toh hai but konsi  photo se aya hai if not in any photo then []

                        is_present = len(source)>0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ", ".join(source) if is_present else "-",
                            "Status": "✅Present" if is_present else "❌Absent"
                        })

                        today = date.today().strftime("%Y-%m-%d")

                        attendance_to_log.append({
                            'timestamp' : current_timestamp,
                            'student_id': student['student_id'],
                            'subject_id': selected_subject_id,
                            "ispresent" : bool(is_present),
                            'attendance_date' : today
               
                        })
                attendance_result_dialog(pd.DataFrame(results), attendance_to_log)

    with c3:
        if st.button("Use Voice Attendance",type='primary',width='stretch',icon=':material/mic:'):
            voice_attendance_dialog(selected_subject_id)




            



def teacher_tab_manage_subjects():
    
    teacher_id = st.session_state.teacher_data['teacher_id']

    col1,col2= st.columns(2)

    with col1:
        st.header("MANAGE SUBJECTS",width='stretch')

    with col2:
       #   adjusting the position of the button thirugh overwriting
        st.markdown("""
               <style>
                    div[data-testid="stButton"] {
                    transform: translateY(-10px);
                                         }
               </style>
               """, unsafe_allow_html=True)
        if st.button('Create New Subjects',width='stretch'):
            create_subject_dialog(teacher_id)



    subjects = get_teacher_subject(teacher_id)
    if subjects:
        for sub in subjects:
            stats = [
                ("👥", "Students", sub["total_students"]),
                ("⏱️", "Classes", sub["total_classes"])
            ]

            def share_btn():
               if st.button(f"Share Code: {sub['name']}", key=f"share_{sub['subject_code']}",icon=":material/share:"):
                    share_subject_dialog(sub['name'],sub['subject_code'])

               st.space()

            subject_card(
               name = sub['name'],
               code = sub['subject_code'],
               section = sub['section'],
               stats =stats,
               footer_callback = share_btn)        
    else:
        st.info("No Subject Found! Create One Above")    




def teacher_tab_attendance_records():
    st.header('ATTENDANCE RECORDS')

    teacher_id = st.session_state.teacher_data.get('teacher_id')
    
    records, total_classes = get_attendance_for_teacher(teacher_id)
    if not records:
        return
    
    data = []

    for r in records:
        ts = r.get('timestamp')

        data.append({
            'ts_group': ts.split(".")[0] if ts else None,   # "2026-09-02T14:30:25.123456" -> ["2026-09-02T14:30:25", "123456"]  in short removing milisecond from the timestamp
            'time': datetime.fromisoformat(ts).strftime("%Y-%m-%d %I:%M %p") if ts else "N'A",   # datetime.fromisoformat(ts) -> converts : 2026-09-02T14:30:25.123456 from a string into a Python datetime object.
            'subjects': r['subjects']['name'],
            'subject_code':r['subjects']['subject_code'],
            'is_present': bool(r.get("ispresent",False))
        })

    df = pd.DataFrame(data)


    summary = (
        df.groupby(['ts_group','time','subjects','subject_code'])
        .agg(
            present_count = ('is_present','sum'),
            total_count = ('is_present','count')
        ).reset_index()
    ) 

    summary['Attendance Stats'] = (
        "✅" + summary['present_count'].astype(str) +  '/'
        + summary['total_count'].astype(str)+ 'students' 
    )
    

    display_df = (
        summary.sort_values(by='ts_group', ascending=False)
        [['time', 'subjects', 'subject_code', 'Attendance Stats']]  # selecting the column that we want to display
    )

    st.dataframe(display_df,width='stretch',hide_index=True)











def login_teacher(teacher_username, teacher_pass):
    if not teacher_username or not teacher_pass:
        return False
    
    teacher = teacher_login(teacher_username, teacher_pass)

    if teacher:
        st.session_state["user_role"]="teacher"
        st.session_state["is_logged_in"]= True
        st.session_state["teacher_data"]=teacher
        st.rerun()
        return True
    return False

def teacher_screen_login():
        
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

        st.space()
        st.header("LOGIN USING PASSWORD",text_alignment='center')
        st.space()

        teacher_username = st.text_input('Enter username',placeholder='Anmol Kumar Rai')
        teacher_password = st.text_input("Enter password",type='password',placeholder='Enter password')

        st.space()
  
        st.divider()

        btn1, btn2 = st.columns(2,gap='medium')
        with btn1:
             if st.button('Login',icon=':material/passkey:',width='stretch',shortcut='control+enter'):
                  if login_teacher(teacher_username, teacher_password):
                     st.toast("welcome back",icon="👋")
                     import time
                     time.sleep(2)
                  else:
                    st.error("invalid username or password!",width='stretch')

        with btn2:
             if st.button("Register Instead",icon=':material/passkey:',width='stretch',type='primary'):
                  st.session_state.teacher_login_type = 'register'
        st.space()
        st.space()
        st.space()
        footer_dashboard()






def register_teacher(teacher_username,teacher_name,teacher_password,teacher_password_confirm):

     if not teacher_username or not teacher_name or not teacher_password:
          return False, "All Fields are required!"

     if teacher_exists(teacher_username):
          return False, "Username already taken!"

     if teacher_password != teacher_password_confirm:
          return False, "Password does'nt match!"

     try:
          create_teacher(teacher_username,teacher_password,teacher_name)
          return True, "Successfully Created! Login Now"

     except Exception as e:
          return False, "Unexpexected Error"


def teacher_screen_register():
        
        c1 , c2 = st.columns(2,vertical_alignment='center',gap='xxlarge')
    
        with c1:
            header_dashboard()
    
        with c2:
            if st.button('Go back to Home',type='secondary',width='content',key='loginbackbtn',shortcut="control+backspace"):
                 st.session_state['login_type']=None
                 st.rerun()  #whenever state changes make rerun


        st.space()
        st.header("REGISTER YOUR TEACHER PROFILE",text_alignment='center')

    
        teacher_username = st.text_input('Enter username',placeholder='Anmol@Rai1234')
        teacher_name = st.text_input('Enter name',placeholder='Anmol Kumar Rai')
        teacher_password = st.text_input("Enter password",type='password',placeholder='Enter password')
        teacher_password_confirm = st.text_input("Confirm password",type='password',placeholder='Confirm password')
  
        st.divider()

        btn1, btn2 = st.columns(2,gap='medium')
        with btn1:
             if st.button('Register Now',icon=':material/passkey:',width='stretch',shortcut='control+enter'):
                  success, message = register_teacher(teacher_username,teacher_name,teacher_password,teacher_password_confirm)
                  if success:
                       st.success(message)
                       import time
                       time.sleep(2)
                       st.session_state['teacher_login_type'] = 'login'
                       st.rerun()

                  else:
                       st.error(message)

        with btn2:
             if st.button("Login Instead",icon=':material/passkey:',width='stretch',type='primary'):
                  st.session_state.teacher_login_type = 'login'

        st.space()
        footer_dashboard()     

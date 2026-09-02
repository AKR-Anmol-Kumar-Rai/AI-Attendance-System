import streamlit as st
from src.screen.database.db import create_subject
from src.screen.database.config import supabase
from src.screen.database.db import enroll_student_to_subject
import time
from PIL import Image


@st.dialog("CAPTURE OR UPLOAD PHOTOS")
def add_photos_dialog():
   st.space()
   st.write("Add classroom photos to scan for attendance")

   if 'photo_tab' not in st.session_state:
      st.session_state.photo_tab = 'camera'

   t1 , t2 = st.columns(2)

   with t1:
      type_camera = 'primary' if st.session_state.photo_tab == 'camera' else 'tertiary'
      if st.button("Camera",type=type_camera,width='stretch'):
         st.session_state.photo_tab = 'camera'

   with t2:
      type_upload = 'primary' if st.session_state.photo_tab == 'upload' else 'tertiary'
      if st.button("Upload photos",type=type_upload,width='stretch'):
         st.session_state.photo_tab = 'upload'


   if st.session_state.photo_tab == 'camera':
      cam_photo = st.camera_input("Take Snapsot",key = "dialog_cam")
      if cam_photo:
         st.session_state.attendance_images.append(Image.open(cam_photo))
         st.toast("Photo Captured")
         st.rerun()
 

   if st.session_state.photo_tab == 'upload':
      uploaded_files = st.file_uploader("Choose image files",type=['jpg','png','jpeg'], accept_multiple_files=True,key = 'dialog_upload')

      if uploaded_files:
         for f in uploaded_files:
            st.session_state.attendance_images.append(Image.open(f))
         st.toast('Photos Uploaded Successfully') 

   st.divider()         
   if st.button("Done", type='primary',width='stretch'):
      st.rerun()
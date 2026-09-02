import dlib
import numpy
import face_recognition_models
from sklearn.svm import SVC
import streamlit as st
import numpy as np

from src.screen.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    face_detector = dlib.get_frontal_face_detector()

    shape_detector = dlib.shape_predictor(
        face_recognition_models.pose_predictor_five_point_model_location()
    )

    face_recognition = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )


    return face_detector, shape_detector, face_recognition


def get_face_embedings(image_np):
    face_detector, shape_detector, face_recognition = load_dlib_models()

    faces = face_detector(image_np,1)  # here 1 means that the images would be processed 1 times to recognize faces

    encodings = []

    for face in faces:
        shape = shape_detector(image_np, face)  # 68-landmarks -> [(x1,y1), (x2,y2), ... (x68,y68)]
        face_descriptor = face_recognition.compute_face_descriptor(image_np, shape, 1)  #128 numbers or embeddings -> [0.12, -0.08, 0.34, 0.51, ..., -0.21]

        encodings.append(np.array(face_descriptor))

    return encodings


# training our classifier
@st.cache_resource
def get_trained_model():
    X=[]
    y=[]
    
    student_db = get_all_students()

    for student in student_db:
        embeddings = student.get("face_embedding")
        if embeddings:
            X.append(np.array(embeddings))
            y.append(student.get("student_id"))

    if len(X)==0:
        return 0

    classifier = SVC(kernel='linear', probability=True,class_weight='balanced')

    try:
        classifier.fit(X,y)
    except ValueError:
        pass  

    return {"clf": classifier,'X':X,'y':y}  



# retraining function.
def train_classifier():
    st.cache_resource.clear()

    model_data = get_trained_model()
    return bool(model_data)



def predict_attendance(class_image_np):
    encodings = get_face_embedings(class_image_np)

    detected_students = {}

    model_data = get_trained_model()

    if not model_data:
        return detected_students , [], len(encodings)   #detected students embedding, students list, no. of students
    
    clf = model_data['clf']
    X_train = model_data['X']
    y_train = model_data['y']


    all_students = sorted(list(set(y_train)))

    for encoding in encodings:
        if(len(all_students)>=2):
            predicted_id = int(clf.predict([encoding])[0])

        else:
            predicted_id = int(all_students[0])    

        student_embeddings = X_train[y_train.index(predicted_id)]

        best_match_score  = np.linalg.norm(student_embeddings - encoding) #This calculates the Euclidean distance between the two embeddings.

        resembler_threshold = 0.6

        if best_match_score <= resembler_threshold:
            detected_students[predicted_id]  = True

    return detected_students, all_students, len(encodings)        

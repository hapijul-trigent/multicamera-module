import cv2
import streamlit as st
import time
from pathlib import Path
from PIL import Image
import os

st.title("Webcam Live Feed")
run = st.checkbox('Run')
camera1 = cv2.VideoCapture(0)
camera2 = cv2.VideoCapture(1)
camera3 = cv2.VideoCapture(2)

camera1.set(cv2.CAP_PROP_FPS, 30)
camera2.set(cv2.CAP_PROP_FPS, 30)
camera3.set(cv2.CAP_PROP_FPS, 30)

col1, col2, col3 = st.columns(3)
with col1:
    st.subheader("Front")    
    FRAME_WINDOW1 = st.image([])
with col2:
    st.subheader("Left")    
    FRAME_WINDOW2 = st.image([])
with col3:
    st.subheader("Right")
    FRAME_WINDOW3 = st.image([])
clicked = st.button("Capture & Save")
while run:
    ret1, frame1 = camera1.read()
    ret2, frame2 = camera2.read()
    ret3, frame3 = camera3.read()

    if ret1:
        frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW1.image(frame1)
    if ret2:
        frame2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW2.image(frame2)
    if ret3:
        frame3 = cv2.cvtColor(frame3, cv2.COLOR_BGR2RGB)
        FRAME_WINDOW3.image(frame3)
    if clicked:
        cv2.imwrite("captured_images/camera1_image.jpg", frame1)
        cv2.imwrite("captured_images/camera2_image.jpg", frame2)
        cv2.imwrite("captured_images/camera3_image.jpg", frame3)
        break    
else:
    camera1.release()
    camera2.release()
    camera3.release()

def display_images_in_grid(folder="captured_images"):
    """Display all images in the folder as a grid."""
    if not os.path.exists(folder):
        st.write("No images to display yet.")
        return

    image_files = list(Path(folder).glob("*.jpg"))
    image_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
    image_files = image_files[:3]
    if not image_files:
        st.write("No images to display yet.")
        return

    cols = st.columns(3)  # Adjust the number of columns for the grid
    for idx, image_file in enumerate(image_files):
        with cols[idx % 3]:
            img = Image.open(image_file)
            st.image(img, caption=image_file.name, use_column_width=True)
st.success("Captured 3 images successfully!")
display_images_in_grid()

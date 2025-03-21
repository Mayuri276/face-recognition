import face_recognition
import numpy as np
import mysql.connector

def add_person(name, image_path):
    # Load image and compute face encoding
    image = face_recognition.load_image_file("C:/Users/Mayuri Jamdar/Downloads/img rec/img rec/images.jpg")
    face_encoding = face_recognition.face_encodings(image)[0]
    encoding_bytes = face_encoding.tobytes()

    # Connect to MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="face_recognition_db"
    )
    cursor = conn.cursor()

    # Insert into the database
    cursor.execute(
        "INSERT INTO people (name, encoding) VALUES (%s, %s)",
        (name, encoding_bytes)
    )
    conn.commit()
    conn.close()
    print(f"✅ Added {name} to the database!")

# Example: Add people
add_person("sunita williams", "images.jpg")                     

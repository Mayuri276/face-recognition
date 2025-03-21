from flask import Flask, request, jsonify
import face_recognition
import numpy as np
import mysql.connector

app = Flask(__name__)

# Root route for testing
@app.route('/')
def home():
    return "Face Recognition API is running!"

# Load data from MySQL
def load_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="face_recognition_db"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT name, encoding FROM people")
    rows = cursor.fetchall()
    conn.close()

    database_names = [row[0] for row in rows]
    database_encodings = [np.frombuffer(row[1], dtype=np.float64) for row in rows]
    return database_names, database_encodings

# Recognize faces (supports both GET and POST)
@app.route('/recognize', methods=['GET', 'POST'])
def recognize():
    if request.method == 'GET':
        return """
        <h1>Upload an Image</h1>
        <form action="/recognize" method="post" enctype="multipart/form-data">
            <input type="file" name="image">
            <input type="submit" value="Upload">
        </form>
        """
    elif request.method == 'POST':
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        file = request.files['image']
        image = face_recognition.load_image_file(file)
        uploaded_encodings = face_recognition.face_encodings(image)

        if not uploaded_encodings:
            return jsonify({"error": "No faces detected"}), 400

        database_names, database_encodings = load_database()
        results = []

        for uploaded_encoding in uploaded_encodings:
            matches = face_recognition.compare_faces(database_encodings, uploaded_encoding)
            face_distances = face_recognition.face_distance(database_encodings, uploaded_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                results.append({"name": database_names[best_match_index]})
            else:
                results.append({"name": "Unknown"})

        return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
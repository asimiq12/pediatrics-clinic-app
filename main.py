from flask import Flask, request, jsonify, render_template, redirect
from datetime import datetime

app = Flask(__name__)

# Mock database
appointments = []
doctors = ["Dr. Chowhan", "Nurse Practitioner A", "Nurse Practitioner B"]

@app.route('/')
def home():
    return "Welcome to Pediatrics of Manassas Appointment API"

@app.route('/book', methods=['POST'])
def book_appointment():
    data = request.get_json()
    required_fields = ["patient_name", "type", "provider", "date", "time"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required appointment fields"}), 400

    appointment = {
        "id": len(appointments) + 1,
        "patient_name": data["patient_name"],
        "type": data["type"],
        "provider": data["provider"],
        "date": data["date"],
        "time": data["time"]
    }
    appointments.append(appointment)
    return jsonify({"message": "Appointment booked successfully", "appointment": appointment}), 200

@app.route('/appointments', methods=['GET'])
def get_appointments():
    return jsonify(appointments)

@app.route('/doctors', methods=['GET'])
def get_doctors():
    return jsonify(doctors)

@app.route('/book-form', methods=['GET'])
def book_form():
    return render_template("index.html")

@app.route('/book-form', methods=['POST'])
def book_form_submit():
    data = {
        "patient_name": request.form["patient_name"],
        "type": request.form["type"],
        "provider": request.form["provider"],
        "date": request.form["date"],
        "time": request.form["time"]
    }
    appointments.append(data)
    return "Appointment booked successfully!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)

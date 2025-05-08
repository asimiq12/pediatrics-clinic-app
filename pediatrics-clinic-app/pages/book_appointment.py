import streamlit as st
import datetime
import json

# File paths
SHIFT_FILE = "shift_calendar.json"
BOOKINGS_FILE = "appointment_slots.json"
STAFF_FILE = "staff_data.json"

# Utility functions
def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

# Load data
shift_data = load_json(SHIFT_FILE)
bookings = load_json(BOOKINGS_FILE)
staff_data = load_json(STAFF_FILE)

# Get all active doctors
active_doctors = [
    f"{emp['first_name']} {emp['last_name']}"
    for emp in staff_data
    if emp.get("role") == "doctor" and emp.get("active")
]

# Duration per type
durations = {"Checkup": 30, "Sick": 15, "Consultation": 30}

# Clinic hours
weekday_start = datetime.time(9, 0)
weekday_end = datetime.time(16, 0)
sat_checkup_slots = [datetime.time(8, 30), datetime.time(9, 0), datetime.time(9, 30), datetime.time(10, 0)]
sat_sick_start = datetime.time(10, 30)
sat_sick_end = datetime.time(12, 15)

# Page layout
st.title("📅 Book an Appointment")

# Patient info
name = st.text_input("Full Name")
phone = st.text_input("Phone Number")
email = st.text_input("Email Address")

appt_type = st.selectbox("Appointment Type", ["Checkup", "Sick", "Consultation"])

# Appointment date
today = datetime.date.today()
max_date = today + datetime.timedelta(days=30)
min_date = today if appt_type == "Sick" else today + datetime.timedelta(days=1)
appt_date = st.date_input("Select Date", min_value=min_date, max_value=max_date)
date_str = appt_date.isoformat()

# Get doctors working on selected day
working_doctors = shift_data.get(date_str, [])

if not working_doctors:
    st.warning("No doctors assigned for this date. Please choose another day.")
    st.stop()

# For checkups: allow choice
if appt_type == "Checkup":
    doctor = st.selectbox("Choose Doctor", [doc for doc in working_doctors if doc in active_doctors])
else:
    doctor = working_doctors[0]  # auto-assign first

# Time slot logic
def generate_slots(start_time, end_time, interval_min):
    slots = []
    current = datetime.datetime.combine(datetime.date.today(), start_time)
    end = datetime.datetime.combine(datetime.date.today(), end_time)
    while current + datetime.timedelta(minutes=interval_min) <= end:
        slots.append(current.time().strftime("%I:%M %p"))
        current += datetime.timedelta(minutes=interval_min)
    return slots

available_slots = []

if appt_date.weekday() == 5:  # Saturday
    if appt_type == "Checkup":
        available_slots = [t.strftime("%I:%M %p") for t in sat_checkup_slots]
    elif appt_type == "Sick":
        if appt_date != today:
            st.warning("Saturday sick visits can only be booked same-day.")
            st.stop()
        available_slots = generate_slots(sat_sick_start, sat_sick_end, durations[appt_type])
else:
    available_slots = generate_slots(weekday_start, weekday_end, durations[appt_type])

# Remove already booked slots
booked_for_day = bookings.get(date_str, {}).get(doctor, [])
free_slots = [s for s in available_slots if s not in booked_for_day]

# Show slot choices
if not free_slots:
    st.error("No available slots for this doctor on this day.")
    st.stop()

time_slot = st.selectbox("Select Time Slot", free_slots)

# Confirm booking
if st.button("✅ Confirm Appointment"):
    if not all([name, phone, time_slot]):
        st.error("Please complete all required fields.")
        st.stop()

    bookings.setdefault(date_str, {}).setdefault(doctor, []).append(time_slot)
    save_json(BOOKINGS_FILE, bookings)

    st.success(f"Appointment booked for {name} with {doctor} on {appt_date} at {time_slot}")

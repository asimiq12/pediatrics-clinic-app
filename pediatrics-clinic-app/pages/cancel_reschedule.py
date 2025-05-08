import streamlit as st
import json
import datetime

APPT_FILE = "appointment_slots.json"

def load_appointments():
    try:
        with open(APPT_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_appointments(data):
    with open(APPT_FILE, "w") as f:
        json.dump(data, f, indent=2)

st.title("🔁 Cancel or Reschedule Appointment")

appointments = load_appointments()
all_dates = sorted(appointments.keys())

if not all_dates:
    st.info("No appointments found.")
    st.stop()

selected_date = st.selectbox("Select a date", all_dates)
doctors = sorted(appointments[selected_date].keys())
selected_doctor = st.selectbox("Select a doctor", doctors)

times = appointments[selected_date].get(selected_doctor, [])
if not times:
    st.warning("No appointments for this doctor on this date.")
    st.stop()

selected_time = st.selectbox("Select a time slot", times)

# Cancellation
if st.button("❌ Cancel Appointment"):
    appointments[selected_date][selected_doctor].remove(selected_time)
    if not appointments[selected_date][selected_doctor]:
        del appointments[selected_date][selected_doctor]
    if not appointments[selected_date]:
        del appointments[selected_date]
    save_appointments(appointments)
    st.success(f"Appointment for {selected_doctor} at {selected_time} on {selected_date} has been cancelled.")

# Placeholder for rescheduling
st.markdown("---")
st.info("✅ Rescheduling functionality coming up next...")

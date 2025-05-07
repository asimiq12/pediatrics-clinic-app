import streamlit as st
import datetime

st.title("📅 Book an Appointment")

# --- Patient Info ---
st.subheader("👤 Parent / Guardian Information")
name = st.text_input("Full Name")
phone = st.text_input("Phone Number")
email = st.text_input("Email Address")

# --- Appointment Type ---
st.subheader("📋 Appointment Type")
appt_type = st.selectbox("Select type", ["Checkup", "Sick", "Consultation"])

# --- Date Selection ---
today = datetime.date.today()
max_date = today + datetime.timedelta(days=30)

if appt_type == "Sick":
    appt_date = st.date_input("Select date", value=today, min_value=today, max_value=max_date)
else:
    appt_date = st.date_input("Select date", min_value=today, max_value=max_date)

# --- Doctor Selection (for Checkup only) ---
doctor = None
if appt_type == "Checkup":
    st.subheader("🩺 Preferred Doctor")
    doctor = st.selectbox("Choose Doctor", ["Dr. Chowhan", "NP Ayesha", "NP Smith"])

# --- Time Slot (placeholder for now) ---
st.subheader("⏰ Available Time Slot")
# We will generate real slots later — placeholder now
time_slot = st.selectbox("Select Time", ["09:00 AM", "09:30 AM", "10:00 AM", "10:30 AM"])

# --- Confirmation ---
if st.button("✅ Confirm Appointment"):
    st.success(f"Appointment booked for {name} on {appt_date} at {time_slot}")
    # Here you would write to appointment_slots.json

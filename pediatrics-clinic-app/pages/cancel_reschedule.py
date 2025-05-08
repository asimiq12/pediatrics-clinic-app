import streamlit as st
import json
import datetime

APPT_FILE = "appointment_slots.json"
SHIFT_FILE = "shift_calendar.json"
STAFF_FILE = "staff_data.json"

def load_json(file):
    try:
        with open(file, "r") as f:
            return json.load(f)
    except:
        return {}

def save_json(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

def generate_slots(start, end, interval_min):
    slots = []
    current = datetime.datetime.combine(datetime.date.today(), start)
    end = datetime.datetime.combine(datetime.date.today(), end)
    while current + datetime.timedelta(minutes=interval_min) <= end:
        slots.append(current.time().strftime("%I:%M %p"))
        current += datetime.timedelta(minutes=interval_min)
    return slots

# Duration per type
durations = {"Checkup": 30, "Sick": 15, "Consultation": 30}
weekday_start = datetime.time(9, 0)
weekday_end = datetime.time(16, 0)
sat_checkup_slots = [datetime.time(8,30), datetime.time(9,0), datetime.time(9,30), datetime.time(10,0)]
sat_sick_start = datetime.time(10,30)
sat_sick_end = datetime.time(12,15)

st.title("🔁 Cancel or Reschedule Appointment")

appointments = load_json(APPT_FILE)
shifts = load_json(SHIFT_FILE)
staff = load_json(STAFF_FILE)

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

col1, col2 = st.columns(2)

with col1:
    if st.button("❌ Cancel Appointment"):
        appointments[selected_date][selected_doctor].remove(selected_time)
        if not appointments[selected_date][selected_doctor]:
            del appointments[selected_date][selected_doctor]
        if not appointments[selected_date]:
            del appointments[selected_date]
        save_json(APPT_FILE, appointments)
        st.success(f"Cancelled appointment for {selected_doctor} at {selected_time} on {selected_date}")

with col2:
    if st.button("🔄 Begin Rescheduling"):
        st.session_state["reschedule_mode"] = True

if "reschedule_mode" in st.session_state and st.session_state["reschedule_mode"]:
    st.markdown("---")
    st.subheader("📅 New Appointment Details")

    appt_type = st.selectbox("Appointment Type", ["Checkup", "Sick", "Consultation"])
    today = datetime.date.today()
    max_date = today + datetime.timedelta(days=30)
    min_date = today if appt_type == "Sick" else today + datetime.timedelta(days=1)

    new_date = st.date_input("Select new date", min_value=min_date, max_value=max_date)
    date_str = new_date.isoformat()
    duration = durations[appt_type]
    working_doctors = shifts.get(date_str, [])

    if selected_doctor not in working_doctors:
        st.warning(f"{selected_doctor} is not assigned on {date_str}")
        st.stop()

    if new_date.weekday() == 5:
        if appt_type == "Checkup":
            new_slots = [t.strftime("%I:%M %p") for t in sat_checkup_slots]
        elif appt_type == "Sick" and new_date == today:
            new_slots = generate_slots(sat_sick_start, sat_sick_end, duration)
        else:
            st.warning("Saturday sick visits must be same-day.")
            st.stop()
    else:
        new_slots = generate_slots(weekday_start, weekday_end, duration)

    booked = appointments.get(date_str, {}).get(selected_doctor, [])
    free_slots = [s for s in new_slots if s not in booked]

    if not free_slots:
        st.error("No available slots.")
        st.stop()

    new_time = st.selectbox("New time slot", free_slots)

    if st.button("✅ Confirm Reschedule"):
        # Remove old
        appointments[selected_date][selected_doctor].remove(selected_time)
        if not appointments[selected_date][selected_doctor]:
            del appointments[selected_date][selected_doctor]
        if not appointments[selected_date]:
            del appointments[selected_date]
        # Add new
        appointments.setdefault(date_str, {}).setdefault(selected_doctor, []).append(new_time)
        save_json(APPT_FILE, appointments)
        st.success(f"Rescheduled to {new_time} on {new_date} with {selected_doctor}")
        st.session_state["reschedule_mode"] = False

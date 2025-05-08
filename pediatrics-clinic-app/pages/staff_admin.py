import streamlit as st
import json
import datetime

st.title("🗓 Doctor Shift Calendar – Pediatrics of Manassas")

CALENDAR_FILE = "shift_calendar.json"
STAFF_FILE = "staff_data.json"

def load_json(file_path):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except:
        return {}

def save_json(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

# Load staff and calendar data
staff_data = load_json(STAFF_FILE)
calendar_data = load_json(CALENDAR_FILE)

# Get active doctors only
doctors = [f"{emp['first_name']} {emp['last_name']}" for emp in staff_data if emp.get("role") == "doctor" and emp.get("active")]

selected_date = st.date_input("Select a date", min_value=datetime.date.today())
date_str = selected_date.isoformat()

assigned = calendar_data.get(date_str, [])
selected = st.multiselect("Choose 2 working doctors", doctors, default=assigned, max_selections=2)

col1, col2 = st.columns([1, 1])

with col1:
    if st.button("💾 Save Shift"):
        calendar_data[date_str] = selected
        save_json(CALENDAR_FILE, calendar_data)
        st.success(f"Shift for {date_str} updated.")

with col2:
    if st.button("🗑️ Delete This Shift"):
        if date_str in calendar_data:
            del calendar_data[date_str]
            save_json(CALENDAR_FILE, calendar_data)
            st.success(f"Shift for {date_str} deleted.")

# View future assignments
st.subheader("📆 Upcoming Assignments")
future = {k: v for k, v in calendar_data.items() if k >= datetime.date.today().isoformat()}
for day in sorted(future.keys()):
    st.write(f"**{day}** → {', '.join(future[day]) if future[day] else 'Unassigned'}")

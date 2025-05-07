import streamlit as st
import json
import datetime

st.title("🗓 Doctor Shift Calendar – Pediatrics of Manassas")

# Load existing calendar
CALENDAR_FILE = "shift_calendar.json"

def load_calendar():
    try:
        with open(CALENDAR_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_calendar(data):
    with open(CALENDAR_FILE, "w") as f:
        json.dump(data, f, indent=2)

calendar_data = load_calendar()

# --- Select Date ---
selected_date = st.date_input("Select a date", min_value=datetime.date.today())
date_str = selected_date.isoformat()

# --- Assign Doctors ---
doctors = ["Dr. Chowhan", "NP Ayesha", "NP Smith"]
assigned = calendar_data.get(date_str, [])
selected = st.multiselect("Choose 2 working doctors", doctors, default=assigned, max_selections=2)

if st.button("💾 Save Shift"):
    calendar_data[date_str] = selected
    save_calendar(calendar_data)
    st.success(f"Shift for {date_str} updated.")

# --- Optional: View Existing Assignments ---
st.subheader("📆 Upcoming Assignments")
future = {k: v for k, v in calendar_data.items() if k >= datetime.date.today().isoformat()}
for day in sorted(future.keys()):
    st.write(f"**{day}** → {', '.join(future[day]) if future[day] else 'Unassigned'}")

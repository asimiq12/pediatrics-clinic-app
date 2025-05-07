# Homepage with navigation

import streamlit as st

st.title('Pediatrics of Manassas')
st.page_link('book_appointment.py', label='📅 Book Appointment')
st.page_link('attendance_portal.py', label='📍 Staff Attendance')
st.page_link('daily_dashboard.py', label='📊 Admin Dashboard')

from pathlib import Path
import streamlit as st
import pandas as pd


# Load datasets

workers = pd.read_csv(r"Workers.csv")
equipment = pd.read_csv(r"Equipment.csv")
incidents = pd.read_csv(r"Incidents.csv")

# Safety Incident Database

elif menu_choice == "Incidents":
    st.header(" Safety Incident Database")
    st.subheader("Central repository for recording and analyzing safety incidents")

    
    st.dataframe(incidents)

    # --- Add new incident ---
    st.markdown("###  Add New Incident")
    with st.form("add_incident_form"):
        incident_id = st.text_input("Incident ID")
        date = st.date_input("Date")
        time = st.time_input("Time")
        shift = st.selectbox("Shift", ["Day", "Night"])
        location = st.text_input("Location")
        department = st.selectbox("Department", ["Drilling", "Hauling", "Maintenance", "Processing", "Exploration"])
        incident_type = st.selectbox("Incident Type", ["Near Miss", "Slip/Trip", "Fire", "Explosion", "Vehicle Collision", "Equipment Failure", "Mechanical Failure", "Chemical Spill"])
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        injury_status = st.selectbox("Injury Status", ["None", "Minor", "Major"])
        lost_time = st.selectbox("Lost-Time Injury", ["No", "Yes"])
        cause = st.text_input("Cause")
        corrective_action = st.text_input("Corrective Action")
        status = st.selectbox("Incident Status", ["Open", "Closed"])
        submitted = st.form_submit_button("Add Incident")

        if submitted:
            new_row = {
                "IncidentID": incident_id,
                "Date": date,
                "Time": time,
                "Shift": shift,
                "Location": location,
                "Department": department,
                "Type": incident_type,
                "Severity": severity,
                "InjuryStatus": injury_status,
                "LostTimeInjury": lost_time,
                "Cause": cause,
                "CorrectiveAction": corrective_action,
                "Status": status
            }
            incidents = pd.concat([incidents, pd.DataFrame([new_row])], ignore_index=True)
            st.success(f"Incident {incident_id} added successfully!")

    # Search and Filter
    st.markdown("###  Search and Filter Incidents")
    search_term = st.text_input("Search by Incident ID, Type, or Department")
    severity_filter = st.multiselect("Filter by Severity", incidents["Severity"].unique())
    status_filter = st.multiselect("Filter by Status", incidents["Status"].unique())

    filtered = incidents.copy()
    if search_term:
        filtered = filtered[
            filtered.apply(lambda row: search_term.lower() in str(row).lower(), axis=1)
        ]
    if severity_filter:
        filtered = filtered[filtered["Severity"].isin(severity_filter)]
    if status_filter:
        filtered = filtered[filtered["Status"].isin(status_filter)]

    st.dataframe(filtered)

    # Categorize and Count 
    st.markdown("Incident Summary")
    total_incidents = len(incidents)
    open_incidents = len(incidents[incidents["Status"] == "Open"])
    closed_incidents = len(incidents[incidents["Status"] == "Closed"])
    critical_incidents = len(incidents[incidents["Severity"] == "Critical"])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Incidents", total_incidents)
    col2.metric("Open Incidents", open_incidents)
    col3.metric("Closed Incidents", closed_incidents)
    col4.metric("Critical Incidents", critical_incidents)

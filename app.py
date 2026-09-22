import streamlit as st

st.set_page_config(
    page_title="AIRB CMMS",
    page_icon="🔧",
    layout="wide"
)

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🔧 AIRB CMMS")
st.sidebar.caption("Computerized Maintenance Management System")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Asset Register",
        "PM Schedule",
        "Work Orders",
        "Corrective Maintenance",
        "Procurement",
        "Maintenance History"
    ]
)

# -----------------------------
# DASHBOARD
# -----------------------------
if page == "Dashboard":

    st.title("Maintenance Dashboard")
    st.caption("AIRB Centralised Maintenance Management System")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("PM Due", 12)
    col2.metric("Overdue PM", 3)
    col3.metric("Open Work Orders", 5)
    col4.metric("Breakdown", 2)

    st.divider()

    st.subheader("Maintenance Overview")

    col1, col2 = st.columns(2)

    with col1:
        st.info("""
        **Preventive Maintenance**

        Monitor scheduled maintenance and upcoming PM activities.
        """)

    with col2:
        st.warning("""
        **Corrective Maintenance**

        Monitor breakdowns, corrective actions and outstanding work.
        """)

    st.subheader("Upcoming Preventive Maintenance")

    st.dataframe(
        {
            "Asset": ["P-101", "BL-02", "RO-P03"],
            "Task": [
                "Pump Inspection",
                "Blower Service",
                "Pump Service"
            ],
            "Due": [
                "Today",
                "24 Sep 2026",
                "25 Sep 2026"
            ],
            "Status": [
                "Due",
                "Planned",
                "Planned"
            ]
        },
        use_container_width=True
    )

# -----------------------------
# OTHER MODULES
# -----------------------------
elif page == "Asset Register":
    st.title("Asset Register")
    st.info("Asset registration module will be developed here.")

elif page == "PM Schedule":
    st.title("Preventive Maintenance Schedule")
    st.info("PM scheduling module will be developed here.")

elif page == "Work Orders":
    st.title("Work Orders")
    st.info("Maintenance work orders will be managed here.")

elif page == "Corrective Maintenance":
    st.title("Corrective Maintenance")
    st.info("Corrective maintenance and breakdown activities will be managed here.")

elif page == "Procurement":
    st.title("Procurement")
    st.info("PR / IER requests triggered by maintenance will appear here.")

elif page == "Maintenance History":
    st.title("Maintenance History")
    st.info("Completed maintenance records will be stored here.")

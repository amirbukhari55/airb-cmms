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
    st.caption("Register and manage plant assets and equipment.")

    # Sample asset database
    assets = [
        {
            "Asset ID": "P-101",
            "Asset Name": "Raw Water Pump 1",
            "Asset Type": "Pump",
            "Location": "Pump House",
            "Status": "Active"
        },
        {
            "Asset ID": "BL-02",
            "Asset Name": "Aeration Blower 2",
            "Asset Type": "Blower",
            "Location": "Blower Room",
            "Status": "Active"
        },
        {
            "Asset ID": "RO-P03",
            "Asset Name": "RO High Pressure Pump",
            "Asset Type": "Pump",
            "Location": "RO Plant",
            "Status": "Active"
        }
    ]

    st.subheader("Registered Assets")
    st.dataframe(assets, use_container_width=True)

    st.divider()

    st.subheader("Register New Asset")

    with st.form("asset_form"):
        col1, col2 = st.columns(2)

        with col1:
            asset_id = st.text_input("Asset ID")
            asset_name = st.text_input("Asset Name")
            asset_type = st.selectbox(
                "Asset Type",
                ["Pump", "Blower", "Motor", "Valve", "Instrument",
                 "Tank", "Filter", "Membrane System", "Other"]
            )

        with col2:
            location = st.text_input("Location")
            status = st.selectbox(
                "Status",
                ["Active", "Inactive", "Under Maintenance"]
            )
            manufacturer = st.text_input("Manufacturer")

        submitted = st.form_submit_button("Register Asset")

        if submitted:
            if asset_id and asset_name:
                st.success(f"Asset {asset_id} - {asset_name} registered successfully.")
            else:
                st.error("Asset ID and Asset Name are required.")

elif page == "PM Schedule":
    st.title("Preventive Maintenance Schedule")
    st.caption("Plan, assign and monitor preventive maintenance activities.")

    # --------------------------------
    # SAMPLE PM SCHEDULE
    # --------------------------------
    pm_data = [
        {
            "PM ID": "PM-001",
            "Asset": "P-101",
            "Task": "Pump Inspection",
            "Maintenance Type": "Preventive Maintenance",
            "Frequency": "Monthly",
            "Next Due Date": "22 Sep 2026",
            "Assigned Technician": "Technician A",
            "Status": "Due"
        },
        {
            "PM ID": "PM-002",
            "Asset": "BL-02",
            "Task": "Blower Service",
            "Maintenance Type": "Preventive Maintenance",
            "Frequency": "Quarterly",
            "Next Due Date": "24 Sep 2026",
            "Assigned Technician": "Technician B",
            "Status": "Planned"
        },
        {
            "PM ID": "PM-003",
            "Asset": "RO-P03",
            "Task": "Pump Service",
            "Maintenance Type": "Preventive Maintenance",
            "Frequency": "Monthly",
            "Next Due Date": "25 Sep 2026",
            "Assigned Technician": "Technician A",
            "Status": "Planned"
        }
    ]

    st.subheader("Upcoming Preventive Maintenance")
    st.dataframe(pm_data, use_container_width=True)

    st.divider()

    # --------------------------------
    # CREATE PM SCHEDULE
    # --------------------------------
    st.subheader("Create PM Schedule")

    with st.form("pm_schedule_form"):

        col1, col2 = st.columns(2)

        with col1:
            pm_id = st.text_input("PM Schedule ID")

            asset = st.selectbox(
                "Asset",
                [
                    "P-101 - Raw Water Pump 1",
                    "BL-02 - Aeration Blower 2",
                    "RO-P03 - RO High Pressure Pump"
                ]
            )

            task = st.text_input("PM Task Name")

            maintenance_type = st.selectbox(
                "Maintenance Type",
                [
                    "Preventive Maintenance",
                    "Inspection",
                    "Calibration",
                    "Testing"
                ]
            )

        with col2:
            frequency = st.selectbox(
                "Frequency",
                [
                    "Daily",
                    "Weekly",
                    "Monthly",
                    "Quarterly",
                    "Half-Yearly",
                    "Yearly"
                ]
            )

            start_date = st.date_input("Start Date")

            technician = st.selectbox(
                "Assigned Technician",
                [
                    "Technician A",
                    "Technician B",
                    "Technician C"
                ]
            )

            duration = st.number_input(
                "Estimated Duration (Hours)",
                min_value=0.5,
                step=0.5
            )

        instructions = st.text_area(
            "PM Instructions",
            placeholder="Enter maintenance instructions..."
        )

        submitted = st.form_submit_button("Create PM Schedule")

        if submitted:
            if pm_id and task:
                st.success(
                    f"PM Schedule {pm_id} for {asset} created successfully."
                )
            else:
                st.error("PM Schedule ID and PM Task Name are required.")

elif page == "Work Orders":
    st.title("Work Orders")
    st.caption("Manage and track maintenance work orders.")

    # -----------------------------
    # WORK ORDER SUMMARY
    # -----------------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Open", 3)

    with col2:
        st.metric("In Progress", 2)

    with col3:
        st.metric("Pending Review", 1)

    with col4:
        st.metric("Completed", 8)

    st.divider()

    # -----------------------------
    # ACTIVE WORK ORDERS
    # -----------------------------
    st.subheader("Active Work Orders")

    work_orders = [
        {
            "WO ID": "WO-001",
            "Asset": "P-101",
            "Work": "Pump Inspection",
            "Type": "Preventive Maintenance",
            "Priority": "Normal",
            "Assigned To": "Technician A",
            "Status": "Assigned"
        },
        {
            "WO ID": "WO-002",
            "Asset": "BL-02",
            "Work": "Investigate abnormal vibration",
            "Type": "Inspection",
            "Priority": "High",
            "Assigned To": "Technician B",
            "Status": "In Progress"
        },
        {
            "WO ID": "WO-003",
            "Asset": "RO-P03",
            "Work": "Mechanical seal inspection",
            "Type": "Corrective Maintenance",
            "Priority": "Urgent",
            "Assigned To": "Technician C",
            "Status": "Pending Engineer Review"
        }
    ]

    st.dataframe(work_orders, use_container_width=True)

    st.divider()

    # -----------------------------
    # CREATE WORK ORDER
    # -----------------------------
    st.subheader("Create Work Order")

    with st.form("work_order_form"):

        col1, col2 = st.columns(2)

        with col1:
            wo_id = st.text_input("Work Order ID")

            asset = st.selectbox(
                "Asset",
                [
                    "P-101 - Raw Water Pump 1",
                    "BL-02 - Aeration Blower 2",
                    "RO-P03 - RO High Pressure Pump"
                ]
            )

            maintenance_type = st.selectbox(
                "Maintenance Type",
                [
                    "Breakdown / Emergency",
                    "Calibration",
                    "Corrective Maintenance",
                    "Inspection",
                    "Preventive Maintenance",
                    "Testing"
                ]
            )

            priority = st.selectbox(
                "Priority",
                ["Low", "Normal", "High", "Urgent"],
                index=1
            )

        with col2:
            technician = st.selectbox(
                "Assigned Technician",
                [
                    "Technician A",
                    "Technician B",
                    "Technician C"
                ]
            )

            status = st.selectbox(
                "Status",
                [
                    "Open",
                    "Assigned",
                    "In Progress",
                    "Pending Engineer Review",
                    "Completed",
                    "Closed"
                ]
            )

            estimated_hours = st.number_input(
                "Estimated Duration (Hours)",
                min_value=0.5,
                step=0.5
            )

        work_description = st.text_area(
            "Work Description",
            placeholder="Describe the maintenance work required..."
        )

        submitted = st.form_submit_button("Create Work Order")

        if submitted:
            if wo_id and work_description:
                st.success(
                    f"Work Order {wo_id} created successfully."
                )
            else:
                st.error(
                    "Work Order ID and Work Description are required."
                )

elif page == "Corrective Maintenance":
    st.title("Corrective Maintenance")
    st.info("Corrective maintenance and breakdown activities will be managed here.")

elif page == "Procurement":
    st.title("Procurement")
    st.info("PR / IER requests triggered by maintenance will appear here.")

elif page == "Maintenance History":
    st.title("Maintenance History")
    st.info("Completed maintenance records will be stored here.")

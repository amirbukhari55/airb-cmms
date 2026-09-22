import streamlit as st
import pandas as pd

# -----------------------------
# SESSION DATA
# -----------------------------

if "assets" not in st.session_state:
    st.session_state.assets = [
        {
            "Asset ID": "P-101",
            "Asset Name": "Raw Water Pump 1",
            "Location": "WTP",
            "Asset Type": "Pump",
            "Status": "Active"
        },
        {
            "Asset ID": "BL-02",
            "Asset Name": "Blower 2",
            "Location": "STP",
            "Asset Type": "Blower",
            "Status": "Active"
        },
        {
            "Asset ID": "RO-P03",
            "Asset Name": "RO High Pressure Pump",
            "Location": "WRP",
            "Asset Type": "Pump",
            "Status": "Active"
        }
    ]
    
if "pm_schedules" not in st.session_state:
    st.session_state.pm_schedules = [
        {
            "PM Schedule ID": "PM-001",
            "Asset": "P-101 - Raw Water Pump 1",
            "Maintenance Type": "Preventive Maintenance",
            "Frequency": "Monthly",
            "Next Due Date": "2026-09-22",
            "Assigned Technician": "Technician A",
            "Status": "Active"
        },
        {
            "PM Schedule ID": "PM-002",
            "Asset": "BL-02 - Blower 2",
            "Maintenance Type": "Preventive Maintenance",
            "Frequency": "Monthly",
            "Next Due Date": "2026-09-24",
            "Assigned Technician": "Technician B",
            "Status": "Active"
        }
    ]
if "corrective_maintenance" not in st.session_state:
    st.session_state.corrective_maintenance = [
        {
            "CM ID": "CM-001",
            "WO ID": "WO-003",
            "Asset": "RO-P03",
            "Problem": "Mechanical seal leakage",
            "Failure Type": "Mechanical",
            "Priority": "Urgent",
            "Downtime": 4.0,
            "Procurement": "Required",
            "Status": "Pending Engineer Review"
        },
        {
            "CM ID": "CM-002",
            "WO ID": "WO-002",
            "Asset": "BL-02",
            "Problem": "Abnormal vibration",
            "Failure Type": "Mechanical",
            "Priority": "High",
            "Downtime": 2.0,
            "Procurement": "Not Required",
            "Status": "In Progress"
        }
    ]
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

    # -----------------------------
    # REGISTERED ASSETS
    # -----------------------------
    st.subheader("Registered Assets")

    assets_df = pd.DataFrame(st.session_state.assets)

    st.dataframe(
        assets_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # -----------------------------
    # REGISTER NEW ASSET
    # -----------------------------
    st.subheader("Register New Asset")

    with st.form("asset_form"):
        col1, col2 = st.columns(2)

        with col1:
            asset_id = st.text_input("Asset ID")
            asset_name = st.text_input("Asset Name")

            asset_type = st.selectbox(
                "Asset Type",
                [
                    "Pump",
                    "Blower",
                    "Motor",
                    "Valve",
                    "Instrument",
                    "Tank",
                    "Filter",
                    "Membrane System",
                    "Other"
                ]
            )

        with col2:
            location = st.text_input("Location")

            status = st.selectbox(
                "Status",
                [
                    "Active",
                    "Inactive",
                    "Under Maintenance"
                ]
            )

            manufacturer = st.text_input("Manufacturer")

        submitted = st.form_submit_button("Register Asset")

        if submitted:

            if asset_id and asset_name:

                new_asset = {
                    "Asset ID": asset_id,
                    "Asset Name": asset_name,
                    "Asset Type": asset_type,
                    "Location": location,
                    "Status": status,
                    "Manufacturer": manufacturer
                }

                st.session_state.assets.append(new_asset)

                st.success(
                    f"Asset {asset_id} - {asset_name} registered successfully."
                )

                st.rerun()

            else:
                st.error("Asset ID and Asset Name are required.")

elif page == "PM Schedule":
    st.title("Preventive Maintenance Schedule")
    st.caption("Plan, assign and monitor preventive maintenance activities.")

    # --------------------------------
    # PM SCHEDULE DATABASE
    # --------------------------------
    if "pm_schedules" not in st.session_state:
        st.session_state.pm_schedules = [
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

    # --------------------------------
    # DISPLAY PM SCHEDULE
    # --------------------------------
    st.subheader("Upcoming Preventive Maintenance")

    st.dataframe(
        st.session_state.pm_schedules,
        use_container_width=True
    )

    if st.button("Generate Work Orders for Due PM"):

        if "work_orders" not in st.session_state:
            st.session_state.work_orders = []

        generated_count = 0

        for pm in st.session_state.pm_schedules:

            if pd.to_datetime(pm["Next Due Date"]).date() <= pd.Timestamp.today().date():

                existing_wo = any(
                    wo.get("PM Schedule ID") == pm["PM Schedule ID"]
                    for wo in st.session_state.work_orders
                )

                if not existing_wo:
        
                    new_wo = {
                        "WO ID": f"WO-{pm['PM Schedule ID']}",
                        "PM Schedule ID": pm["PM Schedule ID"],
                        "Asset": pm["Asset"],
                        "Work": "Scheduled Preventive Maintenance",
                        "Type": "Preventive Maintenance",
                        "Priority": "Normal",
                        "Assigned To": pm["Assigned Technician"],
                        "Status": "Assigned",
                        "Estimated Hours": 1.0
                    }

                    st.session_state.work_orders.append(new_wo)
                    generated_count += 1

                if generated_count > 0:
                    st.success(
                        f"{generated_count} preventive maintenance work order(s) generated."
                    )
                else:
                    st.info(
                        "No new due PM work orders to generate."
                    )

    st.divider()

    # --------------------------------
    # CREATE PM SCHEDULE
    # --------------------------------
    st.subheader("Create PM Schedule")

    with st.form("pm_schedule_form"):

        col1, col2 = st.columns(2)

        with col1:
            pm_id = st.text_input("PM Schedule ID")

            asset_options = [
                f"{item['Asset ID']} - {item['Asset Name']}"
                for item in st.session_state.assets
                if item["Status"] == "Active"
            ]

            asset = st.selectbox(
                "Asset",
                asset_options
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

                asset_id = asset.split(" - ")[0]

                new_pm = {
                    "PM ID": pm_id,
                    "Asset": asset_id,
                    "Task": task,
                    "Maintenance Type": maintenance_type,
                    "Frequency": frequency,
                    "Next Due Date": start_date.strftime("%d %b %Y"),
                    "Assigned Technician": technician,
                    "Status": "Planned"
                }

                st.session_state.pm_schedules.append(new_pm)

                st.success(
                    f"PM Schedule {pm_id} for {asset} created successfully."
                )

                st.rerun()

            else:
                st.error("PM Schedule ID and PM Task Name are required.")
                
elif page == "Work Orders":
    st.title("Work Orders")
    st.caption("Manage and track maintenance work orders.")

    # --------------------------------
    # WORK ORDER DATABASE
    # --------------------------------
    if "work_orders" not in st.session_state:
        st.session_state.work_orders = [
            {
                "WO ID": "WO-001",
                "Asset": "P-101",
                "Work": "Pump Inspection",
                "Type": "Preventive Maintenance",
                "Priority": "Normal",
                "Assigned To": "Technician A",
                "Status": "Assigned",
                "Estimated Hours": 1.0
            },
            {
                "WO ID": "WO-002",
                "Asset": "BL-02",
                "Work": "Investigate abnormal vibration",
                "Type": "Inspection",
                "Priority": "High",
                "Assigned To": "Technician B",
                "Status": "In Progress",
                "Estimated Hours": 2.0
            },
            {
                "WO ID": "WO-003",
                "Asset": "RO-P03",
                "Work": "Mechanical seal inspection",
                "Type": "Corrective Maintenance",
                "Priority": "Urgent",
                "Assigned To": "Technician C",
                "Status": "Pending Engineer Review",
                "Estimated Hours": 4.0
            }
        ]

    # --------------------------------
    # WORK ORDER SUMMARY
    # --------------------------------
    open_count = sum(
        1 for wo in st.session_state.work_orders
        if wo["Status"] == "Open"
    )

    progress_count = sum(
        1 for wo in st.session_state.work_orders
        if wo["Status"] == "In Progress"
    )

    review_count = sum(
        1 for wo in st.session_state.work_orders
        if wo["Status"] == "Pending Engineer Review"
    )

    completed_count = sum(
        1 for wo in st.session_state.work_orders
        if wo["Status"] in ["Completed", "Closed"]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Open", open_count)

    with col2:
        st.metric("In Progress", progress_count)

    with col3:
        st.metric("Pending Review", review_count)

    with col4:
        st.metric("Completed", completed_count)

    st.divider()

    # --------------------------------
    # ACTIVE WORK ORDERS
    # --------------------------------
    st.subheader("Active Work Orders")

    active_work_orders = [
        wo for wo in st.session_state.work_orders
        if wo["Status"] not in ["Completed", "Closed"]
    ]

    st.dataframe(
        active_work_orders,
        use_container_width=True
    )

    st.divider()

    # --------------------------------
    # CREATE WORK ORDER
    # --------------------------------
    st.subheader("Create Work Order")

    with st.form("work_order_form"):

        col1, col2 = st.columns(2)

        with col1:
            wo_id = st.text_input("Work Order ID")

            asset_options = [
                f"{item['Asset ID']} - {item['Asset Name']}"
                for item in st.session_state.assets
                if item["Status"] == "Active"
            ]

            asset = st.selectbox(
                "Asset",
                asset_options
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

                asset_id = asset.split(" - ")[0]

                new_work_order = {
                    "WO ID": wo_id,
                    "Asset": asset_id,
                    "Work": work_description,
                    "Type": maintenance_type,
                    "Priority": priority,
                    "Assigned To": technician,
                    "Status": status,
                    "Estimated Hours": estimated_hours
                }

                st.session_state.work_orders.append(new_work_order)

                st.success(
                    f"Work Order {wo_id} created successfully."
                )

                st.rerun()

            else:
                st.error(
                    "Work Order ID and Work Description are required."
                )
elif page == "Corrective Maintenance":
    st.title("Corrective Maintenance")
    st.caption("Record breakdowns, corrective actions and maintenance findings.")

    # -----------------------------
    # OPEN CORRECTIVE MAINTENANCE
    # -----------------------------
    st.subheader("Open Corrective Maintenance")

    cm_data = [
        {
            "CM ID": "CM-001",
            "WO ID": "WO-003",
            "Asset": "RO-P03",
            "Problem": "Mechanical seal leakage",
            "Priority": "Urgent",
            "Procurement": "Required",
            "Status": "Pending Engineer Review"
        },
        {
            "CM ID": "CM-002",
            "WO ID": "WO-002",
            "Asset": "BL-02",
            "Problem": "Abnormal vibration",
            "Priority": "High",
            "Procurement": "Not Required",
            "Status": "In Progress"
        }
    ]

    st.dataframe(cm_data, use_container_width=True)

    st.divider()

    # -----------------------------
    # CORRECTIVE MAINTENANCE FORM
    # -----------------------------
    st.subheader("Record Corrective Maintenance")

    
    
    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:
            cm_id = st.text_input("CM ID")

            wo_id = st.selectbox(
                "Related Work Order",
                ["WO-001", "WO-002", "WO-003"]
            )

            asset = st.selectbox(
                "Asset",
                [
                    "P-101 - Raw Water Pump 1",
                    "BL-02 - Aeration Blower 2",
                    "RO-P03 - RO High Pressure Pump"
                ]
            )

            priority = st.selectbox(
                "Priority",
                ["Low", "Normal", "High", "Urgent"],
                index=1
            )

        with col2:
            failure_type = st.selectbox(
                "Failure Type",
                [
                    "Mechanical",
                    "Electrical",
                    "Instrumentation",
                    "Process",
                    "Control / PLC",
                    "Other"
                ]
            )

            downtime = st.number_input(
                "Downtime (Hours)",
                min_value=0.0,
                step=0.5
            )

            procurement_required = st.selectbox(
                "Procurement Required?",
                ["No", "Yes"]
            )
            
            status = st.selectbox(
                "Status",
                [
                    "Open",
                    "In Progress",
                    "Pending Engineer Review",
                    "Completed",
                    "Closed"
                ]
            )

        problem = st.text_area(
            "Problem / Failure Description",
            placeholder="Describe the problem or failure..."
        )

        action = st.text_area(
            "Corrective Action",
            placeholder="Describe troubleshooting, repair or corrective action..."
        )

        if procurement_required == "Yes":
            st.warning(
                "Procurement required. A PR / IER request will be initiated."
            )

            item_required = st.text_input(
                "Material / Service Required"
            )

            justification = st.text_area(
                "Procurement Justification"
            )

        submitted = st.button(
            "Submit Corrective Maintenance",
            type="primary"
        )

        if submitted:
            if cm_id and problem:
                st.success(
                    f"Corrective Maintenance {cm_id} submitted successfully."
                )

                if procurement_required == "Yes":
                    st.info(
                        "Procurement request flagged for PR / IER generation."
                    )
            else:
                st.error(
                    "CM ID and Problem / Failure Description are required."
                )

elif page == "Procurement":
    st.title("Maintenance Procurement")
    st.caption("Manage PR / IER requests generated from maintenance activities.")

    # -----------------------------
    # PROCUREMENT SUMMARY
    # -----------------------------
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("New Requests", 2)

    with col2:
        st.metric("Pending Approval", 1)

    with col3:
        st.metric("PR / IER Issued", 3)

    with col4:
        st.metric("Completed", 5)

    st.divider()

    # -----------------------------
    # PROCUREMENT REQUESTS
    # -----------------------------
    st.subheader("Maintenance Procurement Requests")

    procurement_data = [
        {
            "Request ID": "MPR-001",
            "CM ID": "CM-001",
            "WO ID": "WO-003",
            "Asset": "RO-P03",
            "Requirement": "Mechanical Seal",
            "Priority": "Urgent",
            "Document": "PR",
            "Status": "Pending Approval"
        },
        {
            "Request ID": "MPR-002",
            "CM ID": "CM-003",
            "WO ID": "WO-005",
            "Asset": "P-101",
            "Requirement": "External Pump Repair",
            "Priority": "High",
            "Document": "IER",
            "Status": "New"
        }
    ]

    st.dataframe(procurement_data, use_container_width=True)

    st.divider()

    # -----------------------------
    # PROCUREMENT REQUEST DETAILS
    # -----------------------------
    st.subheader("Process Procurement Request")

    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:
            request_id = st.text_input("Request ID")

            cm_reference = st.selectbox(
                "Corrective Maintenance Reference",
                ["CM-001", "CM-002", "CM-003"]
            )

            asset = st.selectbox(
                "Asset",
                [
                    "P-101 - Raw Water Pump 1",
                    "BL-02 - Aeration Blower 2",
                    "RO-P03 - RO High Pressure Pump"
                ]
            )

            requirement_type = st.selectbox(
                "Requirement Type",
                [
                    "Spare Part",
                    "Material",
                    "External Service",
                    "Repair Service",
                    "Replacement Equipment",
                    "Other"
                ]
            )

        with col2:
            priority = st.selectbox(
                "Priority",
                ["Low", "Normal", "High", "Urgent"],
                index=1
            )

            document_type = st.selectbox(
                "Procurement Document",
                ["PR", "IER"]
            )

            estimated_cost = st.number_input(
                "Estimated Cost (RM)",
                min_value=0.0,
                step=100.0
            )

            procurement_status = st.selectbox(
                "Status",
                [
                    "New",
                    "Pending Engineer Review",
                    "Pending Approval",
                    "PR / IER Issued",
                    "PO Issued",
                    "Completed"
                ]
            )

        requirement = st.text_area(
            "Material / Service Required",
            placeholder="Describe the required material, spare part or service..."
        )

        justification = st.text_area(
            "Justification",
            placeholder="Maintenance justification for procurement..."
        )

        generate_document = st.checkbox(
            "Generate PR / IER document"
        )

        if generate_document:
            st.info(
                f"{document_type} will be generated from this maintenance request."
            )

        submitted = st.button(
            "Submit Procurement Request",
            type="primary"
        )

        if submitted:
            if request_id and requirement:
                st.success(
                    f"Procurement Request {request_id} submitted successfully."
                )

                if generate_document:
                    st.success(
                        f"{document_type} generation initiated."
                    )
            else:
                st.error(
                    "Request ID and Material / Service Required are required."
                )

elif page == "Maintenance History":

    st.title("Maintenance History")
    st.caption("Completed preventive and corrective maintenance records")

    history_data = [
        {
            "Date": "15 Sep 2026",
            "WO ID": "WO-001",
            "Asset": "P-101",
            "Maintenance Type": "Preventive Maintenance",
            "Work Description": "Pump inspection and lubrication",
            "Technician": "Technician A",
            "Downtime (hr)": 1.0,
            "Status": "Completed"
        },
        {
            "Date": "18 Sep 2026",
            "WO ID": "WO-002",
            "Asset": "BL-02",
            "Maintenance Type": "Corrective Maintenance",
            "Work Description": "Investigated abnormal vibration",
            "Technician": "Technician B",
            "Downtime (hr)": 2.5,
            "Status": "Completed"
        },
        {
            "Date": "20 Sep 2026",
            "WO ID": "WO-003",
            "Asset": "RO-P03",
            "Maintenance Type": "Corrective Maintenance",
            "Work Description": "Mechanical seal replacement",
            "Technician": "Technician C",
            "Downtime (hr)": 4.0,
            "Status": "Completed"
        }
    ]

    history_df = pd.DataFrame(history_data)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Completed Work Orders", len(history_df))

    with col2:
        st.metric(
            "Total Downtime",
            f"{history_df['Downtime (hr)'].sum()} hr"
        )

    with col3:
        st.metric(
            "Corrective Maintenance",
            len(
                history_df[
                    history_df["Maintenance Type"]
                    == "Corrective Maintenance"
                ]
            )
        )

    st.divider()

    st.subheader("Maintenance Records")

    search_asset = st.text_input(
        "Search Asset",
        placeholder="Example: P-101"
    )

    maintenance_filter = st.selectbox(
        "Maintenance Type",
        [
            "All",
            "Preventive Maintenance",
            "Corrective Maintenance"
        ]
    )

    filtered_history = history_df.copy()

    if search_asset:
        filtered_history = filtered_history[
            filtered_history["Asset"]
            .str.contains(search_asset, case=False, na=False)
        ]

    if maintenance_filter != "All":
        filtered_history = filtered_history[
            filtered_history["Maintenance Type"]
            == maintenance_filter
        ]

    st.dataframe(
        filtered_history,
        use_container_width=True,
        hide_index=True
    )

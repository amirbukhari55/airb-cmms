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
if "procurement_requests" not in st.session_state:
    st.session_state.procurement_requests = [
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

if "procurement_documents" not in st.session_state:
    st.session_state.procurement_documents = []

if "maintenance_documents" not in st.session_state:
    st.session_state.maintenance_documents = []
    
if "maintenance_history" not in st.session_state:
    st.session_state.maintenance_history = [
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

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "navigate_to" in st.session_state:
    st.session_state.page = st.session_state.pop("navigate_to")

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
    ],
    key="page"
)

# -----------------------------
# DASHBOARD
# -----------------------------

if page == "Dashboard":

    st.title("Maintenance Dashboard")
    st.caption("AIRB Centralised Maintenance Management System")

    # -----------------------------
    # DYNAMIC DASHBOARD METRICS
    # -----------------------------
    today = pd.Timestamp.today().date()

    active_pm = [
        pm for pm in st.session_state.pm_schedules
        if pm["Status"] == "Active"
    ]

    pm_due = sum(
        1 for pm in active_pm
        if pd.to_datetime(pm["Next Due Date"]).date() == today
    )

    overdue_pm = sum(
        1 for pm in active_pm
        if pd.to_datetime(pm["Next Due Date"]).date() < today
    )

    open_wo = sum(
        1 for wo in st.session_state.work_orders
        if wo["Status"] not in ["Completed", "Closed"]
    )

    open_cm = sum(
        1 for cm in st.session_state.corrective_maintenance
        if cm["Status"] not in ["Completed", "Closed"]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("PM Due Today", pm_due)
    col2.metric("Overdue PM", overdue_pm)
    col3.metric("Open Work Orders", open_wo)
    col4.metric("Open Corrective Maintenance", open_cm)

    st.divider()

    # -----------------------------
    # MAINTENANCE OVERVIEW
    # -----------------------------
    st.subheader("Maintenance Overview")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Completed Work Orders",
            sum(
                1 for wo in st.session_state.work_orders
                if wo["Status"] in ["Completed", "Closed"]
            )
        )

    with col2:
        st.metric(
            "Pending Engineer Review",
            sum(
                1 for wo in st.session_state.work_orders
                if wo["Status"] == "Pending Engineer Review"
            )
        )

    with col3:
        st.metric(
            "Pending Procurement",
            sum(
                1 for req in st.session_state.procurement_requests
                if req["Status"] != "Completed"
            )
        )

    st.divider()

    # -----------------------------
    # UPCOMING PREVENTIVE MAINTENANCE
    # -----------------------------
    st.subheader("Upcoming Preventive Maintenance")

    upcoming_pm = []

    for pm in active_pm:

        due_date = pd.to_datetime(
            pm["Next Due Date"]
        ).date()

        if due_date < today:
            pm_status = "Overdue"
        elif due_date == today:
            pm_status = "Due Today"
        else:
            pm_status = "Upcoming"

        upcoming_pm.append({
            "PM Schedule ID": pm["PM Schedule ID"],
            "Asset": pm["Asset"],
            "Maintenance Type": pm["Maintenance Type"],
            "Frequency": pm["Frequency"],
            "Due Date": pm["Next Due Date"],
            "Assigned Technician": pm["Assigned Technician"],
            "Status": pm_status
        })

    upcoming_pm.sort(
        key=lambda item: item["Due Date"]
    )

    if upcoming_pm:

        st.dataframe(
            upcoming_pm,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.info("No active preventive maintenance schedules.")

    st.divider()

    # -----------------------------
    # WORK ORDERS REQUIRING ATTENTION
    # -----------------------------
    st.subheader("Work Orders Requiring Attention")

    attention_wos = [
        wo for wo in st.session_state.work_orders
        if wo["Status"] in [
            "Assigned",
            "In Progress",
            "Pending Engineer Review"
        ]
    ]

    if attention_wos:

        st.dataframe(
            attention_wos,
            use_container_width=True,
            hide_index=True
        )

    else:
        st.success("No outstanding work orders.")

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


        generated_count = 0

        for pm in st.session_state.pm_schedules:
            
            if not pm.get("PM Schedule ID"):
                continue

            if pd.to_datetime(pm["Next Due Date"]).date() <= pd.Timestamp.today().date():

                existing_wo = any(
                    wo.get("PM Schedule ID") == pm.get("PM Schedule ID")
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
                
                if any(
                    pm.get("PM Schedule ID") == pm_id.strip()
                    for pm in st.session_state.pm_schedules
                ):
                    st.error("This PM Schedule ID already exists.")
                    st.stop()

                asset_id = asset.split(" - ")[0]

                new_pm = {
                    "PM Schedule ID": pm_id.strip(),
                    "Asset": asset,
                    "Task": task,
                    "Maintenance Type": maintenance_type,
                    "Frequency": frequency,
                    "Next Due Date": start_date.strftime("%Y-%m-%d"),
                    "Assigned Technician": technician,
                    "Status": "Active"
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
    
    # -----------------------------
    # MAINTENANCE DOCUMENT ATTACHMENTS
    # -----------------------------
    st.subheader("Maintenance Document Attachments")

    with st.container(border=True):

        document_wo_id = st.selectbox(
            "Select Work Order for Attachment",
            [
                wo["WO ID"]
                for wo in st.session_state.work_orders
            ],
            key="maintenance_document_wo"
        )

        document_type = st.selectbox(
            "Maintenance Document Type",
            [
                "PM Checklist",
                "Inspection Report",
                "Breakdown Photograph",
                "Service Report",
                "Maintenance Completion Report",
                "Other Supporting Document"
            ],
            key="maintenance_document_type"
        )

        uploaded_maintenance_file = st.file_uploader(
            "Upload Maintenance Document",
            type=["pdf", "docx", "xlsx", "jpg", "jpeg", "png"],
            key="maintenance_file_upload"
        )

        if st.button("Save Maintenance Attachment"):

            if uploaded_maintenance_file is not None:

                new_document = {
                    "WO ID": document_wo_id,
                    "Document Type": document_type,
                    "Filename": uploaded_maintenance_file.name,
                    "File Content": uploaded_maintenance_file.getvalue(),
                    "Uploaded On": pd.Timestamp.today().strftime("%d %b %Y")
                }

                st.session_state.maintenance_documents.append(
                    new_document
                )

                st.success(
                    f"{uploaded_maintenance_file.name} attached to {document_wo_id}."
                )

            else:
                st.error("Please select a document to upload.")
    
    # -----------------------------
    # MAINTENANCE DOCUMENT REGISTER
    # -----------------------------
    st.subheader("Uploaded Maintenance Documents")

    saved_maintenance_documents = [
        doc
        for doc in st.session_state.maintenance_documents
        if doc["WO ID"] == document_wo_id
    ]

    if saved_maintenance_documents:

        maintenance_document_table = [
            {
                "Document Type": doc["Document Type"],
                "Filename": doc["Filename"],
                "Uploaded On": doc["Uploaded On"]
            }
            for doc in saved_maintenance_documents
        ]

        st.dataframe(
            maintenance_document_table,
            use_container_width=True
        )

        selected_maintenance_document = st.selectbox(
            "Select Document to Download",
            range(len(saved_maintenance_documents)),
            format_func=lambda i: saved_maintenance_documents[i]["Filename"],
            key="download_maintenance_document"
        )

        selected_file = saved_maintenance_documents[
            selected_maintenance_document
        ]

        st.download_button(
            "Download Maintenance Document",
            data=selected_file["File Content"],
            file_name=selected_file["Filename"],
            mime="application/octet-stream",
            key="download_maintenance_attachment"
        )

    else:
        st.info("No documents uploaded for this Work Order.")
    st.divider()
    # --------------------------------
    # UPDATE WORK ORDER STATUS
    # --------------------------------
    st.subheader("Update Work Order Status")

    if active_work_orders:

        wo_options = [
            wo["WO ID"] for wo in active_work_orders
        ]

        selected_wo_id = st.selectbox(
            "Select Work Order",
            wo_options
        )

        selected_wo = next(
            wo for wo in st.session_state.work_orders
            if wo["WO ID"] == selected_wo_id
        )

        with st.container(border=True):

            st.write(
                f"**Asset:** {selected_wo['Asset']}"
            )

            st.write(
                f"**Work:** {selected_wo['Work']}"
            )

            create_cm = st.button(
                "Create Corrective Maintenance",
                key="create_cm_from_wo"
            )

            
            if create_cm:
                st.session_state.cm_from_wo = {
                    "WO ID": selected_wo["WO ID"],
                    "Asset": selected_wo["Asset"],
                    "Technician": selected_wo["Assigned To"]
                }

                st.session_state.navigate_to = "Corrective Maintenance"

                st.rerun()
            
            
            new_status = st.selectbox(
                "New Status",
                [
                    "Assigned",
                    "In Progress",
                    "Pending Engineer Review"
                ],
                key="update_wo_status"
            )

            actual_hours = st.number_input(
                "Actual Maintenance Hours",
                min_value=0.0,
                step=0.5
            )

            maintenance_remarks = st.text_area(
                "Maintenance Remarks",
                placeholder="Enter work performed, findings or completion remarks..."
            )

            update_wo = st.button(
                "Update Work Order",
                type="primary"
            )

            if update_wo:

                selected_wo["Status"] = new_status
                selected_wo["Actual Hours"] = actual_hours
                selected_wo["Maintenance Remarks"] = maintenance_remarks

                # Add completed WO to Maintenance History
                if new_status in "Closed":

                    already_in_history = any(
                        record["WO ID"] == selected_wo_id
                        for record in st.session_state.maintenance_history
                    )

                    if not already_in_history:

                        history_record = {
                            "Date": pd.Timestamp.today().strftime("%d %b %Y"),
                            "WO ID": selected_wo_id,
                            "Asset": selected_wo["Asset"],
                            "Maintenance Type": selected_wo["Type"],
                            "Work Description": selected_wo["Work"],
                            "Technician": selected_wo["Assigned To"],
                            "Downtime (hr)": actual_hours,
                            "Status": new_status
                        }

                        st.session_state.maintenance_history.append(
                            history_record
                        )

                st.success(
                    f"Work Order {selected_wo_id} updated to {new_status}."
                )

                st.rerun()

    else:
        st.info("No active work orders available.")

    st.divider()
    
    # -----------------------------
    # ENGINEER REVIEW AND APPROVAL
    # -----------------------------
    st.subheader("Engineer Review & Approval")

    pending_review_wos = [
        wo
        for wo in st.session_state.work_orders
        if wo["Status"] == "Pending Engineer Review"
    ]

    if pending_review_wos:

        review_wo_id = st.selectbox(
            "Select Work Order for Review",
            [wo["WO ID"] for wo in pending_review_wos],
            key="engineer_review_wo"
        )

        review_wo = next(
            wo for wo in pending_review_wos
            if wo["WO ID"] == review_wo_id
        )

        with st.container(border=True):

            st.write(f"**Asset:** {review_wo['Asset']}")
            st.write(f"**Work:** {review_wo['Work']}")
            st.write(f"**Technician:** {review_wo['Assigned To']}")

            st.write(
                f"**Actual Hours:** {review_wo.get('Actual Hours', 0)}"
            )

            st.write(
                f"**Maintenance Remarks:** {review_wo.get('Maintenance Remarks', '')}"
            )

            engineer_remarks = st.text_area(
                "Engineer Review Remarks",
                key="engineer_review_remarks"
            )

            col1, col2 = st.columns(2)

            with col1:
                approve_wo = st.button(
                    "Approve & Close Work Order",
                    type="primary"
                )

            with col2:
                return_wo = st.button(
                    "Return for Rectification"
                )

            if approve_wo:

                review_wo["Status"] = "Closed"
                review_wo["Engineer Remarks"] = engineer_remarks
                review_wo["Review Date"] = pd.Timestamp.today().strftime(
                    "%d %b %Y"
                )

                already_in_history = any(
                    record["WO ID"] == review_wo_id
                    for record in st.session_state.maintenance_history
                )

                if not already_in_history:

                    history_record = {
                        "Date": pd.Timestamp.today().strftime("%d %b %Y"),
                        "WO ID": review_wo_id,
                        "Asset": review_wo["Asset"],
                        "Maintenance Type": review_wo["Type"],
                        "Work Description": review_wo["Work"],
                        "Technician": review_wo["Assigned To"],
                        "Downtime (hr)": review_wo.get("Actual Hours", 0),
                        "Status": "Closed"
                    }

                    st.session_state.maintenance_history.append(
                        history_record
                    )

                st.success(
                    f"Work Order {review_wo_id} approved and closed."
                )

                st.rerun()

            if return_wo:

                if engineer_remarks.strip():

                    review_wo["Status"] = "In Progress"
                    review_wo["Engineer Remarks"] = engineer_remarks

                    st.success(
                        f"Work Order {review_wo_id} returned for rectification."
                    )

                    st.rerun()

                else:
                    st.error(
                        "Engineer remarks are required when returning a WO."
                    )

    else:
        st.info("No work orders pending engineer review.")

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
                ["Assigned"],
                help="New work orders start as Assigned. Technicians update their status after creation."
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
                existing_wo = any(
                    wo["WO ID"] == wo_id
                    for wo in st.session_state.work_orders
                )

                if existing_wo:
                    st.error(
                        f"Work Order {wo_id} already exists. Please use a unique Work Order ID."
                    )
                    st.stop()

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

                
                st.session_state.work_orders.append(new_work_order)

                st.success(
                    f"Work Order {wo_id} created successfully."
                )

                st.rerun()

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

    cm_display = []

    for cm in st.session_state.corrective_maintenance:

        cm_record = cm.copy()

        if cm["Procurement"] == "Required":

            related_requests = [
                req
                for req in st.session_state.procurement_requests
                if req["CM ID"] == cm["CM ID"]
            ]

            if related_requests:
                cm_record["Procurement Status"] = related_requests[-1]["Status"]
            else:
                cm_record["Procurement Status"] = "Pending Request"

        else:
            cm_record["Procurement Status"] = "Not Required"

        cm_display.append(cm_record)

    st.dataframe(
        cm_display,
        use_container_width=True
    )

    st.divider()

    # -----------------------------
    # CORRECTIVE MAINTENANCE FORM
    # -----------------------------
    st.subheader("Record Corrective Maintenance")

    
    
    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:
            
            cm_id = st.text_input("CM ID")

            # Receive WO information from Work Orders page
            cm_prefill = st.session_state.get("cm_from_wo", {})

            wo_options = [
                wo["WO ID"]
                for wo in st.session_state.work_orders
                if wo["Status"] not in ["Completed", "Closed"]
            ]

            # Automatically select the originating WO
            prefill_wo_id = cm_prefill.get("WO ID")

            default_index = (
                wo_options.index(prefill_wo_id)
                if prefill_wo_id in wo_options
                else 0
            )

            wo_id = st.selectbox(
                "Related Work Order",
                wo_options,
                index=default_index,
                key="cm_related_wo"
            )

            selected_wo = next(
                wo for wo in st.session_state.work_orders
                if wo["WO ID"] == wo_id
            )

            asset = selected_wo["Asset"]

            st.text_input(
                "Asset",
                value=asset,
                disabled=True
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

                # Prevent duplicate CM ID
                cm_exists = any(
                    cm["CM ID"] == cm_id
                    for cm in st.session_state.corrective_maintenance
                )

                if cm_exists:
                    st.error(
                        f"Corrective Maintenance {cm_id} already exists."
                    )

                else:
                    new_cm = {
                        "CM ID": cm_id,
                        "WO ID": wo_id,
                        "Asset": asset,
                        "Problem": problem,
                        "Failure Type": failure_type,
                        "Priority": priority,
                        "Downtime": downtime,
                        "Procurement": (
                            "Required"
                            if procurement_required == "Yes"
                            else "Not Required"
                        ),
                        "Status": status
                    }

                    st.session_state.corrective_maintenance.append(new_cm)

                    # Automatically create procurement request
                    if procurement_required == "Yes":

                        request_id = f"MPR-{cm_id}"

                        procurement_exists = any(
                            request["CM ID"] == cm_id
                            for request in st.session_state.procurement_requests
                        )

                        if not procurement_exists:

                            new_procurement = {
                                "Request ID": request_id,
                                "CM ID": cm_id,
                                "WO ID": wo_id,
                                "Asset": asset,
                                "Requirement": item_required,
                                "Priority": priority,
                                "Document": "Pending",
                                "Status": "New"
                            }

                            st.session_state.procurement_requests.append(
                                new_procurement
                            )

                    st.success(
                        f"Corrective Maintenance {cm_id} submitted successfully."
                    )
                    
                    st.session_state.pop("cm_from_wo", None)

                    st.rerun()

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
    new_requests = sum(
        1 for req in st.session_state.procurement_requests
        if req["Status"] == "New"
    )
    
    pending_approval = sum(
        1 for req in st.session_state.procurement_requests
        if req["Status"] in ["Pending Engineer Review", "Pending Approval"]
    )
    
    issued_requests = sum(
        1 for req in st.session_state.procurement_requests
        if req["Status"] in ["PR / IER Issued", "PO Issued"]
    )
    
    completed_requests = sum(
        1 for req in st.session_state.procurement_requests
        if req["Status"] == "Completed"
    )
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("New Requests", new_requests)
    
    with col2:
        st.metric("Pending Approval", pending_approval)
    
    with col3:
        st.metric("PR / IER Issued", issued_requests)
    
    with col4:
        st.metric("Completed", completed_requests)

    st.divider()

    # -----------------------------
    # PROCUREMENT REQUESTS
    # -----------------------------
    st.subheader("Maintenance Procurement Requests")

    st.dataframe(
        st.session_state.procurement_requests,
        use_container_width=True
    )

    st.divider()
    
    # -----------------------------
    # UPDATE EXISTING PROCUREMENT REQUEST
    # -----------------------------
    st.subheader("Update Procurement Request")

    request_options = [
        req["Request ID"]
        for req in st.session_state.procurement_requests
        if req["Status"] != "Completed"
    ]

    if request_options:

        selected_request_id = st.selectbox(
            "Select Existing Request",
            request_options,
            key="update_procurement_request"
        )

        selected_request = next(
            req for req in st.session_state.procurement_requests
            if req["Request ID"] == selected_request_id
        )

        with st.container(border=True):

            st.write(f"**CM ID:** {selected_request['CM ID']}")
            st.write(f"**WO ID:** {selected_request['WO ID']}")
            st.write(f"**Asset:** {selected_request['Asset']}")
            st.write(f"**Requirement:** {selected_request['Requirement']}")
            st.write(f"**Current Status:** {selected_request['Status']}")

            updated_document = st.selectbox(
                "Procurement Document",
                ["Pending", "PR", "IER"],
                index=(
                    ["Pending", "PR", "IER"].index(
                        selected_request["Document"]
                    )
                    if selected_request["Document"] in ["Pending", "PR", "IER"]
                    else 0
                ),
                key="update_procurement_document"
            )

            updated_status = st.selectbox(
                "New Procurement Status",
                [
                    "New",
                    "Pending Engineer Review",
                    "Pending Approval",
                    "PR / IER Issued",
                    "PO Issued",
                    "Completed"
                ],
                key="update_procurement_status"
            )

            if st.button(
                "Update Procurement Request",
                type="primary"
            ):

                
                selected_request["Document"] = updated_document
                selected_request["Status"] = updated_status

                # Update related CM when procurement is completed
                if updated_status == "Completed":

                    related_cm = next(
                        (
                            cm for cm in st.session_state.corrective_maintenance
                            if cm["CM ID"] == selected_request["CM ID"]
                        ),
                        None
                    )

                    if related_cm is not None:
                        related_cm["Procurement Status"] = "Completed"

                st.success(
                    f"{selected_request_id} updated to {updated_status}."
                )

                st.rerun()

    else:
        st.info("No active procurement requests available.")

    st.divider()

    
    # -----------------------------
    # PROCUREMENT DOCUMENT UPLOAD
    # -----------------------------
    st.subheader("Procurement Document Attachments")

    with st.container(border=True):

        document_request_id = st.selectbox(
            "Select Procurement Request",
            [
                req["Request ID"]
                for req in st.session_state.procurement_requests
            ],
            key="document_request_id"
        )

        document_type = st.selectbox(
            "Document Type",
            [
                "PR / IER",
                "Supplier Quotation",
                "Purchase Order (PO)",
                "Delivery Order (DO)",
                "Invoice",
                "Other Supporting Document"
            ],
            key="document_upload_type"
        )

        uploaded_file = st.file_uploader(
            "Upload Document",
            type=["pdf", "docx", "xlsx", "jpg", "jpeg", "png"],
            key="procurement_file_upload"
        )

        if st.button("Save Attachment"):

            if uploaded_file is not None:

                new_document = {
                    "Request ID": document_request_id,
                    "Document Type": document_type,
                    "Filename": uploaded_file.name,
                    "File Content": uploaded_file.getvalue(),
                    "Uploaded On": pd.Timestamp.today().strftime("%d %b %Y")
                }

                st.session_state.procurement_documents.append(
                    new_document
                )

                st.success(
                    f"{uploaded_file.name} attached to {document_request_id}."
                )

            else:
                st.error("Please select a document to upload.")

    
    # -----------------------------
    # PROCUREMENT DOCUMENT REGISTER
    # -----------------------------
    st.subheader("Uploaded Procurement Documents")

    saved_documents = [
        doc
        for doc in st.session_state.procurement_documents
        if doc["Request ID"] == document_request_id
    ]

    if saved_documents:

        document_table = [
            {
                "Document Type": doc["Document Type"],
                "Filename": doc["Filename"],
                "Uploaded On": doc["Uploaded On"]
            }
            for doc in saved_documents
        ]

        st.dataframe(
            document_table,
            use_container_width=True
        )

        selected_document_name = st.selectbox(
            "Select Document to Download",
            [
                f"{i + 1}. {doc['Filename']}"
                for i, doc in enumerate(saved_documents)
            ],
            key="download_procurement_document"
        )

        selected_index = int(
            selected_document_name.split(".")[0]
        ) - 1

        selected_document = saved_documents[selected_index]

        st.download_button(
            "Download Selected Document",
            data=selected_document["File Content"],
            file_name=selected_document["Filename"],
            mime="application/octet-stream",
            key="download_procurement_attachment"
        )

    else:
        st.info("No documents uploaded for this procurement request.")
    
    st.divider()
    
    # -----------------------------
    # PROCUREMENT REQUEST DETAILS
    # -----------------------------
    st.subheader("Process Procurement Request")

    with st.container(border=True):

        col1, col2 = st.columns(2)

        with col1:
            request_id = st.text_input("Request ID")

            cm_options = [
                cm["CM ID"]
                for cm in st.session_state.corrective_maintenance
                if cm["Procurement"] == "Required"
            ]
            
            cm_reference = st.selectbox(
                "Corrective Maintenance Reference",
                cm_options
            )
            
            selected_cm = next(
                cm for cm in st.session_state.corrective_maintenance
                if cm["CM ID"] == cm_reference
            )
            
            asset = selected_cm["Asset"]
            wo_reference = selected_cm["WO ID"]
            
            st.text_input(
                "Asset",
                value=asset,
                disabled=True
            )
            
            st.text_input(
                "Related Work Order",
                value=wo_reference,
                disabled=True
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

                new_request = {
                    "Request ID": request_id,
                    "CM ID": cm_reference,
                    "WO ID": wo_reference,
                    "Asset": asset,
                    "Requirement": requirement,
                    "Priority": priority,
                    "Document": document_type,
                    "Status": procurement_status
                }
        
                st.session_state.procurement_requests.append(new_request)
        
                st.success(
                    f"Procurement Request {request_id} submitted successfully."
                )
        
                if generate_document:
                    st.success(
                        f"{document_type} generation initiated."
                    )
        
                st.rerun()
        
            else:
                st.error(
                    "Request ID and Material / Service Required are required."
                )

elif page == "Maintenance History":

    st.title("Maintenance History")
    st.caption("Completed preventive and corrective maintenance records")

    

    history_df = pd.DataFrame(
        st.session_state.maintenance_history
    )

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

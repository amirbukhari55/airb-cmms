import streamlit as st
import pandas as pd
from supabase import create_client
import json

# -----------------------------
# ADMIN LOGIN
# -----------------------------

import hmac

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:

    st.title("AIRB CMMS Login")
    st.caption("Authorised access only")

    with st.form("login_form"):
        password = st.text_input(
            "Administrator Password",
            type="password"
        )

        login_clicked = st.form_submit_button("Login")

        if login_clicked:
            if hmac.compare_digest(
                password,
                st.secrets["auth"]["admin_password"]
            ):
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Incorrect password.")

    st.stop()

with st.sidebar:
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()


# -----------------------------
# SUPABASE CONNECTION TEST
# -----------------------------

@st.cache_resource
def get_supabase_client():
    return create_client(
        st.secrets["supabase"]["url"],
        st.secrets["supabase"]["key"]
    )

supabase = get_supabase_client()

with st.sidebar.expander("Database Connection", expanded=False):
    
    if st.button("Test Supabase Connection"):
        try:
            result = (
                supabase.table("sites")
                .select("site_id, site_name, site_data")
                .execute()
            )
    
            st.write("Records returned:", len(result.data or []))
            st.json(result.data or [])
    
            if result.data:
                st.success("Supabase connected and site records are readable.")
            else:
                st.warning(
                    "Supabase connection works, but no site records are visible "
                    "to the configured database key."
                )
    
        except Exception as e:
            st.error(f"Database query failed: {e}")

# -----------------------------
# SESSION DATA
# -----------------------------




# --------------------------------
# LOAD SITES FROM SUPABASE
# --------------------------------

try:
    response = (
        supabase.table("sites")
        .select("site_id, site_name, site_data")
        .order("site_id")
        .execute()
    )

    loaded_sites = []

    for row in response.data or []:

        # Convert a JSON string into a dictionary if necessary.
        if isinstance(row, str):
            try:
                row = json.loads(row)
            except (json.JSONDecodeError, TypeError):
                continue

        if not isinstance(row, dict):
            continue

        site = row.get("site_data") or {}

        if isinstance(site, str):
            try:
                site = json.loads(site)
            except (json.JSONDecodeError, TypeError):
                site = {}

        if not isinstance(site, dict):
            site = {}

        loaded_sites.append({
            "Site ID": row.get("site_id", ""),
            "Site Name": row.get("site_name", ""),
            "Location": site.get("Location", ""),
            "Plant Type": site.get("Plant Type", "Other"),
            "Status": site.get("Status", "Active")
        })

    st.session_state.sites = loaded_sites

except Exception as e:
    st.error(f"Unable to load sites from Supabase: {e}")
    st.stop()


if "assets" not in st.session_state:
    try:
        response = (
            supabase.table("assets")
            .select("asset_id, site_id, asset_data")
            .order("asset_id")
            .execute()
        )

        loaded_assets = []

        for row in response.data or []:
            asset = row.get("asset_data") or {}

            if isinstance(asset, str):
                asset = json.loads(asset)

            if not isinstance(asset, dict):
                asset = {}

            asset["Asset ID"] = row["asset_id"]
            asset["Site ID"] = row["site_id"]

            loaded_assets.append(asset)

        st.session_state.assets = loaded_assets

    except Exception as e:
        st.error(f"Unable to load assets from Supabase: {e}")
        st.stop()
    
if "pm_schedules" not in st.session_state:
    st.session_state.pm_schedules = []
    

if "work_orders" not in st.session_state:
    try:
        response = (
            supabase.table("work_orders")
            .select("wo_id, site_id, wo_data")
            .order("wo_id")
            .execute()
        )

        loaded_work_orders = []

        for row in response.data or []:
            wo = row.get("wo_data") or {}

            if isinstance(wo, str):
                wo = json.loads(wo)

            wo["WO ID"] = row["wo_id"]
            wo["Site ID"] = row["site_id"]

            loaded_work_orders.append(wo)

        st.session_state.work_orders = loaded_work_orders

    except Exception as e:
        st.error(f"Unable to load work orders from Supabase: {e}")
        st.stop()
    
if "corrective_maintenance" not in st.session_state:
    st.session_state.corrective_maintenance = []
    
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

if "cm_procurement_loaded" not in st.session_state:
    try:
        cm_response = (
            supabase.table("corrective_maintenance")
            .select("cm_id, site_id, cm_data")
            .execute()
        )

        st.session_state.corrective_maintenance = []

        for row in cm_response.data or []:
            record = row.get("cm_data") or {}
            record["CM ID"] = row["cm_id"]
            record["Site ID"] = row["site_id"]
            st.session_state.corrective_maintenance.append(record)

        procurement_response = (
            supabase.table("procurement_requests")
            .select("request_id, site_id, request_data")
            .execute()
        )

        st.session_state.procurement_requests = []

        for row in procurement_response.data or []:
            record = row.get("request_data") or {}
            record["Request ID"] = row["request_id"]
            record["Site ID"] = row["site_id"]
            st.session_state.procurement_requests.append(record)

        st.session_state.cm_procurement_loaded = True

    except Exception as e:
        st.error(f"Unable to load CM / Procurement records: {e}")
        st.stop()
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

# --------------------------------
# SITE SELECTION
# --------------------------------
site_options = {
    "ALL": "All Sites (Management View)"
}

for site in st.session_state.sites:
    if site["Status"] == "Active":
        site_options[site["Site ID"]] = (
            f"{site['Site ID']} - {site['Site Name']}"
        )

selected_site_id = st.sidebar.selectbox(
    "Select Operational Site",
    options=list(site_options.keys()),
    format_func=lambda site_id: site_options[site_id],
    key="selected_site_id"
)

st.sidebar.caption(
    f"Current view: {site_options[selected_site_id]}"
)

st.sidebar.divider()

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "navigate_to" in st.session_state:
    st.session_state.page = st.session_state.pop("navigate_to")

page = st.sidebar.radio(
    "Navigation",
    
[
    "Dashboard",
    "Site Master",
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

    today = pd.Timestamp.today().date()

    # --------------------------------
    # SITE FILTERING
    # --------------------------------
    if selected_site_id == "ALL":
        dashboard_assets = st.session_state.assets
        dashboard_pm = st.session_state.pm_schedules
        dashboard_wo = st.session_state.work_orders
        dashboard_cm = st.session_state.corrective_maintenance
        dashboard_procurement = st.session_state.procurement_requests

        st.info("Management View — Consolidated performance across all sites")

    else:
        dashboard_assets = [
            asset for asset in st.session_state.assets
            if asset.get("Site ID") == selected_site_id
        ]

        dashboard_pm = [
            pm for pm in st.session_state.pm_schedules
            if pm.get("Site ID") == selected_site_id
        ]

        dashboard_wo = [
            wo for wo in st.session_state.work_orders
            if wo.get("Site ID") == selected_site_id
        ]

        dashboard_cm = [
            cm for cm in st.session_state.corrective_maintenance
            if cm.get("Site ID") == selected_site_id
        ]

        dashboard_procurement = [
            req for req in st.session_state.procurement_requests
            if req.get("Site ID") == selected_site_id
        ]

        site_name = next(
            (
                site["Site Name"]
                for site in st.session_state.sites
                if site["Site ID"] == selected_site_id
            ),
            selected_site_id
        )

        st.info(f"Operational Site: {selected_site_id} - {site_name}")

    # --------------------------------
    # DYNAMIC DASHBOARD METRICS
    # --------------------------------
    active_pm = [
        pm for pm in dashboard_pm
        if pm.get("Status") == "Active"
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
        1 for wo in dashboard_wo
        if wo.get("Status") not in ["Completed", "Closed"]
    )

    open_cm = sum(
        1 for cm in dashboard_cm
        if cm.get("Status") not in ["Completed", "Closed"]
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("PM Due Today", pm_due)
    col2.metric("Overdue PM", overdue_pm)
    col3.metric("Open Work Orders", open_wo)
    col4.metric("Open Corrective Maintenance", open_cm)

    st.divider()

    # --------------------------------
    # MAINTENANCE OVERVIEW
    # --------------------------------
    st.subheader("Maintenance Overview")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Registered Assets", len(dashboard_assets))

    with col2:
        st.metric(
            "Completed Work Orders",
            sum(
                1 for wo in dashboard_wo
                if wo.get("Status") in ["Completed", "Closed"]
            )
        )

    with col3:
        st.metric(
            "Pending Engineer Review",
            sum(
                1 for wo in dashboard_wo
                if wo.get("Status") == "Pending Engineer Review"
            )
        )

    with col4:
        st.metric(
            "Pending Procurement",
            sum(
                1 for req in dashboard_procurement
                if req.get("Status") != "Completed"
            )
        )

    st.divider()

    # --------------------------------
    # MANAGEMENT VIEW - SITE PERFORMANCE
    # --------------------------------
    if selected_site_id == "ALL":

        st.subheader("Operational Site Performance")

        site_summary = []

        for site in st.session_state.sites:

            site_id = site["Site ID"]

            site_assets = [
                asset for asset in st.session_state.assets
                if asset.get("Site ID") == site_id
            ]

            site_pm = [
                pm for pm in st.session_state.pm_schedules
                if pm.get("Site ID") == site_id
                and pm.get("Status") == "Active"
            ]

            site_wo = [
                wo for wo in st.session_state.work_orders
                if wo.get("Site ID") == site_id
            ]

            site_cm = [
                cm for cm in st.session_state.corrective_maintenance
                if cm.get("Site ID") == site_id
            ]

            site_procurement = [
                req for req in st.session_state.procurement_requests
                if req.get("Site ID") == site_id
            ]

            site_summary.append({
                "Site ID": site_id,
                "Site Name": site["Site Name"],
                "Assets": len(site_assets),
                "Active PM": len(site_pm),
                "Overdue PM": sum(
                    1 for pm in site_pm
                    if pd.to_datetime(
                        pm["Next Due Date"]
                    ).date() < today
                ),
                "Open WO": sum(
                    1 for wo in site_wo
                    if wo.get("Status") not in ["Completed", "Closed"]
                ),
                "Pending Review": sum(
                    1 for wo in site_wo
                    if wo.get("Status") == "Pending Engineer Review"
                ),
                "Open CM": sum(
                    1 for cm in site_cm
                    if cm.get("Status") not in ["Completed", "Closed"]
                ),
                "Pending Procurement": sum(
                    1 for req in site_procurement
                    if req.get("Status") != "Completed"
                )
            })

        st.dataframe(
            site_summary,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

    # --------------------------------
    # UPCOMING PREVENTIVE MAINTENANCE
    # --------------------------------
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
            "Site ID": pm.get("Site ID", "Unassigned"),
            "PM Schedule ID": pm.get("PM Schedule ID"),
            "Asset": pm.get("Asset"),
            "Maintenance Type": pm.get("Maintenance Type"),
            "Frequency": pm.get("Frequency"),
            "Due Date": pm.get("Next Due Date"),
            "Assigned Technician": pm.get("Assigned Technician"),
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

    # --------------------------------
    # WORK ORDERS REQUIRING ATTENTION
    # --------------------------------
    st.subheader("Work Orders Requiring Attention")

    attention_wos = [
        wo for wo in dashboard_wo
        if wo.get("Status") in [
            "Assigned",
            "Open",
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


elif page == "Site Master":

    st.title("Site Master")
    st.caption("Register and manage AIRB operational sites.")

    # --------------------------------
    # SITE DATABASE
    # --------------------------------
    

    # --------------------------------
    # REGISTERED SITES
    # --------------------------------
    st.subheader("Registered Sites")

    st.dataframe(
        st.session_state.sites,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    # --------------------------------
    # CREATE NEW SITE
    # --------------------------------
    st.subheader("Register New Site")

    with st.form("site_master_form"):

        site_id = st.text_input("Site ID")

        site_name = st.text_input("Site Name")

        location = st.text_input("Location")

        plant_type = st.selectbox(
            "Plant Type",
            [
                "WTP",
                "WWTP",
                "STP",
                "WRP",
                "Desalination",
                "Other"
            ]
        )

        status = st.selectbox(
            "Status",
            ["Active", "Inactive"]
        )

        submitted = st.form_submit_button("Register Site")

        if submitted:

            clean_site_id = site_id.strip()

            if not clean_site_id or not site_name.strip():
                st.error("Site ID and Site Name are required.")

            elif any(
                site["Site ID"] == clean_site_id
                for site in st.session_state.sites
            ):
                st.error("This Site ID already exists.")
 
            else:
                new_site = {
                    "Site ID": clean_site_id,
                    "Site Name": site_name.strip(),
                    "Location": location.strip(),
                    "Plant Type": plant_type,
                    "Status": status
                }

                try:
                    result = supabase.table("sites").insert({
                        "site_id": clean_site_id,
                        "site_name": site_name.strip(),
                        "site_data": {
                            "Location": location.strip(),
                            "Plant Type": plant_type,
                            "Status": status
                        }
                    }).execute()
                    
                    if not result.data:
                        st.error(
                            "Supabase did not return an inserted record. "
                            "Check database permissions and RLS policies."
                        )
                        st.stop()

                    st.session_state.sites.append(new_site)

                    st.session_state.site_success_message = (
                        f"Site {clean_site_id} registered successfully."
                    )

                    st.rerun()

                except Exception as e:
                    st.error(f"Unable to register site: {e}")

    if "site_success_message" in st.session_state:
        st.success(st.session_state.pop("site_success_message"))

elif page == "Asset Register":
    st.title("Asset Register")
    st.caption("Register and manage plant assets and equipment.")

    # --------------------------------
    # IMPORT ASSET MASTERLIST
    # --------------------------------
    st.subheader("Import Asset Masterlist")

    uploaded_asset_file = st.file_uploader(
        "Upload AIRB Asset Masterlist",
        type=["xlsx"],
        key="asset_masterlist_upload"
    )

    if uploaded_asset_file is not None:

        import_df = pd.read_excel(
            uploaded_asset_file,
            sheet_name="Raw Data",
            header=6
        )

        # Remove completely empty rows.
        import_df = import_df.dropna(how="all")
        
        st.write("### Sites Found in Excel")

        site_summary = (
            import_df.groupby("Site", dropna=False)
            .size()
            .reset_index(name="Asset Count")
        )

        st.dataframe(
            site_summary,
            use_container_width=True,
            hide_index=True
        )

        # Keep rows with an equipment tag.
        import_df = import_df[
            import_df["Tag No"].notna()
        ].copy()

        st.success(
            f"Excel loaded successfully: {len(import_df)} asset records found."
        )

        st.dataframe(
            import_df,
            use_container_width=True,
            hide_index=True
        )
        
        if st.button("Import Assets into CMMS", type="primary"):

            imported_count = 0
            skipped_count = 0
            new_sites_count = 0

            # Register sites found in Excel.
            for site_name in import_df["Site"].dropna().unique():

                site_name = str(site_name).strip()

                existing_site = next(
                    (
                        site for site in st.session_state.sites
                        if site["Site Name"] == site_name
                    ),
                    None
                )

                if existing_site is None:

                    new_site_id = f"SITE-{len(st.session_state.sites) + 1:03d}"

                    st.session_state.sites.append({
                        "Site ID": new_site_id,
                        "Site Name": site_name,
                        "Location": "",
                        "Plant Type": "Other",
                        "Status": "Active"
                    })

                    new_sites_count += 1

            # Import equipment records.
            for _, row in import_df.iterrows():

                asset_id = str(row["Tag No"]).strip()
                site_name = str(row["Site"]).strip()

                site_record = next(
                    site for site in st.session_state.sites
                    if site["Site Name"] == site_name
                )

                existing_asset = any(
                    asset["Asset ID"] == asset_id
                    and asset.get("Site ID") == site_record["Site ID"]
                    for asset in st.session_state.assets
                )

                if existing_asset:
                    skipped_count += 1
                    continue

                st.session_state.assets.append({
                    "Asset ID": asset_id,
                    "Asset Name": str(row["Description"]).strip(),
                    "Site ID": site_record["Site ID"],
                    "Site": site_name,
                    "Location": str(row["Location"]),
                    "Asset Type": "Other",
                    "Status": "Active",
                    "Equipment Status": str(row["Status"])
                })

                imported_count += 1

            st.session_state.asset_import_message = (
                f"Import completed: {imported_count} assets added, "
                f"{skipped_count} duplicates skipped, "
                f"{new_sites_count} new sites registered."
            )

            st.rerun()

        if "asset_import_message" in st.session_state:
            st.success(st.session_state.pop("asset_import_message"))

    st.divider()

    # -----------------------------
    # REGISTERED ASSETS
    # -----------------------------
    st.subheader("Registered Assets")

    
    # Display assets for the selected operational site.
    if selected_site_id == "ALL":
        visible_assets = st.session_state.assets
    else:
        visible_assets = [
            asset for asset in st.session_state.assets
            if asset.get("Site ID") == selected_site_id
        ]

    assets_df = pd.DataFrame(visible_assets)

    st.caption(f"Displaying {len(visible_assets)} assets")

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

    # Identify the site selected in the sidebar.
    registration_site_id = selected_site_id

    if registration_site_id == "ALL":
        registration_site_id = st.selectbox(
            "Assign Asset to Site",
            options=[
                site["Site ID"]
                for site in st.session_state.sites
                if site["Status"] == "Active"
            ],
            format_func=lambda site_id: next(
                site["Site Name"]
                for site in st.session_state.sites
                if site["Site ID"] == site_id
            )
        )
    else:
        st.info(f"Registering asset under: {site_options[registration_site_id]}")

    with st.form("asset_form"):
        col1, col2 = st.columns(2)

        with col1:
            asset_id = st.text_input("Asset ID")
            asset_name = st.text_input("Asset Name")

            asset_type = st.selectbox(
                "Asset Type",
                [
                    "Pump",
                    "RO High-Pressure Pump",
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

            clean_asset_id = asset_id.strip()
            clean_asset_name = asset_name.strip()

            duplicate_asset = any(
                asset.get("Asset ID") == clean_asset_id
                and asset.get("Site ID") == registration_site_id
                for asset in st.session_state.assets
            )

            if not clean_asset_id or not clean_asset_name:
                st.error("Asset ID and Asset Name are required.")

            elif duplicate_asset:
                st.error(
                    f"Asset {clean_asset_id} already exists at this site."
                )

            else:
                site_name = next(
                    site["Site Name"]
                    for site in st.session_state.sites
                    if site["Site ID"] == registration_site_id
                )

                new_asset = {
                    "Asset ID": clean_asset_id,
                    "Asset Name": clean_asset_name,
                    "Site ID": registration_site_id,
                    "Site": site_name,
                    "Asset Type": asset_type,
                    "Location": location.strip(),
                    "Status": status,
                    "Manufacturer": manufacturer.strip()
                }
                
                try:
                    supabase.table("assets").upsert(
                        {
                            "asset_id": clean_asset_id,
                            "site_id": registration_site_id,
                            "asset_data": new_asset
                        },
                        on_conflict="asset_id,site_id"
                    ).execute()
                
                    st.session_state.assets.append(new_asset)
                
                except Exception as e:
                    st.error(f"Unable to save asset to Supabase: {e}")
                    st.stop()

                st.session_state.asset_success_message = (
                    f"Asset {clean_asset_id} registered successfully "
                    f"under {site_name}."
                )

                st.rerun()

    if "asset_success_message" in st.session_state:
        st.success(st.session_state.pop("asset_success_message"))



elif page == "PM Schedule":

    st.title("Preventive Maintenance Schedule")
    st.caption("Plan, assign and monitor preventive maintenance activities.")

    # --------------------------------
    # LOAD PM SCHEDULES FROM SUPABASE
    # --------------------------------
    try:
        response = (
            supabase.table("pm_schedules")
            .select("pm_schedule_id, site_id, pm_data")
            .order("pm_schedule_id")
            .execute()
        )

        loaded_pm = []

        for row in response.data or []:
            pm = row.get("pm_data") or {}

            if not isinstance(pm, dict):
                continue

            pm["PM Schedule ID"] = row["pm_schedule_id"]
            pm["Site ID"] = row["site_id"]

            if pm.get("Asset"):
                pm["Asset"] = str(pm["Asset"]).split(" - ")[0]

            loaded_pm.append(pm)

        st.session_state.pm_schedules = loaded_pm

    except Exception as e:
        st.error(f"Unable to load PM schedules from Supabase: {e}")
        st.stop()

    # --------------------------------
    # FILTER PM SCHEDULE BY SITE
    # --------------------------------
    if selected_site_id == "ALL":
        visible_pm = st.session_state.pm_schedules
    else:
        visible_pm = [
            pm for pm in st.session_state.pm_schedules
            if pm.get("Site ID") == selected_site_id
        ]

    # --------------------------------
    # DISPLAY PM SCHEDULE
    # --------------------------------
    st.subheader("Upcoming Preventive Maintenance")
    st.caption(f"Displaying {len(visible_pm)} PM schedules")

    st.dataframe(
        visible_pm,
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------
    # GENERATE WORK ORDERS
    # --------------------------------
    st.subheader("Generate Work Orders")

    
    if st.button("Generate Work Orders for Due PM"):

        generated_count = 0
        today = pd.Timestamp.today().date()

        for pm in visible_pm:

            if pm.get("Status") not in ["Active", "Due", "Planned"]:
                continue

            if pd.to_datetime(pm["Next Due Date"]).date() > today:
                continue

            pm_id = pm["PM Schedule ID"]
            wo_id = f"WO-{pm_id}"

            # Check existing records, including those loaded from Supabase
            existing_wo = any(
                wo.get("PM Schedule ID") == pm_id
                or wo.get("WO ID") == wo_id
                for wo in st.session_state.work_orders
            )

            if existing_wo:
                continue

            new_wo = {
                "WO ID": wo_id,
                "PM Schedule ID": pm_id,
                "Site ID": pm.get("Site ID"),
                "Asset": pm["Asset"],
                "Work": pm["Task"],
                "Type": pm["Maintenance Type"],
                "Priority": "Normal",
                "Assigned To": pm["Assigned Technician"],
                "Status": "Assigned",
                "Estimated Hours": pm.get("Estimated Hours", 1.0)
            }

            # Save to Supabase before updating the app
            try:
                supabase.table("work_orders").insert({
                    "wo_id": wo_id,
                    "site_id": new_wo["Site ID"],
                    "wo_data": new_wo
                }).execute()

            except Exception as e:
                st.error(
                    f"Unable to save generated Work Order {wo_id}: {e}"
                )
                continue

            st.session_state.work_orders.append(new_wo)
            generated_count += 1

        if generated_count > 0:
            st.success(
                f"{generated_count} preventive maintenance work order(s) generated and saved."
            )
        else:
            st.info("No new due PM work orders to generate.")

    st.divider()

    # --------------------------------
    # CREATE PM SCHEDULE
    # --------------------------------
    st.subheader("Create PM Schedule")

    if selected_site_id == "ALL":
        st.info(
            "Select an operational site from the sidebar "
            "before creating a PM schedule."
        )

    else:
        site_assets = [
            item
            for item in st.session_state.assets
            if item.get("Site ID") == selected_site_id
            and item.get("Status") == "Active"
        ]

        asset_lookup = {
            f"{item['Asset ID']} - {item['Asset Name']}": item["Asset ID"]
            for item in site_assets
        }

        site_name = next(
            (
                site["Site Name"]
                for site in st.session_state.sites
                if site["Site ID"] == selected_site_id
            ),
            selected_site_id
        )

        st.info(
            f"Creating PM schedule under: {selected_site_id} - {site_name}"
        )

        if not asset_lookup:
            st.warning(
                "No active assets registered under this site. "
                "Register or import assets first."
            )

        else:
            with st.form("pm_schedule_form"):

                col1, col2 = st.columns(2)

                with col1:
                    pm_id = st.text_input("PM Schedule ID")

                    asset = st.selectbox(
                        "Asset",
                        list(asset_lookup.keys())
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

                submitted = st.form_submit_button(
                    "Create PM Schedule"
                )

            if submitted:

                clean_pm_id = pm_id.strip()

                if not clean_pm_id or not task.strip():
                    st.error(
                        "PM Schedule ID and PM Task Name are required."
                    )

                elif any(
                    pm.get("PM Schedule ID") == clean_pm_id
                    for pm in st.session_state.pm_schedules
                ):
                    st.error("This PM Schedule ID already exists.")

                else:
                    new_pm = {
                        "PM Schedule ID": clean_pm_id,
                        "Site ID": selected_site_id,
                        "Asset": asset_lookup[asset],
                        "Task": task.strip(),
                        "Maintenance Type": maintenance_type,
                        "Frequency": frequency,
                        "Next Due Date": start_date.strftime("%Y-%m-%d"),
                        "Assigned Technician": technician,
                        "Estimated Hours": duration,
                        "Instructions": instructions,
                        "Status": "Active"
                    }

                    try:
                        (
                            supabase.table("pm_schedules")
                            .insert({
                                "pm_schedule_id": clean_pm_id,
                                "site_id": selected_site_id,
                                "pm_data": new_pm
                            })
                            .execute()
                        )

                        st.session_state.pm_success_message = (
                            f"PM Schedule {clean_pm_id} saved successfully "
                            f"under {site_name}."
                        )

                        st.rerun()

                    except Exception as e:
                        st.error(
                            f"Unable to save PM schedule to Supabase: {e}"
                        )

    if "pm_success_message" in st.session_state:
        st.success(st.session_state.pop("pm_success_message"))

                
elif page == "Work Orders":
    st.title("Work Orders")
    st.caption("Manage and track maintenance work orders.")

    # --------------------------------
    # WORK ORDER DATABASE
    # --------------------------------
    
    # --------------------------------
    # FILTER WORK ORDERS BY SITE
    # --------------------------------
    if selected_site_id == "ALL":
        site_work_orders = st.session_state.work_orders
    else:
        site_work_orders = [
            wo for wo in st.session_state.work_orders
            if wo.get("Site ID") == selected_site_id
        ]    

    # --------------------------------
    # WORK ORDER SUMMARY
    # --------------------------------
    open_count = sum(
        1 for wo in site_work_orders
        if wo["Status"] == "Open"
    )

    progress_count = sum(
        1 for wo in site_work_orders
        if wo["Status"] == "In Progress"
    )

    review_count = sum(
        1 for wo in site_work_orders
        if wo["Status"] == "Pending Engineer Review"
    )

    completed_count = sum(
        1 for wo in site_work_orders
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
        wo for wo in site_work_orders
        if wo["Status"] not in ["Completed", "Closed"]
    ]

    st.dataframe(
        [
            {
                "WO ID": wo.get("WO ID"),
                "Asset": wo.get("Asset"),
                "Work": wo.get("Work"),
                "Type": wo.get("Type"),
                "Status": wo.get("Status"),
                "Priority": wo.get("Priority"),
                "Assigned To": wo.get("Assigned To"),
                "Estimated Hours": wo.get("Estimated Hours"),
                "Actual Hours": wo.get("Actual Hours", 0),
            }
            for wo in active_work_orders
        ],
        use_container_width=True,
        hide_index=True
    )

    st.divider()
    
    
    # -----------------------------
    # MAINTENANCE DOCUMENT ATTACHMENTS
    # -----------------------------
    st.subheader("Maintenance Document Attachments")

    from uuid import uuid4
    from pathlib import Path

    STORAGE_BUCKET = "maintenance-documents"

    with st.container(border=True):

        document_wo_records = [
            wo for wo in st.session_state.work_orders
            if selected_site_id == "ALL"
            or wo.get("Site ID") == selected_site_id
        ]
        
        document_wo_options = [
            wo["WO ID"]
            for wo in document_wo_records
        ]

        document_wo_id = st.selectbox(
            "Select Work Order for Attachment",
            document_wo_options,
            key=f"maintenance_document_wo_{selected_site_id}",
            placeholder="No work orders available"
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

        if st.button(
            "Save Maintenance Attachment",
            disabled=not document_wo_options
        ):

            if uploaded_maintenance_file is None:
                st.error("Please select a document to upload.")

            else:
                selected_document_wo = next(
                    wo for wo in document_wo_records
                    if wo["WO ID"] == document_wo_id
                )

                document_site_id = selected_document_wo["Site ID"]

                filename = Path(
                    uploaded_maintenance_file.name
                ).name

                file_extension = Path(filename).suffix.lower()

                storage_path = (
                    f"{document_site_id}/"
                    f"{document_wo_id}/"
                    f"{uuid4().hex}{file_extension}"
                )

                file_content = uploaded_maintenance_file.getvalue()

                try:
                    # 1. Upload actual file to private Storage bucket
                    supabase.storage.from_(
                        STORAGE_BUCKET
                    ).upload(
                        path=storage_path,
                        file=file_content,
                        file_options={
                            "content-type": (
                                uploaded_maintenance_file.type
                                or "application/octet-stream"
                            ),
                            "upsert": "false"
                        }
                    )

                except Exception as e:
                    st.error(
                        f"Unable to upload document to Storage: {e}"
                    )

                else:
                    try:
                        # 2. Save document details in database
                        supabase.table(
                            "maintenance_documents"
                        ).insert({
                            "wo_id": document_wo_id,
                            "site_id": document_site_id,
                            "document_type": document_type,
                            "filename": filename,
                            "storage_path": storage_path
                        }).execute()

                    except Exception as e:

                        # Remove uploaded file if database save fails
                        try:
                            supabase.storage.from_(
                                STORAGE_BUCKET
                            ).remove([storage_path])
                        except Exception:
                            pass

                        st.error(
                            f"Unable to save document record: {e}"
                        )

                    else:
                        st.success(
                            f"{filename} attached to {document_wo_id}."
                        )

    # -----------------------------
    # MAINTENANCE DOCUMENT REGISTER
    # -----------------------------
    st.subheader("Uploaded Maintenance Documents")

    if document_wo_id is None:

        st.info("No work orders available for document selection.")

    else:

        try:
            document_result = (
                supabase.table("maintenance_documents")
                .select("*")
                .eq("wo_id", document_wo_id)
                .eq(
                    "site_id",
                    next(
                        wo["Site ID"]
                        for wo in document_wo_records
                        if wo["WO ID"] == document_wo_id
                    )
                )
                .order("uploaded_on", desc=True)
                .execute()
            )

            saved_maintenance_documents = document_result.data or []

        except Exception as e:
            saved_maintenance_documents = []
            st.error(
                f"Unable to retrieve maintenance documents: {e}"
            )

        if saved_maintenance_documents:

            maintenance_document_table = [
                {
                    "Document Type": doc["document_type"],
                    "Filename": doc["filename"],
                    "Uploaded On": doc["uploaded_on"]
                }
                for doc in saved_maintenance_documents
            ]

            st.dataframe(
                maintenance_document_table,
                use_container_width=True,
                hide_index=True
            )

            selected_maintenance_document = st.selectbox(
                "Select Document to Download",
                range(len(saved_maintenance_documents)),
                format_func=lambda i: (
                    saved_maintenance_documents[i]["filename"]
                ),
                key="download_maintenance_document"
            )

            selected_file = saved_maintenance_documents[
                selected_maintenance_document
            ]

            try:
                downloaded_content = (
                    supabase.storage.from_(
                        STORAGE_BUCKET
                    ).download(
                        selected_file["storage_path"]
                    )
                )

                st.download_button(
                    "Download Maintenance Document",
                    data=downloaded_content,
                    file_name=selected_file["filename"],
                    mime="application/octet-stream",
                    key="download_maintenance_attachment"
                )

            except Exception as e:
                st.error(
                    f"Unable to retrieve document from Storage: {e}"
                )

        else:
            st.info("No documents uploaded for this Work Order.")

    st.divider()

    # --------------------------------
    # EQUIPMENT-SPECIFIC PM TEMPLATES
    # --------------------------------
    PM_INSPECTION_TEMPLATES = {
        "Pump": [
            "Inspect pump and mechanical seal for leakage",
            "Check bearing temperature",
            "Check abnormal noise and vibration",
            "Check lubrication condition",
            "Record suction and discharge pressure",
            "Record motor current"
        ],
        "Blower": [
            "Inspect air filter condition",
            "Check belt condition and tension",
            "Check abnormal noise and vibration",
            "Record discharge pressure",
            "Check operating temperature",
            "Check lubrication condition"
        ],
        "RO High-Pressure Pump": [
            "Inspect mechanical seal for leakage",
            "Record suction pressure",
            "Record discharge pressure",
            "Check abnormal noise and vibration",
            "Record motor current",
            "Inspect pump and motor condition"
        ]
    }

    DEFAULT_PM_INSPECTION = [
        "Inspect equipment condition",
        "Check for leakage or visible damage",
        "Check abnormal noise or vibration",
        "Verify operating condition"
    ]
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
        # Identify equipment type from Asset Register
        selected_asset = next(
            (
                asset
                for asset in st.session_state.assets
                if asset.get("Asset ID") == selected_wo.get("Asset")
                and asset.get("Site ID") == selected_wo.get("Site ID")
            ),
            None
        )

        equipment_type = (
            selected_asset.get("Asset Type", "Other")
            if selected_asset
            else "Other"
        )

        asset_name = (
            selected_asset.get("Asset Name", selected_wo["Asset"])
            if selected_asset
            else selected_wo["Asset"]
        )

        # Identify the appropriate inspection checklist
        if equipment_type == "Pump" and "RO" in asset_name.upper():
            template_name = "RO High-Pressure Pump"
        else:
            template_name = equipment_type

        inspection_items = PM_INSPECTION_TEMPLATES.get(
            template_name,
            DEFAULT_PM_INSPECTION
        )
        # Load previously saved inspection results for this Work Order
        saved_inspection = selected_wo.get("Inspection Results", {})
        
        inspection_results = {}

        with st.container(border=True):
            st.caption(f"Equipment Type: {template_name}")
            st.caption(f"Inspection Template: {len(inspection_items)} checks")
            st.markdown("#### Equipment Inspection Checklist")

            for item in inspection_items:
            
                inspection_results[item] = st.selectbox(
                    item,
                    ["Not Checked", "Pass", "Fail", "Not Applicable"],
                    index=[
                        "Not Checked", "Pass", "Fail", "Not Applicable"
                    ].index(
                        saved_inspection.get(item, "Not Checked")
                        if saved_inspection.get(item, "Not Checked")
                        in ["Not Checked", "Pass", "Fail", "Not Applicable"]
                        else "Not Checked"
                    ),
                    key=f"inspection_{selected_wo_id}_{item}"
                )
            
            st.divider()
            st.write(
                f"**Asset:** {selected_wo['Asset']}"
            )

            st.write(
                f"**Work:** {selected_wo['Work']}"
            )

            saved_safety = selected_wo.get("Safety Checklist", {})

            # Initialise each WO's form only when first opened.
            # Do not overwrite values while the technician is editing.
            safety_defaults = {
                f"safety_ppe_{selected_wo_id}": saved_safety.get("PPE", False),
                f"safety_equipment_{selected_wo_id}": saved_safety.get(
                    "Equipment Status Confirmed", False
                ),
                f"safety_isolation_{selected_wo_id}": saved_safety.get(
                    "Isolation", "Not Verified"
                ),
                f"safety_permit_{selected_wo_id}": saved_safety.get(
                    "Permit / LOTO", "Not Verified"
                ),
                f"safety_remarks_{selected_wo_id}": saved_safety.get(
                    "Remarks", ""
                )
            }

            for field_key, saved_value in safety_defaults.items():
                if field_key not in st.session_state:
                    st.session_state[field_key] = saved_value
            # --------------------------------
            # A. SAFETY & PREPARATION
            # --------------------------------
            st.markdown("#### A. Safety & Preparation")

            st.caption(
                "Complete the applicable safety checks before starting maintenance."
            )

            safety_ppe = st.checkbox(
                "Appropriate PPE is available and worn",
                key=f"safety_ppe_{selected_wo_id}"
            )

            safety_equipment = st.checkbox(
                "Equipment status (ON/OFF) has been confirmed",
                key=f"safety_equipment_{selected_wo_id}"
            )

            safety_isolation = st.selectbox(
                "Electrical / mechanical isolation and zero-energy verification",
                ["Not Verified", "Verified", "Not Applicable"],
                key=f"safety_isolation_{selected_wo_id}"
            )

            safety_permit = st.selectbox(
                "Work permit / LOTO requirements",
                ["Not Verified", "Verified", "Not Applicable"],
                key=f"safety_permit_{selected_wo_id}"
            )

            safety_remarks = st.text_area(
                "Safety Remarks / Justification",
                key=f"safety_remarks_{selected_wo_id}"
            )

            st.divider()
            create_cm = st.button(
                "Create Corrective Maintenance",
                key="create_cm_from_wo"
            )

            
            if create_cm:
                failed_inspections = [
                    item
                    for item, result in inspection_results.items()
                    if result == "Fail"
                ]
            
                st.session_state.cm_from_wo = {
                    "WO ID": selected_wo["WO ID"],
                    "Asset": selected_wo["Asset"],
                    "Technician": selected_wo["Assigned To"],
                    "Site ID": selected_wo["Site ID"],
                    "Failed Inspections": failed_inspections
                }

                st.session_state.navigate_to = "Corrective Maintenance"

                st.rerun()
            
            
            status_options = [
                "Assigned",
                "In Progress",
                "Pending Engineer Review"
            ]
            
            new_status = st.selectbox(
                "New Status",
                status_options,
                index=status_options.index(selected_wo["Status"]),
                key=f"update_wo_status_{selected_wo_id}"
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

                # Save the safety checklist with this Work Order
                safety_record = {
                    "PPE": safety_ppe,
                    "Equipment Status Confirmed": safety_equipment,
                    "Isolation": safety_isolation,
                    "Permit / LOTO": safety_permit,
                    "Remarks": safety_remarks.strip()
                }

                # Safety requirements must be completed before work proceeds
                safety_ready = (
                    safety_ppe
                    and safety_equipment
                    and safety_isolation != "Not Verified"
                    and safety_permit != "Not Verified"
                )

                na_selected = (
                    safety_isolation == "Not Applicable"
                    or safety_permit == "Not Applicable"
                )

                if (
                    new_status in ["In Progress", "Pending Engineer Review"]
                    and not safety_ready
                ):
                    st.error(
                        "Complete all applicable safety checks before proceeding."
                    )
                    st.stop()

                if na_selected and not safety_remarks.strip():
                    st.error(
                        "Provide a safety justification for any Not Applicable selection."
                    )
                    st.stop()

                # Require all inspection items to be checked before engineer review
                if new_status == "Pending Engineer Review":
                
                    unchecked_items = [
                        item for item, result in inspection_results.items()
                        if result == "Not Checked"
                    ]
                
                    failed_items = [
                        item for item, result in inspection_results.items()
                        if result == "Fail"
                    ]
                
                    if unchecked_items:
                        st.error(
                            "Complete all inspection items before submitting "
                            "the Work Order for engineer review."
                        )
                        st.stop()
                
                    if failed_items:
                        st.error(
                            "Resolve the failed inspection items before submitting "
                            "the Work Order for engineer review."
                        )
                        st.stop()
                    
                    # Check all corrective maintenance records linked to this WO.
                    # A failed inspection cannot be bypassed by changing it to Pass.
                    linked_cm = [
                        cm for cm in st.session_state.corrective_maintenance
                        if cm.get("WO ID") == selected_wo_id
                        and cm.get("Site ID") == selected_wo.get("Site ID")
                    ]
                    
                    unresolved_cm = [
                        cm for cm in linked_cm
                        if cm.get("Status") != "Completed"
                        or cm.get("Engineer Decision") != "Approved"
                    ]
                    
                    if unresolved_cm:
                        st.error(
                            "This Work Order has unresolved corrective maintenance. "
                            "Complete engineer approval for all linked CM records "
                            "before submitting it for WO review."
                        )
                        st.stop()
                updated_wo = selected_wo.copy()
                updated_wo["Status"] = new_status
                updated_wo["Actual Hours"] = actual_hours
                updated_wo["Maintenance Remarks"] = maintenance_remarks
                updated_wo["Safety Checklist"] = safety_record
                updated_wo["Inspection Template"] = template_name
                updated_wo["Inspection Results"] = inspection_results

                try:
                    response = supabase.table("work_orders").update({
                        "wo_data": updated_wo
                    }).eq(
                        "wo_id", selected_wo_id
                    ).execute()

                    if not response.data:
                        st.error(
                            f"Work Order {selected_wo_id} was not found in Supabase."
                        )
                        st.stop()

                    selected_wo.update(updated_wo)

                except Exception as e:
                    st.error(f"Unable to update work order in Supabase: {e}")
                    st.stop()

                st.session_state.wo_success_message = (
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
        if wo.get("Status") == "Pending Engineer Review"
        and (
            selected_site_id == "ALL"
            or wo.get("Site ID") == selected_site_id
        )
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

                updated_wo = review_wo.copy()
                updated_wo["Status"] = "Closed"
                updated_wo["Engineer Remarks"] = engineer_remarks
                updated_wo["Review Date"] = (
                    pd.Timestamp.today().strftime("%d %b %Y")
                )

                try:
                    response = supabase.table("work_orders").update({
                        "wo_data": updated_wo
                    }).eq(
                        "wo_id", review_wo_id
                    ).execute()

                    if not response.data:
                        st.error(
                            f"Work Order {review_wo_id} was not found in Supabase."
                        )
                        st.stop()

                    review_wo.update(updated_wo)

                except Exception as e:
                    st.error(
                        f"Unable to close work order in Supabase: {e}"
                    )
                    st.stop()

                already_in_history = any(
                    record["WO ID"] == review_wo_id
                    for record in st.session_state.maintenance_history
                )

                if not already_in_history:

                    history_record = {
                        "Date": pd.Timestamp.today().strftime("%d %b %Y"),
                        "WO ID": review_wo_id,
                        "Site ID": review_wo.get("Site ID"),
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

                st.session_state.wo_success_message = (
                    f"Work Order {review_wo_id} approved and closed."
                )

                st.rerun()

            if return_wo:

                if engineer_remarks.strip():

                    updated_wo = review_wo.copy()
                    updated_wo["Status"] = "In Progress"
                    updated_wo["Engineer Remarks"] = engineer_remarks

                    try:
                        response = supabase.table("work_orders").update({
                            "wo_data": updated_wo
                        }).eq(
                            "wo_id", review_wo_id
                        ).execute()

                        if not response.data:
                            st.error(
                                f"Work Order {review_wo_id} was not found in Supabase."
                            )
                            st.stop()

                        review_wo.update(updated_wo)

                    except Exception as e:
                        st.error(
                            f"Unable to return work order in Supabase: {e}"
                        )
                        st.stop()

                    st.session_state.wo_success_message = (
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
    
    if "wo_success_message" in st.session_state:
        st.success(st.session_state.pop("wo_success_message"))

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
                    "Site ID": selected_site_id,
                    "Asset": asset_id,
                    "Work": work_description,
                    "Type": maintenance_type,
                    "Priority": priority,
                    "Assigned To": technician,
                    "Status": status,
                    "Estimated Hours": estimated_hours
                }
                
                try:
                    supabase.table("work_orders").insert({
                        "wo_id": wo_id,
                        "site_id": selected_site_id,
                        "wo_data": new_work_order
                    }).execute()

                    st.session_state.work_orders.append(new_work_order)

                except Exception as e:
                    st.error(f"Unable to save work order to Supabase: {e}")
                    st.stop()

                st.session_state.wo_success_message = (
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

    # --------------------------------
    # FILTER RECORDS BY SELECTED SITE
    # --------------------------------
    if selected_site_id == "ALL":
        site_work_orders = st.session_state.work_orders
        site_cm_records = st.session_state.corrective_maintenance
    else:
        site_work_orders = [
            wo for wo in st.session_state.work_orders
            if wo.get("Site ID") == selected_site_id
        ]

        site_cm_records = [
            cm for cm in st.session_state.corrective_maintenance
            if cm.get("Site ID") == selected_site_id
        ]

    # --------------------------------
    # UPDATE CORRECTIVE MAINTENANCE
    # --------------------------------
    st.subheader("Update Corrective Maintenance")

    active_cm = [
        cm for cm in site_cm_records
        if cm.get("Status") not in ["Completed", "Closed"]
    ]

    if active_cm:

        cm_options = [cm["CM ID"] for cm in active_cm]

        selected_cm_id = st.selectbox(
            "Select Corrective Maintenance",
            cm_options,
            key="update_cm_id"
        )

        selected_cm = next(
            cm for cm in active_cm
            if cm["CM ID"] == selected_cm_id
        )

        st.write(f"**Related WO:** {selected_cm['WO ID']}")
        st.write(f"**Problem:** {selected_cm['Problem']}")

        cm_status_options = [
            "Open",
            "In Progress",
            "Pending Engineer Review"
        ]

        updated_cm_status = st.selectbox(
            "New CM Status",
            cm_status_options,
            index=(
                cm_status_options.index(selected_cm["Status"])
                if selected_cm["Status"] in cm_status_options
                else 0
            )
        )

        updated_cm_action = st.text_area(
            "Corrective Action / Resolution",
            value=selected_cm.get("Corrective Action", ""),
            key=f"cm_action_{selected_cm_id}"
        )

        if st.button("Update Corrective Maintenance"):

            if (
                updated_cm_status in ["Pending Engineer Review", "Completed"]
                and not updated_cm_action.strip()
            ):
                st.error("Enter the corrective action before proceeding.")
                st.stop()
            if updated_cm_status == "Pending Engineer Review":

                if updated_cm_action.strip() == (
                    "Inspection finding recorded. Further investigation required."
                ):
                    st.error(
                        "Record the actual corrective work performed before "
                        "submitting for engineer review."
                    )
                    st.stop()

            updated_cm = selected_cm.copy()
            updated_cm["Status"] = updated_cm_status
            updated_cm["Corrective Action"] = updated_cm_action.strip()

            try:
                response = supabase.table(
                    "corrective_maintenance"
                ).update({
                    "cm_data": updated_cm
                }).eq(
                    "cm_id", selected_cm_id
                ).eq(
                    "site_id", selected_cm["Site ID"]
                ).execute()

                if not response.data:
                    st.error("CM record was not found in Supabase.")
                    st.stop()

                selected_cm.update(updated_cm)

            except Exception as e:
                st.error(f"Unable to update CM: {e}")
                st.stop()

            st.success(
                f"{selected_cm_id} updated to {updated_cm_status}."
            )
            st.rerun()

    else:
        st.info("No active CM records to update.")

    st.divider()

    # --------------------------------
    # ENGINEER REVIEW & APPROVAL
    # --------------------------------
    st.subheader("Engineer Review & Approval")

    pending_cm = [
        cm for cm in site_cm_records
        if cm.get("Status") == "Pending Engineer Review"
    ]

    if pending_cm:

        review_cm_id = st.selectbox(
            "Select CM for Engineer Review",
            [cm["CM ID"] for cm in pending_cm],
            key="engineer_review_cm"
        )

        review_cm = next(
            cm for cm in pending_cm
            if cm["CM ID"] == review_cm_id
        )

        with st.container(border=True):

            st.write(f"**CM ID:** {review_cm['CM ID']}")
            st.write(f"**Related WO:** {review_cm['WO ID']}")
            st.write(f"**Asset:** {review_cm['Asset']}")
            st.write(f"**Problem:** {review_cm['Problem']}")
            st.write(
                f"**Corrective Action:** "
                f"{review_cm.get('Corrective Action', '')}"
            )

            engineer_remarks = st.text_area(
                "Engineer Review Remarks",
                key=f"cm_engineer_remarks_{review_cm_id}"
            )

            col1, col2 = st.columns(2)

            with col1:
                approve_cm = st.button(
                    "Approve & Complete CM",
                    type="primary",
                    key=f"approve_cm_{review_cm_id}"
                )

            with col2:
                return_cm = st.button(
                    "Return for Rectification",
                    key=f"return_cm_{review_cm_id}"
                )

            if approve_cm or return_cm:

                if not engineer_remarks.strip():
                    st.error("Engineer review remarks are required.")
                    st.stop()

                updated_cm = review_cm.copy()

                if approve_cm:
                    updated_cm["Status"] = "Completed"
                    updated_cm["Engineer Decision"] = "Approved"
                else:
                    updated_cm["Status"] = "In Progress"
                    updated_cm["Engineer Decision"] = "Returned for Rectification"

                updated_cm["Engineer Review Remarks"] = (
                    engineer_remarks.strip()
                )

                updated_cm["Review Date"] = (
                    pd.Timestamp.now().isoformat()
                )

                try:
                    response = (
                        supabase.table("corrective_maintenance")
                        .update({"cm_data": updated_cm})
                        .eq("cm_id", review_cm_id)
                        .eq("site_id", review_cm["Site ID"])
                        .execute()
                    )

                    if not response.data:
                        st.error("CM record was not found in Supabase.")
                        st.stop()

                    review_cm.update(updated_cm)

                except Exception as e:
                    st.error(
                        f"Unable to save engineer review: {e}"
                    )
                    st.stop()

                st.session_state.cm_review_success = (
                    f"{review_cm_id}: "
                    f"{updated_cm['Engineer Decision']}."
                )

                st.rerun()

    else:
        st.info("No CM records pending engineer review.")

    if "cm_review_success" in st.session_state:
        st.success(
            st.session_state.pop("cm_review_success")
        )

    st.divider()

    # --------------------------------
    # OPEN CORRECTIVE MAINTENANCE
    # --------------------------------
    st.subheader("Open Corrective Maintenance")

    cm_display = []

    for cm in site_cm_records:
        cm_record = cm.copy()

        if cm.get("Procurement") == "Required":
            related_requests = [
                req
                for req in st.session_state.procurement_requests
                if req.get("CM ID") == cm.get("CM ID")
                and req.get("Site ID") == cm.get("Site ID")
            ]

            if related_requests:
                cm_record["Procurement Status"] = related_requests[-1]["Status"]
            else:
                cm_record["Procurement Status"] = "Pending Request"
        else:
            cm_record["Procurement Status"] = "Not Required"

        cm_display.append(cm_record)

    if cm_display:
        st.dataframe(cm_display, use_container_width=True)
    else:
        st.info("No corrective maintenance records for the selected site.")

    st.divider()

    # --------------------------------
    # CORRECTIVE MAINTENANCE FORM
    # --------------------------------
    st.subheader("Record Corrective Maintenance")

    if selected_site_id == "ALL":
        st.info(
            "Select an operational site from the sidebar "
            "before recording corrective maintenance."
        )

    else:
        wo_options = [
            wo["WO ID"]
            for wo in site_work_orders
            if wo.get("Status") not in ["Completed", "Closed"]
        ]

        if not wo_options:
            st.warning(
                "No active Work Orders are available under this site. "
                "Create a Work Order first."
            )

        else:
            with st.container(border=True):
                col1, col2 = st.columns(2)

                with col1:
                    cm_id = st.text_input("CM ID")

                    # Receive WO information from Work Orders page
                    cm_prefill = st.session_state.get("cm_from_wo", {})
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
                        wo for wo in site_work_orders
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

                failed_inspections = (
                    cm_prefill.get("Failed Inspections", [])
                    if cm_prefill.get("WO ID") == wo_id
                    else []
                )
                
                prefilled_problem = (
                    "Failed equipment inspection:\n"
                    + "\n".join(f"- {item}" for item in failed_inspections)
                    if failed_inspections
                    else ""
                )
                
                problem = st.text_area(
                    "Problem / Failure Description",
                    value=prefilled_problem,
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
                    clean_cm_id = cm_id.strip()

                    if not clean_cm_id or not problem.strip():
                        st.error(
                            "CM ID and Problem / Failure Description are required."
                        )

                    elif any(
                        cm.get("CM ID") == clean_cm_id
                        for cm in st.session_state.corrective_maintenance
                    ):
                        st.error(
                            f"Corrective Maintenance {clean_cm_id} already exists."
                        )

                    else:
                        new_cm = {
                            "CM ID": clean_cm_id,
                            "Site ID": selected_site_id,
                            "WO ID": wo_id,
                            "Asset": asset,
                            "Problem": problem.strip(),
                            "Failed Inspections": failed_inspections,
                            "Corrective Action": action.strip(),
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

                        # Prepare procurement request, if required.
                        new_procurement = None

                        if procurement_required == "Yes":
                            request_id = f"MPR-{clean_cm_id}"

                            new_procurement = {
                                "Request ID": request_id,
                                "Site ID": selected_site_id,
                                "CM ID": clean_cm_id,
                                "WO ID": wo_id,
                                "Asset": asset,
                                "Requirement": item_required.strip(),
                                "Justification": justification.strip(),
                                "Priority": priority,
                                "Document": "Pending",
                                "Status": "New"
                            }

                        # Save to Supabase before updating the screen.
                        try:
                            supabase.table("corrective_maintenance").insert({
                                "cm_id": clean_cm_id,
                                "site_id": selected_site_id,
                                "cm_data": new_cm
                            }).execute()

                        except Exception as e:
                            st.error(
                                f"Unable to save corrective maintenance "
                                f"to Supabase: {e}"
                            )
                            st.stop()

                        if new_procurement is not None:
                            try:
                                supabase.table("procurement_requests").insert({
                                    "request_id": request_id,
                                    "site_id": selected_site_id,
                                    "request_data": new_procurement
                                }).execute()

                            except Exception as e:
                                st.error(
                                    f"CM {clean_cm_id} was saved to Supabase, "
                                    f"but its procurement request was not. "
                                    f"Do not resubmit the same CM ID. "
                                    f"Error: {e}"
                                )
                                st.stop()

                        # Update current session after successful saves.
                        st.session_state.corrective_maintenance.append(new_cm)

                        if new_procurement is not None:
                            st.session_state.procurement_requests.append(
                                new_procurement
                            )

                        st.session_state.cm_success_message = (
                            f"Corrective Maintenance {clean_cm_id} "
                            f"submitted successfully."
                        )

                        st.session_state.pop("cm_from_wo", None)
                        st.rerun()

    if "cm_success_message" in st.session_state:
        st.success(st.session_state.pop("cm_success_message"))


elif page == "Procurement":
    st.title("Maintenance Procurement")
    st.caption("Manage PR / IER requests generated from maintenance activities.")

    # -----------------------------
    # SITE-SPECIFIC PROCUREMENT DATA
    # -----------------------------
    # Resolve site through the linked CM/WO for older records
    # that do not yet have a Site ID.

    def procurement_site_id(req):
        if req.get("Site ID"):
            return req["Site ID"]

        related_cm = next(
            (
                cm for cm in st.session_state.corrective_maintenance
                if cm.get("CM ID") == req.get("CM ID")
            ),
            None
        )

        if related_cm and related_cm.get("Site ID"):
            return related_cm["Site ID"]

        related_wo = next(
            (
                wo for wo in st.session_state.work_orders
                if wo.get("WO ID") == req.get("WO ID")
            ),
            None
        )

        return related_wo.get("Site ID") if related_wo else None

    
    site_requests = [
        req
        for req in st.session_state.procurement_requests
        if (
            selected_site_id == "ALL"
            or procurement_site_id(req) == selected_site_id
        )
    ]


    
    site_cm = [
        cm
        for cm in st.session_state.corrective_maintenance
        if (
            selected_site_id == "ALL"
            or cm.get("Site ID") == selected_site_id
        )
        and cm.get("Procurement") == "Required"
    ]


    # -----------------------------
    # PROCUREMENT SUMMARY
    # -----------------------------
    new_requests = sum(
        req.get("Status") == "New"
        for req in site_requests
    )

    pending_approval = sum(
        req.get("Status") in [
            "Pending Engineer Review",
            "Pending Approval"
        ]
        for req in site_requests
    )

    issued_requests = sum(
        req.get("Status") in [
            "PR / IER Issued",
            "PO Issued"
        ]
        for req in site_requests
    )

    completed_requests = sum(
        req.get("Status") == "Completed"
        for req in site_requests
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

    if site_requests:
        st.dataframe(
            site_requests,
            use_container_width=True
        )
    else:
        st.info("No procurement requests for the selected site.")

    st.divider()

    # -----------------------------
    # UPDATE EXISTING PROCUREMENT REQUEST
    # -----------------------------
    st.subheader("Update Procurement Request")

    request_options = [
        req["Request ID"]
        for req in site_requests
        if req.get("Status") != "Completed"
    ]

    if request_options:

        selected_request_id = st.selectbox(
            "Select Existing Request",
            request_options,
            key="update_procurement_request"
        )

        selected_request = next(
            req for req in site_requests
            if req["Request ID"] == selected_request_id
        )

        with st.container(border=True):

            st.write(f"**CM ID:** {selected_request['CM ID']}")
            st.write(f"**WO ID:** {selected_request['WO ID']}")
            st.write(f"**Asset:** {selected_request['Asset']}")
            st.write(f"**Requirement:** {selected_request['Requirement']}")
            st.write(f"**Current Status:** {selected_request['Status']}")

            document_options = ["Pending", "PR", "IER"]

            updated_document = st.selectbox(
                "Procurement Document",
                document_options,
                index=(
                    document_options.index(selected_request.get("Document"))
                    if selected_request.get("Document") in document_options
                    else 0
                ),
                key="update_procurement_document"
            )

            status_options = [
                "New",
                "Pending Engineer Review",
                "Pending Approval",
                "PR / IER Issued",
                "PO Issued",
                "Completed"
            ]

            updated_status = st.selectbox(
                "New Procurement Status",
                status_options,
                index=(
                    status_options.index(selected_request.get("Status"))
                    if selected_request.get("Status") in status_options
                    else 0
                ),
                key="update_procurement_status"
            )

            if st.button(
                "Update Procurement Request",
                type="primary"
            ):

                updated_request = selected_request.copy()
                updated_request["Document"] = updated_document
                updated_request["Status"] = updated_status

                try:
                    supabase.table("procurement_requests").update({
                        "request_data": updated_request
                    }).eq(
                        "request_id", selected_request_id
                    ).execute()

                    selected_request.update(updated_request)

                except Exception as e:
                    st.error(f"Unable to update procurement request in Supabase: {e}")
                    st.stop()

                if updated_status == "Completed":

                    related_cm = next(
                        (
                            cm
                            for cm in st.session_state.corrective_maintenance
                            if cm.get("CM ID") == selected_request["CM ID"]
                        ),
                        None
                    )

                    if related_cm is not None:
                        related_cm["Procurement Status"] = "Completed"

                st.session_state.procurement_success_message = (
                    f"{selected_request_id} updated to {updated_status}."
                )

                st.rerun()

    else:
        st.info("No active procurement requests for the selected site.")

    if "procurement_success_message" in st.session_state:
        st.success(
            st.session_state.pop("procurement_success_message")
        )

    st.divider()

    
    # -----------------------------
    # PROCUREMENT DOCUMENT UPLOAD
    # -----------------------------
    st.subheader("Procurement Document Attachments")

    from uuid import uuid4
    from pathlib import Path

    PROCUREMENT_STORAGE_BUCKET = "maintenance-documents"

    document_request_options = [
        req["Request ID"]
        for req in site_requests
    ]

    if document_request_options:

        with st.container(border=True):

            document_request_id = st.selectbox(
                "Select Procurement Request",
                document_request_options,
                key=f"document_request_id_{selected_site_id}"
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

                if uploaded_file is None:
                    st.error("Please select a document to upload.")

                else:
                    selected_document_request = next(
                        req for req in site_requests
                        if req["Request ID"] == document_request_id
                    )
                    
                    document_site_id = procurement_site_id(selected_document_request)
                    
                    filename = Path(uploaded_file.name).name
                    file_extension = Path(filename).suffix.lower()

                    storage_path = (
                        f"{document_site_id}/procurement/"
                        f"{document_request_id}/"
                        f"{uuid4().hex}{file_extension}"
                    )

                    file_content = uploaded_file.getvalue()

                    try:
                        # 1. Upload actual file to private Storage
                        supabase.storage.from_(
                            PROCUREMENT_STORAGE_BUCKET
                        ).upload(
                            path=storage_path,
                            file=file_content,
                            file_options={
                                "content-type": (
                                    uploaded_file.type
                                    or "application/octet-stream"
                                ),
                                "upsert": "false"
                            }
                        )

                    except Exception as e:
                        st.error(
                            f"Unable to upload procurement document: {e}"
                        )

                    else:
                        try:
                            # 2. Save document details in database
                            supabase.table(
                                "procurement_documents"
                            ).insert({
                                "request_id": document_request_id,
                                "site_id": document_site_id,
                                "document_type": document_type,
                                "filename": filename,
                                "storage_path": storage_path
                            }).execute()

                        except Exception as e:

                            # Remove file if database save fails
                            try:
                                supabase.storage.from_(
                                    PROCUREMENT_STORAGE_BUCKET
                                ).remove([storage_path])
                            except Exception:
                                pass

                            st.error(
                                f"Unable to save procurement document record: {e}"
                            )

                        else:
                            st.success(
                                f"{filename} attached to {document_request_id}."
                            )

        # -----------------------------
        # PROCUREMENT DOCUMENT REGISTER
        # -----------------------------
        st.subheader("Uploaded Procurement Documents")

        try:
            document_result = (
                supabase.table("procurement_documents")
                .select("*")
                .eq("request_id", document_request_id)
                .eq("site_id", procurement_site_id(
                    next(
                        req for req in site_requests
                        if req["Request ID"] == document_request_id
                    )
                ))
                .order("uploaded_on", desc=True)
                .execute()
            )

            saved_documents = document_result.data or []

        except Exception as e:
            saved_documents = []
            st.error(
                f"Unable to retrieve procurement documents: {e}"
            )

        if saved_documents:

            document_table = [
                {
                    "Document Type": doc["document_type"],
                    "Filename": doc["filename"],
                    "Uploaded On": doc["uploaded_on"]
                }
                for doc in saved_documents
            ]

            st.dataframe(
                document_table,
                use_container_width=True,
                hide_index=True
            )

            selected_document_index = st.selectbox(
                "Select Document to Download",
                range(len(saved_documents)),
                format_func=lambda i: saved_documents[i]["filename"],
                key=f"download_procurement_document_{selected_site_id}_{document_request_id}"
            )

            selected_document = saved_documents[
                selected_document_index
            ]

            try:
                downloaded_content = (
                    supabase.storage.from_(
                        PROCUREMENT_STORAGE_BUCKET
                    ).download(
                        selected_document["storage_path"]
                    )
                )

                st.download_button(
                    "Download Selected Document",
                    data=downloaded_content,
                    file_name=selected_document["filename"],
                    mime="application/octet-stream",
                    key="download_procurement_attachment"
                )

            except Exception as e:
                st.error(
                    f"Unable to retrieve procurement document from Storage: {e}"
                )

        else:
            st.info(
                "No documents uploaded for this procurement request."
            )

    else:
        st.info(
            "Create a procurement request for this site before uploading documents."
        )

    st.divider()

    # -----------------------------
    # PROCUREMENT REQUEST DETAILS
    # -----------------------------
    st.subheader("Process Procurement Request")

    if site_cm:

        with st.container(border=True):

            col1, col2 = st.columns(2)

            with col1:
                request_id = st.text_input("Request ID")

                cm_options = [
                    cm["CM ID"]
                    for cm in site_cm
                ]

                cm_reference = st.selectbox(
                    "Corrective Maintenance Reference",
                    cm_options
                )

                selected_cm = next(
                    cm for cm in site_cm
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

                clean_request_id = request_id.strip()

                if not clean_request_id or not requirement.strip():

                    st.error(
                        "Request ID and Material / Service Required are required."
                    )

                elif any(
                    req.get("Request ID") == clean_request_id
                    for req in st.session_state.procurement_requests
                ):

                    st.error(
                        f"Procurement Request {clean_request_id} already exists."
                    )

                else:

                    new_request = {
                        "Request ID": clean_request_id,
                        "Site ID": selected_site_id,
                        "CM ID": cm_reference,
                        "WO ID": wo_reference,
                        "Asset": asset,
                        "Requirement": requirement.strip(),
                        "Requirement Type": requirement_type,
                        "Justification": justification.strip(),
                        "Estimated Cost": estimated_cost,
                        "Priority": priority,
                        "Document": document_type,
                        "Status": procurement_status
                    }
                    try:
                        supabase.table("procurement_requests").insert({
                            "request_id": clean_request_id,
                            "site_id": selected_site_id,
                            "request_data": new_request
                        }).execute()
                    
                    except Exception as e:
                        st.error(
                            f"Unable to save procurement request in Supabase: {e}"
                        )
                    
                    else:
                        st.session_state.procurement_requests.append(
                            new_request
                        )
                    
                        st.session_state.procurement_success_message = (
                            f"Procurement Request {clean_request_id} submitted successfully."
                        )
                    
                        st.rerun()

    else:
        st.info(
            "No corrective maintenance requiring procurement for the selected site."
        )


elif page == "Maintenance History":

    st.title("Maintenance History")
    st.caption("Completed preventive and corrective maintenance records")

    # --------------------------------
    # BUILD HISTORY FROM CLOSED WORK ORDERS
    # --------------------------------
    history_records = []

    for wo in st.session_state.work_orders:

        if wo.get("Status") not in ["Closed", "Completed"]:
            continue

        if (
            selected_site_id != "ALL"
            and wo.get("Site ID") != selected_site_id
        ):
            continue

        history_records.append({
            "Date": wo.get("Review Date", ""),
            "WO ID": wo.get("WO ID", ""),
            "Site ID": wo.get("Site ID", ""),
            "Asset": wo.get("Asset", ""),
            "Maintenance Type": wo.get("Type", ""),
            "Work Description": wo.get("Work", ""),
            "Technician": wo.get("Assigned To", ""),
            "Downtime (hr)": wo.get("Actual Hours", 0) or 0,
            "Status": wo.get("Status", "")
        })

    # Retain existing history records without duplicating WOs
    existing_wo_ids = {
        record["WO ID"] for record in history_records
    }

    for record in st.session_state.maintenance_history:

        if record.get("WO ID") in existing_wo_ids:
            continue

        if (
            selected_site_id != "ALL"
            and record.get("Site ID") != selected_site_id
        ):
            continue

        history_records.append(record)

    history_df = pd.DataFrame(
        history_records,
        columns=[
            "Date",
            "WO ID",
            "Site ID",
            "Asset",
            "Maintenance Type",
            "Work Description",
            "Technician",
            "Downtime (hr)",
            "Status"
        ]
    )

    history_df["Downtime (hr)"] = pd.to_numeric(
        history_df["Downtime (hr)"],
        errors="coerce"
    ).fillna(0)

    # --------------------------------
    # SUMMARY
    # --------------------------------
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Completed Work Orders", len(history_df))

    with col2:
        st.metric(
            "Total Downtime",
            f"{history_df['Downtime (hr)'].sum():g} hr"
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

    # --------------------------------
    # MAINTENANCE RECORDS
    # --------------------------------
    st.subheader("Maintenance Records")

    search_asset = st.text_input(
        "Search Asset",
        placeholder="Example: PUMP-101"
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

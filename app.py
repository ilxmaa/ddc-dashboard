
import streamlit as st

st.set_page_config(
    page_title="DDC Dashboard",
    page_icon="🩺",
    layout="wide"
)

# -----------------------------
# DEMONSTRATION DATA ONLY
# -----------------------------
if "cases" not in st.session_state:
    st.session_state.cases = [
        {
            "Case ID": "DEMO-001",
            "Sample": "Blood culture",
            "Lab alert": "Gram-negative bacilli",
            "Status": "Awaiting review",
            "Elapsed hours": 2
        },
        {
            "Case ID": "DEMO-002",
            "Sample": "Blood culture",
            "Lab alert": "Yeast detected",
            "Status": "Under review",
            "Elapsed hours": 1
        },
        {
            "Case ID": "DEMO-003",
            "Sample": "Blood culture",
            "Lab alert": "Gram-positive cocci",
            "Status": "Review completed",
            "Elapsed hours": 4
        }
    ]

if "containment_checks" not in st.session_state:
    st.session_state.containment_checks = {
        "Isolation readiness reviewed": False,
        "Infection-control team notified": False,
        "Environmental cleaning plan reviewed": False,
        "Contact screening process reviewed": False
    }

# -----------------------------
# SIDEBAR
# -----------------------------
st.sidebar.title("🩺 DDC Dashboard")
st.sidebar.caption("Detect • Decide • Contain")

page = st.sidebar.radio(
    "Navigation",
    ["Overview", "1. Detect", "2. Decide", "3. Contain"]
)

st.sidebar.divider()
st.sidebar.info(
    "Educational prototype using fictional demonstration data. "
    "Not for clinical diagnosis or treatment decisions."
)

# -----------------------------
# HEADER
# -----------------------------
st.title("Detect → Decide → Contain")
st.caption(
    "A demonstration dashboard for a rapid laboratory alert, "
    "stewardship review and infection-control readiness pathway."
)

st.warning(
    "DEMO ONLY — All cases are fictional. "
    "This prototype does not provide medical advice or prescribe treatment."
)

# -----------------------------
# OVERVIEW
# -----------------------------
if page == "Overview":

    st.subheader("Project overview")

    cases = st.session_state.cases
    open_alerts = sum(
        case["Status"] != "Review completed" for case in cases
    )
    completed = sum(
        case["Status"] == "Review completed" for case in cases
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total demo alerts", len(cases))
    col2.metric("Awaiting / in review", open_alerts)
    col3.metric("Reviews completed", completed)

    st.divider()

    st.subheader("The three-stage pathway")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("### 1. DETECT\n\nRecord a positive blood-culture alert and its laboratory information.")

    with col2:
        st.warning("### 2. DECIDE\n\nTrack whether the antimicrobial stewardship team has reviewed the alert.")

    with col3:
        st.success("### 3. CONTAIN\n\nReview infection-control readiness and response steps.")

    st.subheader("Demonstration alerts")
    st.dataframe(cases, use_container_width=True)

# -----------------------------
# DETECT
# -----------------------------
elif page == "1. Detect":

    st.subheader("🔎 DETECT — Laboratory alerts")

    st.write(
        "Record a fictional positive blood-culture alert "
        "for demonstration purposes."
    )

    with st.form("new_alert_form"):
        case_id = st.text_input("Demo case ID", placeholder="DEMO-004")

        sample = st.selectbox(
            "Sample type",
            ["Blood culture"]
        )

        lab_alert = st.selectbox(
            "Demonstration laboratory alert",
            [
                "Gram-negative bacilli",
                "Gram-positive cocci",
                "Yeast detected",
                "Other laboratory finding"
            ]
        )

        elapsed = st.number_input(
            "Hours since positive alert",
            min_value=0,
            max_value=168,
            value=1
        )

        submitted = st.form_submit_button("Add demonstration alert")

        if submitted:
            if not case_id.strip():
                st.error("Please enter a demo case ID.")
            elif any(c["Case ID"] == case_id for c in st.session_state.cases):
                st.error("That demo case ID already exists.")
            else:
                st.session_state.cases.append({
                    "Case ID": case_id.strip(),
                    "Sample": sample,
                    "Lab alert": lab_alert,
                    "Status": "Awaiting review",
                    "Elapsed hours": elapsed
                })
                st.success("Demonstration alert added!")
                st.rerun()

    st.divider()
    st.subheader("Recorded alerts")
    st.dataframe(st.session_state.cases, use_container_width=True)

# -----------------------------
# DECIDE
# -----------------------------
elif page == "2. Decide":

    st.subheader("🧠 DECIDE — Stewardship review tracking")

    st.write(
        "This section records review progress. "
        "It does not recommend or select antimicrobial treatment."
    )

    cases = st.session_state.cases

    if cases:
        case_ids = [case["Case ID"] for case in cases]

        selected_case = st.selectbox(
            "Select a demonstration case",
            case_ids
        )

        selected_status = st.selectbox(
            "Review status",
            [
                "Awaiting review",
                "Under review",
                "Review completed"
            ]
        )

        if st.button("Update review status"):
            for case in st.session_state.cases:
                if case["Case ID"] == selected_case:
                    case["Status"] = selected_status

            st.success("Review status updated!")
            st.rerun()

    st.divider()
    st.subheader("Stewardship review register")
    st.dataframe(st.session_state.cases, use_container_width=True)

    st.info(
        "In a real hospital pathway, clinical decisions would remain "
        "the responsibility of qualified healthcare professionals."
    )

# -----------------------------
# CONTAIN
# -----------------------------
elif page == "3. Contain":

    st.subheader("🛡️ CONTAIN — Infection-control readiness")

    st.write(
        "A demonstration checklist for reviewing preparedness "
        "if Candida auris is suspected or confirmed."
    )

    st.warning(
        "This is a preparedness checklist, not a substitute "
        "for local infection-control protocols or specialist advice."
    )

    for item in st.session_state.containment_checks:
        st.session_state.containment_checks[item] = st.checkbox(
            item,
            value=st.session_state.containment_checks[item]
        )

    completed_checks = sum(
        st.session_state.containment_checks.values()
    )
    total_checks = len(st.session_state.containment_checks)

    st.divider()
    st.subheader("Readiness progress")

    st.progress(completed_checks / total_checks)

    st.metric(
        "Checklist items reviewed",
        f"{completed_checks} / {total_checks}"
    )

    if completed_checks == total_checks:
        st.success("All demonstration checklist items have been reviewed.")
    else:
        st.info("Some checklist items are still pending.")

    st.caption(
        "Actual isolation, screening and environmental measures "
        "must follow hospital policy and expert guidance."
    )

# -----------------------------
# FOOTER
# -----------------------------
st.divider()
st.caption(
    "DDC Dashboard | Educational research prototype | "
    "Fictional data only"
)

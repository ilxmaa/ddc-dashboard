
import streamlit as st
import pandas as pd
from datetime import datetime

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------
st.set_page_config(
    page_title="DDC | Clinical Response Monitor",
    page_icon="🩺",
    layout="wide"
)

# --------------------------------
# PROFESSIONAL DESIGN
# --------------------------------
st.markdown("""
<style>
.stApp {
    background-color: #F5F8FC;
}
[data-testid="stSidebar"] {
    background-color: #EAF1F8;
}
h1, h2, h3 {
    color: #17365D;
}
div[data-testid="stMetric"] {
    background: white;
    padding: 17px;
    border-radius: 12px;
    border: 1px solid #DFE7F0;
}
.ddc-subtitle {
    color: #62748A;
    font-size: 15px;
}
.ddc-note {
    background: #EAF2FA;
    padding: 14px;
    border-radius: 9px;
    color: #244568;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------
# DEMONSTRATION DATA
# --------------------------------
if "cases" not in st.session_state:
    st.session_state.cases = [
        {
            "Case ID": "DEMO-001",
            "Laboratory alert": "Gram-negative bacilli",
            "Stage": "Detect",
            "Status": "Awaiting review",
            "Elapsed hours": 2
        },
        {
            "Case ID": "DEMO-002",
            "Laboratory alert": "Yeast detected",
            "Stage": "Decide",
            "Status": "Under review",
            "Elapsed hours": 1
        },
        {
            "Case ID": "DEMO-003",
            "Laboratory alert": "Gram-positive cocci",
            "Stage": "Decide",
            "Status": "Review completed",
            "Elapsed hours": 4
        }
    ]

if "checks" not in st.session_state:
    st.session_state.checks = {
        "Isolation readiness reviewed": False,
        "Infection-control team notified": False,
        "Environmental cleaning plan reviewed": False,
        "Contact screening process reviewed": False
    }

# --------------------------------
# SIDEBAR NAVIGATION
# --------------------------------
st.sidebar.title("🩺 DDC")
st.sidebar.caption("CLINICAL RESPONSE MONITOR")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    [
        "Dashboard",
        "Detect",
        "Decide",
        "Contain",
        "Research Performance",
        "Case Demonstration",
        "About the Project"
    ]
)

st.sidebar.divider()
st.sidebar.caption("MEDly MERIT 2026")
st.sidebar.caption("Educational research prototype")

# --------------------------------
# MAIN HEADER
# --------------------------------
st.title("Detect → Decide → Contain")
st.markdown(
    '<p class="ddc-subtitle">'
    'A rapid laboratory alert, antimicrobial stewardship '
    'and infection-control readiness pathway.'
    '</p>',
    unsafe_allow_html=True
)

st.warning(
    "EDUCATIONAL DEMONSTRATION ONLY — "
    "All records are fictional. This application does not "
    "diagnose infections or recommend antimicrobial treatment."
)

# --------------------------------
# DASHBOARD
# --------------------------------
if page == "Dashboard":

    st.subheader("Clinical response overview")

    cases = st.session_state.cases

    total = len(cases)
    pending = sum(
        c["Status"] != "Review completed" for c in cases
    )
    completed = sum(
        c["Status"] == "Review completed" for c in cases
    )

    col1, col2, col3 = st.columns(3)

    col1.metric("Total demo alerts", total)
    col2.metric("Pending reviews", pending)
    col3.metric("Completed reviews", completed)

    st.divider()

    st.subheader("The DDC response pathway")

    a, b, c = st.columns(3)

    with a:
        st.info(
            "### 01 | DETECT\n"
            "Record a positive culture alert and "
            "communicate the laboratory finding."
        )

    with b:
        st.warning(
            "### 02 | DECIDE\n"
            "Track timely review by the antimicrobial "
            "stewardship team."
        )

    with c:
        st.success(
            "### 03 | CONTAIN\n"
            "Review infection-control readiness "
            "and response processes."
        )

    st.divider()

    st.subheader("Demonstration case register")
    st.dataframe(
        pd.DataFrame(cases),
        use_container_width=True,
        hide_index=True
    )

# --------------------------------
# DETECT
# --------------------------------
elif page == "Detect":

    st.subheader("01 | DETECT")
    st.write("Laboratory alert registration")

    st.info(
        "Purpose: demonstrate how a positive blood-culture "
        "alert could enter the proposed response pathway."
    )

    with st.form("alert_form"):

        case_id = st.text_input(
            "Demonstration case ID",
            placeholder="DEMO-004"
        )

        alert = st.selectbox(
            "Laboratory finding",
            [
                "Gram-negative bacilli",
                "Gram-positive cocci",
                "Yeast detected",
                "Other laboratory finding"
            ]
        )

        elapsed = st.number_input(
            "Illustrative elapsed time (hours)",
            min_value=0,
            max_value=168,
            value=1
        )

        submit = st.form_submit_button(
            "Register demonstration alert"
        )

        if submit:
            if not case_id.strip():
                st.error("Enter a demonstration case ID.")
            elif any(
                x["Case ID"] == case_id.strip()
                for x in st.session_state.cases
            ):
                st.error("This case ID already exists.")
            else:
                st.session_state.cases.append({
                    "Case ID": case_id.strip(),
                    "Laboratory alert": alert,
                    "Stage": "Detect",
                    "Status": "Awaiting review",
                    "Elapsed hours": elapsed
                })
                st.success("Demonstration alert registered.")
                st.rerun()

    st.divider()
    st.subheader("Registered alerts")
    st.dataframe(
        pd.DataFrame(st.session_state.cases),
        use_container_width=True,
        hide_index=True
    )

# --------------------------------
# DECIDE
# --------------------------------
elif page == "Decide":

    st.subheader("02 | DECIDE")
    st.write("Antimicrobial stewardship review tracking")

    st.info(
        "This module records review progress. "
        "It does not select antibiotics or provide treatment advice."
    )

    cases = st.session_state.cases

    if cases:
        case_ids = [x["Case ID"] for x in cases]

        selected = st.selectbox(
            "Select demonstration case",
            case_ids
        )

        status = st.selectbox(
            "Review status",
            [
                "Awaiting review",
                "Under review",
                "Review completed"
            ]
        )

        if st.button("Update review record"):
            for case in st.session_state.cases:
                if case["Case ID"] == selected:
                    case["Status"] = status
                    case["Stage"] = "Decide"

            st.success("Review record updated.")
            st.rerun()

    st.divider()

    st.subheader("Stewardship register")
    st.dataframe(
        pd.DataFrame(st.session_state.cases),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Clinical decisions remain the responsibility "
        "of qualified healthcare professionals."
    )

# --------------------------------
# CONTAIN
# --------------------------------
elif page == "Contain":

    st.subheader("03 | CONTAIN")
    st.write("Infection-control readiness checklist")

    st.warning(
        "Preparedness demonstration for suspected or confirmed "
        "Candida auris. Follow local infection-control protocols "
        "in actual healthcare settings."
    )

    items = list(st.session_state.checks.keys())

    for i, item in enumerate(items):
        checked = st.checkbox(
            item,
            value=st.session_state.checks[item],
            key=f"containment_{i}"
        )
        st.session_state.checks[item] = checked

    completed = sum(st.session_state.checks.values())
    total_checks = len(items)

    st.divider()
    st.subheader("Readiness progress")

    st.progress(completed / total_checks)

    st.metric(
        "Checklist completion",
        f"{completed}/{total_checks}"
    )

    if completed == total_checks:
        st.success("All demonstration checklist items reviewed.")
    else:
        st.info("Some readiness items remain unreviewed.")

# --------------------------------
# RESEARCH PERFORMANCE
# --------------------------------
elif page == "Research Performance":

    st.subheader("Research performance indicators")

    st.markdown(
        "### Proposed study targets"
    )

    st.caption(
        "These are protocol targets, not observed or validated results."
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Time to appropriate therapy",
        "5 hours",
        help="Proposed reduction compared with baseline."
    )

    col2.metric(
        "Containment response",
        "Within 4 hours",
        help="Proposed response-time target."
    )

    col3.metric(
        "Recommendation adherence",
        "≥80%",
        help="Proposed stewardship recommendation adherence."
    )

    st.divider()

    st.subheader("Illustrative response-time data")

    chart_data = pd.DataFrame(
        {
            "Illustrative hours": [1, 2, 4]
        },
        index=["Detect", "Decide", "Contain"]
    )

    st.bar_chart(chart_data)

    st.caption(
        "Synthetic example values for interface demonstration only. "
        "They are not clinical study findings."
    )

    st.subheader("Suggested study outcomes")

    st.markdown("""
    - Time from positive blood culture to appropriate therapy
    - Time from laboratory alert to stewardship review
    - Time to infection-control response
    - Proportion of recommendations followed
    - Feasibility and implementation costs
    """)

# --------------------------------
# ABOUT THE PROJECT
# --------------------------------
elif page == "About the Project":

    st.subheader("About the research project")

    st.markdown("""
    **Working title**

    Detect → Decide → Contain: A rapid-diagnostics and
    antimicrobial-stewardship pathway for bloodstream infections,
    with Candida auris readiness.

    ### Research rationale

    Delays in communicating microbiology results and coordinating
    clinical review may affect timely infection management.
    A structured response pathway may improve coordination.

    ### Research objectives

    1. Improve communication of positive blood-culture alerts.
    2. Support timely antimicrobial stewardship review.
    3. Strengthen infection-control preparedness.
    4. Evaluate feasibility and response-time indicators.

    ### Proposed methodology

    A single-centre before-and-after pilot study:

    - Six-month retrospective baseline period.
    - Six-month prospective intervention period.
    - Comparison of selected process indicators.
    - Feasibility and implementation assessment.

    ### Three intervention components

    - DETECT: Laboratory notification.
    - DECIDE: Stewardship review and follow-up.
    - CONTAIN: Infection-control readiness.
    """)

    st.info(
        "The dashboard is an educational implementation prototype. "
        "Its usability and impact would require separate evaluation."
    )

# --------------------------------
# INTERACTIVE CASE DEMONSTRATION
# --------------------------------
elif page == "Case Demonstration":

    st.subheader("Interactive DDC Case Journey")

    st.markdown("""
    Follow a fictional bloodstream infection alert through
    the Detect → Decide → Contain pathway.
    """)

    st.warning(
        "SIMULATED CASE ONLY. Yeast detected in a blood culture "
        "does not establish Candida auris infection. "
        "Species identification and clinical decisions require "
        "qualified healthcare professionals."
    )

    # Initialise demonstration progress
    if "demo_stage" not in st.session_state:
        st.session_state.demo_stage = 0

    if "demo_review" not in st.session_state:
        st.session_state.demo_review = False

    if "demo_containment" not in st.session_state:
        st.session_state.demo_containment = False
        
    if "demo_times" not in st.session_state:
        st.session_state.demo_times = {
        "DETECT": None,
        "DECIDE": None,
        "CONTAIN": None
    }
        

    stage = st.session_state.demo_stage

    st.divider()

    st.markdown("### DEMO-004 | Fictional case")

    st.info(
        "**Laboratory finding:** Yeast detected in a positive "
        "blood culture.\n\n"
        "**Species identification:** Pending in this demonstration."
    )

    # Progress indicator
    stage_names = [
        "Detect",
        "Decide",
        "Contain",
        "Completed"
    ]

    st.progress(stage / 3)

    st.write(
        f"**Current stage:** {stage_names[stage]}"
    )

    st.divider()

    # DETECT
    st.markdown("### 01 | DETECT")

    if stage >= 1:
        st.success("Laboratory alert recorded in the demonstration.")
    else:
        st.info("The positive culture alert is awaiting registration.")

    if st.button("Complete DETECT stage"):
        st.session_state.demo_times["DETECT"] = datetime.now()
        st.session_state.demo_stage = 1
        st.rerun()

    st.divider()

    # DECIDE
    st.markdown("### 02 | DECIDE")

    if stage >= 2:
        st.success("Stewardship review recorded.")
    elif stage == 1:
        st.info(
            "The fictional alert is ready for review "
            "by the qualified stewardship team."
        )

        review = st.checkbox(
            "Mark the simulated stewardship review as completed",
            key="demo_review_checkbox"
        )

        if review:
            if st.button("Complete DECIDE stage"):
                st.session_state.demo_times["DECIDE"] = datetime.now()
                st.session_state.demo_review = True
                st.session_state.demo_stage = 2
                st.rerun()

    else:
        st.caption("Complete DETECT to unlock this stage.")

    st.divider()

    # CONTAIN
    st.markdown("### 03 | CONTAIN")

    if stage >= 3:
        st.success("Demonstration readiness review completed.")
    elif stage == 2:
        st.info(
            "Review the infection-control readiness items "
            "in accordance with applicable hospital protocols."
        )

        containment = st.checkbox(
            "Mark the simulated infection-control readiness review as completed",
            key="demo_containment_checkbox"
        )

        if containment:
            if st.button("Complete CONTAIN stage"):
                st.session_state.demo_times["CONTAIN"] = datetime.now()
                st.session_state.demo_containment = True
                st.session_state.demo_stage = 3
                st.rerun()

    else:
        st.caption("Complete DECIDE to unlock this stage.")

    # --------------------------------
    # SIMULATED RESPONSE TIMELINE
    # --------------------------------
    st.divider()
    st.markdown("### Response timeline")

    times = st.session_state.demo_times

    timeline_data = []

    for stage_name in ["DETECT", "DECIDE", "CONTAIN"]:
        recorded_time = times[stage_name]

        if recorded_time is not None:
            timeline_data.append({
                "Stage": stage_name,
                "Recorded at": recorded_time.strftime("%H:%M:%S"),
                "Status": "Completed"
            })
        else:
            timeline_data.append({
                "Stage": stage_name,
                "Recorded at": "Not recorded",
                "Status": "Pending"
            })

    st.dataframe(
        pd.DataFrame(timeline_data),
        use_container_width=True,
        hide_index=True
    )

    recorded_times = [
        times[name]
        for name in ["DETECT", "DECIDE", "CONTAIN"]
        if times[name] is not None
    ]

    if len(recorded_times) >= 2:
        elapsed_seconds = (
            recorded_times[-1] - recorded_times[0]
        ).total_seconds()

        st.metric(
            "Simulated pathway duration",
            f"{elapsed_seconds / 60:.2f} minutes"
        )

        st.caption(
            "Duration is calculated from demonstration button clicks. "
            "It is not a measurement of real laboratory or clinical response time."
        )

    st.caption(
        "Timestamps are generated locally during this demonstration "
        "and are not permanent clinical records."
    )

    # FINAL SUMMARY
    if st.session_state.demo_stage == 3:

        st.divider()
        st.success("DDC demonstration journey completed!")

        st.markdown("### Case summary")

        summary = {
            "Case ID": ["DEMO-004"],
            "DETECT": ["Completed"],
            "DECIDE": ["Completed"],
            "CONTAIN": ["Completed"],
            "Data type": ["Fictional"]
        }

        st.dataframe(
            pd.DataFrame(summary),
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Completion represents a simulated workflow demonstration, "
            "not confirmation of clinical treatment or infection control."
        )

if st.button("Reset demonstration"):
    st.session_state.demo_stage = 0
    st.session_state.demo_review = False
    st.session_state.demo_containment = False
    st.session_state.demo_times = {
        "DETECT": None,
        "DECIDE": None,
        "CONTAIN": None
    }
    st.rerun()

# --------------------------------
# FOOTER
# --------------------------------
st.divider()

st.caption(
    "DDC Dashboard | MEDly MERIT 2026 | "
    "Educational prototype | Fictional data only"
)

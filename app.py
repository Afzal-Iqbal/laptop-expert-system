import streamlit as st
import pandas as pd
from engine import ExpertInferenceEngine, DiagnosticResult, AuditScorecard

# Page configuration
st.set_page_config(
    page_title="LapDoc | Laptop Diagnostic Expert System",
    page_icon="💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E88E5;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #555;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 8px;
        padding: 15px;
        border-left: 5px solid #1E88E5;
        margin-bottom: 15px;
    }
    .defect-card {
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 10px;
        border: 1px solid #e0e0e0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_engine():
    return ExpertInferenceEngine()


engine = get_engine()

# Initialize session states
if "emergency_history" not in st.session_state:
    st.session_state.emergency_history = []

if "audit_answers" not in st.session_state:
    st.session_state.audit_answers = {}

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/laptop.png", width=64)
    st.title("LapDoc Expert System")
    st.markdown("**Rule-Based Inference Engine for Laptop Hardware & Firmware**")
    st.divider()

    st.subheader("🛠️ Diagnostic Mode")
    app_mode = st.radio(
        "Select Operating Mode:",
        ["⚡ Emergency Fast-Triage", "🔍 50-Point Subsystem Audit"],
        help="Emergency mode finds the root cause quickly with early exit. Audit mode checks all 52 subsystem rules."
    )

    st.divider()
    st.subheader("💻 Hardware Profile")
    brand = st.selectbox(
        "Manufacturer / Brand:",
        ["Dell", "Lenovo (ThinkPad/IdeaPad)", "HP (Spectre/Pavilion)", "Apple (MacBook)", "Asus (ROG/ZenBook)", "Acer", "MSI", "Microsoft Surface", "Other / Custom"]
    )
    processor = st.selectbox(
        "Processor Platform:",
        ["Intel Core (12th-14th Gen / Ultra)", "Intel Core (Legacy 8th-11th Gen)", "AMD Ryzen 5000/7000/8000", "Apple Silicon (M1/M2/M3/M4)", "Other"]
    )
    chassis_type = st.selectbox(
        "Laptop Category:",
        ["Standard Ultrabook / Thin & Light", "High-Performance Gaming Laptop", "Mobile Workstation", "2-in-1 Convertible / Touchscreen"]
    )

    st.divider()
    st.caption(f"Knowledge Base: **{len(engine.nodes)-1} Active Rules**")
    st.caption(f"Monitored Subsystems: **{len(engine.categories)} Domains**")

    if st.button("🔄 Reset Diagnostic Session", use_container_width=True):
        st.session_state.emergency_history = []
        st.session_state.audit_answers = {}
        st.rerun()


# ==============================================================================
# MODE 1: EMERGENCY FAST-TRIAGE
# ==============================================================================
if app_mode == "⚡ Emergency Fast-Triage":
    st.markdown('<p class="main-header">⚡ Emergency Fast-Triage Mode</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">Targeted DAG diagnosis for <b>{brand}</b> ({processor}) | <i>Halts immediately upon detecting root cause</i></p>', unsafe_allow_html=True)

    # Process step through inference engine
    step_res = engine.process_emergency_step(st.session_state.emergency_history)

    if step_res["status"] == "in_progress":
        node = step_res["current_node"]
        curr_step = len(st.session_state.emergency_history) + 1

        # Breadcrumbs
        col_crumbs, col_back = st.columns([4, 1])
        with col_crumbs:
            st.markdown(f"**Step {curr_step}:** Category → `{engine.categories.get(node['category'], node['category']).upper()}`")
        with col_back:
            if st.session_state.emergency_history:
                if st.button("⬅ Back", use_container_width=True):
                    st.session_state.emergency_history.pop()
                    st.rerun()

        # Question Presentation
        st.subheader(f"{node['title']}")
        st.info(f"👉 **{node['question']}**")

        # Explanation Facility (Why this question is asked)
        with st.expander("💡 Explanation Facility: Why is the system asking this?"):
            st.write(node["why"])
            st.caption("Classic AI Expert Systems feature an explanation facility to guarantee reasoning transparency.")

        # Options selection form
        with st.form(f"form_step_{node['id']}"):
            options_labels = [opt["label"] for opt in node["options"]]
            selected_label = st.radio(
                "Select observed symptom / condition:",
                options_labels,
                index=0
            )

            submitted = st.form_submit_button("Confirm & Advance Inference ➔", use_container_width=True)
            if submitted:
                selected_opt = next(opt for opt in node["options"] if opt["label"] == selected_label)
                st.session_state.emergency_history.append((node["id"], selected_opt["key"]))
                st.rerun()

    else:
        # DIAGNOSIS CONCLUDED
        res: DiagnosticResult = step_res["result"]

        st.success("🎯 Root Cause Analysis Completed!")

        # High level diagnosis banner
        urgency_color = {
            "Critical": "red",
            "High": "orange",
            "Medium": "blue",
            "Routine": "green"
        }.get(res.urgency, "gray")

        st.markdown(f"""
        <div style="background-color: #f1f8e9; border: 2px solid #81c784; border-radius: 10px; padding: 20px; margin-bottom: 25px;">
            <h2 style="color: #2e7d32; margin-top: 0;">{res.title}</h2>
            <p style="font-size: 1.15rem; color: #333;">{res.issue}</p>
        </div>
        """, unsafe_allow_html=True)

        col_urg, col_cost, col_diy = st.columns(3)
        with col_urg:
            st.metric("Urgency Level", res.urgency)
        with col_cost:
            st.metric("Estimated Repair Cost", res.estimated_cost)
        with col_diy:
            st.metric("Repair Feasibility", "User Serviceable" if res.diy_friendly else "Board Technician")

        st.divider()

        # Step by step remediation
        st.subheader("🛠️ Actionable Remediation Plan")
        for i, step in enumerate(res.remediation, 1):
            st.markdown(f"**{i}.** {step}")

        st.divider()

        # Inference Trace
        st.subheader("📜 Inference Trace (How This Conclusion Was Derived)")
        trace_data = []
        for t in res.history_trace:
            trace_data.append({
                "Step": f"#{t['step']}",
                "Subsystem": t['title'],
                "Observed Answer": t['chosen_label'],
                "Inference Purpose": t['why']
            })
        st.table(pd.DataFrame(trace_data))

        # Restart
        if st.button("🔄 Start New Triage Session", type="primary", use_container_width=True):
            st.session_state.emergency_history = []
            st.rerun()


# ==============================================================================
# MODE 2: 50-POINT SUBSYSTEM AUDIT
# ==============================================================================
elif app_mode == "🔍 50-Point Subsystem Audit":
    st.markdown('<p class="main-header">🔍 50-Point Subsystem Hardware Audit</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">Comprehensive inspection for <b>{brand}</b> across 52 subsystem checkpoints. Ideal for pre-purchase evaluation and routine maintenance.</p>', unsafe_allow_html=True)

    audit_questions = engine.get_audit_questions()

    col_btn1, col_btn2 = st.columns([1, 1])
    with col_btn1:
        if st.button("✨ Auto-Fill Healthy Defaults (Demo / Benchmark)", use_container_width=True):
            for q in audit_questions:
                healthy_opt = next((o for o in q["options"] if o.get("is_healthy", True)), q["options"][0])
                st.session_state.audit_answers[q["id"]] = healthy_opt["key"]
            st.rerun()
    with col_btn2:
        if st.button("🧹 Clear All Answers", use_container_width=True):
            st.session_state.audit_answers = {}
            st.rerun()

    # Group questions by category
    categories_dict = engine.categories
    grouped_questions = {cat_id: [] for cat_id in categories_dict.keys()}
    for q in audit_questions:
        cat = q.get("category", "other")
        if cat in grouped_questions:
            grouped_questions[cat].append(q)

    # Progress bar
    answered_count = len(st.session_state.audit_answers)
    total_q = len(audit_questions)
    st.progress(answered_count / total_q, text=f"Audit Completion: {answered_count}/{total_q} questions answered")

    # Render category tabs
    tab_titles = [f"{cat_name.split()[0]} ({len(grouped_questions[cid])})" for cid, cat_name in categories_dict.items()]
    tabs = st.tabs(tab_titles)

    for tab, (cat_id, cat_name) in zip(tabs, categories_dict.items()):
        with tab:
            st.markdown(f"### {cat_name}")
            for q in grouped_questions[cat_id]:
                curr_saved = st.session_state.audit_answers.get(q["id"])
                opts = q["options"]
                opt_labels = [o["label"] for o in opts]
                
                # Determine default index
                default_idx = 0
                if curr_saved:
                    for i, o in enumerate(opts):
                        if o["key"] == curr_saved:
                            default_idx = i
                            break

                chosen_label = st.selectbox(
                    f"**{q['title']}**: {q['question']}",
                    opt_labels,
                    index=default_idx,
                    key=f"select_{q['id']}"
                )
                chosen_opt = next(o for o in opts if o["label"] == chosen_label)
                st.session_state.audit_answers[q["id"]] = chosen_opt["key"]

    st.divider()

    # Generate Audit Report Button
    if st.button("📊 Evaluate & Generate Full Audit Report", type="primary", use_container_width=True):
        scorecard: AuditScorecard = engine.evaluate_audit(st.session_state.audit_answers)

        st.subheader("📋 Audit Executive Summary")

        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.metric("Total Health Score", f"{scorecard.total_score} / 100")
        with col_s2:
            st.metric("Condition Grade", scorecard.letter_grade)
        with col_s3:
            st.metric("Est. Total Repair Cost", f"${scorecard.total_estimated_repair_min} - ${scorecard.total_estimated_repair_max}")

        st.info(f"**Verdict:** {scorecard.verdict}")

        # Category Score Breakdown
        st.subheader("Subsystem Health Breakdown")
        df_cats = pd.DataFrame([
            {"Subsystem": categories_dict.get(cid, cid), "Score (0-100)": score}
            for cid, score in scorecard.category_scores.items()
        ])
        st.bar_chart(df_cats.set_index("Subsystem"))

        # Flagged Defects
        st.subheader(f"⚠️ Flagged Defects & Required Repairs ({len(scorecard.flagged_defects)})")
        if not scorecard.flagged_defects:
            st.success("🎉 No hardware or firmware defects detected! The device passed all 52 diagnostic checks.")
        else:
            for d in scorecard.flagged_defects:
                severity_badge = "🔴 CRITICAL" if d['severity'] == "CRITICAL" else ("🟠 HIGH" if d['severity'] == "HIGH" else "🟡 MEDIUM")
                with st.expander(f"{severity_badge} | {d['title']} ({d['cost']})"):
                    st.write(f"**Category:** {d['category']}")
                    st.write(f"**Observed Symptom:** {d['observed']}")
                    st.write(f"**Technical Defect:** {d['defect']}")
                    st.write(f"**Estimated Repair Expense:** {d['cost']}")

        # Download Report
        st.download_button(
            "📥 Download Diagnostic Audit Report (.md)",
            data=scorecard.summary_markdown,
            file_name=f"LapDoc_Audit_{brand.split()[0]}_Scorecard.md",
            mime="text/markdown",
            use_container_width=True
        )

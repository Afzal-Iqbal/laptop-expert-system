import streamlit as st
import pandas as pd
from engine import ExpertInferenceEngine, DiagnosticResult, AuditScorecard, TreeAuditStepResult

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

if "tree_audit_state" not in st.session_state or "tree_audit_step" not in st.session_state:
    state, step_res = engine.start_tree_audit()
    st.session_state.tree_audit_state = state
    st.session_state.tree_audit_step = step_res

# Sidebar Configuration
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/laptop.png", width=64)
    st.title("LapDoc Expert System")
    st.markdown("**Rule-Based Inference Engine for Laptop Hardware & Firmware**")
    st.divider()

    st.subheader("🛠️ Diagnostic Mode")
    app_mode = st.radio(
        "Select Operating Mode:",
        ["⚡ Emergency Fast-Triage", "🔍 Cascading Decision-Tree Audit"],
        help="Emergency mode finds the root cause quickly with early exit. Cascading tree audit traverses all 7 subsystems with deep component drill-downs."
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
        s, r = engine.start_tree_audit()
        st.session_state.tree_audit_state = s
        st.session_state.tree_audit_step = r
        st.rerun()


# ==============================================================================
# MODE 1: EMERGENCY FAST-TRIAGE
# ==============================================================================
if app_mode == "⚡ Emergency Fast-Triage":
    st.markdown('<p class="main-header">⚡ Emergency Fast-Triage Mode</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">Targeted DAG diagnosis for <b>{brand}</b> ({processor}) | <i>Halts immediately upon detecting root cause</i></p>', unsafe_allow_html=True)

    step_res = engine.process_emergency_step(st.session_state.emergency_history)

    if step_res["status"] == "in_progress":
        node = step_res["current_node"]
        curr_step = len(st.session_state.emergency_history) + 1

        col_crumbs, col_back = st.columns([4, 1])
        with col_crumbs:
            st.markdown(f"**Step {curr_step}:** Category → `{engine.categories.get(node['category'], node['category']).upper()}`")
        with col_back:
            if st.session_state.emergency_history:
                if st.button("⬅ Back", use_container_width=True):
                    st.session_state.emergency_history.pop()
                    st.rerun()

        st.subheader(f"{node['title']}")
        st.info(f"👉 **{node['question']}**")

        with st.expander("💡 Explanation Facility: Why is the system asking this?"):
            st.write(node["why"])
            st.caption("Classic AI Expert Systems feature an explanation facility to guarantee reasoning transparency.")

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
        res: DiagnosticResult = step_res["result"]
        st.success("🎯 Root Cause Analysis Completed!")

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

        st.subheader("🛠️ Actionable Remediation Plan")
        for i, step in enumerate(res.remediation, 1):
            st.markdown(f"**{i}.** {step}")

        st.divider()

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

        if st.button("🔄 Start New Triage Session", type="primary", use_container_width=True):
            st.session_state.emergency_history = []
            st.rerun()


# ==============================================================================
# MODE 2: CASCADING DECISION-TREE SUBSYSTEM AUDIT
# ==============================================================================
elif app_mode == "🔍 Cascading Decision-Tree Audit":
    st.markdown('<p class="main-header">🔍 Cascading Decision-Tree Subsystem Audit</p>', unsafe_allow_html=True)
    st.markdown(f'<p class="sub-header">Hierarchical deep-dive inspection for <b>{brand}</b> across 7 subsystems with interactive early-exit intercept.</p>', unsafe_allow_html=True)

    pipeline_names = [
        ("🔋", "Power"),
        ("🖥️", "Display"),
        ("❄️", "Thermals"),
        ("💾", "Storage"),
        ("🧠", "Memory"),
        ("⌨️", "I/O Ports"),
        ("🔊", "Audio")
    ]

    step_res: TreeAuditStepResult = st.session_state.tree_audit_step
    state = st.session_state.tree_audit_state

    # Render Pipeline Stepper Header
    stepper_cols = st.columns(len(pipeline_names))
    curr_idx = step_res.subsystem_index if step_res.status in ["in_progress", "critical_intercept"] else len(pipeline_names)
    for i, (col, (icon, name)) in enumerate(zip(stepper_cols, pipeline_names)):
        with col:
            if i < curr_idx:
                st.markdown(f"<div style='text-align: center; color: #2e7d32; font-weight: bold;'>✓ {icon}<br><span style='font-size:0.8rem'>{name}</span></div>", unsafe_allow_html=True)
            elif i == curr_idx and step_res.status in ["in_progress", "critical_intercept"]:
                st.markdown(f"<div style='text-align: center; color: #1565c0; font-weight: bold; border-bottom: 3px solid #1565c0;'>⏳ {icon}<br><span style='font-size:0.8rem'>{name}</span></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div style='text-align: center; color: #9e9e9e;'>⚪ {icon}<br><span style='font-size:0.8rem'>{name}</span></div>", unsafe_allow_html=True)

    st.divider()

    # Case 1: Critical Intercept Modal
    if step_res.status == "critical_intercept":
        crit = step_res.critical_leaf
        st.error(f"### 🚨 Critical Hardware Defect Detected: {crit['title']}")
        st.markdown(f"""
        <div style="background-color: #ffebee; border: 2px solid #ef5350; border-radius: 8px; padding: 15px; margin-bottom: 20px;">
            <p style="font-size: 1.1rem; color: #c62828; margin: 0;"><b>Root Fault:</b> {crit['issue']}</p>
            <p style="margin-top: 10px; margin-bottom: 0;"><b>Subsystem:</b> {step_res.subsystem_name} | <b>Estimated Cost:</b> {crit.get('cost', 'Varies')}</p>
        </div>
        """, unsafe_allow_html=True)

        st.warning("⚠️ **Decision Point:** A fatal or high-severity component failure has been reached. Would you like to terminate now and generate the emergency repair plan, or continue auditing the remaining hardware domains?")

        col_term, col_cont = st.columns(2)
        with col_term:
            if st.button("🛑 Terminate Now & View Repair Plan", type="primary", use_container_width=True):
                st.session_state.tree_audit_step = engine.advance_tree_audit(state, action="terminate_critical")
                st.rerun()
        with col_cont:
            if st.button("⏩ Continue Auditing Remaining Subsystems", use_container_width=True):
                st.session_state.tree_audit_step = engine.advance_tree_audit(state, action="continue_critical")
                st.rerun()

    # Case 2: In-Progress Question Card
    elif step_res.status == "in_progress":
        node = step_res.current_node
        depth = step_res.depth_level
        depth_badge = "Level 1: Gateway Triage" if depth == 1 else f"Level {depth}: Component Deep-Dive"

        col_cat, col_depth = st.columns([3, 1])
        with col_cat:
            st.markdown(f"**Current Domain:** `{step_res.subsystem_name.upper()}`")
        with col_depth:
            st.markdown(f"<span style='background-color: #e3f2fd; color: #0d47a1; padding: 4px 8px; border-radius: 4px; font-size: 0.85rem; font-weight: bold;'>{depth_badge}</span>", unsafe_allow_html=True)

        st.subheader(node["title"])
        st.info(f"👉 **{node['question']}**")

        with st.expander("💡 Explanation Facility: Why is the system asking this?"):
            st.write(node.get("why", "Evaluating subsystem behavior."))
            st.caption("The tree deep-dives further if symptoms are detected, or advances to the next subsystem if nominal.")

        with st.form(f"tree_form_{node['id']}"):
            opt_labels = [opt["label"] for opt in node["options"]]
            selected_label = st.radio("Select observed condition / answer:", opt_labels, index=0)

            submitted = st.form_submit_button("Confirm & Advance Tree ➔", use_container_width=True)
            if submitted:
                selected_opt = next(o for o in node["options"] if o["label"] == selected_label)
                st.session_state.tree_audit_step = engine.advance_tree_audit(state, action="answer", answer_key=selected_opt["key"])
                st.rerun()

    # Case 3: Concluded Early (from Critical Intercept)
    elif step_res.status == "concluded_early":
        res: DiagnosticResult = step_res.result
        st.success("🎯 Early Root Cause Analysis Generated")

        st.markdown(f"""
        <div style="background-color: #ffebee; border: 2px solid #ef5350; border-radius: 10px; padding: 20px; margin-bottom: 25px;">
            <h2 style="color: #c62828; margin-top: 0;">🛑 Audit Terminated Early: {res.title}</h2>
            <p style="font-size: 1.15rem; color: #333;">{res.issue}</p>
        </div>
        """, unsafe_allow_html=True)

        col_urg, col_cost, col_diy = st.columns(3)
        with col_urg:
            st.metric("Urgency Level", res.urgency)
        with col_cost:
            st.metric("Estimated Repair Cost", res.estimated_cost)
        with col_diy:
            st.metric("Repair Feasibility", "User Serviceable" if res.diy_friendly else "Board Technician Required")

        st.divider()
        st.subheader("🛠️ Step-by-Step Remediation Plan")
        for i, step in enumerate(res.remediation, 1):
            st.markdown(f"**{i}.** {step}")

        st.divider()
        st.subheader("📜 Audit Traversal Trace (Prior to Early Termination)")
        trace_data = []
        for t in res.history_trace:
            trace_data.append({
                "Step": f"#{t['step']}",
                "Subsystem": t['subsystem'],
                "Depth": f"Level {t['depth']}",
                "Question": t['title'],
                "Observed Answer": t['chosen_label']
            })
        st.table(pd.DataFrame(trace_data))

        if st.button("🔄 Start New Cascading Audit", type="primary", use_container_width=True):
            s, r = engine.start_tree_audit()
            st.session_state.tree_audit_state = s
            st.session_state.tree_audit_step = r
            st.rerun()

    # Case 4: Concluded Full (All Subsystems Traversed)
    elif step_res.status == "concluded_full":
        scorecard: AuditScorecard = step_res.scorecard
        st.success("🎉 All 7 Hardware Subsystems Successfully Audited!")

        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.metric("Overall Health Score", f"{scorecard.total_score} / 100")
        with col_s2:
            st.metric("Condition Grade", scorecard.letter_grade)
        with col_s3:
            st.metric("Est. Total Repair Cost", f"${scorecard.total_estimated_repair_min} - ${scorecard.total_estimated_repair_max}")

        st.info(f"**Condition Verdict:** {scorecard.verdict}")

        st.subheader("📊 Subsystem Health Breakdown")
        categories_dict = engine.categories
        df_cats = pd.DataFrame([
            {"Subsystem": categories_dict.get(cid, cid), "Score (0-100)": score}
            for cid, score in scorecard.category_scores.items()
        ])
        st.bar_chart(df_cats.set_index("Subsystem"))

        st.subheader(f"⚠️ Flagged Defects Across Traversed Branches ({len(scorecard.flagged_defects)})")
        if not scorecard.flagged_defects:
            st.success("✓ No hardware or firmware defects detected! The device passed all audited checkpoints.")
        else:
            for d in scorecard.flagged_defects:
                severity_badge = "🔴 CRITICAL" if d['severity'] == "CRITICAL" else ("🟠 HIGH" if d['severity'] == "HIGH" else "🟡 MEDIUM")
                with st.expander(f"{severity_badge} | {d['title']} ({d['cost']})"):
                    st.write(f"**Category:** {d['category']}")
                    st.write(f"**Observed Symptom:** {d['observed']}")
                    st.write(f"**Technical Defect:** {d['defect']}")
                    st.write(f"**Estimated Repair Expense:** {d['cost']}")

        st.download_button(
            "📥 Download Diagnostic Scorecard Report (.md)",
            data=scorecard.summary_markdown,
            file_name=f"LapDoc_TreeAudit_{brand.split()[0]}_Scorecard.md",
            mime="text/markdown",
            use_container_width=True
        )

        if st.button("🔄 Restart Audit Traversal", type="primary", use_container_width=True):
            s, r = engine.start_tree_audit()
            st.session_state.tree_audit_state = s
            st.session_state.tree_audit_step = r
            st.rerun()

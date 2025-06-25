import streamlit as st

from agents.orchestrator import run_diagnostics
from tools import utils

# Page config
st.set_page_config(
    page_title="Strategic Education Diagnostics",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Header
st.title("Strategic Education Diagnostics")
st.markdown(
    "Get AI-powered insights and strategic recommendations tailored to your preferred approach"
)

st.markdown("---")

# 1) System Configuration
st.header("System Configuration")
st.markdown(
    "Configure your education system parameters and strategic preferences "
    "for personalized analysis"
)

# Inputs
country = st.selectbox(
    "Select Country",
    options=["🇮🇩 Indonesia", "🇸🇬 Singapore", "🇰🇪 Kenya", "🇫🇮 Finland"],
    index=0,
    help="Choose the country you want diagnostics for"
)

approach = st.selectbox(
    "Preferred Strategic Approach (Optional)",
    options=[
        "Amplify Existing Strengths",
        "Address Most Urgent Priorities",
        "Strengthen Foundations",
        "Balanced Multi-Front Approach"
    ],
    index=None,
    help="Choose how you'd like to approach system improvement"
)

priority_focus = st.selectbox(
    "Priority Focus (Optional)",
    options=[
        "Learning Performance",
        "Equity and Inclusion",
        "Learning Environment"
    ],
    index=None,
    help="Select specific areas you want to prioritize in diagnostics"
)

planned_reforms = st.multiselect(
    "Planned Policy Reforms (Optional)",
    options=[
        "Curriculum Reform",
        "Teacher Reform",
        "Funding Reform",
        "Technology Reform"
    ],
    accept_new_options=True,
    help="Select any planned reforms that may impact diagnostics"
)

additional_context = st.text_area(
    "Additional Context (Optional)",
    placeholder="Any specific challenges, goals, or constraints you'd like to address..."
)

st.markdown("---")

# 2) Run button
if st.button("Generate Strategic Recommendations"):
    st.info("Running AI diagnostics…")
    # Prepare payload
    inputs = {
        "country": country,
        "approach": approach,
        "focus": priority_focus,
        "pol_reform": planned_reforms,
        "add_context": additional_context,
    }
    
    # Call the LangChain agent pipeline
    results = run_diagnostics(inputs)

    # Parse the results
    outputs = utils.parse_json_string(results['messages'][-1].content)

    # print(f"JSON outputs: {outputs}")


    # 3) Diagnostics Summary
    st.subheader("Strategic Diagnostic")
    st.markdown(f"**Country: {inputs['country']}**")
    st.markdown(f"**Approach: {inputs['approach']}**")
    st.write(outputs['strategic_diagnostic'])
    st.markdown("---")

    # 4) Detailed Recommendations
    st.subheader("Strategic Recommendations")
    for i, srec in enumerate(outputs['strategic_recommendations']):
        st.markdown(f"### {i+1}. {srec['recommendation']['title']}")
        st.markdown(f"**Priority**: {srec['recommendation']['priority']}")
        st.write(f"{srec['recommendation']['description']}")
        st.write(f"**Key performance indicator**: {srec['recommendation']['key_performance_indicators']}")
        st.write(f"**Cross sectoral linkages**: {srec['recommendation']['cross_sectoral_linkages']}")
        st.markdown(f"**References**: ")
        for ref in srec['references']:
            st.markdown(f"- {ref}")
    # for rec in result["recommendations"]:
    #     st.markdown(f"### {rec['title']}  ·  _{rec['priority']}_")
    #     st.markdown(f"**Type:** {rec['type']}")
    #     st.markdown(f"**Strategic Rationale:**\n>{rec['rationale']}")
    #     st.markdown(f"**Implementation Approach:**\n{rec['implementation']}")
    #     st.markdown(f"**Timeline:** {rec['timeline']}")

    #     # Best practices
    #     st.markdown("**Best Practices from Similar Contexts**")
    #     for bp in rec["best_practices"]:
    #         st.markdown(
    #             f"- **{bp['title']}** ({bp['location']}): {bp['outcome']}  "
    #             f"[View Report]({bp['link']})"
    #         )

    #     # Academic research
    #     st.markdown("**Supporting Academic Research**")
    #     for paper in rec["papers"]:
    #         st.markdown(
    #             f"- **{paper['title']}**, {paper['authors']} • {paper['journal']}  "
    #             f"_Key Finding:_ {paper['key_finding']}  "
    #             f"[Read Paper]({paper['link']})"
    #         )

    #     # Takeaways
    #     st.markdown("**Key Takeaways**")
    #     for tk in rec["takeaways"]:
    #         st.markdown(f"- {tk}")

    #     # Action items
    #     st.markdown("**Key Action Items**")
    #     for action in rec["action_items"]:
    #         st.markdown(f"- {action}")

    #     st.markdown("---")

    # 5) Footer buttons
    col1, col2, col3 = st.columns(3)
    # with col1:
    #     st.download_button(
    #         "Download Strategic Plan",
    #         # data=result.get("plan_file", b""),
    #         file_name="strategic_plan.pdf",
    #         mime="application/pdf"
    #     )
    with col2:
        if st.button("Rerun Analysis"):
            st.experimental_rerun()
    with col3:
        if st.button("Create Implementation Roadmap"):
            st.info("Launching roadmap builder…")
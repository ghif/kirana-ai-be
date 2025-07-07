import streamlit as st

from agents.orchestrator import run_diagnostics_with_planned_reforms
from tools import utils

# initialize session state
if "step" not in st.session_state:
    st.session_state.step = 1
    st.session_state.path = None

def reset():
    for key in ["step", "path", "country", "challenges", "additional", "planned_reforms", "outcome", "context", "strategy"]:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.step = 1

st.title("Strategic Education Diagnostics")
st.write("Get AI-powered insights and strategic recommendations tailored to your approach.")
st.write("You can generate recommendations based on emerging issues from your dashboard, or based on a reform you already plan to implement.")

country_options = ["", "🇮🇩 Indonesia", "🇿🇦 South Africa", "🇧🇷 Brazil", "🇪🇪 Estonia", "🇵🇱 Poland"]
challenge_options = [
    "Low foundational learning outcomes (18.3% proficiency)",
    "Significant mathematics learning gaps (81.9% below basic level)",
    "Limited digital learning integration (45.2% ICT use)",
    "Teacher support system gaps (67.8% access)"
]

strategy_options = [
    "Amplify Existing Strengths",
    "Address Most Urgent Priorities",
    "Strengthen Foundations",
    "Balanced Multi-Front Approach"
]

reform_options = [
    "Curriculum Reform", "Teacher Reform", "Funding Reform",
    "Technology Reform", "Assessment Reform", "Governance Reform"
]
outcome_options =  [
    "Improve Equity & Inclusion",
    "Raise Academic Performance",
    "Increase Student Engagement",
    "Strengthen Teaching Quality",
    "Enhance Learning Environment",
    "Improve Digital Integration",
    "Increase Civic Engagement",
    "Reduce Dropout Rates",
]

country = st.selectbox(
    "Select Country",
    country_options,
    format_func=lambda x: x if x else "Choose your country..."
)

# -----------------
# Main Interface with Tabs
# -----------------

# Only show tabs if a country has been selected
if not country:
    st.warning("Please select a country above to get started.")
else:
    st.session_state.country = country  # Store selected country

    tab1, tab2 = st.tabs(["Start from Dashboard Insights", "Start from Planned Reforms"])

    # --- Tab 1: Dashboard Insights ---
    with tab1:
        st.header("📊 Dashboard Insights Analysis")
        st.write("Select the challenges identified from your country's dashboard data:")

        challenges = st.multiselect(
            "Key Challenges from Dashboard Data", 
            options=challenge_options,
            accept_new_options=True,
            default=None, 
            key="dashboard_challenges"
        )
        additional = st.text_input("Add Additional Challenge (Optional)", key="dashboard_additional")

        st.header("Strategic Approach (Optional)")

        strategy = st.selectbox(
            "Choose how you'd like to approach system improvement based on your context and priorities",
            options=strategy_options,
            index=None,
            help="Choose how you'd like to approach system improvement",
            key="dashboard_strategy"
        )

        if st.button("Generate Recommendations from Insights", type="primary"):
            st.success(f"""Generating recommendations for **{st.session_state.country}**  
            - Challenges: {', '.join(challenges)}  
            - Additional: {additional or '–'}  
            - Approach: {strategy}""")
            # Placeholder for backend call
            # from agents.orchestrator import run_diagnostics
            # outputs = run_diagnostics(country=st.session_state.country, priority=challenges, additional_context=additional, approach=strategy)
            # ... display outputs ...
            if st.button("Start Over", key="reset_dashboard"):
                reset()

    # --- Tab 2: Planned Reforms ---
    with tab2:
        st.header("🛠 Planned Reform Configuration")
        st.write("Configure your planned reforms and expected outcomes:")

        
        planned = st.multiselect(
            label="Planned Policy Reforms", 
            options=reform_options, 
            accept_new_options=True,
            default=reform_options[0],
            key="reform_planned"
        )
        
        outcome = st.selectbox("Expected Primary Outcome", outcome_options, key="reform_outcome")
        
        context = st.text_area("Additional Context (Optional)", key="reform_context")

        st.header("Strategic Approach (Optional)")

        strategy = st.selectbox(
            "Choose how you'd like to approach system improvement based on your context and priorities",
            options=strategy_options,
            index=None,
            help="Choose how you'd like to approach system improvement",
            key="reform_strategy"
        )


        if st.button("Generate Recommendations from Reforms", type="primary"):
            st.info("Running AI diagnostics…")

            # Prepare input payload
            inputs = {
                "country": st.session_state.country,
                "planned_reforms": planned,
                "expected_outcome": outcome,
                "add_context": context,
                "strategy": strategy
            }

            print(f"Inputs for diagnostics: {inputs}")

            results = run_diagnostics_with_planned_reforms(inputs)
            # Parse the results
            outputs = utils.parse_json_string(results['messages'][-1].content)

            print(f"JSON outputs {outputs.keys()}: {outputs}")

            st.success(f"""Generating recommendations for **{st.session_state.country}**  
            - Reforms: {', '.join(planned)}  
            - Outcome: {outcome}  
            - Context: {context or '–'}  
            - Approach: {strategy}""")

            ### Diagnostic Summary
            st.subheader("Strategic Diagnostic")
            st.markdown(f"**Country: {inputs['country']}**")
            st.markdown(f"**Approach: {inputs['strategy']}**")
            st.write(outputs['strategic_diagnostic'])
            st.markdown("---")
            
            ### Detailed Recommendations
            st.subheader("Strategic Recommendations")
            for i, srec in enumerate(outputs['strategic_recommendations']):
                # recommendation = srec['recommendation']
                
                # Title and Priority
                st.markdown(f"### {i+1}. {srec['title']}")
                st.markdown(f"**Priority**: {srec['priority']}")
                st.write(f"{srec['description']}")

                st.markdown(f"**Strategic Rationale**: {srec['strategic_rationale']}")
                # st.markdown(f"**Implementation Approach**: {srec['implementation_approach']}")
                st.markdown(f"**Implementation Approach**: ")
                for approach in srec['implementation_approach']:
                    st.markdown(f"- {approach}")
                st.markdown(f"**Timeline**: {srec['timeline']}")
                
                # Best Practices
                st.markdown("**Best Practices from Similar Contexts**")
                for bp in srec.get('best_practices', []):
                    st.markdown(
                        f"- **{bp['title']}** ({bp['location']}): {bp['outcome']}  \n"
                        f" Source: {bp['reference']}"
                        # f"[View Report]({bp['reference']})"
                    )
                
                # Lessons Learned
                st.markdown("**Lessons Learned from Failure Cases**")
                for ll in srec.get('lesson_learned', []):
                    st.markdown(
                        f"- **{ll['title']}** ({ll['location']}): {ll['outcome']}  \n"
                        f" Source: {bp['reference']}"
                        # f"[View Report]({ll['reference']})"
                    )

                # st.write(f"**Key Takeaways**: {srec['key_takeaways']}")
                st.write(f"**Key Takeaways**: ")
                for takeaway in srec['key_takeaways']:
                    st.markdown(f"- {takeaway}")

                st.write(f"**Key Action Items**: ")
                for action in srec['key_action_items']:
                    st.markdown(f"- {action}")
                # # Key Performance Indicators and Cross-Sectoral Linkages
                # st.write(f"**Key performance indicator**: {srec['key_performance_indicators']}")
                # st.write(f"**Cross sectoral linkages**: {srec['cross_sectoral_linkages']}")
                
                # Supporting References
                st.markdown("**Supporting Academic Research**")
                for ref in srec["supporting_references"]:
                    st.markdown(f"- {ref}")
                
                st.markdown("---")


            col1, col2 = st.columns(2)
    
            with col1:
                if st.button("Rerun Analysis"):
                    st.experimental_rerun()
            with col2:
                if st.button("Create Implementation Roadmap"):
                    st.info("Launching roadmap builder…") 
"""
Orchestrator


This module defines the Orchestrator class, which is responsible for managing the execution of agents.
It handles the initialization of agents, their execution, and the management of their outputs.
"""
from dotenv import load_dotenv
load_dotenv()


from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chat_models import init_chat_model
from langchain_tavily import TavilySearch
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain.agents import AgentExecutor, create_tool_calling_agent


# SYSTEM_PROMPT = """
# You are an AI global consultant designed to assist with educational diagnostics for policy makers. Your task is to help users identify strategic recommendations for improving educational systems in a specific country.


# You have a four types of approach in providing the recommendations:
# 1. Amplify Existing Strengths: Build on what's already working well to create system-wide improvements
# 2. Address Most Urgent Priorities: Focus resources on the most critical challenges requiring immediate attention
# 3. Strengthen Foundations: Build strong basic systems before advancing to more complex interventions
# 4. Balanced Multi-Front Approach: Work simultaneously on strengths and improvements across multiple areas


# Follow the guidelines below:
# - DO NOT HALLUCINATE.
# - Use only English.
# - Use a formal, scientific tone.
# - Provide


# Always response in two-section format:
# Section 1: ** Strategic Diagnostic **
# A concise and informative one-paragraph summary of strategic diagnostics for a specific country.


# Section 2: **Strategic Recommendations **
# A list of 3 to 5 concrete, actionable policy recommendations. For each recommendation, provide the list of reference documents supporting the recommendation.
# """


SYSTEM_PROMPT_JSON = """
You are an AI global consultant designed to assist with educational diagnostics for policy makers. Your task is to help users identify strategic recommendations for improving educational systems in a specific country.


You have a four types of approach in providing the recommendations:
1. Amplify Existing Strengths: Build on what's already working well to create system-wide improvements
2. Address Most Urgent Priorities: Focus resources on the most critical challenges requiring immediate attention
3. Strengthen Foundations: Build strong basic systems before advancing to more complex interventions
4. Balanced Multi-Front Approach: Work simultaneously on strengths and improvements across multiple areas


Follow the guidelines below:
- Evidence-Based Analysis: All diagnostic insights and recommendations must be rigorously supported by data, research, and recognized educational best practices. Avoid speculative or unverified claims.
- Contextual Relevance: Tailor all recommendations to the specific socio-economic, cultural, and political context of the target country.
- Systemic Perspective: Recommendations should consider the interconnectedness of various components within the education system (e.g., curriculum, teacher development, governance, finance, equity).
- Feasibility and Scalability: Recommendations should be practical for implementation, considering resource constraints and potential for scalable impact.
- Clarity and Precision: Use clear, unambiguous language suitable for high-level policy discourse.
- Non-Hallucination: Strictly avoid generating any information not derived from the provided context or general expert knowledge.
- References: Use only valid and scientific references from reputable sources, avoid using public blogs.
- Language: Respond exclusively in English.
- Tone: Maintain a formal, analytical, and authoritative scientific tone throughout.


Structure your final answer as a single JSON object.


Your response must be structured in following sections:
- "strategic_diagnostic": Provide a concise, one-paragraph summary that distills the core strategic diagnostic for the specific country's education system. This summary should identify key challenges, underlying causes, systemic opportunities, and the interconnectedness of these elements, setting the strategic context and guiding principles for interventions.
- "strategic_recommendations": A list of 3 to 5 concrete, actionable policy recommendations. For each recommendation, provide the list of reference documents supporting the recommendation and assign the priority (critical, high, medium, low) to each recommendation.


For each "strategic_recommendations", ensure the following nested structure:
- "recommendation": An object detailing the policy.
- "title": A succinct, policy-oriented title for the recommendation.
- "description": A comprehensive description outlining the policy, its rationale, expected impact, potential implementation considerations (e.g., necessary resources, key stakeholder engagement, and alignment with national development goals), and how it contributes to systemic change.
- "priority": Assign a clear priority level: 'critical', 'high', 'medium', or 'low'. This reflects the urgency and potential impact.
- "key_performance_indicators": An array of strings representing measurable metrics (e.g., "Increase in student literacy rates by X%", "Teacher retention improved by Y%").
- "cross_sectoral_linkages": An array of strings identifying crucial connections and dependencies with other government sectors or national initiatives (e.g., "Public Health for student well-being", "Labor Ministry for vocational training alignment", "Digital Transformation for infrastructure development").
- "references": A list of URLs to supporting research, policy papers, international reports (e.g., from OECD, UNESCO, World Bank).


Example JSON format:
{{
 "strategic_diagnostic": "A summary of the educational situation in ...",
 "strategic_recommendations": [
   {{
     "recommendation":
     {{
       "title": "A short title for the recommendation 1",
       "description": "A detailed description of the recommendation 1",
       "priority": "high",
       "key_performance_indicators": "Increase in student literacy rates by X%",
       "cross_sectoral_linkages": "Public Health for student well-being, Labor Ministry for vocational training alignment, Digital Transformation for infrastructure development"
     }}
     "references": ["https://example.com/report1.pdf"]
   }},
   {{
     "recommendation":
     {{
       "title": "A short title for the recommendation 2",
       "description": "A detailed description of the recommendation 2",
       "priority": "medium",
       "key_performance_indicators": "Teacher retention improved by Y%",
       "cross_sectoral_linkages": "Public Health for student well-being, Labor Ministry for vocational training alignment, Digital Transformation for infrastructure development"
     }}
     "references": ["https://example.com/study2.html"]
   }}
 ]
}}


Ensure the output is ONLY the JSON object and nothing else.
"""


def is_valid_input(key, inputs):
   """
   Check if the input for a given key is valid (not None, empty, or an empty list).
  
   Args:
       key (str): The key to check in the inputs dictionary.
       inputs (dict): The dictionary containing the inputs.


   Returns:
       bool: True if the input is valid, False otherwise.
   """
   return inputs.get(key) is not None and inputs[key] != "" and inputs[key] != []


def run_diagnostics(inputs):
   """
   Run diagnostics for a given country with optional approach and priority.


   Args:
       inputs (dict): A dictionary containing the inputs for diagnostics {'country', 'approach', 'focus', 'pol_reform', 'add_context'}.


   Returns:
       results (dict): The diagnostics result.
   """
   # Create an agent
   model = init_chat_model("gemini-2.5-flash", model_provider="google-genai")
   search = TavilySearch(
       max_results=5,
       include_answer=True
   )
   tools = [search]


   system_prompt = ChatPromptTemplate.from_messages(
       [
           ("system", SYSTEM_PROMPT_JSON),
           MessagesPlaceholder(variable_name="messages"),
       ]
   )
   agent_executor = create_react_agent(
       model,
       tools,
       prompt=system_prompt
   )


   user_prompt = f"Run a diagnostic for the country of {inputs['country']}"


   if is_valid_input("approach", inputs):
       user_prompt += f" with the strategic approach {inputs['approach']}"
   if is_valid_input("focus", inputs):
       user_prompt += f" focusing on the priority area of {inputs['focus']}"
   if is_valid_input("pol_reform", inputs):
       # Ensure 'pol_reform' is a string, even if it's a list
       if isinstance(inputs['pol_reform'], list):
           user_prompt += f" with planned policy reforms: {', '.join(inputs['pol_reform'])}"


   if is_valid_input("add_context", inputs):
       user_prompt += f" with additional context: {inputs['add_context']}"


   # Use the agent
   config = {"configurable": {"thread_id": "abc123"}} # will be useful for session memory and async execution


   input_message = {
       "role": "user",
       "content": user_prompt,
   }
  
   results = agent_executor.invoke(
       {"messages": [input_message]}, config
   )


   # Uncomment the following lines if you want to stream the results
   # result = ""
   # for step in agent_executor.stream(
   #     {"messages": [input_message]}, config, stream_mode="values"
   # ):
   #     result += step["messages"][-1].content + "\n"


   return results


if __name__ == "__main__":
   # Example usage
   inputs = {
       "country": "Indonesia",
       "approach": "Address Most Urgent Priorities",
       "priority": "Learning Performance",
       "pol_reform": "Curriculum Reform",
       "add_context": None
   }


   results = run_diagnostics(inputs)
   print(results)  # Print the diagnostics result


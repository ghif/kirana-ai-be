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
- DO NOT HALLUCINATE.
- Use only English.
- Use a formal, scientific tone.

Structure your final answer as a single JSON object with the following keys: "strategic_diagnostic" and "strategic_recommendations".

Always response in two-section format:
- "strategic_diagnostic": A concise and informative one-paragraph summary of strategic diagnostics for a specific country.
- "strategic_recommendations": A list of 3 to 5 concrete, actionable policy recommendations. For each recommendation, provide the list of reference documents supporting the recommendation.

Example JSON format:
{{
  "strategic_diagnostic": "A summary of the educational situation in ...",
  "strategic_recommendations": [
    {{
      "recommendation": 
      {{
        "title": "A short title for the recommendation 1",
        "description": "A detailed description of the recommendation 1"
      }}
      "references": ["https://example.com/report1.pdf"]
    }},
    {{
      "recommendation": 
      {{
        "title": "A short title for the recommendation 2",
        "description": "A detailed description of the recommendation 2"
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
    config = {"configurable": {"thread_id": "abc123"}}

    input_message = {
        "role": "user",
        "content": user_prompt,
    }
    
    results = agent_executor.invoke(
        {"messages": [input_message]}, config
    )
    # result = ""
    # for step in agent_executor.stream(
    #     {"messages": [input_message]}, config, stream_mode="values"
    # ):
    #     result += step["messages"][-1].content + "\n"

    return results

# # Create an agent
# model = init_chat_model("gemini-2.5-flash", model_provider="google-genai")
# search = TavilySearch(
#     max_results=3,
#     include_answer=True
# )
# tools = [search]

# system_prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system", SYSTEM_PROMPT),
#         MessagesPlaceholder(variable_name="messages"),
#     ]
# )
# agent_executor = create_react_agent(
#     model, 
#     tools,
#     prompt=system_prompt
# )

# country = "Indonesia"
# approach = "Address Most Urgent Priorities"
# priority = "Equity and Inclusion"
# additional_context = None

# user_prompt = f"Run a diagnostic for the country of {country}"

# if approach is not None:
#     user_prompt += f" with the strategic approach {approach}"
# if priority is not None:
#     user_prompt += f" focusing on the priority area of {priority}"
# if additional_context is not None:
#     user_prompt += f" with additional context: {additional_context}"

# # Use the agent
# config = {"configurable": {"thread_id": "abc123"}}


# input_message = {
#     "role": "user",
#     "content": user_prompt,
# }
# for step in agent_executor.stream(
#     {"messages": [input_message]}, config, stream_mode="values"
# ):
#     step["messages"][-1].pretty_print()

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
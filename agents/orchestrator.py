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
from templates import SYSTEM_PROMPT_JSON
from tools import rag_retrievers as rr

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

def run_diagnostics_with_planned_reforms(inputs, use_tool="vertex_rag"):
    """
    Run diagnostics for a given country with planned reforms and expected outcomes.


    Args:
        inputs (dict): A dictionary containing the inputs for diagnostics {'country', 'planned_reforms', 'expected_outcome', 'add_context', 'strategy', 'language'}.


    Returns:
        results (dict): The diagnostics result.
    """
    # Create an agent
    model = init_chat_model("gemini-2.5-flash", model_provider="google-genai")

    if use_tool == "tavily":
        search = TavilySearch(
            max_results=5,
            include_answer=True
        )
        tools = [search]
    elif use_tool == "vertex_rag":
        tools = [rr.retrieve_from_vertex_rag_engine]


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

    if is_valid_input("language", inputs):
        user_prompt += f" in {inputs['language']} language"
    if is_valid_input("planned_reforms", inputs):
        user_prompt += f" with planned reforms: {', '.join(inputs['planned_reforms'])}"
    if is_valid_input("expected_outcome", inputs):
        user_prompt += f" with expected outcome: {inputs['expected_outcome']}"
    if is_valid_input("add_context", inputs):
        user_prompt += f" with additional context: {inputs['add_context']}"
    if is_valid_input("strategy", inputs):
        user_prompt += f" using the strategic approach: {inputs['strategy']}"

    if use_tool == "vertex_rag":
        user_prompt += "\nMake sure that all the cited and retrieved documents (including for 'best_practices' and 'lesson_learned') and the diagnostic insights are taken from the Vertex RAG Engine -- no citation outside of the RAG corpus is allowed."


    # Use the agent
    config = {"configurable": {"thread_id": "abc123"}}  # will be useful for session memory and async execution


    input_message = {
        "role": "user",
        "content": user_prompt,
    }
  
    results = agent_executor.invoke(
        {"messages": [input_message]}, config
    )

    return results


if __name__ == "__main__":
    # Example usage
    # inputs = {
    #     "country": "Indonesia",
    #     "approach": "Address Most Urgent Priorities",
    #     "priority": "Learning Performance",
    #     "pol_reform": "Curriculum Reform",
    #     "add_context": None
    # }


    # results = run_diagnostics(inputs)
    # print(results)  # Print the diagnostics result

    inputs = {
        "country": "Indonesia",
        "planned_reforms": ["Curriculum Reform", "Teacher Reform"],
        "expected_outcome": "Improved student literacy rates",
        "add_context": None,
        "strategy": "Amplify Existing Strengths",
        "language": "English"
    }

    results = run_diagnostics_with_planned_reforms(inputs, use_tool="vertex_rag")
    # print(results)  # Print the diagnostics result
    print("Diagnostics Results:")
    for message in results['messages']:
        message.pretty_print()

    # query = "summarize the latest research on education aid"

    # serialized_docs = rr.retrieve_from_vertex_rag_engine(query)

    


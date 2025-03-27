from backend.states.state import SharedState
from backend.models.models import getLLM
from backend.prompts.prompts import planner_agent_prompt, research_agent_prompt, reviewer_agent_prompt
import re
from backend.utils.research_helper import run_research_task
import json


def planner_agent(state: SharedState):
    print("=========entring planner agent=========")

    title = state.get("title")
    location = state.get("location")
    jobs_length = state["jobs_length"]
    llm = getLLM("gemini")

    rag_chain = planner_agent_prompt | llm

    response = rag_chain.invoke({"title":title,"location":location,"jobs_length":jobs_length })
    response_content = response.content
    cleaned_json = re.sub(r"```json\n|```", "", response_content).strip()
    planner_data = json.loads(cleaned_json)
    state["planner_response"] = planner_data
    print("=========exiting planner agent=========")    
    return state

def researcher_agent(state: SharedState):
    print("=========entering research agent=========")    
    data = state["planner_response"]


    # Extract search term
    search_term = data["search_term"]
    overall_strategy = data["overall_strategy"]

    # Extract platform details
    companies_list = data["companies"]

    # Jobs length
    jobs_length = state["jobs_length"]

    # Prepare structured filters and notes

    # Import the function
    llm = getLLM("gemini")  # Initialize LLM

    responses = run_research_task(companies_list,overall_strategy, search_term, llm, research_agent_prompt,jobs_length)

    print("response", responses)

    state["publisher_response"] = responses # Correctly store the responses dictionary
    print("=========exiting research agent=========")    
    return state


def executor_agent(state:  SharedState):
    print("=========starting executor agent=========")    
  #  report = generate_report(state["publisher_response"])
    jobs=state["publisher_response"]
    print("=========executor jobs=========")
    print(jobs)
    
    llm = getLLM("gemini")  # Initialize LLM

    rag_chain = reviewer_agent_prompt | llm

    response = rag_chain.invoke({"jobs":jobs })
    response_content = response.content

    state["executor_response"]= response_content
    print("=========exiting executor agent=========")    
    return state


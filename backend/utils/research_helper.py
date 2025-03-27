from backend.tools.tavily import tavily_tool
from langchain.agents import AgentExecutor, create_react_agent
import re
import json

tools=[tavily_tool]

def format_filters(filters_str):
    """Formats a string of filters into a list of formatted lines."""
    if not filters_str:
        return "No filters provided."
    filter_lines = [f" - {filter_item.strip()}" for filter_item in filters_str.split(",")] #split the string into a list.
    return "\n".join(filter_lines)

def format_notes(notes_list):
    """Formats a list of notes into a string of formatted lines."""
    if not notes_list:
        return "No notes provided."
    note_lines = [f" - {note.strip()}" for note in notes_list]
    return "\n".join(note_lines)

def run_research_task(companies,overall_strategy, search_term, llm, prompt,jobs_length):
    response=""
    
    print("companies",companies)
    print("overall_strategy",overall_strategy)
    print("search_term",search_term)
   
    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,
                                   handle_parsing_errors=True,
                                   max_iterations=len(companies) * 5)

   # Format your input data
    formatted_companies = "\n".join(
        f"""- {p['company_name']}
            Filters: {p['filters']}
            Notes: {p['notes']}"""
        for p in companies
    )

    # Run the agent
    response = agent_executor.invoke({
        "input": f"Find {search_term} listings across companies",
        "search_term": search_term,
        "overall_strategy": overall_strategy,
        "companies": formatted_companies,
        "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in tools]),
        "tool_names": ", ".join([tool.name for tool in tools]),
        "jobs_length": jobs_length
    })


        
    # Extract and clean the output (assuming the agent outputs JSON within its final response)
    response_content = response["output"]

    cleaned_json = re.sub(r"```json\n|```", "", response_content).strip()

    data = json.loads(cleaned_json)

    return data



def run_reviewer_task(jobs, llm, prompt):
    response=""

    agent = create_react_agent(llm=llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True,
                                   handle_parsing_errors=True,
                                   max_iterations=len(jobs) * 3)
    # Run the agent
    response = agent_executor.invoke({
       "input": f"Find details of each listings using jobs list",
        "jobs": jobs,
        "tools": "\n".join([f"{tool.name}: {tool.description}" for tool in tools]),
        "tool_names": ", ".join([tool.name for tool in tools])
    })


    print("reviewer task",response["output"])
        
    # Extract and clean the output (assuming the agent outputs JSON within its final response)
    response_content = response["output"]

    cleaned_json = re.sub(r"```json\n|```", "", response_content).strip()

    data = json.loads(cleaned_json)

    return data
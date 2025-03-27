from langchain_core.prompts import ChatPromptTemplate, PromptTemplate

planner_prompt_template="""
You are a planner. Your task is to create a search plan based on the user's provided job title and location, with an emphasis on identifying popular companies in the given area and searching for relevant job openings at those companies.

User Input:
- Job Title: {title}
- Location: {location}
- Number of Jobs: {jobs_length}

Your plan should include:
- The most relevant search term that incorporates both the job details and the companies' angle.
- Guidance for the researcher agent on how to search across popular job sites and company career pages to find the most relevant jobs at popular companies in the given location.
- Suggestions on refining the search using platform-specific filters and sorting options.
- Additional considerations such as identifying top companies in the area that are known for hiring in this field.
- Ensure the plan only covers the number of jobs requested by the user.

### Instructions:
- Construct an optimal search term that includes the job title, location, and hints at targeting top companies.
- Guide the researcher agent on refining their search across various companies, including both job boards and individual company career pages.
- Suggest filters (e.g., company rating, industry-specific filters) and sorting options (e.g., most recent, highest salary) relevant to each platform.
- Provide any additional insights or considerations based on the specific features of the companies and the prominence of companies in the given location.

### Response Format:
```json
{{
    "search_term": "The most relevant search term to start with, incorporating job title, location, and company emphasis",
    "overall_strategy": "The overall strategy to guide the search process, including targeting popular companies in the location",
    "companies": [
        {{
            "company_name": "Genesys",
            "initial_search": "The tailored search term for Indeed",
            "filters": "Filters and sorting options relevant to Indeed (e.g., company rating, date posted)",
            "notes": "Additional considerations for Indeed, including ways to identify popular companies"
        }}
    ]
}}
"""



research_prompt_template ="""You are an expert job search assistant specialized in finding most relevant jobs find atleast {jobs_length} jobs. Follow these steps:

1. Analyze companies: {companies}
2. Use strategy: {overall_strategy}
3. Search term: {search_term}
4. Use tools: {tools}

Follow this format:

Question: The user's job search request
Thought: Your step-by-step reasoning process
Action: The tool to use (must be one of [{tool_names}])
Action Input: The search query input
Observation: The search result
... (repeat until you have the final answer)
Final Answer: Give listing job in JSON format

Current Search Details:
Search Term: {search_term}
Overall Strategy: {overall_strategy}
Companies Details:
{companies}

Begin!

Question: {input}
{agent_scratchpad}"""



reviewer_prompt_template = """**Role**: Expert Job Data Consolidator

**Objective**: Extract and unify key details from multiple job listings. Follow these steps:

**URL Processing**
   - Iterate through job: {jobs}
   - For each job extract:
     a. Description
     b. Platform
     c. Location
     d. Job Title
     e. Experience
     f. Company
     g. Industry
     h. Employment Type
     i. Salary
     j. Url of the job listing

**Output Format**: 
Return the results as plain text in a list format. Each job should be a separate list item formatted as follows:

Job Title: [Job Title]
Platform: [Platform]
Location: [Location]
URL: [Job URL]
Employment Type: [Employment Type]
Experience: [Experience]
Salary: [Salary]
Company: [Company]
Industry: [Industry]

Ensure that each job listing appears as a separate, clearly delineated text item in the final output.
"""




planner_agent_prompt = ChatPromptTemplate.from_template(planner_prompt_template)


research_agent_prompt = PromptTemplate(
        template=research_prompt_template,
        input_variables=[
            "input",
            "tools",
            "tool_names",
            "agent_scratchpad",
            "search_term",
            "overall_strategy",
            "companies",
            "jobs_length"
        ]
    )


reviewer_agent_prompt = ChatPromptTemplate.from_template(reviewer_prompt_template)
# reviewer_agent_prompt = PromptTemplate(
#         template=reviewer_prompt_template_two,
#         input_variables=[
#             "input",
#             "tools",
#             "tool_names",
#             "agent_scratchpad",
#             "jobs"
#         ]
#     )



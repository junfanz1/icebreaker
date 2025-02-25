import os
from dotenv import load_dotenv

from tools.tools import get_profile_url_tavily

load_dotenv()
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import Tool
from langchain.agents import (
    create_react_agent,
    AgentExecutor,
)
# ReAct_agent to create agents in LLM
# AgentExecutor is the object to receive prompt

# Create ReAct agent with LangChain
def lookup(name: str) -> str:
    llm = ChatOpenAI(
        temperature = 0,
        model_name = "gpt-4o-mini",
    )
    template = """
    given full name {name_of_person}, get a link to their Linkedin profile page, answer contain only a URL
    """
    prompt_template = PromptTemplate(
        template=template, input_variables=["name_of_person"]
    )
    tool_for_agent = [
        Tool(
            name="crawl Google 4 Linkedin profile page",
            func=get_profile_url_tavily,
            description="useful for when you need get the LinkedIn URL page",
        )
    ]

    react_prompt = hub.pull("hwchase17/react")
    agent = create_react_agent(llm=llm, tools=tool_for_agent, prompt=react_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tool_for_agent, verbose=True)

    result = agent_executor.invoke(
        input={"input": prompt_template.format_prompt(name_of_person=name)}
    )

    linkedin_profile_url = result["output"]
    return linkedin_profile_url

if __name__ == "__main__":
    linkedin_url = lookup(name="Eden Marco")
    print(linkedin_url)
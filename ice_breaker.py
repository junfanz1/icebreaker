from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.schema import StrOutputParser
from langchain_ollama import ChatOllama
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import summary_parser, Summary


def ice_break_with(name: str) -> Tuple[Summary, str]:
    linkedin_username = linkedin_lookup_agent(name=name)
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_username)
    summary_template = """
        Given Linkedin information {information} of the person, create:
        1. short summary of the person
        2. two interesting facts about the person
        Use both information from Twitter and LinkedIn
        \n{format_instructions}
        """
    summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template,
                                             partial_variables={"format_instructions": summary_parser.get_format_instructions()})
    llm = ChatOpenAI(temperature=0, model_name="gpt-4o-mini")
    chain = summary_prompt_template | llm | summary_parser # pipe operator coming from LangChain expression language
    linkedin_data = scrape_linkedin_profile(linkedin_profile_url="https://www.linkedin.com/in/junfan-zhu/")
    res:Summary = chain.invoke(input={"information": linkedin_data})
    return res, linkedin_data.get("profile_pic_url")

if __name__ == "__main__":
    load_dotenv()
    print("Ice Breaker!")
    #llm = ChatOllama(model="llama3")
    ice_break_with(name="Junfan Zhu UChicago")




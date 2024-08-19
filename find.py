import os
from inference import Inference
from config import Config
from groq import Groq
import re
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_community.tools.tavily_search import TavilySearchResults

class FindInfo:
    def __init__(self, sys_prompt: str = None, user_prompt: str = None, model_name: str = "gemma-7b-it", config = None):
        self.user_prompt = user_prompt
        self.sys_prompt = sys_prompt 
        self.model_name = model_name
        self.config = config

        self.inference = Inference()

        #self.should_search()
        self.generate_search_query()

    def should_search(self):
        # Ask model if the Wiki contains relavant information to answer query
        # If no, continue to search
        # If yes, return to main RP

        eng = """Given the above wiki, simply, does the wiki have enough information to fully answer the below query? 
        Answer: No
        Answer: Yes
        Asnwer: Yes
        """
        sys_prompt_eng = f"{self.config.wiki_init}\n\n{eng}"
        user_prompt_eng = f"""Given the above wiki, simply, does the wiki have enough information to fully answer this query: {self.user_prompt}? 
        Answer: No
        Answer: Yes
        Asnwer: Yes
        Asnwer:
        """

        response = self.inference.infer(sys_prompt_eng, user_prompt_eng, self.model_name)
        response = re.sub('[.,:;?`~!*]', '', response.lower()).split()

        print(response)

        if "no" in response:
            print("Must search")
            self.generate_search_query()
        elif "yes" or "yes." in response:
            print("No need to search")
            return

    def generate_search_query(self):
        #eng = """Generate a google search to obtain missing information need to help answer the below query

        self.sys_prompt = """
        We've been discussing the character Echidna from the series Re:Zero. The conversation started with a long block of text about Echidna's appearance, personality, history, abilities, and trivia. We didn't discuss Subaru's birthday yet, but we can go back to that question now.

        To answer your question, Subaru's birthday is not mentioned in the provided text. If you need to know Subaru's birthday, I can try to find that information for you from other sources or by asking follow-up questions.
        """
        eng = "Given the above summary for context, generate a descriptive, complete google search to help retrieve data missing from the above wiki from google, needed to help answer the below question:\n"
        
        sys_prompt_eng = f"{self.config.wiki_init}\n\n{eng}"
        sys_prompt_eng = f"{self.sys_prompt}\n\n{eng}"
        user_prompt_eng = f"{self.user_prompt}\nSearch:"

        print(sys_prompt_eng, user_prompt_eng)

        response = self.inference.infer(sys_prompt_eng, user_prompt_eng, self.model_name)

        print(response)


    def search_tavily(query):
        search = TavilySearchResults(max_results=2)
        search_results = search.invoke(query)
        return search_results

if __name__ == "__main__":
    pass


# Figure out if a search is needed

# You are a data analyst, given the above wiki please decide wether further data gathering is necassary
# Answer: No
# Answer: Yes
# Answer: Yes


# Summarize missing info
# Consruct google search
# Appened to wiki





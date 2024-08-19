import os
from tavily import TavilyClient
from groq import Groq
import re

from langchain_core.chat_history import (
    BaseChatMessageHistory,
    InMemoryChatMessageHistory,
)
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

class Inference:
    def __init__(self, character_prompt: str = None, config = None):
        self.char_prompt = character_prompt
        self.char_data = self._init_search()
        self.config = config
        self.rp_prompt = self.config.sys_prompt_rp 
        self.store = {}
        self.chat_config = {"configurable": {"session_id": "abc2"}}

    # Perform original data scrape for RP prompt
    def _init_search(self):
        self.client = TavilyClient(api_key="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")

        char_prompt_eng = f"Tell me about {self.char_prompt}, in detail and depth"
        char_data = self.client.qna_search(char_prompt_eng, search_depth="advance", topic="general")

        return char_data
    
    def generic_search(self, search: str = None):
        response = self.client.qna_search(search, search_depth="basic", topic="general")
        print(f"===== Generic Search =====: \n {response}")
        return response
    
    # Judge a search to be needed or not by wether it references contextual information
    def _search_needed(self, search: str = None):
        prompt = """Roleplay as a recluse person who does not say more then one word at a time. \n Given a sequence of text, classify if it references contextual conversational information or not. Please answer with Yes or No"""
        response = self.infer(sys_prompt=prompt, user_prompt=search)
        response = re.sub('[.,:;?`~!*]', '', response.lower()).split()

        if "no" in response:
            return False
        elif "yes" in response:
            return True
    
    def _add_ctx(self, search: str):
        prompt = self.char_data + "\n\n" + """Rephrase the below question to be about the above context, please use simple words and keep the question straight to the point. Keep the original intent of the question the same. Phrase the question more like a google search"""
        print(f"===== Add Ctx Prompt ===== : \n {prompt}")

        response = self.infer(sys_prompt=prompt, user_prompt=search)
        print(f"===== Add Ctx response =====: \n {response}")
        return response

    def _update_sys_prompt(self, user_prompt: str = None):
        #if self._search_needed(user_prompt):
        self.char_data += "\n" + self.generic_search(self._add_ctx(user_prompt))
        self.sys_prompt = self.char_data + "\n\n" + self.rp_prompt

        print(f"===== Updated Sys prompt =====: \n {self.sys_prompt}")
    
    def infer(self, user_prompt: str = None, sys_prompt: str = None, model_name: str = "gemma2-9b-it"):
        client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": sys_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ],
            model=model_name,
        )

        return chat_completion.choices[0].message.content

    def _get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        if session_id not in self.store:
            self.store[session_id] = InMemoryChatMessageHistory()
        return self.store[session_id]

    def user_infer(self, user_prompt: str = None, model_name: str = "gemma2-9b-it"):
        self._update_sys_prompt(user_prompt)

        model = ChatGroq(model=model_name)
        with_message_history = RunnableWithMessageHistory(model, self._get_session_history)

        response = with_message_history.invoke(
            [
                HumanMessage(content=user_prompt), 
                SystemMessage(content=self.sys_prompt)
            ],
            config=self.chat_config,
        )

        return response.content
    
# Old user_infer, no chat history
    # Generic inference, gotta handle sys prompt on the backend 
    # def user_infer(self, user_prompt: str = None, model_name: str = "gemma2-9b-it"):
    #     self.update_sys_prompt(user_prompt)

    #     print(self.sys_prompt)

    #     client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

    #     chat_completion = client.chat.completions.create(
    #         messages=[
    #             {
    #                 "role": "system",
    #                 "content": self.sys_prompt
    #             },
    #             {
    #                 "role": "user",
    #                 "content": user_prompt
    #             }
    #         ],
    #         model=model_name,
    #     )

    #     return chat_completion.choices[0].message.content

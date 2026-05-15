from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field

class Scheme(BaseModel):
    isAppRequest: bool = Field(description="TRUE if user explicitly requesting to create, build something, If you don't understand what user wants to build ask them to elaborate more. eg.(I wanna build something, Let's create a project, I want to write a code etc.)")
    isInfo: bool = Field(description="TRUE if providing facts to be remembered for a long time. eg.(name, age, location, profession, projects etc.)")

class Filter:
    def __init__(self, model="gpt-oss:120b-cloud"): 
        self.llm = ChatOllama(model=model, temperature=0, format="json") 
        self.structured_llm = self.llm.with_structured_output(Scheme)
        print(f"\033[93m[layer 1 loaded]\033[0m")

    def filter(self, msg):
        prompt = ChatPromptTemplate.from_messages([
            ("system", "You are a filter that determines if the user's message is an app request or information to be remembered. An app request is when the user is asking you to create, build, or write something. Information to be remembered is when the user is providing facts or details that should be stored for future reference. Please analyze the user's message and respond with a JSON object containing two boolean fields: 'isAppRequest' and 'isInfo'."),
            ("user", "{input}")
        ])
        
        chain = prompt | self.structured_llm

        try:
            res = chain.invoke({"input": msg})
            return res.isAppRequest, res.isInfo
        except Exception as e:
            print(f"\033[91m[Filter Error]:\033[0m {e}")
            return False, False
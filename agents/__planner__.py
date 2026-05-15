from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional

class FileScheme(BaseModel):
    filename: str = Field(description="The name of the file to create")
    description: str = Field(description="Description of what the file does")
    file_path: str = Field(
        description="The path where the file should be created")

class Scheme(BaseModel):
    plan_content: str = Field(
        description="The narrative plan to execute in a paragraph format (3-4 sentences)."
    )
    tech_stack: str = Field(
        description="A comma-separated list of the technologies to be used."
    )
    files: list[FileScheme] = Field(
        description="A list of files to create, each with a filename, description, and file path. If assets are needed, include them here with their description and file path. MUST BE DETAILED. YOU MUST INCLUDE a one-click execution script (e.g., 'run.sh' for Linux/Mac and 'run.bat' for Windows) that installs all dependencies (e.g., pip install) and starts the main application."
    )

class Planner:
    def __init__(self, model: str = "gpt-oss:120b-cloud"):
        self.model = model
        self.llm = ChatOllama(model=self.model, temperature=0, format="json")
        self.parser = PydanticOutputParser(pydantic_object=Scheme)
        
        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a part of a big system of AI agents. You are the planner.
                Your job is to create a detailed plan for how to build an application based on the user's request.
                Your plan is then submitted to the System Engineer AI. Plan accordingly so that the next LLM can build your design seamlessly.
                DO NOT write a single line of code; that is the job for the System Engineer AI.

                CRITICAL REQUIREMENT:
                You must ALWAYS include a 'run.sh' and/or 'run.bat' script in your file list. This script must contain the commands to install required dependencies (e.g., npm install, pip install -r requirements.txt) and launch the application.
                
                You must format your output strictly as a JSON object matching the following instructions:
            {format_instructions}"""),
            ("user", "{user_input}")
        ])
        
        self.chain = self.prompt_template | self.llm | self.parser
        
        print(f"\033[93m[Layer 1 loaded]\033[0m")
    
    def plan(self, user_input: str) -> Optional[Scheme]:
        print(f"\033[94m[Please wait while our agent designs your request...]\033[0m\n")

        try:
            planning_response = self.chain.invoke({
                "user_input": user_input,
                "format_instructions": self.parser.get_format_instructions()
            })
            return planning_response
        except Exception as e:
            print(f"\033[91m[Planner Agent Error]:\033[0m {e}")
            return None
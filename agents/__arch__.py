from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate 
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Optional

class Code(BaseModel):
    filename: str = Field(description="The name of the file to be created, including extension.")
    code: str = Field(description="The complete, working code for this file. Do not truncate.")
    filePath: str = Field(description="Path to the generated file")

class CodeFiles(BaseModel):
    files: list[Code] = Field(description="The complete list of all generated code files required for the project.")
class Arch:
    def __init__(self, model: str = "gpt-oss:120b-cloud"):
        self.model = model
        self.llm = ChatOllama(model=self.model, temperature=0, format="json")
        self.parser = PydanticOutputParser(pydantic_object=CodeFiles)

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", """You are a part of a big system of AI agents. You are the System Engineer and Lead Programmer.
                Your job is to write complete, fully functioning code based on the provided architectural plan.
                Your generated code will then be saved to the system with the specific path and file name.
                For images/asset files, write description of the image in place of code, it will be send to a image generation model as prompt
                You must format your output strictly as a JSON object matching the following instructions:
                {format_instructions}"""),
            ("user", "{user_input}")
        ])

        self.chain = self.prompt_template | self.llm | self.parser
        
        print(f"\033[93m[Layer 3 loaded]\033[0m")

    def build(self, prompt: str) -> Optional[CodeFiles]:
        print(f"\033[94m[Please wait while our agent writes the code files...]\033[0m\n")

        try:
            code_response = self.chain.invoke({
                "user_input": prompt,
                "format_instructions": self.parser.get_format_instructions()
            })
            return code_response
        except Exception as e:
            print(f"\033[91m[Builder Agent Error]:\033[0m {e}")
            return None
from agents import __prompt_filterer__
from agents import __assistant__

def saveInformation(info):
    # Save our information in PostgreSQL/JSON/TEXT-file
    print(f"\033[92m[Information Saved]:\033[0m {info}")
    pass

class PromptEngine:
    def __init__(self, model="gpt-oss:120b-cloud"):
        self.prompt_filterer = __prompt_filterer__.Filter(model=model)
    def run(self, prompt: str):
        try:
            isAppRequest, isInfo = self.prompt_filterer.filter(prompt)
            
            if isAppRequest:
                return True
            else:
                # Loading assistant here as user will most likely send app req
                __assistant__.Assistant().get_response(prompt)
                if isInfo:
                    saveInformation(prompt)

                return False
        except Exception as e:
            print(f"\033[91m[Prompt Engine Error]:\033[0m {e}")
            return False
import ollama

class Assistant:
    def __init__(self, model="gpt-oss:120b-cloud"):
        self.model = model
    def get_response(self, prompt):
        stream = ollama.chat(model=self.model, 
                             messages=[{'role': 'user', 'content': prompt}],
                             stream=True)
        for chunk in stream:
            content = chunk['message']['content']
            print(content, end="", flush=True)
        
        print("\n")
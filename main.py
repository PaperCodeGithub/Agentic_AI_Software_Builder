import os
from colorama import Fore, Style

from engines import PromptEngine
from engines import PlannerEngine
from engines import ArchEngine
from engines import MemoryEngine

from traversing import __chain_traverse__
from traversing.__chain_traverse__ import AgentResponse 

from rich.console import Console

class Orchestrator:
    def __init__(self):
        print(f"{Fore.CYAN}[Initializing Engines...]{Style.RESET_ALL}")

        self.console = Console()
        with self.console.status("[bold cyan][/bold cyan]", spinner="bouncingBar"):
            self.prompt_engine = PromptEngine.PromptEngine()
            self.planner_engine = PlannerEngine.PlannerEngine()
            self.arch_engine = ArchEngine.ArchEngine()
            self.mem_engine = MemoryEngine.MemoryEngine(db_path="data/agent.db")

    def start_traversal(self, name: str):
        project_path = os.path.join("Generated Projects", name)
        traversal = __chain_traverse__.TraverseEngine(project_path)
        
        vector_store = traversal.traverse()
        
        ai_agent_chain = traversal.loadAIAgent(vector_store, AgentResponse)
        query_chain = traversal.loadQueryModel(vector_store)

        print(f"\n{Fore.GREEN}[Entering Traversal Mode for '{name}']{Style.RESET_ALL}")
        print("Type 'exit' to return to the main menu.\n")

        while True:
            query = input(f"{Fore.CYAN}>> {Style.RESET_ALL}").strip()

            if query.lower() in ["exit", "quit"]:
                print(f"{Fore.YELLOW}[Exiting Traversal Mode]{Style.RESET_ALL}")
                break
            
            if not query:
                continue  

            if self.prompt_engine.prompt_filterer(query): 
                try:
                    print(f"\n{Fore.CYAN}Thinking...{Style.RESET_ALL}")
                    result = ai_agent_chain.invoke(query)
                    print(f"\n{Fore.YELLOW}AI:{Style.RESET_ALL} {result.explanation}\n")
            
                    if result.files:
                        for file in result.files:
                            full_path = os.path.join(project_path, file.filepath)
                            directory = os.path.dirname(full_path)
                            
                            if directory:
                                os.makedirs(directory, exist_ok=True)
                                
                            with open(full_path, "w", encoding="utf-8") as f:
                                f.write(file.code)
                                
                            print(f"{Fore.GREEN}[Saved]{Style.RESET_ALL} {full_path}")
                    else:
                        print(f"{Fore.MAGENTA}No files were generated.{Style.RESET_ALL}")
                except Exception as e:
                    print(f"{Fore.RED}[Agent Error]:{Style.RESET_ALL} {e}")

            else:
                try:
                    for chunk in query_chain.stream({"input": query}):
                        if "answer" in chunk:
                            print(chunk["answer"], end="", flush=True)
                    print("\n")
                except Exception as e:
                    print(f"{Fore.RED}[Query Error]:{Style.RESET_ALL} {e}")

    def run_work_flow(self, prompt: str):
        try:
            name = input(f"{Fore.YELLOW}Enter project name: {Style.RESET_ALL}").strip()
            if not name:
                print(f"{Fore.RED}[Error]{Style.RESET_ALL} Project name cannot be empty.")
                return

            plan = self.planner_engine.run(prompt)
            if not plan:
                return

            parsed_prompt = f"Goal: {plan.plan_content}\nTech-stack: {plan.tech_stack}\nFiles:\n{plan.files}"
            
            self.arch_engine.run(parsed_prompt, name)
            
            self.mem_engine.save_turn(role="user", content=prompt)
            self.mem_engine.save_turn(role="planner", content=str(plan.plan_content))

            print(f"\n{Fore.GREEN}[Project Generation is complete]{Style.RESET_ALL}\n")

            while True:
                choice = input("Do you want to traverse the project and debug/learn about it? (y/n): ").lower().strip()
                if choice == "y":
                    self.start_traversal(name)
                    break
                elif choice == "n":
                    break
                else:
                    print(f"{Fore.RED}Not a valid choice. Please enter 'y' or 'n'.{Style.RESET_ALL}")
                    
        except Exception as e:
            print(f"\033[91m[Workflow Error]:\033[0m {e}")
    
def main():
    app = Orchestrator()
    print(f"\n{Fore.MAGENTA}--- AI Builder Ready ---{Style.RESET_ALL}")

    while True:
        user_input = input(f"\nEnter your prompt: ").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting the program.")
            break

        if not user_input:
            continue

        if app.prompt_engine.run(user_input):           
            app.run_work_flow(user_input)
        
if __name__ == "__main__":
    main()
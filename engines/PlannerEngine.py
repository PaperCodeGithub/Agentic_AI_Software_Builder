from agents import __planner__

class PlannerEngine:
    def __init__(self, model="gpt-oss:120b-cloud"):
        self.planner = __planner__.Planner(model=model)
    
    def run(self, user_input):
        try:
            plan = self.planner.plan(user_input)
            if plan is None:
                print(f"\033[91m[Engine Error]:\033[0m No plan generated.")
            else:
                print(f"\033[92m[Plan Generated Successfully]\033[0m")
                print(f"\033[93m[Plan Details]:\033[0m {plan.plan_content}")
                print(f"\033[93m[Tech Stack]:\033[0m {plan.tech_stack}")
                print(f"\033[93m[Files]:\033[0m")
                for file in plan.files:
                    fdesc = getattr(file, 'description', 'No description')
                    fpath = getattr(file, 'file_path', 'No path')
                    print(f"  - {fpath}: {fdesc}")
                
            return plan

        except Exception as e:
            print(f"\033[91m[Planner Engine Error]:\033[0m {e}")
            return None
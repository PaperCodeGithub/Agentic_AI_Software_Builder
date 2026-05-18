import os
import stat
from agents import __arch__
from engines import AssetEngine

class ArchEngine():
    def __init__(self, model="gpt-oss:120b-cloud"):
        self.arch = __arch__.Arch(model=model)
        self.assetE = AssetEngine.AssetEngine()

    def run(self, prompt: str, name: str):
        try:
            res = self.arch.build(prompt=prompt)

            if res and res.files:
                for file in res.files:
                    fpath = file.filePath
                    fname = file.filename
                    fcode = file.code

                    if fname not in fpath:
                        relative_path = os.path.join(fpath, fname)
                    else:
                        relative_path = fpath

                    full_path = os.path.join("Generated Projects", name, relative_path)
                    directory = os.path.dirname(full_path)
                    
                    if directory:
                        os.makedirs(directory, exist_ok=True)
                        
                    try:
                        if fname.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):        
                            if not os.path.exists(full_path):
                                self.assetE.generate(fcode, full_path)
                                print(f"\033[92m[Asset Generated]\033[0m {full_path}")
                            else:
                                print(f"  \033[90m[Skipping]: {fname} already exists.\033[0m")
                        
                        # ROUTE 2: Normal source/text file (The Crucial Fix)
                        else:
                            with open(full_path, "w", encoding="utf-8") as f:
                                f.write(fcode)
                            print(f"\033[92m[Saved]\033[0m {full_path}")

                        # Grant shell scripts executable privileges
                        if fname.endswith(".sh"):
                            st = os.stat(full_path)
                            os.chmod(full_path, st.st_mode | stat.S_IEXEC)
                            print(f"\033[93m[Made Executable]\033[0m {full_path}")

                    except Exception as e:
                        print(f"\033[91m[Error saving {fname}]:\033[0m {e}")
            else:
                print("\033[91m[ArchEngine Error]:\033[0m No files were generated.")
        except Exception as e:
            print(f"\033[91m[Builder Agent Error]:\033[0m {e}")
import os
from pathlib import Path
import torch
from diffusers import StableDiffusionPipeline

class AssetEngine:
    def __init__(self):
        self.model = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16)
        self.model.to("cuda")
        print(f"\033[93m[Asset Engine Ready (Powered by HF Client)]\033[0m")

    def generate(self, prompt, file_path):
            print(f"\n\033[95m[Asset Engine]:\033[0m Generating image for '{Path(file_path).name}'...")
            
            enhanced_prompt = f"{prompt}, simple 2d video game asset, flat design, solid background, high quality"
            
            try:
                image = self.model(enhanced_prompt).images[0]
                
                os.makedirs(os.path.dirname(file_path) or '.', exist_ok=True)
                image.save(file_path)
                
                print(f"  \033[92m[Asset Saved]:\033[0m {file_path}")
                return True
                
            except Exception as e:
                print(f"  \033[91m[Asset Generation Failed]:\033[0m {str(e)}")
                return False
        
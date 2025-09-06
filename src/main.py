from models import gemma3, llama3p2, llama3p1, deepseek_r1, gemini
from utils import load
from preprocessor import preprocessor
from rewriter import rewriter
from formatter import formatter
from tqdm import tqdm
import asyncio
import time
import os
import shutil


async def main():

    master_resume = load("data/resume.json")

    loaded_postings = [load(os.path.join("data/postings", file)) for file in os.listdir("data/postings")]

    for filename in os.listdir("data/postings"):
        shutil.move(f"data/postings/{filename}", f"data/processed/{filename}")

    loaded_template = load("templates/resume_template.tex")

    payload = await preprocessor(resume=master_resume, postings=loaded_postings, llm=gemini, batch_size=1)

    rewritten_resumes = await rewriter(payload=payload, llm=gemini, batch_size=1)

    formatted_resumes = await formatter(payload=rewritten_resumes, template=loaded_template, llm=gemini, batch_size=1)

    for key in tqdm(formatted_resumes, desc="Saving Formatted Resumes"):
        if key != "resume":
            filename = key
            content = formatted_resumes[key]["rewritten_resume"]
            with open(f"output/{filename}.tex", 'w', encoding="utf-8") as file:
                file.write(content)


if __name__ == "__main__":
    print("###############################################")
    print("Agentic Resume Optimizer")
    print("###############################################")
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time:.2f} seconds")
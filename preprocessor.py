from langchain.prompts import PromptTemplate
from models import gemma3, llama3p2, llama3p1, deepseek_r1, gemini
from utils import load
from tqdm import tqdm
import asyncio
import time
import re
import os
import json


async def preprocessor(resume: str, postings: list, llm, batch_size: int = 1) -> list:
    
    sys_prompt = PromptTemplate(
        input_variables=["resume", "posting"],
        template="""You will be given a resume and a job posting.
        Extract the full name of the applicant, the company name, and the job title from the job posting.
        Return a string in the format 'firstname_lastname_company_jobtitle' without any spaces or special characters.
        Here is the resume:
        {resume}
        
        Here is the job posting:
        {posting}

        String:"""
    )

    prompts = [sys_prompt.format(resume=resume, posting=p) for p in postings]

    responses = []
    for i in tqdm(range(0, len(prompts), batch_size), desc="Metadata Extraction Progress"):
        batch_jobs = prompts[i:i+batch_size]
        batch_responses = await llm.abatch(batch_jobs)
        responses.extend(batch_responses)

    payload = {}
    for r in responses:
        metadata = {}
        metadata["posting"] = postings[responses.index(r)]
        payload[r.content] = metadata

    payload["resume"] = resume

    if len(responses) != len(postings):
        raise ValueError("Number of filenames does not match number of postings.")

    return payload


async def run():
    print("###############################################")
    print("Preprocessor Tester")
    print("###############################################")
    start_time = time.time()
    loaded_resume = load("resume.json")
    loaded_postings = [load("postings/hardware_sample_posting.txt")]
    output = await preprocessor(resume=loaded_resume, postings=loaded_postings, llm=gemini, batch_size=1)
    print(output)
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time:.2f} seconds")

if __name__ == "__main__":
    asyncio.run(run())
    
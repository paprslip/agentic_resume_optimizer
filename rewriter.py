from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from models import gemma3, llama3p2, llama3p1, deepseek_r1
from utils import load
from tqdm import tqdm
import asyncio
import time
import re
import os
import json


async def rewriter(resume, postings: list, llm: ChatOllama, batch_size: int = 1) -> list:
    
    sys_prompt = PromptTemplate(
        input_variables=["resume", "posting"],
        template="""You are an expert resume writer. Rewrite the resume to better match the job posting. 
        Use the job posting to identify keywords and skills that should be highlighted in the resume. 
        Ensure the rewritten resume is ATS friendly and uses a professional tone. 
        Keep the formatting simple and clean, one page max. 
        Only return the resume, without any thoughts or description.
        Return the resume in latex format.
        Here is the resume:
        {resume}
        
        Here is the job posting:
        {posting}
        
        Rewritten Resume:"""
    )

    prompts = [sys_prompt.format(resume=resume, posting=p) for p in postings]

    responses = []
    for i in tqdm(range(0, len(prompts), batch_size), desc="Resume Optimization Progress"):
        batch_jobs = prompts[i:i+batch_size]
        batch_responses = await llm.abatch(batch_jobs)
        responses.extend(batch_responses)

    response_txt = [r.content for r in responses]
    return response_txt


def format_rewriter(response):
    #application = list(response[0])
    #resume = response[1].replace('\\\\', '\\').replace('\\n', '\n')

    #feature request: put name of applicant and job title in filename
    #with open(application[0].replace(' ','_') + "_" + application[1].replace(' ','_') + ".tex", 'w', encoding="utf-8") as file:
    with open("rewritten_resume.tex", 'w', encoding="utf-8") as file:
        for i in range(len(response)):
            file.write(response[i])


if __name__ == "__main__":
    print("###############################################")
    print("Rewriter Tester")
    print("###############################################")
    start_time = time.time()
    loaded_resume = load("terrence.json")
    #print(type(loaded_resume))
    loaded_postings = [load("sample_posting.pdf")]
    #loaded_template = load("resume_template.tex")
    output = asyncio.run(rewriter(resume=loaded_resume, postings=loaded_postings, llm=llama3p1, batch_size=1))
    print(output)
    test = format_rewriter(output)
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time:.2f} seconds")
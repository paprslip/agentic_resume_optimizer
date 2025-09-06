from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from models import gemma3, llama3p2, llama3p1, deepseek_r1
from utils import load
from rewriter import rewriter
from tqdm import tqdm
import asyncio
import time
import re
import os


async def formatter(resumes, template, llm: ChatOllama, batch_size: int = 1):
    
    sys_prompt = PromptTemplate(
        input_variables=["resume", "template"],
        template="""You are a resume formatting expert. Given the resume content and another peron's LaTeX resume as a template, format the resume according to the template.
        Only return the resume, without any thoughts or description.
        Return the resume in LaTeX format.
        Here is the resume:
        {resume}
        
        Here is the template:
        {template}
        
        Rewritten Resume:"""
    )

    prompts = [sys_prompt.format(resume=r, template=template) for r in resumes]

    responses = []
    for i in tqdm(range(0, len(resumes), batch_size), desc="Resume Formatting Progress"):
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
    print("Formatter Tester")
    print("###############################################")
    start_time = time.time()
    loaded_resumes = [load("terrence.json")]
    #print(type(loaded_resume))
    loaded_postings = [load("sample_posting.pdf")]
    loaded_template = load("resume_template.tex")
    output = asyncio.run(rewriter(resume=loaded_resumes, postings=loaded_postings, llm=llama3p1, batch_size=1))
    #print(output)
    output2 = asyncio.run(formatter(resumes=[output], template=loaded_template, llm=llama3p1, batch_size=1))
    #print(output)
    print(output2)
    test = format_rewriter(output2)
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time:.2f} seconds")
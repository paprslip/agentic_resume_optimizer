from langchain.prompts import PromptTemplate
from models import gemma3, llama3p2, llama3p1, deepseek_r1, gemini
from utils import load
from rewriter import rewriter
from tqdm import tqdm
import asyncio
import time
import re
import os


async def formatter(payload: dict, template: str, llm, batch_size: int = 1):
    
    resumes = [payload[key]["rewritten_resume"] for key in payload if key != "resume"]

    sys_prompt = PromptTemplate(
        input_variables=["resume", "template"],
        template="""You are a resume formatting expert.
        You have been provided an applicant's resume and a John Doe resume to use as a LaTeX template.
        Create a resume that uses the applicant's information but follows the structure, style, and formatting of the provided template.
        Keep the length of the resume to one page by summarizing or removing less relevant content.
        Only return the resume, without any thoughts or description.
        Return the resume in LaTeX format without any code block or markdown formatting.
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

    #payload["rewritten_resumes"] = [r.content for r in responses]
    for key in payload:
        if key != "resume":
            payload[key]["rewritten_resume"] = responses[list(payload.keys()).index(key)-1].content

    return payload


def format_rewriter(response):
    with open("output/ewritten_resume.tex", 'w', encoding="utf-8") as file:
        for i in range(len(response)):
            file.write(response[i])


async def run():
    print("###############################################")
    print("Formatter Tester")
    print("###############################################")
    start_time = time.time()
    loaded_resume = load("data/resume.json")
    loaded_postings = [load("data/postings/sample_posting.pdf")]
    loaded_template = load("templates/resume_template.tex")
    output = await rewriter(resume=loaded_resume, postings=loaded_postings, llm=gemini, batch_size=1)
    output2 = await formatter(resumes=[output], template=loaded_template, llm=gemini, batch_size=1)
    test = format_rewriter(output2)
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(run())
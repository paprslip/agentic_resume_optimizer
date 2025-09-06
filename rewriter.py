from langchain.prompts import PromptTemplate
from models import gemma3, llama3p2, llama3p1, deepseek_r1, gemini
from utils import load
from tqdm import tqdm
import asyncio
import time
import re
import os
import json


async def rewriter(payload: dict, llm, batch_size: int = 1) -> list:

    resume = payload["resume"]
    postings = [payload[key]["posting"] for key in payload if key != "resume"]

    sys_prompt = PromptTemplate(
        input_variables=["resume", "posting", "template"],
        template="""You are an expert resume writer.
        You have been provided a detailed file containing an applicant's background, skills, and experiences in JSON format.
        You have also been provided a job posting that the applicant is interested in applying for.
        Identify relevant points, discard irrelevant ones, and reframe the resume to best align with the job posting.
        Return twithout any thoughts or description.
        Return the resume in the same JSON format as the input without any code block or markdown formatting.
        
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

    #response_txt = [r.content for r in responses]
    #payload["rewritten_resumes"] = [r.content for r in responses]
    for key in payload:
        if key != "resume":
            payload[key]["rewritten_resume"] = responses[list(payload.keys()).index(key)-1].content

    return payload


def format_rewriter(response):
    #application = list(response[0])
    #resume = response[1].replace('\\\\', '\\').replace('\\n', '\n')

    #feature request: put name of applicant and job title in filename
    #with open(application[0].replace(' ','_') + "_" + application[1].replace(' ','_') + ".tex", 'w', encoding="utf-8") as file:
    with open("rewritten_resume.json", 'w', encoding="utf-8") as file:
        for i in range(len(response)):
            file.write(response[i])


async def run():
    print("###############################################")
    print("Rewriter Tester")
    print("###############################################")
    start_time = time.time()
    loaded_resume = load("resume.json")
    loaded_postings = [load("postings/hardware_sample_posting.txt")]
    output = await rewriter(resume=loaded_resume, postings=loaded_postings, llm=gemini, batch_size=1)
    test = format_rewriter(output)
    end_time = time.time()
    print(f"Total time taken: {end_time - start_time:.2f} seconds")


if __name__ == "__main__":
    asyncio.run(run())
    
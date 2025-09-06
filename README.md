Agentic Resume Optimizer
-
Agentic Resume Optimizer is a GPT-wrapper that takes in a JSON profile of a job seeker and then feeds it through a series of LLMs that process, optimize, format, and output a LaTeX resume optimized for each job posting.

Features
- 
- Automatically formats a JSON containing candidate info like experiences, projects, skills, into a simple and ATS-safe resume
- Prioritizes skills and experiences that best fit the job, along with rewording them to incorporate key terms from the posting
- Free (uses Gemini API, which is free at time of writing)
- Should always be reviewed by a human (made this at 4am, I make no SLA or RAS guarantees)

Installation
-
Install required packages

```pip install -r requirements.txt```

Clone the repo

``` git clone https://github.com/paprslip/agentic_resume_optimizer.git```

Configuration
-
Create a ```.env``` file in the root folder, and then add your API keys. This program uses Gemini and 4o-mini, so both either API keys for these need to be added, or you can simply comment out/delete the model you do not want in ```models.py```.

To use a different model, you simply change the LLM in ```main.py```. Local models can also be run and used through Ollama. Warning that my testing with Llama3.2 and Llama3.1 have yielded mixed results, I recommend just using the Gemini API since it's smarter and free.

Usage
-
1. Put your own resume information into ```resume.json```. Be as detailed as possible.
2. Save job postings as PDF or copy the page into a ```.txt``` file, and then put that in ```data/postings```.
3. Run the program in the terminal with ```python src/main.py```
4. profit

Structure
-
Three agents process the data before the output.

The **resume.json** file contains all the information about the applicant. This should be as detailed as possible to give the LLM more to work with when selecting or summarizing experiences and skills.

This info is then passed into the preprocessor agent, which extracts the applicant name and job info for the filename, and then passes all of this in a dictionary into the rewriter.

The rewriter is takes the payload from the preprocessor and then processes the JSON and the job description to highlight relevant experiences and use wording from the job posting.

The formatter takes the output from the rewritter and puts all this information into a LaTeX template found on Overleaf by Jake Gutierrez.

When running this program, it will process all files in the postings folder and generate a resume for each one.
```
agentic-resume-optimizer/
├── data/
│   ├── resume.json
│   ├── postings/
│   │   ├── job2.txt
│   │   ├── job3.txt
│   └── processed/
│       └── job1.txt
├── output/
│   └── name_company_job1.tex
├── src/
│   ├── formatter.py
│   ├── main.py
│   ├── models.py
│   ├── preprocessor.py
│   ├── rewriter.py
│   └── utils.py
├── templates/
│   └── resume_template.tex
├── README.md
└── requirements.txt
```

Acknowledgements
- roddy for the convos that led to this on 09/05/2025
- [Free Gemini API which this runs on](https://ai.google.dev/gemini-api/docs/pricing)
- [LangChain](https://python.langchain.com/docs/introduction/)
- [Jake Gutierrez](https://www.overleaf.com/latex/templates/jakes-resume/syzfjbzwjncs)

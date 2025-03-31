from cleaned import process_resume
import json
import datetime
import asyncio
from langchain_google_genai import GoogleGenerativeAI
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")

def extract_employment_data(resume_data):
    """Extract and format employment history from resume data."""

    if isinstance(resume_data, list):
        if len(resume_data) > 0 and isinstance(resume_data[0], dict):
            resume_data = resume_data[0]  
        else:
            return []

    employment_history = resume_data.get("Employment History", [])
    structured_data = []

    for entry in employment_history:
        company = entry.get("company")
        from_date_raw = entry.get("from")
        to_date_raw = entry.get("to")

        try:
            from_date = datetime.datetime.strptime(from_date_raw, "%Y-%m-%d") if from_date_raw else None
        except (TypeError, ValueError):
            from_date = None

        if to_date_raw == "Present":
            to_date = datetime.datetime.now()
        else:
            try:
                to_date = datetime.datetime.strptime(to_date_raw, "%Y-%m-%d") if to_date_raw else None
            except (TypeError, ValueError):
                to_date = None

        months_worked = (to_date - from_date).days // 30 if from_date and to_date else None
        tenure_category = (
            "Long tenure" if months_worked and months_worked >= 36 else
            "Moderate tenure" if months_worked and months_worked >= 24 else
            "Short tenure"
        )

        structured_data.append({
            "company": company,
            "from": from_date_raw,
            "to": to_date_raw,
            "months_worked": months_worked,
            "tenure_category": tenure_category
        })

    return structured_data

def analyze_with_llm(employment_summary):
    """Use LLM to generate a job stability status and analysis."""
    llm = GoogleGenerativeAI(model=GEMINI_MODEL, google_api_key=GEMINI_API_KEY)
    
    # Generate a professional stability analysis
    prompt_template = PromptTemplate(
        input_variables=["employment_summary"],
        template=(
            "Here is the employment history summary: {employment_summary}. "
            "Based on this, provide a professional job stability analysis. "
            "Then, classify the candidate as 'Stable', 'Moderately Stable', or 'Unstable' based on corporate hiring standards."
        )
    )
    
    chain = LLMChain(llm=llm, memory=ConversationBufferMemory(), prompt=prompt_template)
    response = chain.run({"employment_summary": employment_summary})

    # Extract structured stability status from LLM response
    stability_status = "Moderately Stable"  # Default fallback
    if "Stable" in response:
        stability_status = "Stable"
    elif "Unstable" in response:
        stability_status = "Unstable"

    return response, stability_status

async def main():
    resume_data = await process_resume()
    employment_data = extract_employment_data(resume_data)
    
    if not employment_data:
        print("No Employment History found.")
        return

    employment_summary = "\n".join([
        f"{entry['company']}: {entry['months_worked']} months – {entry['tenure_category']}"
        for entry in employment_data if entry['months_worked'] is not None
    ])

    analysis, stability_status = analyze_with_llm(employment_summary)

    result = {
        "employment_data": employment_data,
        "stability_status": stability_status,
        "analysis": analysis
    }

    with open("analysis.json", "w") as f:
        json.dump(result, f, indent=4)

if __name__ == "__main__":
    asyncio.run(main())

import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import asyncio
import re
from typing import List, Dict, Any
from cleaned import process_single_resume

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")

# Initialize Gemini model
model = genai.GenerativeModel(model_name=GEMINI_MODEL)

def clean_json_response(response_text: str) -> Dict[str, Any]:
    """
    Clean and parse JSON response, handling cases where Gemini returns code block formatting.
    """
    response_text = response_text.replace('```json', '').replace('```', '').strip()
    
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass
    
    return {"company_name": "Unknown", "error": "Failed to parse response", "raw_response": response_text}

async def extract_company_details(company_name: str) -> Dict[str, Any]:
    """
    Extract structured company details using Gemini.
    """
    prompt = f"""
    Provide a structured JSON summary for the company '{company_name}' with relevant insights.
    Focus on **key aspects only**, avoiding unnecessary details.

    {{
        "company_name": "{company_name}",
        "classification": {{
            "type": "Startup/MNC/SME",
            "industry": "IT/Finance/etc",
            "size": "Small/Medium/Large",
            "business_model": "Product/Service/Consulting"
        }},
        "profile": {{
            "core_focus": "Main business area",
            "technologies": ["Tech1", "Tech2"],
            "market_position": "Leading/Emerging/Established"
        }},
        "work_environment": {{
            "culture": "Collaborative/Fast-paced/etc",
            "tech_stack": ["Python", "React", "PostgreSQL"],
            "growth_potential": "High/Moderate/Low"
        }}
    }}

    Ensure the response is a valid and clean JSON.
    """

    try:
        response = model.generate_content(prompt)
        company_details = clean_json_response(response.text)
        company_details["company_name"] = company_name
        return company_details

    except Exception as e:
        print(f"Error extracting details for {company_name}: {e}")
        return {"company_name": company_name, "error": str(e)}

async def process_companies(employment_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Process companies from employment history to extract structured details.
    """
    tasks = [extract_company_details(job["company"]) for job in employment_history if "company" in job]
    return await asyncio.gather(*tasks)

def main():
    resume_data = asyncio.run(process_single_resume())
    employment_history = resume_data.get("Employment History", [])
    
    company_details = asyncio.run(process_companies(employment_history))

    with open("company_details.json", "w") as f:
        json.dump(company_details, f, indent=4)

    for company in company_details:
        print(f"\nCompany: {company.get('company_name', 'Unknown')}")
        for key, value in company.items():
            if key != 'company_name':
                print(f"{key.replace('_', ' ').title()}: {json.dumps(value, indent=2)}")

if __name__ == "__main__":
    main()

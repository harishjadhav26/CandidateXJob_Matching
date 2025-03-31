import google.generativeai as genai
from dotenv import load_dotenv
import os
import json
import asyncio
import re
from typing import List, Dict, Any
from pymongo import MongoClient
# You can't directly use process_resume since it now requires a data parameter
# Instead, we'll import the cleaned module and access the database directly

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-pro")

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["CandidateMatch"]
resume_collection = db["Resume_parsed"]
cleaned_collection = db["Cleaned"]

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

async def process_all_companies():
    """
    Process all companies from all resumes in the database.
    """
    print("Beginning company extraction process...")
    
    # Two options:
    # 1. Use already processed data from cleaned_collection (if available)
    # 2. Or get raw data and process employment history from resume_collection
    
    all_companies = set()
    all_company_details = []
    processed_count = 0
    
    # Option 1: Try to use cleaned collection first
    if cleaned_collection.count_documents({}) > 0:
        print("Using processed resumes from Cleaned collection...")
        cursor = cleaned_collection.find({})
        
        for doc in cursor:
            employment_history = doc.get("Employment History", [])
            if employment_history:
                companies = [job.get("company", "") for job in employment_history if job.get("company")]
                companies = [c for c in companies if c]  # Filter out empty strings
                
                # Only process new companies we haven't seen before
                new_companies = [c for c in companies if c not in all_companies]
                
                if new_companies:
                    company_details = await process_companies([{"company": c} for c in new_companies])
                    all_company_details.extend(company_details)
                    all_companies.update(new_companies)
                
                processed_count += 1
                if processed_count % 10 == 0:
                    print(f"Processed {processed_count} resumes, found {len(all_companies)} unique companies")
    
    # Option 2: If cleaned collection is empty, process from raw data
    elif resume_collection.count_documents({}) > 0:
        print("Using raw resumes from Resume_parsed collection...")
        cursor = resume_collection.find({})
        
        for doc in cursor:
            resume_text = doc.get("resumeParseData", "")
            resume_parse_data = {}
            
            # Try to parse resumeParseData if it's a string
            if isinstance(resume_text, str):
                try:
                    resume_parse_data = json.loads(resume_text)
                except json.JSONDecodeError:
                    print("Error parsing resumeParseData for a document")
                    continue
            else:
                resume_parse_data = resume_text
            
            # Extract company names from employment history
            employment_positions = resume_parse_data.get("EmploymentHistory", {}).get("Positions", [])
            companies = []
            
            for pos in employment_positions:
                company_name = pos.get("Employer", {}).get("Name", {}).get("Normalized", "")
                if company_name:
                    companies.append(company_name)
            
            # Only process new companies we haven't seen before
            new_companies = [c for c in companies if c not in all_companies]
            
            if new_companies:
                company_details = await process_companies([{"company": c} for c in new_companies])
                all_company_details.extend(company_details)
                all_companies.update(new_companies)
            
            processed_count += 1
            if processed_count % 10 == 0:
                print(f"Processed {processed_count} resumes, found {len(all_companies)} unique companies")
    
    else:
        print("No resume data found in either collection.")
        return []
    
    print(f"Finished processing {processed_count} resumes.")
    print(f"Found {len(all_companies)} unique companies.")
    
    # Save all unique company details to a JSON file
    with open("all_company_details.json", "w") as f:
        json.dump(all_company_details, f, indent=4)
    
    print("Company details saved to all_company_details.json")
    return all_company_details

def main():
    print("Starting company detail extraction process...")
    company_details = asyncio.run(process_all_companies())
    
    print(f"\nExtracted details for {len(company_details)} companies.")
    
    # Print a sample of the first 3 companies
    for i, company in enumerate(company_details[:3], 1):
        print(f"\nCompany {i}: {company.get('company_name', 'Unknown')}")
        for key, value in company.items():
            if key != 'company_name':
                print(f"{key.replace('_', ' ').title()}: {json.dumps(value, indent=2)}")
    
    if len(company_details) > 3:
        print(f"\n... and {len(company_details) - 3} more companies")

if __name__ == "__main__":
    main()
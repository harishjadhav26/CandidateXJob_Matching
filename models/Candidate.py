import company
import json
import stability
from cleaned import process_all_resume
import location
import os
from dotenv import load_dotenv
import asyncio

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")

async def main():
    # Extract personal details from the resume
    cleaned_data = await process_all_resume()
    
    # Extract location details asynchronously
    city = cleaned_data.get("City", "")
    state = cleaned_data.get("State", "")
    country_code = cleaned_data.get("Country Code", "")
    
    location_details = await location.extract_location(city, state, country_code)
    
    # Example employer location (this should be dynamic based on employer input)
    employer_location = {
        "city": "Meerut",
        "state": "Uttar Pradesh",
        "country": "India"
    }
    
    employer_coordinates = await location.get_coordinates(
        employer_location["city"], 
        employer_location["state"], 
        employer_location["country"]
    )
    
    employer_location_full = {
        **employer_location,
        **(employer_coordinates or {})
    }
    
    distance = location.calculate_distance(location_details, employer_location_full)
    
    employment_history = cleaned_data.get("Employment History", [])
    company_details = await company.process_companies(employment_history)

    # Extract stability information
    employment_data = stability.extract_employment_data(cleaned_data)

    # Generate stability status using LLM
    employment_summary = "\n".join([
        f"{entry['company']}: {entry['months_worked']} months – {entry['tenure_category']}"
        for entry in employment_data if entry['months_worked'] is not None
    ])

    analysis, stability_status = stability.analyze_with_llm(employment_summary)

    stability_info = {
        "employment_data": employment_data,
        "stability_status": stability_status,
        "analysis": analysis
    }

    # Build the final structure
    Structure = {
        "Personal_details": cleaned_data,
        "location": {
            "employee_location": location_details,
            "employer_location": employer_location_full,
            "distance_km": distance
        },
        "company_details": company_details,
        "stability_info": stability_info
    }
    
    # Save the structure to a JSON file
    with open("PersonalDetails.json", "w") as json_file:
        json.dump(Structure, json_file, indent=4)
    
    print("PersonalDetails saved to PersonalDetails.json")

if __name__ == "__main__":
    asyncio.run(main())

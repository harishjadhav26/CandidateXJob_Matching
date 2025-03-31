# # import json
# # import re
# # from datetime import datetime
# # import math
# # import os
# # from typing import Dict, List, Any, Optional, Tuple, Union
# # import cleaned
# # import location
# # import company
# # import stability
# # class CandidateScorer:
# #     def __init__(self, job_requirements: Dict[str, Any], weights: Optional[Dict[str, float]] = None):
# #         """
# #         Initialize the scorer with job requirements and optional custom weights.
        
# #         Args:
# #             job_requirements: Dictionary containing job requirements
# #             weights: Optional dictionary of weights for different scoring categories
# #         """
# #         self.job_requirements = job_requirements
        
# #         # Default weights for different scoring categories
# #         self.weights = {
# #             "skills_match": 0.30,
# #             "experience": 0.20,
# #             "project_relevance": 0.15,
# #             "education": 0.10,
# #             "job_stability": 0.08,
# #             "location_compatibility": 0.07,
# #             "company_relevance": 0.05,
# #             "work_preference_match": 0.05
# #         }
        
# #         # Override defaults with custom weights if provided
# #         if weights:
# #             self.weights.update(weights)
    
# #     def score_candidate(self, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
# #         """
# #         Score a candidate based on their data against job requirements.
        
# #         Args:
# #             candidate_data: Dictionary containing candidate information
            
# #         Returns:
# #             Dictionary with scores for each category and an overall score
# #         """
# #         try:
# #             # Calculate scores for each category
# #             skills_score = self._score_skills(candidate_data)
# #             experience_score = self._score_experience(candidate_data)
# #             project_score = self._score_projects(candidate_data)
# #             education_score = self._score_education(candidate_data)
# #             stability_score = self._score_job_stability(candidate_data)
# #             location_score = self._score_location(candidate_data)
# #             company_score = self._score_company_relevance(candidate_data)
# #             preference_score = self._score_work_preference(candidate_data)
            
# #             # Calculate weighted overall score
# #             overall_score = (
# #                 skills_score * self.weights["skills_match"] +
# #                 experience_score * self.weights["experience"] +
# #                 project_score * self.weights["project_relevance"] +
# #                 education_score * self.weights["education"] +
# #                 stability_score * self.weights["job_stability"] +
# #                 location_score * self.weights["location_compatibility"] +
# #                 company_score * self.weights["company_relevance"] +
# #                 preference_score * self.weights["work_preference_match"]
# #             )
            
# #             # Round to 2 decimal places
# #             overall_score = round(overall_score, 2)
            
# #             # Create detailed scoring breakdown
# #             score_breakdown = {
# #                 "overall_score": overall_score,
# #                 "category_scores": {
# #                     "skills_match": round(skills_score, 2),
# #                     "experience": round(experience_score, 2),
# #                     "project_relevance": round(project_score, 2),
# #                     "education": round(education_score, 2),
# #                     "job_stability": round(stability_score, 2),
# #                     "location_compatibility": round(location_score, 2),
# #                     "company_relevance": round(company_score, 2),
# #                     "work_preference_match": round(preference_score, 2)
# #                 },
# #                 "category_weights": self.weights,
# #                 "candidate_strengths": self._identify_strengths(candidate_data),
# #                 "candidate_gaps": self._identify_gaps(candidate_data)
# #             }
            
# #             return score_breakdown
        
# #         except Exception as e:
# #             print(f"Error scoring candidate: {e}")
# #             return {"error": str(e), "overall_score": 0}
    
# #     def _score_skills(self, candidate_data: Dict[str, Any]) -> float:
# #         """Score candidate's skills against job requirements."""
# #         required_skills = set(self.job_requirements.get("required_skills", []))
# #         preferred_skills = set(self.job_requirements.get("preferred_skills", []))
        
# #         candidate_skills = set([skill.lower() for skill in candidate_data.get("Skills", [])])
        
# #         # Calculate required skills match
# #         if required_skills:
# #             required_match = len(required_skills.intersection([s.lower() for s in candidate_skills])) / len(required_skills)
# #         else:
# #             required_match = 1.0
            
# #         # Calculate preferred skills match
# #         if preferred_skills:
# #             preferred_match = len(preferred_skills.intersection([s.lower() for s in candidate_skills])) / len(preferred_skills)
# #         else:
# #             preferred_match = 1.0
        
# #         # Weight required skills more heavily
# #         return (required_match * 0.7) + (preferred_match * 0.3)
    
# #     def _score_experience(self, candidate_data: Dict[str, Any]) -> float:
# #         """Score candidate's experience level."""
# #         required_experience = self.job_requirements.get("required_experience", 0)
        
# #         # Extract experience from candidate data
# #         experience_str = candidate_data.get("Work Experience", "0")
        
# #         # Try to extract years from experience string
# #         years_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:year|yr)', experience_str, re.IGNORECASE)
# #         months_match = re.search(r'(\d+)\s*month', experience_str, re.IGNORECASE)
        
# #         years = float(years_match.group(1)) if years_match else 0
# #         months = float(months_match.group(1))/12 if months_match else 0
        
# #         total_years = years + months
        
# #         # Calculate experience score
# #         if total_years >= required_experience:
# #             if total_years >= required_experience * 1.5:
# #                 # Exceeds required experience by 50% or more
# #                 return 1.0
# #             else:
# #                 # Meets required experience
# #                 return 0.8 + (total_years - required_experience) / (required_experience * 1.5 - required_experience) * 0.2
# #         else:
# #             # Below required experience
# #             return max(0.0, total_years / required_experience * 0.8)
    
# #     def _score_projects(self, candidate_data: Dict[str, Any]) -> float:
# #         """Score candidate's projects for relevance."""
# #         required_techs = set([tech.lower() for tech in self.job_requirements.get("required_skills", [])])
# #         candidate_data= cleaned.clean_data(candidate_data)  # Clean candidate data
        
# #         projects = candidate_data.get("Projects", [])
# #         if not projects:
# #             return 0.0
        
# #         total_relevance = 0.0
        
# #         for project in projects:
# #             # Extract project technologies
# #             project_techs = set()
# #             for tech in project.get("tools_used/skill_used", []):
# #                 project_techs.add(tech.lower())
            
# #             # Calculate tech overlap
# #             if required_techs:
# #                 tech_overlap = len(required_techs.intersection(project_techs)) / len(required_techs)
# #             else:
# #                 tech_overlap = 0.5  # Neutral score if no required techs
            
# #             # Calculate project complexity based on description length
# #             description = project.get("description", "")
# #             complexity_factor = min(1.0, len(description) / 500)  # Scale up to 500 chars
            
# #             # Calculate project relevance
# #             project_relevance = (tech_overlap * 0.7) + (complexity_factor * 0.3)
# #             total_relevance += project_relevance
        
# #         # Average project relevance, with a bonus for having multiple projects
# #         project_count_bonus = min(0.3, (len(projects) - 1) * 0.1)  # Up to 0.3 bonus for 4+ projects
# #         return min(1.0, (total_relevance / len(projects)) + project_count_bonus)
    
# #     def _score_education(self, candidate_data: Dict[str, Any]) -> float:
# #         """Score candidate's education."""
# #         required_degree = self.job_requirements.get("required_degree", "")
# #         required_field = self.job_requirements.get("required_field", "")
        
# #         education_entries = candidate_data.get("Education", [])
# #         if not education_entries:
# #             return 0.0
        
# #         # Define degree hierarchy
# #         degree_levels = {
# #             "high school": 1,
# #             "associate": 2,
# #             "bachelor": 3,
# #             "master": 4, 
# #             "phd": 5,
# #             "doctorate": 5
# #         }
        
# #         highest_degree_level = 0
# #         field_match = False
        
# #         # Find highest degree and check for field match
# #         for entry in education_entries:
# #             degree = entry.get("degree", "").lower()
            
# #             # Check degree level
# #             for level_name, level_value in degree_levels.items():
# #                 if level_name in degree:
# #                     highest_degree_level = max(highest_degree_level, level_value)
            
# #             # Check field match
# #             field = entry.get("specialization", "").lower()
# #             if required_field.lower() in field or field in required_field.lower():
# #                 field_match = True
        
# #         # Calculate degree level score
# #         required_level = 0
# #         for level_name, level_value in degree_levels.items():
# #             if level_name in required_degree.lower():
# #                 required_level = level_value
        
# #         # Calculate degree match score
# #         if highest_degree_level >= required_level:
# #             degree_score = 1.0
# #         else:
# #             degree_score = highest_degree_level / required_level if required_level > 0 else 0.5
        
# #         # Calculate overall education score
# #         if not required_field:
# #             return degree_score
# #         else:
# #             return (degree_score * 0.7) + (0.3 if field_match else 0.0)
    
# #     def _score_job_stability(self, candidate_data: Dict[str, Any]) -> float:
# #         """Score candidate's job stability."""
# #         employment_history = candidate_data.get("Employment History", [])
# #         if not employment_history:
# #             return 0.5  # Neutral score if no history
        
# #         # Calculate average tenure
# #         total_months = 0
# #         job_count = 0
        
# #         for job in employment_history:
# #             from_date_raw = job.get("from", "")
# #             to_date_raw = job.get("to", "")
            
# #             try:
# #                 from_date = datetime.strptime(from_date_raw, "%Y-%m-%d") if from_date_raw else None
                
# #                 if to_date_raw == "Present":
# #                     to_date = datetime.now()
# #                 else:
# #                     to_date = datetime.strptime(to_date_raw, "%Y-%m-%d") if to_date_raw else None
                
# #                 if from_date and to_date:
# #                     months = (to_date.year - from_date.year) * 12 + (to_date.month - from_date.month)
# #                     total_months += months
# #                     job_count += 1
# #             except (ValueError, TypeError):
# #                 continue
        
# #         if job_count == 0:
# #             return 0.5  # Neutral score if no valid jobs
        
# #         avg_tenure = total_months / job_count
        
# #         # Score based on average tenure
# #         # Less than 1 year: 0.2-0.4
# #         # 1-2 years: 0.4-0.7
# #         # 2+ years: 0.7-1.0
# #         if avg_tenure < 12:
# #             return max(0.2, 0.4 * (avg_tenure / 12))
# #         elif avg_tenure < 24:
# #             return 0.4 + 0.3 * ((avg_tenure - 12) / 12)
# #         else:
# #             return min(1.0, 0.7 + 0.3 * min(1.0, (avg_tenure - 24) / 12))
    
# #     def _score_location(self, candidate_data: Dict[str, Any]) -> float:
# #         """Score candidate's location compatibility."""
# #         remote_work = self.job_requirements.get("remote_work", False)
# #         relocation = self.job_requirements.get("relocation_allowed", False)
        
# #         # If remote work is offered, location is less important
# #         if remote_work:
# #             return 0.9
        
# #         job_location = self.job_requirements.get("location", {})
# #         candidate_location = {
# #             "city": candidate_data.get("City", ""),
# #             "state": candidate_data.get("State", ""),
# #             "country": candidate_data.get("Country Code", "")
# #         }
        
# #         # Check if locations match
# #         same_city = job_location.get("city", "").lower() == candidate_location.get("city", "").lower()
# #         same_state = job_location.get("state", "").lower() == candidate_location.get("state", "").lower()
# #         same_country = job_location.get("country", "").lower() == candidate_location.get("country", "").lower()
        
# #         # Calculate location score
# #         if same_city:
# #             return 1.0
# #         elif same_state:
# #             return 0.8
# #         elif same_country:
# #             return 0.6
# #         elif relocation:
# #             return 0.4  # Candidate would need to relocate
# #         else:
# #             return 0.1  # Poor location match
    
# #     def _score_company_relevance(self, candidate_data: Dict[str, Any]) -> float:
# #         """Score relevance of candidate's previous companies."""
# #         target_industry = self.job_requirements.get("industry", "")
# #         employment_history = candidate_data.get("Employment History", [])
        
# #         if not employment_history or not target_industry:
# #             return 0.5  # Neutral score
        
# #         # Check if any previous company is in the same industry
# #         industry_match = False
# #         for job in employment_history:
# #             company = job.get("company", "")
# #             # Ideally we'd use the company data from company.py here
# #             # This is a simplified version
# #             if target_industry.lower() in company.lower():
# #                 industry_match = True
# #                 break
        
# #         # Calculate company relevance score
# #         if industry_match:
# #             return 0.8
# #         else:
# #             return 0.4
    
# #     def _score_work_preference(self, candidate_data: Dict[str, Any]) -> float:
# #         """Score match between candidate's work preference and job type."""
# #         job_type = self.job_requirements.get("job_type", "")  # e.g., "Full-time", "Contract", etc.
# #         work_preference = candidate_data.get("Work Preference", "")
        
# #         if not job_type or not work_preference:
# #             return 0.5  # Neutral score
        
# #         # Check for exact match
# #         if job_type.lower() in work_preference.lower():
# #             return 1.0
        
# #         # Check for partial match
# #         if ("full" in job_type.lower() and "full" in work_preference.lower()) or \
# #            ("part" in job_type.lower() and "part" in work_preference.lower()) or \
# #            ("contract" in job_type.lower() and "contract" in work_preference.lower()) or \
# #            ("remote" in job_type.lower() and "remote" in work_preference.lower()):
# #             return 0.8
        
# #         # No match
# #         return 0.2
    
# #     def _identify_strengths(self, candidate_data: Dict[str, Any]) -> List[str]:
# #         """Identify candidate's key strengths for this job."""
# #         strengths = []
        
# #         # Check skills
# #         required_skills = set(self.job_requirements.get("required_skills", []))
# #         candidate_skills = set([skill.lower() for skill in candidate_data.get("Skills", [])])
        
# #         skills_match_ratio = len(required_skills.intersection([s.lower() for s in candidate_skills])) / len(required_skills) if required_skills else 0
        
# #         if skills_match_ratio > 0.8:
# #             strengths.append("Strong skills match")
        
# #         # Check experience
# #         experience_str = candidate_data.get("Work Experience", "0")
# #         years_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:year|yr)', experience_str, re.IGNORECASE)
# #         years = float(years_match.group(1)) if years_match else 0
        
# #         required_experience = self.job_requirements.get("required_experience", 0)
# #         if years >= required_experience * 1.2:
# #             strengths.append("Exceeds required experience")
        
# #         # Check education
# #         education_entries = candidate_data.get("Education", [])
# #         required_degree = self.job_requirements.get("required_degree", "").lower()
        
# #         if education_entries and required_degree:
# #             for entry in education_entries:
# #                 degree = entry.get("degree", "").lower()
# #                 if "master" in degree or "phd" in degree or "doctorate" in degree:
# #                     if "bachelor" in required_degree:
# #                         strengths.append("Advanced degree")
# #                     break
        
# #         return strengths
    
# #     def _identify_gaps(self, candidate_data: Dict[str, Any]) -> List[str]:
# #         """Identify candidate's key gaps for this job."""
# #         gaps = []
        
# #         # Check skills
# #         required_skills = set(self.job_requirements.get("required_skills", []))
# #         candidate_skills = set([skill.lower() for skill in candidate_data.get("Skills", [])])
        
# #         missing_skills = required_skills - set([s.lower() for s in candidate_skills])
# #         if missing_skills:
# #             gaps.append(f"Missing skills: {', '.join(missing_skills)}")
        
# #         # Check experience
# #         experience_str = candidate_data.get("Work Experience", "0")
# #         years_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:year|yr)', experience_str, re.IGNORECASE)
# #         years = float(years_match.group(1)) if years_match else 0
        
# #         required_experience = self.job_requirements.get("required_experience", 0)
# #         if years < required_experience:
# #             gaps.append(f"Experience gap: {required_experience - years} years")
        
# #         # Check education
# #         education_entries = candidate_data.get("Education", [])
# #         required_degree = self.job_requirements.get("required_degree", "").lower()
# #         required_field = self.job_requirements.get("required_field", "").lower()
        
# #         if required_degree and not education_entries:
# #             gaps.append("Missing education information")
# #         elif required_field and education_entries:
# #             field_match = False
# #             for entry in education_entries:
# #                 field = entry.get("specialization", "").lower()
# #                 if required_field in field or field in required_field:
# #                     field_match = True
# #                     break
            
# #             if not field_match:
# #                 gaps.append(f"Education not in required field: {required_field}")
        
# #         return gaps


# # def main():
# #     # Load candidate data
# #     try:
# #         with open("cleaned_resume.json", "r") as f:
# #             candidate_data = json.load(f)
# #     except FileNotFoundError:
# #         print("Error: cleaned_resume.json not found")
# #         return
    
# #     # Example job requirements
# #     job_requirements = {
# #         "title": "Senior Backend Developer",
# #         "required_skills": ["Python", "Django", "PostgreSQL", "REST API", "Git"],
# #         "preferred_skills": ["Docker", "Kubernetes", "AWS", "GraphQL"],
# #         "required_experience": 5,  # Years
# #         "required_degree": "Bachelor's",
# #         "required_field": "Computer Science",
# #         "industry": "Technology",
# #         "job_type": "Full-time",
# #         "remote_work": True,
# #         "relocation_allowed": True,
# #         "location": {
# #             "city": "Seattle",
# #             "state": "Washington",
# #             "country": "USA"
# #         }
# #     }
    
# #     # Create scorer and score candidate
# #     scorer = CandidateScorer(job_requirements)
# #     results = scorer.score_candidate(candidate_data)
    
# #     # Print results
# #     print("\nCandidate Scoring Results:")
# #     print("-" * 50)
# #     print(f"Overall Score: {results['overall_score']}/1.0")
# #     print("\nCategory Scores:")
# #     for category, score in results['category_scores'].items():
# #         print(f"  {category.replace('_', ' ').title()}: {score}/1.0")
    
# #     print("\nCandidate Strengths:")
# #     for strength in results['candidate_strengths']:
# #         print(f"  ✓ {strength}")
    
# #     print("\nCandidate Gaps:")
# #     for gap in results['candidate_gaps']:
# #         print(f"  ✗ {gap}")
    
# #     # Save results to file
# #     with open("candidate_score.json", "w") as f:
# #         json.dump(results, f, indent=4)
    
# #     print("\nDetailed results saved to candidate_score.json")

# # if __name__ == "__main__":
# #     main()




# import json
# import re
# from datetime import datetime
# import math
# import os
# from typing import Dict, List, Any, Optional, Tuple, Union
# import cleaned
# import location
# import company
# import stability

# class EnhancedCandidateScorer:
#     """
#     An advanced scoring system for ranking candidates against job requirements,
#     leveraging external modules for data enrichment and dynamic scoring.
#     """
    
#     def __init__(self, job_requirements: Dict[str, Any], weights: Optional[Dict[str, float]] = None,
#                  proximity_threshold: int = 100):
#         """
#         Initialize the scorer with job requirements and optional custom weights.
        
#         Args:
#             job_requirements: Dictionary containing job requirements
#             weights: Optional dictionary of weights for different scoring categories
#             proximity_threshold: Maximum distance in km for location compatibility (default: 100)
#         """
#         self.job_requirements = job_requirements
#         self.proximity_threshold = proximity_threshold
        
#         # Default weights for different scoring categories
#         self.weights = {
#             "skills_match": 0.30,
#             "experience": 0.20,
#             "project_relevance": 0.15,
#             "education": 0.10,
#             "job_stability": 0.08,
#             "location_compatibility": 0.07,
#             "company_relevance": 0.05,
#             "work_preference_match": 0.05
#         }
        
#         # Override defaults with custom weights if provided
#         if weights:
#             self.weights.update(weights)
    
#     def score_candidate(self, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
#         """
#         Score a candidate based on their data against job requirements.
        
#         Args:
#             candidate_data: Dictionary containing candidate information
            
#         Returns:
#             Dictionary with scores for each category and an overall score
#         """
#         try:
#             # Clean candidate data
#             cleaned_candidate_data = cleaned.clean_data(candidate_data)
            
#             # Calculate scores for each category
#             skills_score = self._score_skills(cleaned_candidate_data)
#             experience_score = self._score_experience(cleaned_candidate_data)
#             project_score = self._score_projects(cleaned_candidate_data)
#             education_score = self._score_education(cleaned_candidate_data)
#             stability_score = self._score_job_stability(cleaned_candidate_data)
#             location_score = self._score_location(cleaned_candidate_data)
#             company_score = self._score_company_relevance(cleaned_candidate_data)
#             preference_score = self._score_work_preference(cleaned_candidate_data)
            
#             # Calculate weighted overall score
#             overall_score = (
#                 skills_score * self.weights["skills_match"] +
#                 experience_score * self.weights["experience"] +
#                 project_score * self.weights["project_relevance"] +
#                 education_score * self.weights["education"] +
#                 stability_score * self.weights["job_stability"] +
#                 location_score * self.weights["location_compatibility"] +
#                 company_score * self.weights["company_relevance"] +
#                 preference_score * self.weights["work_preference_match"]
#             )
            
#             # Round to 2 decimal places
#             overall_score = round(overall_score, 2)
            
#             # Create detailed scoring breakdown
#             score_breakdown = {
#                 "overall_score": overall_score,
#                 "category_scores": {
#                     "skills_match": round(skills_score, 2),
#                     "experience": round(experience_score, 2),
#                     "project_relevance": round(project_score, 2),
#                     "education": round(education_score, 2),
#                     "job_stability": round(stability_score, 2),
#                     "location_compatibility": round(location_score, 2),
#                     "company_relevance": round(company_score, 2),
#                     "work_preference_match": round(preference_score, 2)
#                 },
#                 "category_weights": self.weights,
#                 "candidate_strengths": self._identify_strengths(cleaned_candidate_data) or [],
#                 "candidate_gaps": self._identify_gaps(cleaned_candidate_data) or []
#             }
            
#             return score_breakdown
        
#         except Exception as e:
#             print(f"Error scoring candidate: {e}")
#             return {"error": str(e), "overall_score": 0}
    
#     def _score_skills(self, candidate_data: Dict[str, Any]) -> float:
#         """
#         Score candidate's skills against job requirements.
        
#         Enhanced to consider:
#         - Skill frequency in work history
#         - Recency of skill usage
#         - Different scoring strategy based on experience level
#         """
#         required_skills = set(self.job_requirements.get("required_skills", []))
#         preferred_skills = set(self.job_requirements.get("preferred_skills", []))
        
#         # Ensure "Skills" key is handled properly
#         candidate_skills = set([skill.lower() for skill in candidate_data.get("Skills", [])]) if "Skills" in candidate_data else set()
        
#         # Determine if candidate is entry-level or experienced
#         is_entry_level = self._is_entry_level(candidate_data)
        
#         # Extract skills from employment history and projects
#         skill_usage_data = self._extract_skill_usage(candidate_data)
        
#         # Calculate required skills match
#         if required_skills:
#             # For entry-level, we're more lenient with required skills
#             if is_entry_level:
#                 # Give partial credit for skills mentioned but not extensively used
#                 required_match = sum(self._calculate_skill_score(skill, skill_usage_data, is_entry_level) 
#                                  for skill in required_skills) / len(required_skills)
#             else:
#                 # For experienced candidates, require more intensive skill usage
#                 required_match = sum(self._calculate_skill_score(skill, skill_usage_data, is_entry_level) 
#                                  for skill in required_skills) / len(required_skills)
#         else:
#             required_match = 1.0
            
#         # Calculate preferred skills match
#         if preferred_skills:
#             preferred_match = sum(self._calculate_skill_score(skill, skill_usage_data, is_entry_level) 
#                                for skill in preferred_skills) / len(preferred_skills)
#         else:
#             preferred_match = 1.0
        
#         # Weight required skills more heavily
#         return (required_match * 0.7) + (preferred_match * 0.3)
    
#     def _calculate_skill_score(self, skill: str, skill_usage_data: Dict[str, Dict], is_entry_level: bool) -> float:
#         """Calculate score for an individual skill based on usage data."""
#         skill_lower = skill.lower()
        
#         # If skill not found at all
#         if skill_lower not in skill_usage_data:
#             return 0.0
            
#         skill_data = skill_usage_data[skill_lower]
        
#         # For entry-level candidates, just having the skill is good
#         if is_entry_level:
#             base_score = 0.7
#             # Bonus if used in projects
#             if skill_data.get("project_count", 0) > 0:
#                 base_score += 0.3
#             return base_score
        
#         # For experienced candidates, need more evidence
#         else:
#             # Base score from job history usage
#             job_count = skill_data.get("job_count", 0)
#             job_score = min(1.0, job_count / 2)  # Max score at 2+ jobs
            
#             # Recency bonus (0-0.3)
#             months_since_last_use = skill_data.get("months_since_last_use", 60)
#             recency_bonus = max(0, 0.3 - (months_since_last_use / 60) * 0.3)
            
#             # Project usage bonus (0-0.2)
#             project_count = skill_data.get("project_count", 0)
#             project_bonus = min(0.2, project_count * 0.1)
            
#             return min(1.0, job_score * 0.5 + recency_bonus + project_bonus)
    
#     def _extract_skill_usage(self, candidate_data: Dict[str, Any]) -> Dict[str, Dict]:
#         """Extract skill usage patterns from work history and projects."""
#         skill_data = {}
#         current_date = datetime.now()
        
#         # Get all skills (lowercase for comparison)
#         all_skills = [s.lower() for s in candidate_data.get("Skills", [])]
#         for skill in all_skills:
#             skill_data[skill] = {
#                 "job_count": 0,
#                 "project_count": 0,
#                 "months_since_last_use": 60  # Default to 5 years
#             }
        
#         # Process employment history
#         for job in candidate_data.get("Employment History", []):
#             job_description = job.get("description", "").lower()
            
#             # Get job dates
#             from_date_raw = job.get("from", "")
#             to_date_raw = job.get("to", "")
            
#             try:
#                 from_date = datetime.strptime(from_date_raw, "%Y-%m-%d") if from_date_raw else None
                
#                 if to_date_raw == "Present":
#                     to_date = current_date
#                 else:
#                     to_date = datetime.strptime(to_date_raw, "%Y-%m-%d") if to_date_raw else None
                
#                 # Check each skill
#                 for skill in all_skills:
#                     # Check if skill mentioned in description
#                     if skill in job_description:
#                         skill_data[skill]["job_count"] += 1
                        
#                         # Update recency if more recent
#                         if to_date:
#                             months_since = (current_date.year - to_date.year) * 12 + (current_date.month - to_date.month)
#                             skill_data[skill]["months_since_last_use"] = min(
#                                 skill_data[skill]["months_since_last_use"], 
#                                 months_since
#                             )
#             except (ValueError, TypeError):
#                 continue
        
#         # Process projects
#         for project in candidate_data.get("Projects", []):
#             project_description = project.get("description", "").lower()
#             project_techs = [tech.lower() for tech in project.get("tools_used/skill_used", [])]
            
#             # Check each skill
#             for skill in all_skills:
#                 # Check if skill mentioned in description or tools used
#                 if skill in project_description or skill in project_techs:
#                     skill_data[skill]["project_count"] += 1
        
#         return skill_data
    
#     def _is_entry_level(self, candidate_data: Dict[str, Any]) -> bool:
#         """Determine if candidate is entry-level based on experience."""
#         # Extract experience from candidate data
#         experience_str = candidate_data.get("Work Experience", "0")
        
#         # Try to extract years from experience string
#         years_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:year|yr)', experience_str, re.IGNORECASE)
#         years = float(years_match.group(1)) if years_match else 0
        
#         # Less than 2 years of experience is considered entry-level
#         return years < 2
    
#     def _score_experience(self, candidate_data: Dict[str, Any]) -> float:
#         """
#         Score candidate's experience level.
        
#         Enhanced to consider:
#         - Quality of experience (based on company profiles)
#         - Relevance to job requirements
#         - Growth trajectory
#         """
#         required_experience = self.job_requirements.get("required_experience", 0)
#         required_skills = set(self.job_requirements.get("required_skills", []))
        
#         # Extract experience from candidate data
#         experience_str = candidate_data.get("Work Experience", "0")
        
#         # Try to extract years from experience string
#         years_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:year|yr)', experience_str, re.IGNORECASE)
#         months_match = re.search(r'(\d+)\s*month', experience_str, re.IGNORECASE)
        
#         years = float(years_match.group(1)) if years_match else 0
#         months = float(months_match.group(1))/12 if months_match else 0
        
#         total_years = years + months
        
#         # Calculate base experience score
#         if total_years >= required_experience:
#             if total_years >= required_experience * 1.5:
#                 # Exceeds required experience by 50% or more
#                 base_score = 1.0
#             else:
#                 # Meets required experience
#                 base_score = 0.8 + (total_years - required_experience) / (required_experience * 1.5 - required_experience) * 0.2
#         else:
#             # Below required experience
#             base_score = max(0.0, total_years / required_experience * 0.8)
        
#         # Calculate experience quality score
#         quality_score = self._assess_experience_quality(candidate_data, required_skills)
        
#         # Combine scores (70% base experience, 30% quality)
#         return (base_score * 0.7) + (quality_score * 0.3)
    
#     def _assess_experience_quality(self, candidate_data: Dict[str, Any], required_skills: set) -> float:
#         """Assess the quality of candidate's experience."""
#         employment_history = candidate_data.get("Employment History", [])
#         if not employment_history:
#             return 0.5  # Neutral score if no history
        
#         total_quality_score = 0
#         job_count = 0
        
#         for job in employment_history:
#             job_quality = 0
#             company_name = job.get("company", "")
#             job_description = job.get("description", "").lower()
            
#             # Get company data if available
#             try:
#                 company_data = company.get_company_data(company_name)
                
#                 # Assess company quality based on profile
#                 if company_data:
#                     # Company size and market position bonus
#                     if company_data.get("classification", {}).get("type") == "Enterprise":
#                         job_quality += 0.2
                    
#                     # Relevant tech stack bonus
#                     tech_stack = company_data.get("work_environment", {}).get("tech_stack", [])
#                     tech_match = len(set([t.lower() for t in tech_stack]).intersection(required_skills))
#                     if tech_match > 0:
#                         job_quality += min(0.3, tech_match * 0.1)
                    
#                     # Growth potential bonus
#                     growth_potential = company_data.get("work_environment", {}).get("growth_potential", "")
#                     if growth_potential == "High":
#                         job_quality += 0.2
#                     elif growth_potential == "Moderate":
#                         job_quality += 0.1
#             except:
#                 # If company data not available, use simplified assessment
#                 pass
            
#             # Check for required skills in job description
#             skill_match_count = sum(1 for skill in required_skills if skill.lower() in job_description)
#             skill_match_score = min(0.5, skill_match_count * 0.1)
#             job_quality += skill_match_score
            
#             # Add job quality score
#             total_quality_score += min(1.0, job_quality)
#             job_count += 1
        
#         # Return average quality score
#         return total_quality_score / job_count if job_count > 0 else 0.5
    
#     def _score_projects(self, candidate_data: Dict[str, Any]) -> float:
#         """
#         Score candidate's projects for relevance.
        
#         Enhanced to consider:
#         - Technical complexity
#         - Direct relevance to job requirements
#         - Evidence of completion
#         """
#         required_skills = set([tech.lower() for tech in self.job_requirements.get("required_skills", [])])
        
#         projects = candidate_data.get("Projects", [])
#         if not projects:
#             return 0.0
        
#         total_relevance = 0.0
        
#         for project in projects:
#             # Extract project technologies
#             project_techs = set([tech.lower() for tech in project.get("tools_used/skill_used", [])])
            
#             # Calculate tech overlap
#             if required_skills:
#                 tech_overlap = len(required_skills.intersection(project_techs)) / len(required_skills)
#             else:
#                 tech_overlap = 0.5  # Neutral score if no required techs
            
#             # Calculate project complexity based on description and duration
#             description = project.get("description", "")
#             complexity_factors = [
#                 min(1.0, len(description) / 500),  # Description length
#                 0.3 if "architecture" in description.lower() else 0,
#                 0.2 if "database" in description.lower() else 0,
#                 0.2 if "api" in description.lower() else 0,
#                 0.2 if "algorithm" in description.lower() else 0,
#                 0.2 if "optimization" in description.lower() else 0
#             ]
#             complexity_factor = min(1.0, sum(complexity_factors) / 2)  # Cap at 1.0
            
#             # Calculate completion evidence
#             has_links = "github" in description.lower() or "link" in description.lower()
#             has_results = "result" in description.lower() or "achieved" in description.lower()
#             completion_factor = 0.5 + (0.25 if has_links else 0) + (0.25 if has_results else 0)
            
#             # Calculate project relevance
#             project_relevance = (tech_overlap * 0.5) + (complexity_factor * 0.3) + (completion_factor * 0.2)
#             total_relevance += project_relevance
        
#         # Average project relevance, with a bonus for having multiple projects
#         project_count_bonus = min(0.3, (len(projects) - 1) * 0.1)  # Up to 0.3 bonus for 4+ projects
#         return min(1.0, (total_relevance / len(projects)) + project_count_bonus)
    
#     def _score_education(self, candidate_data: Dict[str, Any]) -> float:
#         """Score candidate's education."""
#         required_degree = self.job_requirements.get("required_degree", "")
#         required_field = self.job_requirements.get("required_field", "")
        
#         education_entries = candidate_data.get("Education", [])
#         if not education_entries:
#             return 0.0
        
#         # Define degree hierarchy
#         degree_levels = {
#             "high school": 1,
#             "associate": 2,
#             "bachelor": 3,
#             "master": 4, 
#             "phd": 5,
#             "doctorate": 5
#         }
        
#         highest_degree_level = 0
#         field_match = False
#         school_quality = 0.5  # Default neutral score
        
#         # Find highest degree and check for field match
#         for entry in education_entries:
#             degree = entry.get("degree", "").lower()
#             school = entry.get("institution", "").lower()
            
#             # Check degree level
#             for level_name, level_value in degree_levels.items():
#                 if level_name in degree:
#                     highest_degree_level = max(highest_degree_level, level_value)
            
#             # Check field match
#             field = entry.get("specialization", "").lower()
#             if required_field.lower() in field or field in required_field.lower():
#                 field_match = True
            
#             # Simple school quality check (could be expanded with actual data)
#             if "university" in school:
#                 school_quality = max(school_quality, 0.7)
#             if any(elite in school for elite in ["mit", "stanford", "harvard", "oxford", "cambridge"]):
#                 school_quality = 1.0
        
#         # Calculate degree level score
#         required_level = 0
#         for level_name, level_value in degree_levels.items():
#             if level_name in required_degree.lower():
#                 required_level = level_value
        
#         # Calculate degree match score
#         if highest_degree_level >= required_level:
#             degree_score = 1.0
#         else:
#             degree_score = highest_degree_level / required_level if required_level > 0 else 0.5
        
#         # Calculate overall education score
#         if not required_field:
#             return (degree_score * 0.8) + (school_quality * 0.2)
#         else:
#             return (degree_score * 0.6) + (0.3 if field_match else 0.0) + (school_quality * 0.1)
    
#     def _score_job_stability(self, candidate_data: Dict[str, Any]) -> float:
#         """
#         Score candidate's job stability.
        
#         Enhanced to use stability.py module data including tenure categories.
#         """
#         employment_history = candidate_data.get("Employment History", [])
#         if not employment_history:
#             return 0.5  # Neutral score if no history
        
#         # Try to use stability data if available
#         try:
#             stability_scores = []
            
#             for job in employment_history:
#                 company_name = job.get("company", "")
                
#                 # Get stability data
#                 stability_data = stability.analyze_job_stability(job)
                
#                 if stability_data:
#                     # Convert tenure category to score
#                     tenure_category = stability_data.get("tenure_category", "")
                    
#                     if tenure_category == "Very short tenure":
#                         score = 0.2
#                     elif tenure_category == "Short tenure":
#                         score = 0.4
#                     elif tenure_category == "Average tenure":
#                         score = 0.6
#                     elif tenure_category == "Long tenure":
#                         score = 0.8
#                     elif tenure_category == "Very long tenure":
#                         score = 1.0
#                     else:
#                         score = 0.5
                    
#                     stability_scores.append(score)
            
#             if stability_scores:
#                 # Weight recent jobs more heavily
#                 weighted_scores = [score * (i+1) for i, score in enumerate(reversed(stability_scores))]
#                 weighted_total = sum(weighted_scores)
#                 weights_sum = sum(i+1 for i in range(len(stability_scores)))
                
#                 return weighted_total / weights_sum
            
#         except:
#             pass
        
#         # Fallback to the original method if stability data not available
#         # Calculate average tenure
#         total_months = 0
#         job_count = 0
        
#         for job in employment_history:
#             from_date_raw = job.get("from", "")
#             to_date_raw = job.get("to", "")
            
#             try:
#                 from_date = datetime.strptime(from_date_raw, "%Y-%m-%d") if from_date_raw else None
                
#                 if to_date_raw == "Present":
#                     to_date = datetime.now()
#                 else:
#                     to_date = datetime.strptime(to_date_raw, "%Y-%m-%d") if to_date_raw else None
                
#                 if from_date and to_date:
#                     months = (to_date.year - from_date.year) * 12 + (to_date.month - from_date.month)
#                     total_months += months
#                     job_count += 1
#             except (ValueError, TypeError):
#                 continue
        
#         if job_count == 0:
#             return 0.5  # Neutral score if no valid jobs
        
#         avg_tenure = total_months / job_count
        
#         # Score based on average tenure
#         if avg_tenure < 12:
#             return max(0.2, 0.4 * (avg_tenure / 12))
#         elif avg_tenure < 24:
#             return 0.4 + 0.3 * ((avg_tenure - 12) / 12)
#         else:
#             return min(1.0, 0.7 + 0.3 * min(1.0, (avg_tenure - 24) / 12))
    
#     def _score_location(self, candidate_data: Dict[str, Any]) -> float:
#         """
#         Score candidate's location compatibility using location.py for distance calculation.
        
#         Enhanced to use actual distance calculations and proximity thresholds.
#         """
#         remote_work = self.job_requirements.get("remote_work", False)
#         relocation = self.job_requirements.get("relocation_allowed", False)
        
#         # If remote work is offered, location is less important
#         if remote_work:
#             return 0.9
        
#         job_location = {
#             "city": self.job_requirements.get("location", {}).get("city", ""),
#             "state": self.job_requirements.get("location", {}).get("state", ""),
#             "country": self.job_requirements.get("location", {}).get("country", "")
#         }
        
#         candidate_location = {
#             "city": candidate_data.get("City", ""),
#             "state": candidate_data.get("State", ""),
#             "country": candidate_data.get("Country Code", "")
#         }
        
#         try:
#             # Use location module to get distance
#             distance = location.calculate_distance(job_location, candidate_location)
            
#             # Score based on distance relative to threshold
#             if distance <= 20:  # Same city or very close
#                 return 1.0
#             elif distance <= 50:  # Reasonable commute
#                 return 0.8
#             elif distance <= self.proximity_threshold:  # Within threshold but longer commute
#                 return 0.6
#             elif relocation:
#                 # Candidate outside threshold but relocation allowed
#                 if candidate_location.get("country", "") == job_location.get("country", ""):
#                     return 0.4  # Same country, easier relocation
#                 else:
#                     return 0.2  # International relocation
#             else:
#                 return 0.1  # Outside threshold, no relocation
#         except:
#             # Fallback to basic location matching if distance calculation fails
#             same_city = job_location.get("city", "").lower() == candidate_location.get("city", "").lower()
#             same_state = job_location.get("state", "").lower() == candidate_location.get("state", "").lower()
#             same_country = job_location.get("country", "").lower() == candidate_location.get("country", "").lower()
            
#             # Calculate location score
#             if same_city:
#                 return 1.0
#             elif same_state:
#                 return 0.8
#             elif same_country:
#                 return 0.6
#             elif relocation:
#                 return 0.4  # Candidate would need to relocate
#             else:
#                 return 0.1  # Poor location match
    
#     def _score_company_relevance(self, candidate_data: Dict[str, Any]) -> float:
#         """
#         Score relevance of candidate's previous companies using company.py data.
        
#         Enhanced to use company classification, industry match, and work environment data.
#         """
#         target_industry = self.job_requirements.get("industry", "")
#         employment_history = candidate_data.get("Employment History", [])
        
#         if not employment_history or not target_industry:
#             return 0.5  # Neutral score
        
#         total_relevance = 0.0
#         job_count = 0
        
#         for job in employment_history:
#             company_name = job.get("company", "")
            
#             try:
#                 # Get company data
#                 company_data = company.get_company_data(company_name)
                
#                 if company_data:
#                     relevance_score = 0.0
                    
#                     # Check industry match
#                     company_industry = company_data.get("classification", {}).get("industry", "")
#                     if company_industry.lower() == target_industry.lower():
#                         relevance_score += 0.6
#                     elif target_industry.lower() in company_industry.lower() or company_industry.lower() in target_industry.lower():
#                         relevance_score += 0.3
                    
#                     # Check business model match
#                     business_model = company_data.get("classification", {}).get("business_model", "")
#                     if business_model and business_model.lower() == self.job_requirements.get("business_model", "").lower():
#                         relevance_score += 0.2
                    
#                     # Check tech stack match with required skills
#                     tech_stack = company_data.get("work_environment", {}).get("tech_stack", [])
#                     required_skills = self.job_requirements.get("required_skills", [])
                    
#                     if tech_stack and required_skills:
#                         tech_match_ratio = len(set([t.lower() for t in tech_stack]).intersection(
#                             [s.lower() for s in required_skills])) / len(required_skills)
#                         relevance_score += tech_match_ratio * 0.2
                    
#                     total_relevance += min(1.0, relevance_score)
#                     job_count += 1
#                 else:
#                     # If company data not available, use basic industry match
#                     if target_industry.lower() in company_name.lower():
#                         total_relevance += 0.4
#                         job_count += 1
#             except:
#                 # Fallback if company module fails
#                 if target_industry.lower() in company_name.lower():
#                     total_relevance += 0.4
#                     job_count += 1
        
#         # Return average company relevance, weighted toward more recent companies
#         return total_relevance / job_count if job_count > 0 else 0.5
    
#     def _score_work_preference(self, candidate_data: Dict[str, Any]) -> float:
#         """Score match between candidate's work preference and job type."""
#         job_type = self.job_requirements.get("job_type", "")  # e.g., "Full-time", "Contract", etc.
#         work_preference = candidate_data.get("Work Preference", "")
        
#         if not job_type or not work_preference:
#             return 0.5  # Neutral score
        
#         # Check for exact match
#         if job_type.lower() in work_preference.lower():
#             return 1.0
        
#         # Check for partial match
#         if ("full" in job_type.lower() and "full" in work_preference.lower()) or \
#            ("part" in job_type.lower() and "part" in work_preference.lower()) or \
#            ("contract" in job_type.lower() and "contract" in work_preference.lower()) or \
#            ("remote" in job_type.lower() and "remote" in work_preference.lower()):
#             return 0.8
        
#         # No match
#         return 0.2
    
#     def _identify_strengths(self, candidate_data: Dict[str, Any]) -> List[str]:
#         """Identify candidate's key strengths for this job."""
#         strengths = []
        
#         # Check skills
#         required_skills = set(self.job_requirements.get("required_skills", []))
#         candidate_skills = set([skill.lower() for skill in candidate_data.get("Skills", [])])
        
#         skills_match_ratio = len(required_skills.intersection([s.lower() for s in candidate_skills])) / len(required_skills) if required_skills else 0
        
#         if skills_match_ratio > 0.8:
#             strengths.append("Strong skills match")
        
#         # Check experience
#         experience_str = candidate_data.get("Work Experience", "0")
#         years_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:year|yr)', experience_str, re.IGNORECASE)
#         years = float(years_match.group(1)) if years_match else 0
#         #NEED TO CHECK FROM HERE
#         required_experience = self.job_requirements.get("required_experience", 0)
#         if years >= required_experience * 1.2:
#             strengths.append("Exceeds required experience")
#         # Check education   
#         education_entries = candidate_data.get("Education", [])
#         required_degree = self.job_requirements.get("required_degree", "").lower()
#         if education_entries and required_degree:
#             for entry in education_entries:
#                 degree = entry.get("degree", "").lower()
#                 if "master" in degree or "phd" in degree or "doctorate" in degree:
#                     if "bachelor" in required_degree:
#                         strengths.append("Advanced degree")
#                     break
#         # Check project relevance   
#         project_score = self._score_projects(candidate_data)
#         if project_score > 0.7:
#             strengths.append("Strong project relevance")
#         # Check job stability 
#         stability_score = self._score_job_stability(candidate_data)
#         if stability_score > 0.7:
#             strengths.append("Strong job stability")
#         # Check location compatibility  
#         location_score = self._score_location(candidate_data)
#         if location_score > 0.7:
#             strengths.append("Good location compatibility")
#         # Check company relevance   
#         company_score = self._score_company_relevance(candidate_data)
#         if company_score > 0.7:
#             strengths.append("Strong company relevance")
#         # Check work preference match
#         preference_score = self._score_work_preference(candidate_data)
#         if preference_score > 0.7:
#             strengths.append("Strong work preference match")
#         # Check job type match
#         job_type = self.job_requirements.get("job_type", "")
#         if job_type.lower() in candidate_data.get("Work Preference", "").lower():
#             strengths.append("Job type matches preference")
#         # Check relocation willingness
#         relocation = self.job_requirements.get("relocation_allowed", False)
#         if relocation:
#             strengths.append("Willing to relocate")
#         return strengths
    
#     def _identify_gaps(self, candidate_data: Dict[str, Any]) -> List[str]:
#         """Identify candidate's key gaps for this job."""
#         gaps = []
        
#         # Check skills
#         required_skills = set(self.job_requirements.get("required_skills", []))
#         candidate_skills = set([skill.lower() for skill in candidate_data.get("Skills", [])])
        
#         missing_skills = required_skills - set([s.lower() for s in candidate_skills])
#         if missing_skills:
#             gaps.append(f"Missing skills: {', '.join(missing_skills)}")
        
#         # Check experience
#         experience_str = candidate_data.get("Work Experience", "0")
#         years_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:year|yr)', experience_str, re.IGNORECASE)
#         years = float(years_match.group(1)) if years_match else 0
        
#         required_experience = self.job_requirements.get("required_experience", 0)
#         if years < required_experience:
#             gaps.append(f"Experience gap: {required_experience - years} years")
        
#         # Check education
#         education_entries = candidate_data.get("Education", [])
#         required_degree = self.job_requirements.get("required_degree", "").lower()
#         required_field = self.job_requirements.get("required_field", "").lower()
        
#         if required_degree and not education_entries:
#             gaps.append("Missing education information")
#         elif required_field and education_entries:
#             field_match = False
#             for entry in education_entries:
#                 field = entry.get("specialization", "").lower()
#                 if required_field in field or field in required_field:
#                     field_match = True
#                     break
            
#             if not field_match:
#                 gaps.append(f"Education not in required field: {required_field}")
        
#         # Check project relevance
#         project_score = self._score_projects(candidate_data)
#         if project_score < 0.5:
#             gaps.append("Projects lack relevance to job requirements")
        
#         # Check job stability
#         stability_score = self._score_job_stability(candidate_data)
#         if stability_score < 0.5:
#             gaps.append("Job stability is below expectations")
        
#         # Check location compatibility
#         location_score = self._score_location(candidate_data)
#         if location_score < 0.5:
#             gaps.append("Location compatibility is low")
        
#         # Check company relevance
#         company_score = self._score_company_relevance(candidate_data)
#         if company_score < 0.5:
#             gaps.append("Previous companies lack relevance to target industry")
        
#         # Check work preference match
#         preference_score = self._score_work_preference(candidate_data)
#         if preference_score < 0.5:
#             gaps.append("Work preference does not align with job type")
        
#         return gaps

# # Example usage
# def main():
#     # Define job requirements
#     job_requirements = {
#         "required_skills": ["Python", "Machine Learning", "Data Analysis"],
#         "preferred_skills": ["TensorFlow", "Keras"],
#         "required_experience": 3,
#         "required_degree": "Bachelor's in Computer Science",
#         "required_field": "Computer Science",
#         "job_type": "Full-time",
#         "location": {
#             "city": "New York",
#             "state": "NY",
#             "country": "USA"
#         },
#         "remote_work": False,
#         "relocation_allowed": True,
#         "industry": "Technology",
#         "business_model": "Software Development"
#     }
#     # Define candidate data
#     candidate_data = {
#         "Skills": candidate_data.get("Skills", []),
#         "Skills": ["Python", "Machine Learning", "Data Analysis", "TensorFlow"],
#         "Work Experience": "4 years",
#         "Education": [
#             {
#                 "degree": "Bachelor's in Computer Science",
#                 "institution": "XYZ University",
#                 "specialization": "Computer Science",
#                 "year_of_graduation": 2018
#             }
#         ],
#         "Projects": [
#             {
#                 "name": "Predictive Analytics System",
#                 "description": "Developed a predictive analytics system using Python and TensorFlow to forecast sales trends.",
#                 "tools_used/skill_used": ["Python", "TensorFlow", "Data Analysis"]
#             },
#             {
#                 "name": "Customer Segmentation",
#                 "description": "Implemented a customer segmentation model using Keras and scikit-learn for targeted marketing.",
#                 "tools_used/skill_used": ["Keras", "scikit-learn", "Machine Learning"]
#             }
#         ],
#         "Employment History": [
#             {
#                 "company": "TechCorp",
#                 "from": "2019-01-01",
#                 "to": "2022-12-31",
#                 "description": "Worked as a Data Scientist, focusing on machine learning and data analysis projects."
#             },
#             {
#                 "company": "DataSolutions",
#                 "from": "2018-06-01",
#                 "to": "2018-12-31",
#                 "description": "Interned as a Data Analyst, assisting in data cleaning and visualization tasks."
#             }
#         ],
#         "City": "New York",
#         "State": "NY",
#         "Country Code": "USA",
#         "Work Preference": "Full-time"
#     }

#     # Create an instance of the EnhancedCandidateScorer
#     scorer = EnhancedCandidateScorer(job_requirements)

#     # Score the candidate
#     results = scorer.score_candidate(candidate_data)

#     # Print the results
#     print("\nCandidate Scoring Results:")
#     print("-" * 50)
#     print(f"Overall Score: {results['overall_score']}/1.0")
#     print("\nCategory Scores:")
#     if 'category_scores' in results:
#         for category, score in results['category_scores'].items():
#             print(f"  {category.replace('_', ' ').title()}: {score}/1.0")

#     print("\nCandidate Strengths:")
#     for strength in results['candidate_strengths']:
#         print(f"  ✓ {strength}")

#     print("\nCandidate Gaps:")
#     for gap in results['candidate_gaps']:
#         print(f"  ✗ {gap}")

#     # Save results to a file
#     with open("candidate_score.json", "w") as f:
#         json.dump(results, f, indent=4)

#     print("\nDetailed results saved to candidate_score.json")


# if __name__ == "__main__":
#     main()
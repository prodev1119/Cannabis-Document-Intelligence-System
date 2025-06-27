# Sample municipal documents for cannabis business relevance testing
# These represent realistic city documents that would be found in municipal systems

import os
import pdfplumber
from docx import Document
from typing import Dict, List

def process_pdf_documents(folder_path: str = "docs") -> Dict[str, str]:
    """
    Find all PDFs in a folder, extract text, and return a dictionary.

    Args:
        folder_path: The path to the folder containing PDFs.

    Returns:
        A dictionary where keys are filenames and values are the extracted text.
    """
    pdf_texts = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith(".pdf"):
                file_path = os.path.join(root, file)
                try:
                    with pdfplumber.open(file_path) as pdf:
                        text = ""
                        for page in pdf.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                        pdf_texts[file] = text
                except Exception as e:
                    print(f"Could not read {file_path}: {e}")
    return pdf_texts

def extract_all_documents(folder_path: str = "docs") -> Dict[str, str]:
    """
    Recursively find and extract text from all .pdf, .docx, and .txt files in the given folder.
    Skips .doc files and prints a warning.
    Returns a dict of {filename: content}.
    """
    supported_exts = [".pdf", ".docx", ".txt"]
    documents = {}
    for root, _, files in os.walk(folder_path):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            file_path = os.path.join(root, file)
            if ext in supported_exts:
                try:
                    if ext == ".pdf":
                        with pdfplumber.open(file_path) as pdf:
                            text = ""
                            for page in pdf.pages:
                                page_text = page.extract_text()
                                if page_text:
                                    text += page_text + "\n"
                        documents[file] = text
                    elif ext == ".docx":
                        doc = Document(file_path)
                        text = "\n".join([para.text for para in doc.paragraphs])
                        documents[file] = text
                    elif ext == ".txt":
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            documents[file] = f.read()
                except Exception as e:
                    print(f"Could not read {file_path}: {e}")
            elif ext == ".doc":
                print(f"Skipping unsupported DOC file (requires textract or antiword): {file_path}")
    return documents

SAMPLE_DOCUMENTS = {
    "cannabis_retail_ordinance_approved.txt": """
CITY COUNCIL MEETING MINUTES
Date: December 15, 2024
Location: City Hall Council Chambers

AGENDA ITEM 7.3: CANNABIS RETAIL ORDINANCE

The council discussed the proposed cannabis retail ordinance for the downtown district. 
After extensive public hearing and planning commission review, the ordinance was approved 
with a 5-2 vote. The licensing program will open on January 15, 2025, with an application 
window of 30 days. Merit-based selection will be used for the initial 5 dispensary licenses.

Key provisions:
- Conditional use permit approved for cannabis retail in C-2 zones
- Social equity program included for local business owners
- Application period: January 15 - February 14, 2025
- Second reading scheduled for January 5, 2025

Motion passed. Ordinance effective immediately.
""",

    "planning_commission_hearing.txt": """
PLANNING COMMISSION MEETING
Date: November 28, 2024

PUBLIC HEARING: DRAFT ORDINANCE - CANNABIS BUSINESS ZONING

The commission held a public hearing on proposed zoning amendments for cannabis business 
operations. The draft ordinance would allow cannabis retail, cultivation, and processing 
in designated industrial zones. Several community members spoke in favor of the economic 
benefits, citing potential tax revenue increases.

Study session scheduled for December 10 to review public comments.
No action taken - item continued to next meeting.
""",

    "city_budget_discussion.txt": """
ANNUAL BUDGET WORKSHOP
Date: October 20, 2024

BUDGET DISCUSSION: CANNABIS TAX REVENUE

The finance department presented projections for cannabis tax revenue in the upcoming 
fiscal year. Based on current dispensary operations and proposed new licenses, the city 
expects $2.3 million in cannabis-related tax revenue. This represents a 15% increase 
from the previous year.

General mention was made of expanding cannabis business opportunities, but no specific 
action items were proposed.
""",

    "moratorium_lifted.txt": """
CITY COUNCIL SPECIAL MEETING
Date: January 10, 2025

EMERGENCY ITEM: CANNABIS MORATORIUM LIFTED

The council voted unanimously to lift the temporary moratorium on cannabis business 
applications. The moratorium was originally enacted to allow time for comprehensive 
ordinance development. With the new cannabis business regulations now in place, the 
moratorium is no longer necessary.

Effective immediately, new cannabis business applications may be submitted.
""",

    "dispensary_license_application.txt": """
DEPARTMENT OF LICENSING AND PERMITS
Date: February 1, 2025

NOTICE: DISPENSARY LICENSE APPLICATION WINDOW OPEN

The city is now accepting applications for dispensary licenses. The application period 
runs from February 1 to March 1, 2025. A total of 3 licenses are available for the 
north district. Merit-based selection criteria include business experience, financial 
capacity, and community benefit plans.

Application forms available at city hall or online at city.gov/cannabis
""",

    "zoning_amendment_approved.txt": """
PLANNING AND ZONING COMMISSION
Date: December 5, 2024

ZONING AMENDMENT: CANNABIS CULTIVATION FACILITIES

The commission approved zoning amendments to allow cannabis cultivation facilities in 
agricultural zones. The amendment passed with a 4-1 vote. Conditional use permits will 
be required for all cultivation operations. The amendment is effective January 1, 2025.

Public hearing was well-attended with strong community support for local cannabis 
cultivation opportunities.
""",

    "cannabis_tax_ordinance.txt": """
CITY COUNCIL MEETING
Date: November 12, 2024

ORDINANCE: CANNABIS BUSINESS TAX

The council approved a new cannabis business tax ordinance. The ordinance establishes 
a 5% tax on gross receipts for all cannabis retail operations and a 3% tax on cultivation 
facilities. The tax revenue will be dedicated to public safety and community programs.

Budget discussion included projections for $1.8 million in annual cannabis tax revenue.
Ordinance passed 6-1, effective January 1, 2025.
""",

    "social_equity_program.txt": """
DEPARTMENT OF ECONOMIC DEVELOPMENT
Date: January 20, 2025

SOCIAL EQUITY CANNABIS BUSINESS PROGRAM

The city has launched a social equity program for cannabis business licensing. The 
program provides technical assistance, reduced fees, and priority consideration for 
applicants from communities disproportionately impacted by cannabis prohibition.

Application period opens March 1, 2025. Study session scheduled for February 15.
""",

    "cannabis_retail_denied.txt": """
PLANNING COMMISSION DECISION
Date: December 20, 2024

CONDITIONAL USE PERMIT DENIED: CANNABIS RETAIL

The commission denied a conditional use permit for a proposed cannabis retail location 
at 123 Main Street. The denial was based on proximity to schools and insufficient 
parking. The applicant may appeal the decision within 30 days.

Public hearing was held on December 15 with significant community opposition.
""",

    "cannabis_ordinance_study.txt": """
CITY MANAGER'S OFFICE
Date: October 5, 2024

STUDY SESSION: CANNABIS ORDINANCE DEVELOPMENT

The city manager convened a study session to discuss cannabis ordinance development. 
Staff presented research on cannabis business regulations from other cities and 
recommendations for local implementation. No formal action was taken.

General mention of cannabis business opportunities and regulatory framework.
""",

    "park_maintenance.txt": """
PARKS AND RECREATION DEPARTMENT
Date: January 15, 2025

PARK MAINTENANCE SCHEDULE

The department has scheduled routine maintenance for all city parks. Work will include 
landscaping, playground equipment inspection, and facility repairs. No cannabis-related 
activities or discussions included in this maintenance schedule.

Maintenance to be completed by March 1, 2025.
""",

    "traffic_signal_repair.txt": """
PUBLIC WORKS DEPARTMENT
Date: February 10, 2025

TRAFFIC SIGNAL REPAIR NOTICE

The traffic signal at the intersection of Oak Street and Pine Avenue will be repaired 
on February 15, 2025. Temporary traffic control measures will be in place. This is 
routine maintenance with no connection to cannabis business operations.

Repair expected to take 4 hours.
""",

    "library_hours.txt": """
PUBLIC LIBRARY ANNOUNCEMENT
Date: January 25, 2025

LIBRARY HOURS UPDATE

The public library will extend its hours beginning February 1, 2025. New hours: 
Monday-Friday 9 AM - 8 PM, Saturday 10 AM - 6 PM, Sunday 1 PM - 5 PM. This change 
is unrelated to any cannabis business activities or regulations.

Extended hours made possible by increased city budget allocation.
""",

    "water_main_repair.txt": """
UTILITIES DEPARTMENT
Date: February 5, 2025

WATER MAIN REPAIR SCHEDULE

Emergency water main repair scheduled for February 8, 2025, on Elm Street between 
2nd and 3rd Avenues. No cannabis business operations or regulatory activities 
involved. Standard utility maintenance procedure.

Repair expected to take 6 hours with temporary water service interruption.
""",

    "garbage_collection.txt": """
SANITATION DEPARTMENT
Date: January 30, 2025

GARBAGE COLLECTION SCHEDULE UPDATE

Due to the upcoming holiday, garbage collection will be delayed by one day for all 
routes. This affects all city residents and businesses, including any cannabis 
businesses operating in the city. No special cannabis-related considerations.

Updated schedule effective February 1, 2025.
"""
}


def get_sample_documents():
    """Return the sample documents dictionary."""
    return SAMPLE_DOCUMENTS


def save_sample_documents_to_files():
    """Save sample documents to individual text files for testing."""
    import os
    
    # Create documents directory if it doesn't exist
    os.makedirs("sample_documents", exist_ok=True)
    
    for filename, content in SAMPLE_DOCUMENTS.items():
        filepath = os.path.join("sample_documents", filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip())
    
    print(f"Saved {len(SAMPLE_DOCUMENTS)} sample documents to sample_documents/ directory")


if __name__ == "__main__":
    save_sample_documents_to_files() 
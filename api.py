"""
FastAPI Web Interface for Cannabis Document Intelligence System
==============================================================

Provides REST API endpoints for document classification and automation workflows.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import uvicorn
import json
import os

from cannabis_classifier import CannabisDocumentClassifier, ClassificationResult, PriorityLevel
from automation_workflows import AutomationWorkflows

app = FastAPI(
    title="Cannabis Document Intelligence API",
    description="API for classifying municipal documents for cannabis business relevance",
    version="1.0.0"
)

# Initialize components
classifier = CannabisDocumentClassifier()
automation = AutomationWorkflows()


class DocumentRequest(BaseModel):
    document_name: str
    content: str


class DocumentResponse(BaseModel):
    document_name: str
    classification: str
    score: int
    reasoning: str
    key_phrases: List[str]
    recommended_action: str
    processed_at: str


class BatchAnalysisRequest(BaseModel):
    documents: Dict[str, str]


class BatchAnalysisResponse(BaseModel):
    results: List[DocumentResponse]
    summary: Dict[str, Any]
    automation_results: Dict[str, Any]


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with API documentation."""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cannabis Document Intelligence API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .header { background-color: #4CAF50; color: white; padding: 20px; border-radius: 5px; }
            .endpoint { border: 1px solid #ddd; margin: 10px 0; padding: 15px; border-radius: 5px; }
            .method { font-weight: bold; color: #2196F3; }
            .url { font-family: monospace; background-color: #f5f5f5; padding: 5px; }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🌿 Cannabis Document Intelligence API</h1>
            <p>Classify municipal documents for cannabis business relevance</p>
        </div>
        
        <h2>Available Endpoints:</h2>
        
        <div class="endpoint">
            <div class="method">GET</div>
            <div class="url">/docs</div>
            <p>Interactive API documentation (Swagger UI)</p>
        </div>
        
        <div class="endpoint">
            <div class="method">POST</div>
            <div class="url">/classify</div>
            <p>Classify a single document</p>
        </div>
        
        <div class="endpoint">
            <div class="method">POST</div>
            <div class="url">/classify-batch</div>
            <p>Classify multiple documents</p>
        </div>
        
        <div class="endpoint">
            <div class="method">GET</div>
            <div class="url">/sample-documents</div>
            <p>Get sample municipal documents for testing</p>
        </div>
        
        <div class="endpoint">
            <div class="method">POST</div>
            <div class="url">/automation-workflows</div>
            <p>Execute automation workflows for classified documents</p>
        </div>
        
        <div class="endpoint">
            <div class="method">GET</div>
            <div class="url">/methodology</div>
            <p>Get detailed methodology explanation</p>
        </div>
    </body>
    </html>
    """
    return html_content


@app.post("/classify", response_model=DocumentResponse)
async def classify_document(request: DocumentRequest):
    """
    Classify a single document for cannabis business relevance.
    
    Returns classification result with score, reasoning, and recommended action.
    """
    try:
        result = classifier.classify_document(request.content, request.document_name)
        
        return DocumentResponse(
            document_name=result.document_name,
            classification=result.classification.value,
            score=result.score,
            reasoning=result.reasoning,
            key_phrases=result.key_phrases,
            recommended_action=result.recommended_action,
            processed_at=result.processed_at.isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification error: {str(e)}")


@app.post("/classify-batch", response_model=BatchAnalysisResponse)
async def classify_batch_documents(request: BatchAnalysisRequest):
    """
    Classify multiple documents and return comprehensive results.
    
    Includes summary statistics and automation workflow execution.
    """
    try:
        # Classify all documents
        results = classifier.process_documents(request.documents)
        
        # Convert to response format
        document_responses = []
        for result in results:
            document_responses.append(DocumentResponse(
                document_name=result.document_name,
                classification=result.classification.value,
                score=result.score,
                reasoning=result.reasoning,
                key_phrases=result.key_phrases,
                recommended_action=result.recommended_action,
                processed_at=result.processed_at.isoformat()
            ))
        
        # Generate summary
        summary = {
            "total_documents": len(results),
            "high_priority": len([r for r in results if r.classification == PriorityLevel.HIGH_PRIORITY]),
            "medium_priority": len([r for r in results if r.classification == PriorityLevel.MEDIUM_PRIORITY]),
            "low_priority": len([r for r in results if r.classification == PriorityLevel.LOW_PRIORITY]),
            "irrelevant": len([r for r in results if r.classification == PriorityLevel.IRRELEVANT]),
            "average_score": sum(r.score for r in results) / len(results) if results else 0
        }
        
        # Execute automation workflows
        automation_results = automation.process_automation_workflows(results)
        
        return BatchAnalysisResponse(
            results=document_responses,
            summary=summary,
            automation_results=automation_results
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch classification error: {str(e)}")


@app.post("/automation-workflows")
async def execute_automation_workflows(request: BatchAnalysisRequest):
    """
    Execute automation workflows for classified documents.
    
    Processes documents and returns automation results for each priority level.
    """
    try:
        # First classify the documents
        results = classifier.process_documents(request.documents)
        
        # Execute automation workflows
        automation_results = automation.process_automation_workflows(results)
        
        return {
            "message": "Automation workflows executed successfully",
            "document_count": len(results),
            "automation_results": automation_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Automation workflow error: {str(e)}")


@app.get("/methodology")
async def get_methodology():
    """
    Get detailed explanation of the classification methodology.
    
    Returns comprehensive documentation of the scoring system and business logic.
    """
    methodology = """
Cannabis Document Classification Methodology
===========================================

Scoring System Overview:
The system uses a weighted keyword-based approach with context modifiers to score
documents for cannabis business relevance. The methodology is designed to identify
documents that represent immediate business opportunities or require monitoring.

Keyword Categories:

1. HIGH VALUE KEYWORDS (10 points each):
   - "cannabis retail", "dispensary license", "application window"
   - "ordinance approved", "licensing program", "application period"
   - "merit-based selection", "conditional use permit approved", "second reading"
   
   Rationale: These phrases indicate immediate business opportunities, active
   licensing processes, or approved regulatory changes that create new markets.

2. MEDIUM VALUE KEYWORDS (5 points each):
   - "public hearing", "planning commission", "draft ordinance"
   - "zoning amendment", "social equity", "moratorium lifted"
   - "cannabis business", "study session"
   
   Rationale: These indicate regulatory processes in progress, potential future
   opportunities, or policy discussions that require monitoring.

3. LOW VALUE KEYWORDS (2 points each):
   - "cannabis", "marijuana", "dispensary", "retail"
   - "tax revenue", "budget discussion", "general mention"
   
   Rationale: These are general mentions that may indicate background relevance
   but don't represent immediate opportunities.

Context Modifiers:

1. POSITIVE MODIFIERS (+3 points each):
   - "approved", "passed", "effective", "final"
   
   Rationale: These words indicate completed actions that create immediate
   business opportunities.

2. NEGATIVE MODIFIERS (-3 points each):
   - "prohibited", "banned", "rejected"
   
   Rationale: These words indicate restrictions that limit business opportunities.

3. DATE BONUS (+5 points for dates within 90 days):
   Rationale: Recent dates indicate current or upcoming opportunities that
   require immediate attention.

4. TITLE/HEADING BONUS (+2 points):
   Rationale: Keywords in titles or headings indicate the document's primary
   focus on cannabis-related matters.

Classification Thresholds:

- 70+ points: HIGH PRIORITY (immediate action needed)
- 30-69 points: MEDIUM PRIORITY (monitor and plan)
- 10-29 points: LOW PRIORITY (background awareness)
- Under 10 points: IRRELEVANT (ignore)

Automation Workflows:

1. HIGH PRIORITY: Immediate Slack alerts with detailed information
2. MEDIUM PRIORITY: Weekly digest emails for planning purposes
3. LOW PRIORITY: JSON logging for future reference
4. IRRELEVANT: No action taken

Business Logic Adjustments Made:

1. Enhanced date detection to handle multiple date formats
2. Added title/heading analysis for better context understanding
3. Implemented comprehensive keyword matching with case-insensitive search
4. Created detailed reasoning generation for transparency
5. Built robust automation workflows that match business needs

This methodology balances sensitivity (catching relevant documents) with specificity
(avoiding false positives) to provide actionable intelligence for cannabis business
opportunities.
"""
    return {
        "methodology": methodology,
        "scoring_system": {
            "high_value_keywords": classifier.high_value_keywords,
            "medium_value_keywords": classifier.medium_value_keywords,
            "low_value_keywords": classifier.low_value_keywords,
            "positive_modifiers": classifier.positive_modifiers,
            "negative_modifiers": classifier.negative_modifiers,
            "thresholds": {
                "high_priority": classifier.thresholds[PriorityLevel.HIGH_PRIORITY],
                "medium_priority": classifier.thresholds[PriorityLevel.MEDIUM_PRIORITY],
                "low_priority": classifier.thresholds[PriorityLevel.LOW_PRIORITY]
            }
        }
    }


@app.post("/upload-file")
async def upload_and_classify_file(file: UploadFile = File(...)):
    """
    Upload a document file and classify it for cannabis business relevance.
    
    Supports text files (.txt) and will extract content for classification.
    """
    if not file.filename or not file.filename.endswith('.txt'):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")
    
    try:
        content = await file.read()
        document_content = content.decode('utf-8')
        
        result = classifier.classify_document(document_content, file.filename)
        
        return DocumentResponse(
            document_name=result.document_name,
            classification=result.classification.value,
            score=result.score,
            reasoning=result.reasoning,
            key_phrases=result.key_phrases,
            recommended_action=result.recommended_action,
            processed_at=result.processed_at.isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File processing error: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000) 
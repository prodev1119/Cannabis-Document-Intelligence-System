#!/usr/bin/env python3
"""
Cannabis Document Intelligence System
====================================

Main application for classifying municipal documents for cannabis business relevance
and executing automation workflows based on priority levels.

This system implements the scoring methodology specified in the test requirements:
- High value keywords (10 points each)
- Medium value keywords (5 points each) 
- Low value keywords (2 points each)
- Context modifiers (bonus/penalty points)
- Date bonuses for recent documents
- Title/heading bonuses
"""

import json
import os
from datetime import datetime
from typing import Dict, List

from cannabis_classifier import CannabisDocumentClassifier, PriorityLevel
from automation_workflows import AutomationWorkflows
from sample_documents import get_sample_documents, save_sample_documents_to_files


class CannabisDocumentIntelligenceSystem:
    def __init__(self):
        self.classifier = CannabisDocumentClassifier()
        self.automation = AutomationWorkflows()
        
    def run_complete_analysis(self, documents: Dict[str, str] | None = None) -> Dict:
        """
        Run the complete document analysis and automation workflow.
        
        Args:
            documents: Dictionary of document names to content. If None, uses sample documents.
            
        Returns:
            Dictionary containing all results and reports
        """
        print("🌿 Cannabis Document Intelligence System")
        print("=" * 50)
        
        # Use sample documents if none provided
        if documents is None:
            print("Using sample municipal documents for analysis...")
            documents = get_sample_documents()
            save_sample_documents_to_files()
        
        print(f"Processing {len(documents)} documents...")
        
        # Step 1: Classify all documents
        print("\n📊 Step 1: Document Classification")
        print("-" * 30)
        classification_results = self.classifier.process_documents(documents)
        
        # Display individual results
        for result in classification_results:
            emoji = {
                PriorityLevel.HIGH_PRIORITY: "🔴",
                PriorityLevel.MEDIUM_PRIORITY: "🟡", 
                PriorityLevel.LOW_PRIORITY: "🟢",
                PriorityLevel.IRRELEVANT: "⚪"
            }[result.classification]
            
            print(f"{emoji} {result.document_name}")
            print(f"   Score: {result.score} | Classification: {result.classification.value}")
            print(f"   Reasoning: {result.reasoning}")
            if result.key_phrases:
                print(f"   Key Phrases: {', '.join(result.key_phrases[:3])}")
            print()
        
        # Step 2: Generate summary report
        print("\n📋 Step 2: Summary Report")
        print("-" * 30)
        summary_report = self.classifier.generate_summary_report(classification_results)
        print(summary_report)
        
        # Step 3: Execute automation workflows
        print("\n🤖 Step 3: Automation Workflows")
        print("-" * 30)
        automation_results = self.automation.process_automation_workflows(classification_results)
        
        # Step 4: Generate automation report
        print("\n📈 Step 4: Automation Report")
        print("-" * 30)
        automation_report = self.automation.generate_automation_report(classification_results)
        print(automation_report)
        
        # Step 5: Export results
        print("\n💾 Step 5: Exporting Results")
        print("-" * 30)
        
        # Export classification results
        classification_file = self.classifier.export_results(classification_results)
        print(f"✅ Classification results saved to: {classification_file}")
        
        # Export automation results
        automation_file = "automation_results.json"
        print(f"✅ Automation results saved to: {automation_file}")
        
        # Save summary reports
        with open("summary_report.txt", 'w') as f:
            f.write(summary_report)
        print("✅ Summary report saved to: summary_report.txt")
        
        with open("automation_report.txt", 'w') as f:
            f.write(automation_report)
        print("✅ Automation report saved to: automation_report.txt")
        
        # Return comprehensive results
        return {
            "classification_results": classification_results,
            "automation_results": automation_results,
            "summary_report": summary_report,
            "automation_report": automation_report,
            "files_generated": [
                classification_file,
                automation_file,
                "summary_report.txt",
                "automation_report.txt",
                "automation_log.json"
            ]
        }
    
    def analyze_single_document(self, document_name: str, content: str) -> Dict:
        """
        Analyze a single document and return detailed results.
        
        Args:
            document_name: Name of the document
            content: Document content
            
        Returns:
            Dictionary with classification result and automation workflow
        """
        print(f"🔍 Analyzing single document: {document_name}")
        
        # Classify document
        result = self.classifier.classify_document(content, document_name)
        
        # Execute appropriate automation workflow
        if result.classification == PriorityLevel.HIGH_PRIORITY:
            automation_result = self.automation.send_slack_alert(result)
        elif result.classification == PriorityLevel.MEDIUM_PRIORITY:
            automation_result = self.automation.send_weekly_digest([result])
        elif result.classification == PriorityLevel.LOW_PRIORITY:
            automation_result = self.automation.log_low_priority([result])
        else:
            automation_result = {"status": "ignored", "reason": "Document classified as irrelevant"}
        
        return {
            "document_name": document_name,
            "classification_result": result,
            "automation_result": automation_result
        }
    
    def get_methodology_explanation(self) -> str:
        """
        Return detailed explanation of the classification methodology.
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
        return methodology


def main():
    """Main function to run the cannabis document intelligence system."""
    system = CannabisDocumentIntelligenceSystem()
    
    # Run complete analysis with sample documents
    results = system.run_complete_analysis()
    
    # Display methodology
    print("\n📚 Methodology Explanation")
    print("=" * 50)
    methodology = system.get_methodology_explanation()
    print(methodology)
    
    # Save methodology to file
    with open("methodology.txt", 'w') as f:
        f.write(methodology)
    print("✅ Methodology saved to: methodology.txt")
    
    print("\n🎉 Analysis Complete!")
    print("=" * 50)
    print("Files generated:")
    for file in results["files_generated"]:
        print(f"  - {file}")
    print("  - methodology.txt")
    
    print("\n📊 Summary:")
    total_docs = len(results["classification_results"])
    high_priority = len([r for r in results["classification_results"] if r.classification == PriorityLevel.HIGH_PRIORITY])
    medium_priority = len([r for r in results["classification_results"] if r.classification == PriorityLevel.MEDIUM_PRIORITY])
    low_priority = len([r for r in results["classification_results"] if r.classification == PriorityLevel.LOW_PRIORITY])
    irrelevant = len([r for r in results["classification_results"] if r.classification == PriorityLevel.IRRELEVANT])
    
    print(f"  Total Documents: {total_docs}")
    print(f"  High Priority: {high_priority}")
    print(f"  Medium Priority: {medium_priority}")
    print(f"  Low Priority: {low_priority}")
    print(f"  Irrelevant: {irrelevant}")


if __name__ == "__main__":
    main() 
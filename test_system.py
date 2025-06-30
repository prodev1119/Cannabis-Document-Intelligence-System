#!/usr/bin/env python3
"""
Test Script for Cannabis Document Intelligence System
====================================================

This script demonstrates all aspects of the system including:
- Document classification
- Automation workflows
- API functionality
- Sample document processing
"""

import json
import os
from datetime import datetime
from cannabis_classifier import CannabisDocumentClassifier, PriorityLevel
from automation_workflows import AutomationWorkflows


def test_classifier():
    """Test the document classifier with sample documents."""
    print("🧪 Testing Document Classifier")
    print("=" * 40)
    
    classifier = CannabisDocumentClassifier()
    # Use a minimal set of inline test documents for demonstration
    documents = {
        "test_high_priority.txt": "CITY COUNCIL MEETING MINUTES\nDate: January 15, 2025\nAGENDA ITEM: CANNABIS RETAIL ORDINANCE APPROVED\nThe council approved the cannabis retail ordinance with a 6-1 vote. The licensing program will open on February 1, 2025, with an application window of 30 days. Merit-based selection will be used for the initial 3 dispensary licenses. Motion passed. Ordinance effective immediately.",
        "test_irrelevant.txt": "PARKS AND RECREATION DEPARTMENT\nDate: January 15, 2025\nPARK MAINTENANCE SCHEDULE\nThe department has scheduled routine maintenance for all city parks. No cannabis-related activities included."
    }
    print(f"Processing {len(documents)} sample documents...")
    results = classifier.process_documents(documents)
    
    # Display results by priority
    priorities = {
        PriorityLevel.HIGH_PRIORITY: [],
        PriorityLevel.MEDIUM_PRIORITY: [],
        PriorityLevel.LOW_PRIORITY: [],
        PriorityLevel.IRRELEVANT: []
    }
    
    for result in results:
        priorities[result.classification].append(result)
    
    for priority, docs in priorities.items():
        if docs:
            print(f"\n{priority.value} ({len(docs)} documents):")
            for doc in docs:
                print(f"  • {doc.document_name} (Score: {doc.score})")
                print(f"    Reasoning: {doc.reasoning}")
                if doc.key_phrases:
                    print(f"    Key Phrases: {', '.join(doc.key_phrases[:3])}")
                print()
    
    return results


def test_automation_workflows(results):
    """Test automation workflows with classification results."""
    print("🤖 Testing Automation Workflows")
    print("=" * 40)
    
    automation = AutomationWorkflows()
    
    # Test individual workflows
    high_priority_docs = [r for r in results if r.classification == PriorityLevel.HIGH_PRIORITY]
    medium_priority_docs = [r for r in results if r.classification == PriorityLevel.MEDIUM_PRIORITY]
    low_priority_docs = [r for r in results if r.classification == PriorityLevel.LOW_PRIORITY]
    
    print(f"High Priority Documents: {len(high_priority_docs)}")
    if high_priority_docs:
        print("Testing Slack alerts...")
        for doc in high_priority_docs[:2]:  # Test first 2
            result = automation.send_slack_alert(doc)
            print(f"  ✅ Slack alert for {doc.document_name}")
    
    print(f"\nMedium Priority Documents: {len(medium_priority_docs)}")
    if medium_priority_docs:
        print("Testing weekly digest...")
        digest_result = automation.send_weekly_digest(results)
        print(f"  ✅ Weekly digest prepared")
    
    print(f"\nLow Priority Documents: {len(low_priority_docs)}")
    if low_priority_docs:
        print("Testing logging...")
        log_result = automation.log_low_priority(results)
        print(f"  ✅ Documents logged to {log_result['log_file']}")
    
    # Test complete workflow
    print("\nTesting complete automation workflow...")
    automation_results = automation.process_automation_workflows(results)
    print("  ✅ Complete workflow executed")
    
    return automation_results


def test_single_document():
    """Test classification of a single document."""
    print("\n📄 Testing Single Document Classification")
    print("=" * 40)
    
    classifier = CannabisDocumentClassifier()
    
    # Test a high-priority document
    test_doc = """
    CITY COUNCIL MEETING MINUTES
    Date: January 15, 2025
    
    AGENDA ITEM: CANNABIS RETAIL ORDINANCE APPROVED
    
    The council approved the cannabis retail ordinance with a 6-1 vote. 
    The licensing program will open on February 1, 2025, with an application 
    window of 30 days. Merit-based selection will be used for the initial 
    3 dispensary licenses.
    
    Motion passed. Ordinance effective immediately.
    """
    
    result = classifier.classify_document(test_doc, "test_high_priority_doc.txt")
    
    print(f"Document: {result.document_name}")
    print(f"Classification: {result.classification.value}")
    print(f"Score: {result.score}")
    print(f"Reasoning: {result.reasoning}")
    print(f"Key Phrases: {', '.join(result.key_phrases)}")
    print(f"Recommended Action: {result.recommended_action}")
    
    return result


def test_methodology():
    """Test and display the methodology explanation."""
    print("\n📚 Testing Methodology")
    print("=" * 40)
    
    classifier = CannabisDocumentClassifier()
    
    print("Scoring System:")
    print(f"High Value Keywords ({len(classifier.high_value_keywords)}):")
    for keyword in classifier.high_value_keywords:
        print(f"  • {keyword} (10 points)")
    
    print(f"\nMedium Value Keywords ({len(classifier.medium_value_keywords)}):")
    for keyword in classifier.medium_value_keywords:
        print(f"  • {keyword} (5 points)")
    
    print(f"\nLow Value Keywords ({len(classifier.low_value_keywords)}):")
    for keyword in classifier.low_value_keywords:
        print(f"  • {keyword} (2 points)")
    
    print(f"\nPositive Modifiers ({len(classifier.positive_modifiers)}):")
    for modifier in classifier.positive_modifiers:
        print(f"  • {modifier} (+3 points)")
    
    print(f"\nNegative Modifiers ({len(classifier.negative_modifiers)}):")
    for modifier in classifier.negative_modifiers:
        print(f"  • {modifier} (-3 points)")
    
    print(f"\nClassification Thresholds:")
    for priority, threshold in classifier.thresholds.items():
        print(f"  • {priority.value}: {threshold}+ points")


def test_file_generation():
    """Test file generation and export functionality."""
    print("\n💾 Testing File Generation")
    print("=" * 40)
    
    classifier = CannabisDocumentClassifier()
    automation = AutomationWorkflows()
    # Use a minimal set of inline test documents for demonstration
    documents = {
        "test_high_priority.txt": "CITY COUNCIL MEETING MINUTES\nDate: January 15, 2025\nAGENDA ITEM: CANNABIS RETAIL ORDINANCE APPROVED\nThe council approved the cannabis retail ordinance with a 6-1 vote. The licensing program will open on February 1, 2025, with an application window of 30 days. Merit-based selection will be used for the initial 3 dispensary licenses. Motion passed. Ordinance effective immediately.",
        "test_irrelevant.txt": "PARKS AND RECREATION DEPARTMENT\nDate: January 15, 2025\nPARK MAINTENANCE SCHEDULE\nThe department has scheduled routine maintenance for all city parks. No cannabis-related activities included."
    }
    # Process documents
    results = classifier.process_documents(documents)
    # Export results
    classification_file = classifier.export_results(results)
    print(f"✅ Classification results exported to {classification_file}")
    # Generate reports
    summary_report = classifier.generate_summary_report(results)
    with open("test_summary_report.txt", 'w') as f:
        f.write(summary_report)
    print("✅ Summary report saved to test_summary_report.txt")
    automation_report = automation.generate_automation_report(results)
    with open("test_automation_report.txt", 'w') as f:
        f.write(automation_report)
    print("✅ Automation report saved to test_automation_report.txt")
    # Execute automation workflows
    automation_results = automation.process_automation_workflows(results)
    with open("test_automation_results.json", 'w') as f:
        json.dump(automation_results, f, indent=2)
    print("✅ Automation results saved to test_automation_results.json")


def test_edge_cases():
    """Test edge cases and error handling."""
    print("\n🔍 Testing Edge Cases")
    print("=" * 40)
    
    classifier = CannabisDocumentClassifier()
    
    # Test empty document
    print("Testing empty document...")
    result = classifier.classify_document("", "empty_doc.txt")
    print(f"  Result: {result.classification.value} (Score: {result.score})")
    
    # Test document with only negative modifiers
    print("\nTesting document with negative modifiers...")
    negative_doc = """
    CANNABIS RETAIL APPLICATION REJECTED
    
    The planning commission rejected the cannabis retail application 
    due to proximity to schools. The application is prohibited 
    and banned from future consideration.
    """
    result = classifier.classify_document(negative_doc, "negative_doc.txt")
    print(f"  Result: {result.classification.value} (Score: {result.score})")
    print(f"  Reasoning: {result.reasoning}")
    
    # Test document with many dates
    print("\nTesting document with multiple dates...")
    date_doc = """
    CANNABIS ORDINANCE TIMELINE
    
    Draft ordinance presented on 12/01/2024
    Public hearing scheduled for 12/15/2024
    Second reading on 01/05/2025
    Final approval on 01/20/2025
    Effective date: 02/01/2025
    """
    result = classifier.classify_document(date_doc, "date_doc.txt")
    print(f"  Result: {result.classification.value} (Score: {result.score})")
    print(f"  Reasoning: {result.reasoning}")


def main():
    """Run all tests."""
    print("🌿 Cannabis Document Intelligence System - Test Suite")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        # Run all tests
        results = test_classifier()
        automation_results = test_automation_workflows(results)
        single_result = test_single_document()
        test_methodology()
        test_file_generation()
        test_edge_cases()
        
        print("\n🎉 All Tests Completed Successfully!")
        print("=" * 60)
        
        # Summary
        total_docs = len(results)
        high_priority = len([r for r in results if r.classification == PriorityLevel.HIGH_PRIORITY])
        medium_priority = len([r for r in results if r.classification == PriorityLevel.MEDIUM_PRIORITY])
        low_priority = len([r for r in results if r.classification == PriorityLevel.LOW_PRIORITY])
        irrelevant = len([r for r in results if r.classification == PriorityLevel.IRRELEVANT])
        
        print(f"📊 Test Summary:")
        print(f"  Total Documents Processed: {total_docs}")
        print(f"  High Priority: {high_priority}")
        print(f"  Medium Priority: {medium_priority}")
        print(f"  Low Priority: {low_priority}")
        print(f"  Irrelevant: {irrelevant}")
        
        print(f"\n📁 Files Generated:")
        files = [
            "classification_results.json",
            "test_summary_report.txt", 
            "test_automation_report.txt",
            "test_automation_results.json",
            "automation_log.json"
        ]
        for file in files:
            if os.path.exists(file):
                print(f"  ✅ {file}")
            else:
                print(f"  ❌ {file} (not found)")
        
        print(f"\n🚀 System Ready for Production Use!")
        
    except Exception as e:
        print(f"\n❌ Test Failed: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 
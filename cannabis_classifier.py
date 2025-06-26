import re
import json
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum
# import pandas as pd


class PriorityLevel(Enum):
    HIGH_PRIORITY = "HIGH_PRIORITY"
    MEDIUM_PRIORITY = "MEDIUM_PRIORITY"
    LOW_PRIORITY = "LOW_PRIORITY"
    IRRELEVANT = "IRRELEVANT"


@dataclass
class ClassificationResult:
    classification: PriorityLevel
    score: int
    reasoning: str
    key_phrases: List[str]
    recommended_action: str
    document_name: str
    processed_at: datetime


class CannabisDocumentClassifier:
    def __init__(self):
        # High value keywords (10 points each)
        self.high_value_keywords = [
            "cannabis retail", "dispensary license", "application window",
            "ordinance approved", "licensing program", "application period",
            "merit-based selection", "conditional use permit approved", "second reading"
        ]
        
        # Medium value keywords (5 points each)
        self.medium_value_keywords = [
            "public hearing", "planning commission", "draft ordinance", 
            "zoning amendment", "social equity", "moratorium lifted", 
            "cannabis business", "study session"
        ]
        
        # Low value keywords (2 points each)
        self.low_value_keywords = [
            "cannabis", "marijuana", "dispensary", "retail", "tax revenue", 
            "budget discussion", "general mention"
        ]
        
        # Context modifiers
        self.positive_modifiers = ["approved", "passed", "effective", "final"]
        self.negative_modifiers = ["prohibited", "banned", "rejected"]
        
        # Scoring thresholds
        self.thresholds = {
            PriorityLevel.HIGH_PRIORITY: 70,
            PriorityLevel.MEDIUM_PRIORITY: 30,
            PriorityLevel.LOW_PRIORITY: 10
        }

    def extract_dates(self, text: str) -> List[datetime]:
        """Extract dates from text and return list of datetime objects."""
        # Common date patterns
        date_patterns = [
            r'\b\d{1,2}/\d{1,2}/\d{4}\b',  # MM/DD/YYYY
            r'\b\d{4}-\d{1,2}-\d{1,2}\b',  # YYYY-MM-DD
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',  # Month DD, YYYY
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    if '/' in match:
                        date_obj = datetime.strptime(match, '%m/%d/%Y')
                    elif '-' in match:
                        date_obj = datetime.strptime(match, '%Y-%m-%d')
                    else:
                        # Handle "Month DD, YYYY" format
                        date_obj = datetime.strptime(match, '%B %d, %Y')
                    dates.append(date_obj)
                except ValueError:
                    continue
        
        return dates

    def calculate_date_bonus(self, text: str) -> int:
        """Calculate bonus points for dates within 90 days."""
        dates = self.extract_dates(text)
        current_date = datetime.now()
        bonus = 0
        
        for date in dates:
            days_diff = abs((date - current_date).days)
            if days_diff <= 90:
                bonus += 5
        
        return bonus

    def check_title_heading_bonus(self, text: str, document_name: str) -> int:
        """Check if keywords appear in title or section headings."""
        bonus = 0
        
        # Split into lines and check first few lines for headings
        lines = text.split('\n')[:10]  # Check first 10 lines
        
        for line in lines:
            line_lower = line.lower().strip()
            if line_lower and len(line_lower) < 100:  # Likely a heading
                for keyword in self.high_value_keywords + self.medium_value_keywords:
                    if keyword.lower() in line_lower:
                        bonus += 2
                        break
        
        # Check document name
        doc_name_lower = document_name.lower()
        for keyword in self.high_value_keywords + self.medium_value_keywords:
            if keyword.lower() in doc_name_lower:
                bonus += 2
                break
        
        return bonus

    def classify_document(self, text: str, document_name: str = "unknown") -> ClassificationResult:
        """Classify a document based on cannabis business relevance."""
        text_lower = text.lower()
        score = 0
        key_phrases = []
        
        # Score high value keywords
        for keyword in self.high_value_keywords:
            if keyword.lower() in text_lower:
                score += 10
                key_phrases.append(keyword)
        
        # Score medium value keywords
        for keyword in self.medium_value_keywords:
            if keyword.lower() in text_lower:
                score += 5
                key_phrases.append(keyword)
        
        # Score low value keywords
        for keyword in self.low_value_keywords:
            if keyword.lower() in text_lower:
                score += 2
                key_phrases.append(keyword)
        
        # Apply context modifiers
        for modifier in self.positive_modifiers:
            if modifier.lower() in text_lower:
                score += 3
        
        for modifier in self.negative_modifiers:
            if modifier.lower() in text_lower:
                score -= 3
        
        # Date bonus
        date_bonus = self.calculate_date_bonus(text)
        score += date_bonus
        
        # Title/heading bonus
        title_bonus = self.check_title_heading_bonus(text, document_name)
        score += title_bonus
        
        # Determine classification
        if score >= self.thresholds[PriorityLevel.HIGH_PRIORITY]:
            classification = PriorityLevel.HIGH_PRIORITY
            recommended_action = "immediate_follow_up"
        elif score >= self.thresholds[PriorityLevel.MEDIUM_PRIORITY]:
            classification = PriorityLevel.MEDIUM_PRIORITY
            recommended_action = "weekly_digest"
        elif score >= self.thresholds[PriorityLevel.LOW_PRIORITY]:
            classification = PriorityLevel.LOW_PRIORITY
            recommended_action = "log_only"
        else:
            classification = PriorityLevel.IRRELEVANT
            recommended_action = "ignore"
        
        # Generate reasoning
        reasoning_parts = []
        if key_phrases:
            reasoning_parts.append(f"Found key phrases: {', '.join(key_phrases[:3])}")
        if date_bonus > 0:
            reasoning_parts.append(f"Recent dates detected (+{date_bonus} points)")
        if title_bonus > 0:
            reasoning_parts.append(f"Keywords in headings (+{title_bonus} points)")
        
        reasoning = "; ".join(reasoning_parts) if reasoning_parts else "Limited cannabis relevance"
        
        return ClassificationResult(
            classification=classification,
            score=score,
            reasoning=reasoning,
            key_phrases=key_phrases,
            recommended_action=recommended_action,
            document_name=document_name,
            processed_at=datetime.now()
        )

    def process_documents(self, documents: Dict[str, str]) -> List[ClassificationResult]:
        """Process multiple documents and return classification results."""
        results = []
        for doc_name, content in documents.items():
            result = self.classify_document(content, doc_name)
            results.append(result)
        return results

    def export_results(self, results: List[ClassificationResult], filename: str = "classification_results.json"):
        """Export results to JSON file."""
        data = []
        for result in results:
            data.append({
                "document_name": result.document_name,
                "classification": result.classification.value,
                "score": result.score,
                "reasoning": result.reasoning,
                "key_phrases": result.key_phrases,
                "recommended_action": result.recommended_action,
                "processed_at": result.processed_at.isoformat()
            })
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        return filename

    def generate_summary_report(self, results: List[ClassificationResult]) -> str:
        """Generate a summary report of all classifications."""
        summary = {
            "total_documents": len(results),
            "high_priority": len([r for r in results if r.classification == PriorityLevel.HIGH_PRIORITY]),
            "medium_priority": len([r for r in results if r.classification == PriorityLevel.MEDIUM_PRIORITY]),
            "low_priority": len([r for r in results if r.classification == PriorityLevel.LOW_PRIORITY]),
            "irrelevant": len([r for r in results if r.classification == PriorityLevel.IRRELEVANT]),
            "average_score": sum(r.score for r in results) / len(results) if results else 0
        }
        
        report = f"""
Cannabis Document Classification Summary
=======================================
Total Documents Processed: {summary['total_documents']}
High Priority: {summary['high_priority']}
Medium Priority: {summary['medium_priority']}
Low Priority: {summary['low_priority']}
Irrelevant: {summary['irrelevant']}
Average Score: {summary['average_score']:.1f}

High Priority Documents:
"""
        
        high_priority_docs = [r for r in results if r.classification == PriorityLevel.HIGH_PRIORITY]
        for doc in high_priority_docs:
            report += f"- {doc.document_name} (Score: {doc.score}) - {doc.reasoning}\n"
        
        return report 
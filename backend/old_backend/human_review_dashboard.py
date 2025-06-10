#!/usr/bin/env python3
"""
Human Review Dashboard for AI Research Results
Provides interface for reviewing low-confidence answers and adding human insights
"""

import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
import os

logger = logging.getLogger(__name__)

class HumanReviewDashboard:
    """
    Dashboard for human review of AI research results
    """
    
    def __init__(self, review_output_dir: str = "human_review_output"):
        self.review_output_dir = Path(review_output_dir)
        self.review_output_dir.mkdir(exist_ok=True)
        
        # Review status tracking
        self.review_status = {
            'pending': [],
            'in_review': [],
            'completed': [],
            'escalated': []
        }
        
        logger.info(f"Human Review Dashboard initialized - output: {self.review_output_dir}")
    
    def process_research_results(self, research_results: List[Dict]) -> Dict:
        """
        Process research results and identify items requiring human review
        """
        review_summary = {
            'total_subnets': len(research_results),
            'subnets_requiring_review': 0,
            'total_items_for_review': 0,
            'high_priority_items': 0,
            'review_categories': {
                'low_confidence_answers': 0,
                'red_flags_detected': 0,
                'no_data_answers': 0,
                'conflicting_information': 0
            },
            'review_queue': []
        }
        
        for subnet_results in research_results:
            if subnet_results.get('research_status') != 'completed':
                continue
                
            # Check if human review is required
            metadata = subnet_results.get('analysis_metadata', {})
            if not metadata.get('human_review_required', False):
                continue
            
            review_summary['subnets_requiring_review'] += 1
            
            # Process subnet for review
            subnet_review_items = self._extract_review_items(subnet_results)
            
            if subnet_review_items:
                review_summary['total_items_for_review'] += len(subnet_review_items)
                review_summary['review_queue'].append({
                    'subnet_netuid': subnet_results['subnet_netuid'],
                    'subnet_name': subnet_results['subnet_name'],
                    'review_items': subnet_review_items,
                    'priority': self._calculate_review_priority(subnet_results),
                    'estimated_review_time': self._estimate_review_time(subnet_review_items)
                })
                
                # Count categories
                for item in subnet_review_items:
                    category = item['review_category']
                    if category in review_summary['review_categories']:
                        review_summary['review_categories'][category] += 1
                    
                    if item['priority'] == 'high':
                        review_summary['high_priority_items'] += 1
        
        # Sort review queue by priority
        review_summary['review_queue'].sort(
            key=lambda x: (x['priority'] == 'high', x['priority'] == 'medium'), 
            reverse=True
        )
        
        # Save review summary
        self._save_review_summary(review_summary)
        
        return review_summary
    
    def _extract_review_items(self, subnet_results: Dict) -> List[Dict]:
        """
        Extract specific items that need human review from subnet results
        """
        review_items = []
        
        # Process each answer category
        for category_key, category_answers in subnet_results.get('answers', {}).items():
            for question_key, answer_data in category_answers.items():
                
                # Check if this answer needs review
                if not answer_data.get('human_review_required', False):
                    continue
                
                # Determine review category and priority
                review_category = self._categorize_review_need(answer_data)
                priority = self._determine_priority(answer_data, subnet_results)
                
                review_item = {
                    'category': category_key,
                    'question_key': question_key,
                    'question': answer_data['question'],
                    'ai_answer': answer_data['answer'],
                    'confidence_level': answer_data['confidence_level'],
                    'evidence_quality': answer_data['evidence_quality'],
                    'evidence_sources': answer_data.get('evidence_sources', []),
                    'red_flags': answer_data.get('red_flags', []),
                    'additional_notes': answer_data.get('additional_notes', ''),
                    'review_category': review_category,
                    'priority': priority,
                    'review_status': 'pending',
                    'human_input': {
                        'revised_answer': '',
                        'confidence_adjustment': '',
                        'additional_evidence': [],
                        'reviewer_notes': '',
                        'action_required': False,
                        'escalate': False
                    },
                    'review_metadata': {
                        'created_at': datetime.now().isoformat(),
                        'reviewer_id': '',
                        'review_started_at': '',
                        'review_completed_at': '',
                        'time_spent_minutes': 0
                    }
                }
                
                review_items.append(review_item)
        
        return review_items
    
    def _categorize_review_need(self, answer_data: Dict) -> str:
        """
        Categorize why this answer needs human review
        """
        confidence = answer_data.get('confidence_level', 'MEDIUM')
        red_flags = answer_data.get('red_flags', [])
        answer = answer_data.get('answer', '').lower()
        
        if red_flags:
            return 'red_flags_detected'
        elif confidence == 'NO_DATA':
            return 'no_data_answers'
        elif confidence == 'LOW':
            return 'low_confidence_answers'
        elif 'not available' in answer or 'conflicting' in answer:
            return 'conflicting_information'
        else:
            return 'low_confidence_answers'
    
    def _determine_priority(self, answer_data: Dict, subnet_results: Dict) -> str:
        """
        Determine review priority for this item
        """
        red_flags = answer_data.get('red_flags', [])
        confidence = answer_data.get('confidence_level', 'MEDIUM')
        evidence_quality = answer_data.get('evidence_quality', 'FAIR')
        
        # High priority conditions
        if red_flags:
            return 'high'
        if confidence == 'NO_DATA' and evidence_quality == 'POOR':
            return 'high'
        
        # Medium priority conditions  
        if confidence == 'LOW':
            return 'medium'
        if evidence_quality == 'POOR':
            return 'medium'
        
        return 'low'
    
    def _calculate_review_priority(self, subnet_results: Dict) -> str:
        """
        Calculate overall review priority for a subnet
        """
        metadata = subnet_results.get('analysis_metadata', {})
        red_flags = metadata.get('red_flags_detected', [])
        overall_confidence = metadata.get('overall_confidence', 'MEDIUM')
        
        if red_flags or overall_confidence == 'LOW':
            return 'high'
        elif overall_confidence == 'MEDIUM':
            return 'medium'
        else:
            return 'low'
    
    def _estimate_review_time(self, review_items: List[Dict]) -> int:
        """
        Estimate review time in minutes
        """
        base_time_per_item = 5  # 5 minutes per item
        
        total_time = 0
        for item in review_items:
            time_estimate = base_time_per_item
            
            # Adjust based on priority
            if item['priority'] == 'high':
                time_estimate *= 2
            elif item['priority'] == 'low':
                time_estimate *= 0.5
            
            # Adjust based on review category
            if item['review_category'] == 'red_flags_detected':
                time_estimate *= 1.5
            elif item['review_category'] == 'no_data_answers':
                time_estimate *= 2  # May need research
            
            total_time += time_estimate
        
        return int(total_time)
    
    def generate_review_worksheet(self, subnet_netuid: int) -> Dict:
        """
        Generate a structured worksheet for reviewing a specific subnet
        """
        # Load review queue
        review_summary = self._load_review_summary()
        
        # Find subnet in review queue
        subnet_review = None
        for item in review_summary.get('review_queue', []):
            if item['subnet_netuid'] == subnet_netuid:
                subnet_review = item
                break
        
        if not subnet_review:
            raise ValueError(f"Subnet {subnet_netuid} not found in review queue")
        
        # Create worksheet
        worksheet = {
            'subnet_info': {
                'netuid': subnet_review['subnet_netuid'],
                'name': subnet_review['subnet_name'],
                'priority': subnet_review['priority'],
                'estimated_time': subnet_review['estimated_review_time']
            },
            'review_instructions': self._generate_review_instructions(subnet_review),
            'review_items': subnet_review['review_items'],
            'review_checklist': [
                "Review all flagged items thoroughly",
                "Verify AI confidence assessments",
                "Add missing information where possible",
                "Flag items requiring escalation",
                "Provide final recommendation"
            ],
            'worksheet_metadata': {
                'generated_at': datetime.now().isoformat(),
                'status': 'ready_for_review',
                'reviewer_assigned': '',
                'deadline': ''
            }
        }
        
        # Save worksheet
        worksheet_path = self.review_output_dir / f"worksheet_subnet_{subnet_netuid}.json"
        with open(worksheet_path, 'w') as f:
            json.dump(worksheet, f, indent=2)
        
        logger.info(f"Review worksheet generated for subnet {subnet_netuid}: {worksheet_path}")
        
        return worksheet
    
    def _generate_review_instructions(self, subnet_review: Dict) -> List[str]:
        """
        Generate specific review instructions based on the subnet's issues
        """
        instructions = []
        
        review_items = subnet_review['review_items']
        
        # Count issue types
        red_flag_items = [item for item in review_items if item['review_category'] == 'red_flags_detected']
        no_data_items = [item for item in review_items if item['review_category'] == 'no_data_answers']
        low_conf_items = [item for item in review_items if item['review_category'] == 'low_confidence_answers']
        
        if red_flag_items:
            instructions.append(f"🚨 PRIORITY: {len(red_flag_items)} red flags detected - investigate immediately")
            instructions.append("   - Verify each red flag claim with external sources")
            instructions.append("   - Determine if red flags are deal-breakers or manageable risks")
        
        if no_data_items:
            instructions.append(f"📊 DATA GAPS: {len(no_data_items)} questions have no data")
            instructions.append("   - Search for additional sources (social media, news, forums)")
            instructions.append("   - Mark as 'information unavailable' if genuinely no data exists")
        
        if low_conf_items:
            instructions.append(f"🔍 VERIFICATION: {len(low_conf_items)} low-confidence answers")
            instructions.append("   - Cross-reference with multiple sources")
            instructions.append("   - Upgrade confidence if evidence supports AI answer")
        
        # Priority-specific instructions
        if subnet_review['priority'] == 'high':
            instructions.append("⚡ HIGH PRIORITY REVIEW - Complete within 24 hours")
        
        return instructions
    
    def process_completed_review(self, subnet_netuid: int, completed_worksheet: Dict) -> Dict:
        """
        Process a completed review worksheet and integrate human insights
        """
        # Validate worksheet
        if completed_worksheet['worksheet_metadata']['status'] != 'completed':
            raise ValueError("Worksheet is not marked as completed")
        
        # Process each reviewed item
        processed_results = {
            'subnet_netuid': subnet_netuid,
            'review_completed_at': datetime.now().isoformat(),
            'reviewer_id': completed_worksheet['worksheet_metadata'].get('reviewer_assigned', 'unknown'),
            'total_review_time': sum(item['review_metadata']['time_spent_minutes'] 
                                   for item in completed_worksheet['review_items']),
            'items_processed': len(completed_worksheet['review_items']),
            'confidence_improvements': 0,
            'escalated_items': 0,
            'final_recommendation': completed_worksheet.get('final_recommendation', ''),
            'enhanced_answers': {}
        }
        
        # Process individual items
        for item in completed_worksheet['review_items']:
            human_input = item['human_input']
            
            # Check for improvements
            if human_input.get('revised_answer'):
                processed_results['confidence_improvements'] += 1
            
            if human_input.get('escalate'):
                processed_results['escalated_items'] += 1
            
            # Store enhanced answer
            category = item['category']
            question_key = item['question_key']
            
            if category not in processed_results['enhanced_answers']:
                processed_results['enhanced_answers'][category] = {}
            
            processed_results['enhanced_answers'][category][question_key] = {
                'original_ai_answer': item['ai_answer'],
                'original_confidence': item['confidence_level'],
                'human_revised_answer': human_input.get('revised_answer', ''),
                'final_confidence': human_input.get('confidence_adjustment', item['confidence_level']),
                'additional_evidence': human_input.get('additional_evidence', []),
                'reviewer_notes': human_input.get('reviewer_notes', ''),
                'requires_action': human_input.get('action_required', False),
                'escalated': human_input.get('escalate', False)
            }
        
        # Save processed results
        results_path = self.review_output_dir / f"processed_review_subnet_{subnet_netuid}.json"
        with open(results_path, 'w') as f:
            json.dump(processed_results, f, indent=2)
        
        logger.info(f"Processed review results saved: {results_path}")
        
        return processed_results
    
    def generate_review_report(self, timeframe_days: int = 7) -> Dict:
        """
        Generate summary report of review activities
        """
        # Scan for completed reviews
        completed_reviews = []
        for file_path in self.review_output_dir.glob("processed_review_subnet_*.json"):
            try:
                with open(file_path, 'r') as f:
                    review_data = json.load(f)
                    completed_reviews.append(review_data)
            except Exception as e:
                logger.error(f"Error loading review file {file_path}: {e}")
        
        # Generate report
        report = {
            'report_generated_at': datetime.now().isoformat(),
            'timeframe_days': timeframe_days,
            'summary': {
                'total_reviews_completed': len(completed_reviews),
                'total_items_reviewed': sum(r['items_processed'] for r in completed_reviews),
                'total_review_time_hours': sum(r['total_review_time'] for r in completed_reviews) / 60,
                'confidence_improvements': sum(r['confidence_improvements'] for r in completed_reviews),
                'escalated_items': sum(r['escalated_items'] for r in completed_reviews)
            },
            'reviewer_performance': {},
            'common_issues': {},
            'recommendations': []
        }
        
        # Analyze reviewer performance
        reviewer_stats = {}
        for review in completed_reviews:
            reviewer = review.get('reviewer_id', 'unknown')
            if reviewer not in reviewer_stats:
                reviewer_stats[reviewer] = {
                    'reviews_completed': 0,
                    'items_processed': 0,
                    'total_time_hours': 0,
                    'avg_time_per_item': 0
                }
            
            stats = reviewer_stats[reviewer]
            stats['reviews_completed'] += 1
            stats['items_processed'] += review['items_processed']
            stats['total_time_hours'] += review['total_review_time'] / 60
        
        # Calculate averages
        for reviewer, stats in reviewer_stats.items():
            if stats['items_processed'] > 0:
                stats['avg_time_per_item'] = stats['total_time_hours'] * 60 / stats['items_processed']
        
        report['reviewer_performance'] = reviewer_stats
        
        # Generate recommendations
        if report['summary']['escalated_items'] > 0:
            report['recommendations'].append("High number of escalated items - consider additional training")
        
        if report['summary']['total_review_time_hours'] > 40:
            report['recommendations'].append("Review process taking significant time - consider automation opportunities")
        
        # Save report
        report_path = self.review_output_dir / f"review_report_{datetime.now().strftime('%Y%m%d')}.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        return report
    
    def _save_review_summary(self, review_summary: Dict):
        """Save review summary to file"""
        summary_path = self.review_output_dir / "current_review_summary.json"
        with open(summary_path, 'w') as f:
            json.dump(review_summary, f, indent=2)
    
    def _load_review_summary(self) -> Dict:
        """Load review summary from file"""
        summary_path = self.review_output_dir / "current_review_summary.json"
        try:
            with open(summary_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

# CLI interface for human reviewers
def main():
    """CLI interface for human review dashboard"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Human Review Dashboard for AI Research")
    parser.add_argument('--action', choices=['process', 'worksheet', 'report'], 
                       required=True, help='Action to perform')
    parser.add_argument('--input-file', help='Input file with research results')
    parser.add_argument('--subnet-id', type=int, help='Subnet ID for worksheet generation')
    parser.add_argument('--output-dir', default='human_review_output', 
                       help='Output directory for review files')
    
    args = parser.parse_args()
    
    dashboard = HumanReviewDashboard(args.output_dir)
    
    if args.action == 'process':
        if not args.input_file:
            print("--input-file required for process action")
            return
        
        with open(args.input_file, 'r') as f:
            research_results = json.load(f)
        
        summary = dashboard.process_research_results(research_results)
        print(f"Review summary generated: {summary['total_items_for_review']} items need review")
    
    elif args.action == 'worksheet':
        if not args.subnet_id:
            print("--subnet-id required for worksheet action")
            return
        
        worksheet = dashboard.generate_review_worksheet(args.subnet_id)
        print(f"Review worksheet generated for subnet {args.subnet_id}")
    
    elif args.action == 'report':
        report = dashboard.generate_review_report()
        print(f"Review report generated: {report['summary']['total_reviews_completed']} reviews completed")

if __name__ == "__main__":
    main() 
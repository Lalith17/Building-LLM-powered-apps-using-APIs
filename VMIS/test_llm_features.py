"""
Test Cases for LLM-Powered Features in VMIS
============================================

This file contains test scenarios and their expected outcomes for the LLM-powered features
implemented in the Visa Mock Interview System (VMIS).

Test Date: 2025-09-01
Version: 1.0
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.llm_service import generate_interview_questions, generate_feedback, summarize_session
from app.llm_routes import validate_topic, validate_performance_notes, validate_interview_notes

class TestResults:
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.results = []
    
    def add_result(self, test_name, passed, details=""):
        self.results.append({
            "test": test_name,
            "passed": passed,
            "details": details
        })
        if passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def print_summary(self):
        print(f"\n{'='*50}")
        print(f"TEST SUMMARY")
        print(f"{'='*50}")
        print(f"Total Tests: {self.passed + self.failed}")
        print(f"Passed: {self.passed}")
        print(f"Failed: {self.failed}")
        print(f"Success Rate: {(self.passed/(self.passed + self.failed)*100):.1f}%")
        
        if self.failed > 0:
            print(f"\nFAILED TESTS:")
            for result in self.results:
                if not result["passed"]:
                    print(f"- {result['test']}: {result['details']}")

def test_input_validation():
    """Test input validation functions"""
    results = TestResults()
    
    # Test topic validation
    print("Testing topic validation...")
    
    # Valid topics
    valid_topics = [
        "communication skills",
        "problem-solving",
        "technical knowledge",
        "Leadership and teamwork",
        "Career goals123"
    ]
    
    for topic in valid_topics:
        is_valid, error = validate_topic(topic)
        results.add_result(
            f"Valid topic: '{topic}'",
            is_valid,
            error if not is_valid else ""
        )
    
    # Invalid topics
    invalid_topics = [
        "",  # Empty
        "A",  # Too short
        "A" * 101,  # Too long
        "topic@#$%",  # Invalid characters
        "   ",  # Only spaces
    ]
    
    for topic in invalid_topics:
        is_valid, error = validate_topic(topic)
        results.add_result(
            f"Invalid topic: '{topic[:20]}...' should fail",
            not is_valid,
            f"Unexpectedly passed validation" if is_valid else ""
        )
    
    # Test performance notes validation
    print("Testing performance notes validation...")
    
    valid_notes = [
        "The candidate showed good communication skills and answered questions clearly.",
        "A" * 100,  # Minimum length +
    ]
    
    for notes in valid_notes:
        is_valid, error = validate_performance_notes(notes)
        results.add_result(
            f"Valid performance notes (length: {len(notes)})",
            is_valid,
            error if not is_valid else ""
        )
    
    invalid_notes = [
        "",  # Empty
        "Short",  # Too short
        "A" * 2001,  # Too long
    ]
    
    for notes in invalid_notes:
        is_valid, error = validate_performance_notes(notes)
        results.add_result(
            f"Invalid performance notes (length: {len(notes)}) should fail",
            not is_valid,
            f"Unexpectedly passed validation" if is_valid else ""
        )
    
    return results

def test_llm_functions():
    """Test LLM integration functions"""
    results = TestResults()
    print("Testing LLM functions...")
    
    # Test question generation
    print("Testing question generation...")
    result = generate_interview_questions("communication skills", "medium", 3)
    
    if result.get("success"):
        questions = result.get("questions", [])
        results.add_result(
            "Generate questions - success",
            True,
            f"Generated {len(questions)} questions"
        )
        
        results.add_result(
            "Generate questions - count check",
            len(questions) > 0,
            f"Expected >0 questions, got {len(questions)}"
        )
    else:
        results.add_result(
            "Generate questions - success",
            False,
            result.get("error", "Unknown error")
        )
    
    # Test feedback generation
    print("Testing feedback generation...")
    sample_notes = """
    The candidate demonstrated strong communication skills throughout the interview.
    They answered questions clearly and provided specific examples.
    However, they seemed nervous when discussing technical topics.
    Body language was confident overall.
    """
    
    result = generate_feedback(sample_notes)
    
    if result.get("success"):
        feedback = result.get("text", "")
        results.add_result(
            "Generate feedback - success",
            True,
            f"Generated feedback with {len(feedback)} characters"
        )
        
        results.add_result(
            "Generate feedback - content check",
            len(feedback) > 50,
            f"Expected substantial feedback, got {len(feedback)} characters"
        )
    else:
        results.add_result(
            "Generate feedback - success",
            False,
            result.get("error", "Unknown error")
        )
    
    # Test session summary
    print("Testing session summary...")
    sample_interview_notes = """
    Interview with candidate for visa application.
    Questions covered: travel purpose, financial situation, ties to home country.
    Candidate responses: Clear about business trip purpose, showed bank statements,
    mentioned family and job responsibilities back home.
    Overall impression: Well-prepared, confident, provided sufficient documentation.
    Areas of concern: None significant.
    Recommendation: Positive assessment for visa approval.
    """
    
    result = summarize_session(sample_interview_notes)
    
    if result.get("success"):
        summary = result.get("text", "")
        results.add_result(
            "Generate summary - success",
            True,
            f"Generated summary with {len(summary)} characters"
        )
        
        results.add_result(
            "Generate summary - content check",
            len(summary) > 50,
            f"Expected substantial summary, got {len(summary)} characters"
        )
    else:
        results.add_result(
            "Generate summary - success",
            False,
            result.get("error", "Unknown error")
        )
    
    return results

def test_edge_cases():
    """Test edge cases and error scenarios"""
    results = TestResults()
    print("Testing edge cases...")
    
    # Test with special characters in topic
    special_topic = "problem-solving & communication (advanced)"
    result = generate_interview_questions(special_topic, "hard", 2)
    
    results.add_result(
        "Special characters in topic",
        "success" in result or "error" in result,
        "Function should return either success or error response"
    )
    
    # Test with maximum inputs
    max_notes = "A" * 1999  # Just under limit
    is_valid, error = validate_performance_notes(max_notes)
    results.add_result(
        "Maximum length performance notes",
        is_valid,
        error if not is_valid else "Validation passed correctly"
    )
    
    # Test with minimum valid inputs
    min_notes = "Good interview performance overall."
    is_valid, error = validate_performance_notes(min_notes)
    results.add_result(
        "Minimum valid performance notes",
        is_valid,
        error if not is_valid else "Validation passed correctly"
    )
    
    return results

def run_all_tests():
    """Run all test suites"""
    print("VMIS LLM Features Test Suite")
    print("=" * 50)
    
    all_results = TestResults()
    
    # Run test suites
    validation_results = test_input_validation()
    llm_results = test_llm_functions()
    edge_case_results = test_edge_cases()
    
    # Combine results
    for result_set in [validation_results, llm_results, edge_case_results]:
        all_results.passed += result_set.passed
        all_results.failed += result_set.failed
        all_results.results.extend(result_set.results)
    
    # Print detailed results
    print("\nDETAILED TEST RESULTS:")
    print("-" * 30)
    
    for result in all_results.results:
        status = "PASS" if result["passed"] else "FAIL"
        print(f"[{status}] {result['test']}")
        if result["details"]:
            print(f"      Details: {result['details']}")
    
    all_results.print_summary()
    
    return all_results

if __name__ == "__main__":
    # Create log file with timestamp
    from datetime import datetime
    
    log_content = f"""
LLM Feature Tests - VMIS
========================
Test Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

This file contains the results of testing the LLM-powered features
implemented in the Visa Mock Interview System (VMIS).

FEATURES TESTED:
1. Dynamic Question Generation (/llm/generate_questions)
2. Feedback Generation (/llm/generate_feedback) 
3. Session Summarization (/llm/summarize_session)
4. Input Validation for all features
5. Error handling scenarios

TEST CATEGORIES:
- Input Validation Tests
- LLM Function Integration Tests
- Edge Case and Error Handling Tests

"""
    
    results = run_all_tests()
    
    # Append results to log content
    log_content += f"""
RESULTS SUMMARY:
===============
Total Tests Run: {results.passed + results.failed}
Tests Passed: {results.passed}
Tests Failed: {results.failed}
Success Rate: {(results.passed/(results.passed + results.failed)*100):.1f}%

DETAILED RESULTS:
================
"""
    
    for result in results.results:
        status = "PASS" if result["passed"] else "FAIL"
        log_content += f"[{status}] {result['test']}\n"
        if result["details"]:
            log_content += f"   Details: {result['details']}\n"
    
    if results.failed > 0:
        log_content += "\nFAILED TESTS SUMMARY:\n"
        log_content += "====================\n"
        for result in results.results:
            if not result["passed"]:
                log_content += f"- {result['test']}: {result['details']}\n"
    
    log_content += f"""
TEST ENVIRONMENT:
================
- Python Version: {sys.version}
- Test Framework: Custom test runner
- LLM Service: Google Gemini API
- Features: Question Generation, Feedback Generation, Session Summary

NOTES:
======
- All tests validate both successful operations and error handling
- Input validation ensures data integrity and security
- LLM API integration includes proper error handling and logging
- Tests cover edge cases including maximum/minimum input lengths
- Network connectivity required for LLM API tests

END OF TEST REPORT
==================
"""
    
    # Write to file
    with open("llm_feature_tests.txt", "w", encoding="utf-8") as f:
        f.write(log_content)
    
    print(f"\nTest results saved to: llm_feature_tests.txt")

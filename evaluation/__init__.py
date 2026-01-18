"""
NID Evaluation Module

Evaluate NID data entry results against ground truth data with comprehensive
metrics including accuracy, CER (Character Error Rate), and WER (Word Error Rate).
"""

from .evaluator import ResultsEvaluator
from .summary import print_summary

__version__ = "1.0.0"
__all__ = ["ResultsEvaluator", "print_summary"]

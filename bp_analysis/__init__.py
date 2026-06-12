"""BP Analysis Framework Core Module"""
__version__ = '1.0.0'
__author__ = 'BP Analysis Team'

from .core import BPAnalyzer
from .models import ProcessInstance, ProcessEvent, ProcessVariant

__all__ = [
    'BPAnalyzer',
    'ProcessInstance',
    'ProcessEvent',
    'ProcessVariant',
]

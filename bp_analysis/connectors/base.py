"""Base Connector for Database Operations"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
import pandas as pd


class BaseConnector(ABC):
    """Abstract base class for database connectors"""
    
    @abstractmethod
    def connect(self):
        """Establish database connection"""
        pass
    
    @abstractmethod
    def disconnect(self):
        """Close database connection"""
        pass
    
    @abstractmethod
    def bulk_insert_events(self, df: pd.DataFrame) -> int:
        """Bulk insert process events"""
        pass
    
    @abstractmethod
    def get_instances_by_process(self, process_name: str) -> List:
        """Get all instances of a process"""
        pass
    
    @abstractmethod
    def get_events_by_process(self, process_name: str) -> List:
        """Get all events for a process"""
        pass
    
    @abstractmethod
    def execute_query(self, query: str, params: Optional[Dict] = None) -> List:
        """Execute custom SQL query"""
        pass

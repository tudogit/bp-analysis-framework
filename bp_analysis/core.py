"""Core BP Analyzer Module"""
import logging
from typing import List, Dict, Optional
import pandas as pd
import json

from .models import ProcessInstance, ProcessEvent
from .connectors.base import BaseConnector
from .etl.transformer import DataTransformer
from .analysis.performance import PerformanceAnalyzer
from .analysis.discovery import ProcessDiscovery
from .analysis.bottleneck import BottleneckDetector
from .utils.logger import get_logger

logger = get_logger(__name__)


class BPAnalyzer:
    """Main Business Process Analyzer Class"""
    
    def __init__(self, connector: BaseConnector, cache_enabled: bool = True):
        """Initialize BPAnalyzer
        
        Args:
            connector: Database connector instance
            cache_enabled: Enable result caching
        """
        self.connector = connector
        self.cache_enabled = cache_enabled
        self.cache = {}
        
        self.performance = PerformanceAnalyzer(connector)
        self.discovery = ProcessDiscovery(connector)
        self.bottleneck_detector = BottleneckDetector(connector)
        self.transformer = DataTransformer()
        
        logger.info(f"BPAnalyzer initialized with {connector.__class__.__name__}")
    
    def import_events(self, file_path: str, process_name: str, format: str = 'csv') -> int:
        """Import process events from file
        
        Args:
            file_path: Path to the events file
            process_name: Name of the process
            format: File format (csv, json, xlsx)
            
        Returns:
            Number of events imported
        """
        logger.info(f"Importing events from {file_path}")
        
        if format == 'csv':
            df = pd.read_csv(file_path)
        elif format == 'json':
            df = pd.read_json(file_path)
        elif format == 'xlsx':
            df = pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        df = self.transformer.normalize_events(df, process_name)
        
        validation_result = self.transformer.validate_events(df)
        if not validation_result['valid']:
            logger.warning(f"Validation warnings: {validation_result['warnings']}")
        
        count = self.connector.bulk_insert_events(df)
        logger.info(f"Successfully imported {count} events")
        
        self._clear_cache()
        
        return count
    
    def calculate_metrics(self, process_name: Optional[str] = None, 
                         start_date: Optional[str] = None,
                         end_date: Optional[str] = None) -> Dict:
        """Calculate performance metrics for processes"""
        cache_key = f"metrics_{process_name}_{start_date}_{end_date}"
        if self.cache_enabled and cache_key in self.cache:
            logger.debug(f"Returning cached metrics for {cache_key}")
            return self.cache[cache_key]
        
        metrics = self.performance.calculate_all_metrics(
            process_name=process_name,
            start_date=start_date,
            end_date=end_date
        )
        
        if self.cache_enabled:
            self.cache[cache_key] = metrics
        
        return metrics
    
    def discover_process_flow(self, process_name: str) -> Dict:
        """Discover process flow using process mining algorithms"""
        logger.info(f"Discovering process flow for {process_name}")
        
        events = self.connector.get_events_by_process(process_name)
        df = pd.DataFrame([dict(e) if isinstance(e, dict) else dict(zip([col[0] for col in e.description], e)) for e in events])
        
        flow = self.discovery.discover_flow_alpha_algorithm(df)
        variants = self.discovery.extract_variants(df)
        
        return {
            'flow': flow,
            'variants': variants,
            'process_name': process_name
        }
    
    def detect_bottlenecks(self, process_name: str, threshold_percentile: int = 90) -> List[Dict]:
        """Detect bottleneck activities in the process"""
        logger.info(f"Detecting bottlenecks for {process_name}")
        
        events = self.connector.get_events_by_process(process_name)
        df = pd.DataFrame([dict(e) if isinstance(e, dict) else dict(zip([col[0] for col in e.description], e)) for e in events])
        
        bottlenecks = self.bottleneck_detector.detect(
            df, 
            threshold_percentile=threshold_percentile
        )
        
        return bottlenecks
    
    def _clear_cache(self):
        """Clear analysis cache"""
        self.cache.clear()
        logger.debug("Cache cleared")
    
    def export_results(self, data: Dict, output_path: str, format: str = 'json'):
        """Export analysis results to file"""
        logger.info(f"Exporting results to {output_path}")
        
        if format == 'json':
            with open(output_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        elif format == 'csv':
            df = pd.DataFrame(data)
            df.to_csv(output_path, index=False)
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
        logger.info(f"Results exported successfully")

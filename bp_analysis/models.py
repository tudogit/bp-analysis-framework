"""Database Models using SQLAlchemy ORM"""
from sqlalchemy import Column, Integer, String, DateTime, Float, Boolean, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()


class ProcessInstance(Base):
    """Process Instance Model"""
    __tablename__ = 'process_instances'
    
    instance_id = Column(Integer, primary_key=True)
    process_name = Column(String(255), nullable=False, index=True)
    process_type = Column(String(100))
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime)
    duration_minutes = Column(Integer)
    status = Column(String(50), nullable=False, default='RUNNING')
    initiator = Column(String(255))
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<ProcessInstance(id={self.instance_id}, name={self.process_name}, status={self.status})>"


class ProcessEvent(Base):
    """Process Event Model"""
    __tablename__ = 'process_events'
    
    event_id = Column(Integer, primary_key=True)
    instance_id = Column(Integer, ForeignKey('process_instances.instance_id'), nullable=False, index=True)
    activity_name = Column(String(255), nullable=False, index=True)
    activity_type = Column(String(100))
    timestamp = Column(DateTime, nullable=False, index=True)
    duration_seconds = Column(Integer)
    resource_name = Column(String(255))
    resource_type = Column(String(100))
    status = Column(String(50), nullable=False, default='COMPLETED')
    error_message = Column(Text)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ProcessEvent(id={self.event_id}, activity={self.activity_name}, time={self.timestamp})>"


class ProcessVariant(Base):
    """Process Variant Model"""
    __tablename__ = 'process_variants'
    
    variant_id = Column(Integer, primary_key=True)
    process_name = Column(String(255), nullable=False)
    variant_path = Column(Text, nullable=False)
    frequency = Column(Integer, default=1)
    avg_duration_minutes = Column(Float)
    min_duration_minutes = Column(Float)
    max_duration_minutes = Column(Float)
    instance_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ProcessVariant(id={self.variant_id}, process={self.process_name}, freq={self.frequency})>"


class PerformanceMetrics(Base):
    """Performance Metrics Model"""
    __tablename__ = 'performance_metrics'
    
    metric_id = Column(Integer, primary_key=True)
    process_name = Column(String(255), nullable=False, index=True)
    metric_date = Column(String(10), nullable=False)  # YYYY-MM-DD
    avg_cycle_time_minutes = Column(Float)
    min_cycle_time_minutes = Column(Float)
    max_cycle_time_minutes = Column(Float)
    throughput = Column(Integer)  # Instances per day
    completed_instances = Column(Integer)
    failed_instances = Column(Integer)
    waiting_time_minutes = Column(Float)
    resource_utilization = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<PerformanceMetrics(process={self.process_name}, date={self.metric_date})>"

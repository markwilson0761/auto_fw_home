from sqlalchemy import Column, Integer, String, DateTime, Enum
from app.config import Base
from datetime import datetime

class RuleSet(Base):
    __tablename__ = "rule_set"

    id = Column(Integer, primary_key=True, autoincrement=True)
    src_zone = Column(String, nullable=False)  # 源安全域
    dst_zone = Column(String, nullable=False)  # 目的安全域
    action = Column(Enum('ALLOW', 'DENY', name='action_types'), nullable=False)  # 策略
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

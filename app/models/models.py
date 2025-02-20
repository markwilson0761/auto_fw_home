# app/models/models.py
from sqlalchemy import create_engine, Column, String, DateTime, func, Integer, CheckConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import sessionmaker, relationship
from app.config import DATABASE_URL

# 连接数据库
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class SecurityZone(Base):
    """ 存储所有合法的安全域名称 """
    __tablename__ = 'security_zones'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<SecurityZone(name={self.name})>"

# 规则集表
class RuleSet(Base):
    """ 维护防火墙规则，关联合法的安全域，并限制 policy 只能是 allow/restrict """
    __tablename__ = 'rule_sets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    src_zone_id = Column(Integer, ForeignKey('security_zones.id'), nullable=False)
    dst_zone_id = Column(Integer, ForeignKey('security_zones.id'), nullable=False)
    action = Column(String, nullable=False)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    changed_by = Column(String, nullable=False, default='manual')

    # 限制 action 只能是 'allow' 或 'restrict'
    __table_args__ = (
        CheckConstraint("action IN ('allow', 'restrict')", name="valid_action"),
    )
# 初始化数据库
    src_zone = relationship("SecurityZone", foreign_keys=[src_zone_id])
    dst_zone = relationship("SecurityZone", foreign_keys=[dst_zone_id])

    def __repr__(self):
        return f"<RuleSet(src={self.src_zone_id}, dst={self.dst_zone_id}, action={self.action})>"
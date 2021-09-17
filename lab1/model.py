from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from base import Base


class AuditNames(Base):
    __tablename__ = "audit_names"

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    audit_info = relationship("AuditInfo", backref="audit_names")

    def __init__(self, filename):
        self.filename = filename


class AuditInfo(Base):
    __tablename__ = "audit_info"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    body = Column(String)
    audit_name_id = Column(Integer, ForeignKey('audit_names.id'))

    def __init__(self, info_title, info_body, audit_name_id=None):
        self.title = info_title
        self.body = info_body
        self.audit_name_id = audit_name_id

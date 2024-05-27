from sqlalchemy import Column, DateTime, INTEGER, String, Boolean
from datetime import datetime

from sqlalchemy.orm import Session

from autonode.models.base_model import DBBaseModel
import sqlalchemy as sa

from autonode.utils.enums.request_status import RequestStatus


class Requests(DBBaseModel):
    """
    Creates a new Job object to store the job details.

    Attributes:
        id: INTEGER column to store the unique identifier for the job.
        description: String column to store the description of the job.
        url: String column to store the URL of the job.
        requests_dir: String column to store the directory path of the job. Screenshots will be stored in this directory.
        status: String column to store the status of the job.
        completed_at: DateTime column to store the timestamp about when a job is completed.
        created_at: DateTime column to store the timestamp about when a job is created.
        updated_at: DateTime column to store the timestamp about when a job is updated.
    """

    __tablename__ = 'requests'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    description = Column(String, nullable=False)
    url = Column(String, nullable=False)
    requests_dir = Column(String, nullable=False)
    tree_location = Column(String, nullable=False)
    status = Column(String, nullable=False, default=RequestStatus.PENDING.value)
    completed_at = Column(DateTime, default=None)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=sa.false(), nullable=sa.false(), server_default=sa.false())

    @classmethod
    def get_request_by_id(cls, session, job_id):
        return session.query(cls).filter(cls.id == job_id).first()

    @classmethod
    def add_request(cls, session, description, url, requests_dir, graph_path):
        request = cls(description=description, url=url, requests_dir=requests_dir, tree_location=graph_path)
        session.add(request)
        session.commit()
        session.flush()
        return request

    @classmethod
    def update_request_status(cls, session: Session, request_id: int, status: str):
        request = session.query(cls).filter_by(id=request_id).first()
        request.status = status
        session.commit()
        session.refresh(request)
        return request

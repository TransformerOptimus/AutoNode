from datetime import datetime
from typing import Optional
from sqlalchemy import Column, INTEGER, String, func, DateTime, Boolean
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Session
from autonode.models.base_model import DBBaseModel


class Files(DBBaseModel):
    """
    Creates a new ScreenshotsStore object to store the screenshots of a job.

    Attributes:
        id: INTEGER column to store the unique identifier for the screenshot.
        request_id: INTEGER column to store the unique identifier for the job.
        path: String column to store the path of the screenshot image.
        category: String column to store the category of the file like DEBUG, OUTPUT etc.
        meta_data: String column to store the metadata of the file/video.
        created_at: DateTime column to store the timestamp about when a screenshot is created.
        updated_at: DateTime column to store the timestamp about when a screenshot is updated.
    """

    __tablename__ = 'files'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    request_id = Column(INTEGER, nullable=False)
    path = Column(String, nullable=False)
    category = Column(String, nullable=True)
    meta_data = Column(JSONB, nullable=True)
    file_type = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=sa.false(), nullable=sa.false(), server_default=sa.false())

    @classmethod
    def add_file(cls, session: Session, request_id: int, path: str, category: str, file_type: Optional[str],
                 meta_data: Optional[dict]):
        file = cls(request_id=request_id, path=path, category=category, meta_data=meta_data, file_type=file_type)
        session.add(file)
        session.commit()
        session.flush()
        return file

    @classmethod
    def get_files_by_req_id(cls, session: Session, request_id: int):
        return session.query(cls).filter_by(request_id=request_id).order_by(cls.created_at).all()

    @classmethod
    def get_files_by_type(cls, session: Session, file_type: str):
        return session.query(cls).filter_by(file_type=file_type).order_by(cls.created_at).all()

    @classmethod
    def get_files_by_meta_data(cls, session: Session, meta_data: dict, file_type: str):
        """
        Retrieves files whose meta_data column contains the passed meta_data dictionary as a subset.

        Args:
            session (Session): SQLAlchemy session to perform the database operations.
            meta_data (dict): A dictionary of meta_data we want to check as a subset.
            file_type (str): The type of the file to retrieve

        Returns:
            list: A list of Files instances that match the criteria.
        """
        meta_data_jsonb = func.jsonb_build_object(*sum(meta_data.items(), ()))

        result = session.query(cls).filter(cls.meta_data.contains(meta_data_jsonb),
                                           file_type=file_type).order_by(cls.created_at).all()

        return result

from sqlalchemy import Column, INTEGER, String, DateTime, Boolean
from datetime import datetime
import sqlalchemy as sa
from autonode.models.base_model import DBBaseModel


class Actions(DBBaseModel):
    """
    Stores the actions taken by the LLM while processing a job.

    Attributes:

    """
    __tablename__ = 'actions'
    id = Column(INTEGER, primary_key=True, autoincrement=True)
    request_id = Column(INTEGER, nullable=False)
    screenshot_id = Column(INTEGER, nullable=False)
    prompt = Column(String, nullable=False)
    llm_response = Column(String, nullable=False)
    action = Column(String, nullable=False)
    node_id = Column(INTEGER, nullable=False)
    text = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_deleted = Column(Boolean, default=sa.false(), nullable=sa.false(), server_default=sa.false())

    @classmethod
    def add_action_taken(cls, session, request_id, screenshot_id, prompt, llm_response, action, node_id, text):
        action = cls(request_id=request_id, screenshot_id=screenshot_id, prompt=prompt, llm_response=llm_response,
                     action=action, node_id=node_id, text=text)
        session.add(action)
        session.commit()
        session.flush()
        return action

    @classmethod
    def delete_action_by_id(cls, session, action_id):
        action = session.query(cls).filter(cls.id == action_id).first()
        session.delete(action)
        session.commit()
        return action

    @classmethod
    def get_node_metatdata(cls, session, node_id):
        pass

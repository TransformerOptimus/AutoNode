from fastapi_sqlalchemy import db
from fastapi import APIRouter
from autonode.logger.logger import logger
from autonode.models.requests import Requests
from autonode.models.types.requests.initiate_autonode import InitiateAutoNodeRequest
from autonode.services.autonode import AutonodeService
from autonode.utils.helpers.naming_helper import NamingHelper

router = APIRouter()


@router.post("/initiate")
def initiate_autonode(request: InitiateAutoNodeRequest):
    try:
        req = Requests.add_request(session=db.session,
                                   description=request.objective,
                                   url=request.site_url,
                                   graph_path=request.graph_path,
                                   requests_dir=f"requests/{NamingHelper.request_folder_name_generator()}")

        from autonode.worker import initiate_autonode

        initiate_autonode.delay(request_id=req.id,
                                url=request.site_url,
                                objective=request.objective,
                                graph_path=request.graph_path,
                                screenshots_dir=f"requests/{NamingHelper.request_folder_name_generator()}")

        return {"success": True, "message": f"Initiated AutoNode for Request ID {req.id} successfully"}

    except Exception as e:
        logger.error(f"Error initiating Autonode: {str(e)}")
        return {"success": False, "message": f"Error initiating Autonode: {e}"}

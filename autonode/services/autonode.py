import os
import random
import time
import asyncio
from autonode.config.config import get_config
from autonode.llms.open_ai import OpenAi
from autonode.logger.logger import logger
from abc import ABC
from sqlalchemy.orm import Session
from autonode.config.settings import Settings
from autonode.agents.traversal_agent import TraversalAgent
from autonode.services.graph import Graph
from autonode.services.web_automation import WebAutomationService
from autonode.models.requests import Requests
from autonode.utils.decorators.retry_decorator import retry
from autonode.utils.enums.request_status import RequestStatus
from autonode.utils.exceptions.element_not_found_exception import ElementNotFoundException
from autonode.utils.exceptions.llm_objective_exception import LLMObjectiveException


class AutonodeService(ABC):

    def __init__(self, objective, graph_path, root_node="1") -> None:
        self.llm = OpenAi(api_key=os.getenv("OPENAI_API_KEY"), model=get_config("GPT_4_0125_PREVIEW_VERSION"),
                          temperature=random.uniform(0.0, 0.2), top_p=random.uniform(0.9, 0.99),
                          presence_penalty=1, frequency_penalty=1)
        self.objective = objective
        self.graph_path = graph_path
        self.root_node = root_node
        self.config = Settings()
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        # Uncomment If you have aws account and want to store result in your AWS S3
        # self.s3_client = S3Helper(access_key=self.config.AWS_ACCESS_KEY_ID,
        #                           secret_key=self.config.AWS_SECRET_ACCESS_KEY,
        #                           bucket_name=self.config.bucket_name)

        # Initialising run variables
        self.web_automator = None
        self.read_graph = None
        self.curr_graph_node = None
        self.prev_graph_node = None
        self.actions_taken = []
        self.prompt = ""
        self.response = ""

    @retry(max_attempts=3, backoff=0, exceptions=(ElementNotFoundException, LLMObjectiveException))
    def run(self, session: Session, request_id: int, request_dir: str, url: str, planner_prompt: str):
        try:
            Requests.update_request_status(session=session, request_id=request_id,
                                           status=RequestStatus.IN_PROGRESS.value)
            self._setup_directories(request_id=request_id, request_dir=request_dir)
            self._initialise(url=url)
            self._run(session=session, request_id=request_id, request_dir=request_dir, planner_prompt=planner_prompt)
            Requests.update_request_status(session=session, request_id=request_id, status=RequestStatus.COMPLETED.value)

        except Exception as e:
            Requests.update_request_status(session=session, request_id=request_id, status=RequestStatus.FAILED.value)
            logger.error(f"Error in executing the objective for request id {request_id}: {e}")
            raise e

        finally:
            if self.web_automator:
                self.loop.run_until_complete(self.web_automator.stop_trace(request_dir))
                self.loop.run_until_complete(self.web_automator.close_browser())

    def _run(self, session: Session, request_id: int, request_dir: str, planner_prompt: str):
        steps = 0
        logger.info(f"Running Node : {self.curr_graph_node} {request_id}")
        time.sleep(3)
        while True:
            try:
                self.curr_graph_node.run(
                    autonode_object=self,
                    steps=steps,
                    history=self.actions_taken,
                    objective=self.objective,
                    web_automater=self.web_automator,
                    previous_node=self.prev_graph_node,
                    db_session=session,
                    # Pass self.s3_client If you have AWS account and want to store result in your AWS S3
                    s3_client=None,
                    request_id=request_id,
                    request_dir=request_dir,
                    prompt=self.prompt,
                    llm_response=self.response,
                    loop=self.loop,
                    llm_instance=self.llm,
                    planner_prompt=planner_prompt
                )

            except Exception as e:
                logger.error(f"Error in running the Node: {self.curr_graph_node.node_name} - {e}")
                raise e
            self.actions_taken.append(self.curr_graph_node.actions_taken())
            steps += 1
            if not self._traverse():
                break

    def _setup_directories(self, request_id: int, request_dir: str):
        self.cropped_image_folder = os.path.join("cropped_image", str(request_id))
        os.makedirs(self.cropped_image_folder, exist_ok=True)
        os.makedirs(request_dir, exist_ok=True)
        logger.info(f"Created the directories for the Request: {request_id}")

    def _initialise(self, url: str):
        self.web_automator = WebAutomationService(url=url)
        self.loop.run_until_complete(self.web_automator.initialise())
        self.graph = Graph(graph_path=self.graph_path)
        self.curr_graph_node, self.prev_graph_node = self.graph.graph_dict[self.root_node], None

    def _traverse(self) -> bool:
        self.prev_graph_node = self.curr_graph_node

        if self._is_leaf_node():
            self._call_end_of_traversal()
            return False

        if len(self.curr_graph_node.adjacent_to) == 1:
            logger.info(f"{self.curr_graph_node.node_name} has SINGLE CHILD: - Defaulting to the child")
            self.curr_graph_node = self.graph.graph_dict[str(self.curr_graph_node.adjacent_to[0])]
            return True

        logger.info(f"MULTIPLE CHILDREN - Traversing to the next node: {self.curr_graph_node.node_name}")
        self.curr_graph_node, self.prompt, self.response = TraversalAgent(llm_instance=self.llm).execute(
            objective=self.objective,
            actions_taken="\n".join(
                [f"{idx + 1}: {action}" for
                 idx, action in
                 enumerate(self.actions_taken)]),
            graph_node=self.curr_graph_node,
            graph_dict=self.graph.graph_dict)
        return True

    def _is_leaf_node(self) -> bool:
        return not self.curr_graph_node.adjacent_to

    def _call_end_of_traversal(self) -> None:
        logger.info(
            f" End of Traversal: {self.curr_graph_node.node_name}")

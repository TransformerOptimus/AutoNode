import os
import time
from autonode.logger.logger import logger
from autonode.nodes.base_node import Node
from autonode.models.actions import Actions
from autonode.factories.node_factory import NodeFactory
from autonode.services.web_automation import WebAutomationService
from autonode.agents.typing_agent import TypingAgent
from autonode.utils.exceptions.element_not_found_exception import ElementNotFoundException
from autonode.utils.helpers.cleanup_helper import CleanupHelper
from autonode.services.bounding_box import BoundingBoxService
from autonode.utils.screenshot_generator import ScreenshotGenerator


@NodeFactory.register_node_type("clickable_and_typeable")
class ClickableAndTypeableNode(Node):
    """Actionable element on the screen that can be clicked and typed into

    Args:
        id (str): Unique identifier for the node
        node_name (str): Type of the node
        adjacent_from (list): List of nodes that are adjacent to this node
        adjacent_to (list): List of nodes that this node is adjacent to
        llm (str): The instance of the llm will be chosen from the llm factory module
        actionable_element_type (str): Type of the actionable element
        location (list): Location of the actionable element on the screen
        is_type (bool): Whether the actionable element is typeable
        description (str): Description of the actionable element
        type_description (str): Description of the type of the actionable element
    """

    def __init__(self, id: str, node_name: str, adjacent_from: list, adjacent_to: list,
                 description: str,
                 llm: str, actionable_element_type: str, location: list,
                 is_type: bool, type_description: str,):
        super().__init__(id, node_name, adjacent_from, adjacent_to, description, llm)
        self.loop = None
        self.screenshot_filename = None
        self.actionable_element_type = actionable_element_type
        self.location = [location[0] / 100, location[1] / 100]
        self.is_type = is_type
        self.type_description = type_description
        self.type_value = None
        self.is_visited = False
        self.screenshot_id = None
        self.web_automator = None
        self.counter_for_element_not_found_through_ocr_yolo = 0

    def run(self, autonode_object, steps, history, objective, web_automater, db_session, s3_client,
            request_id, request_dir, prompt, llm_response, loop, previous_node, llm_instance, **kwargs):

        self.loop = loop
        time.sleep(1)

        screenshot_filename, self.screenshot_id = ScreenshotGenerator().run(
            db_session=db_session, s3_client=s3_client, web_automator=web_automater,
            step=steps, request_id=request_id, request_dir=request_dir, loop=self.loop
        )

        cropped_images_folder = os.path.join(request_dir, "cropped_images")
        os.makedirs(cropped_images_folder, exist_ok=True)

        self._get_clicking_location(screenshot_filename, cropped_images_folder, previous_node, db_session, s3_client,
                                    web_automater, steps, request_id, request_dir)
        self._click(web_automater)

        if self.is_type:
            self._get_typing_information(objective, history, llm_instance)
            self._type(web_automater)

        self.update_action_in_db(db_session, request_id, prompt, llm_response)

    def update_action_in_db(self, session, request_id, prompt, llm_response):
        if self.is_type and self.type_value:
            Actions.add_action_taken(session=session, request_id=request_id, screenshot_id=self.screenshot_id,
                                     prompt=prompt, llm_response=llm_response, node_id=self.id, text=self.type_value,
                                     action=f"Clicked on {self.node_name}. Typed {self.type_value} on the textbox"
                                            f" {self.node_name}")
        elif not self.is_type:
            Actions.add_action_taken(session=session, request_id=request_id, screenshot_id=self.screenshot_id,
                                     prompt=prompt, llm_response=llm_response, action=f"Clicked on {self.node_name}",
                                     node_id=self.id, text="")
        else:
            Actions.add_action_taken(session=session, request_id=request_id, screenshot_id=self.screenshot_id,
                                     prompt=prompt, llm_response=llm_response, node_id=self.id, text="",
                                     action=f"Clicked on {self.node_name}. Nothing typed on the textbox")

    def actions_taken(self):
        if self.is_type and self.type_value:
            return f"Clicked on {self.node_name}. \nTyped {self.type_value} on the textbox {self.node_name}"
        elif not self.is_type:
            return f"Clicked on {self.node_name}"

    def _click(self, web_automater: WebAutomationService):
        clicked_location = self.loop.run_until_complete(
            web_automater.click_on_page(self.location)
        )
        logger.info(
            f"Click Action: Clicked on {self.node_name} at location {clicked_location}"
        )

    def _type(self, web_automator: WebAutomationService):
        self.loop.run_until_complete(web_automator.type_on_page(self.type_value))
        logger.info(
            f"Type Action: Typed {self.type_value} on the textbox {self.node_name}"
        )

    def _get_clicking_location(
            self, screenshot_filepath, cropped_image_folder, previous_node, db_session, s3_client, web_automater,
            steps, request_id, request_dir
    ):
        """Passes the screenshot through YOLO + OCR to get the accurate location to click.

        Args:
            screenshot_filepath (str): screenshot filepath
        """
        if self.is_visited:
            return

        if not isinstance(previous_node, ClickableAndTypeableNode):
            previous_node = None

        clickable_objects = BoundingBoxService().get_bounding_box(image_path=screenshot_filepath,
                                                                  folder_path=cropped_image_folder)

        similarity_of_updated_location, updated_location = BoundingBoxService().get_location(
            self, clickable_objects, previous_node, screenshot_filepath)

        if updated_location is None:
            if self.counter_for_element_not_found_through_ocr_yolo == 5:
                raise ElementNotFoundException(element=self.node_name, request_id=request_id)

            self.counter_for_element_not_found_through_ocr_yolo += 1  # Element not found by OCR+YOLO

            logger.info(f"Element not found - {self.node_name} by OCR+YOLO. Retrying..."
                             f"{self.counter_for_element_not_found_through_ocr_yolo}")

            time.sleep(2)
            new_screenshot_filename, self.screenshot_id = ScreenshotGenerator().run(
                db_session=db_session, s3_client=s3_client, web_automator=web_automater,
                step=steps, request_id=request_id, request_dir=request_dir, loop=self.loop
            )
            return self._get_clicking_location(new_screenshot_filename, cropped_image_folder, previous_node, db_session,
                                               s3_client, web_automater, steps, request_id, request_dir)

        logger.info(f"Updating Location: {self.node_name}  x,y: {updated_location}")
        self.location = updated_location
        self.is_visited = True
        self.counter_for_element_not_found_through_ocr_yolo = 0
        return

    def _get_typing_information(self, objective, history, llm_instance):
        """
        This function retrieves typing information based on user input and logs the action being typed.
        """

        typing_response, prompt, response = TypingAgent(llm_instance=llm_instance).execute(
            objective=objective,
            actions="\n".join([f"{idx + 1}: {action}" for idx, action in enumerate(history)]),
            description=self.type_description,
        )

        logger.info(f"Type Action: {self.node_name} typing: {typing_response['type']}")

        if isinstance(typing_response["type"], str):
            type_on_page = CleanupHelper.type_response_cleaner(response=typing_response["type"])
        elif isinstance(typing_response["type"], list):
            type_on_page = typing_response["type"]
        else:
            type_on_page = str(typing_response["type"])
        self.type_value = type_on_page

    def __repr__(self):
        return f"ClickableAndTypeableNode({self.id}, {self.node_name}, {self.description})"

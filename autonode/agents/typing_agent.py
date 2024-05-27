import ast
from autonode.agents.base_agent import BaseAgent
from autonode.llms.base_llm import BaseLlm
from autonode.logger.logger import logger
from autonode.prompts.openai_prompt import TYPING_INFO_PROMPT, ERROR_HANDLING_PROMPT
from autonode.utils.helpers.cleanup_helper import CleanupHelper


class TypingAgent(BaseAgent):

    def __init__(self, llm_instance: BaseLlm):
        super().__init__(llm_instance)

    def execute(self, objective, actions, description):
        # TODO: Refactor the prompt to place actionable items in the type instruction.
        # TODO : Make the typing util parse the typing instruction to determine the typing action.
        """
        Ask GPT to generate what needs to be typed on a given textbox.
        """
        prompt = TYPING_INFO_PROMPT.format(objective=objective, actions=actions, description=description)
        messages = [{"role": "user", "content": prompt}]

        for i in range(3):
            response = self.llm.chat_completion(messages=messages)
            content = response["content"]
            content = CleanupHelper.clean_response(response=content)
            logger.info("Asking llm what to type: ", content)
            try:
                content_object = ast.literal_eval(content)
                return content_object, prompt, content
            except Exception as e:
                logger.error("Error while running Typing Agent", str(e))
                if i == 2:
                    content_object = self.handle_error(prompt, content, str(e))
                    return content_object, prompt, content
                continue
        return None

    # TODO Handle Prompt Injection in retry decorator
    def handle_error(self, prompt, llm_response, error):
        error_handling_prompt = ERROR_HANDLING_PROMPT.format(prompt=prompt, llm_response=llm_response, error=error)
        response = self.llm.chat_completion(messages=[{"role": "user", "content": error_handling_prompt}])
        content = response["content"]
        content = CleanupHelper.clean_response(response=content)
        try:
            content_object = ast.literal_eval(content)
            logger.info('Handled Typing Agent Error: ', content_object)
            return content_object
        except Exception as e:
            raise Exception("Error while retrying Typing Agent", str(e))

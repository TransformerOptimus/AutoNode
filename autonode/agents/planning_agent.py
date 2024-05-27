from autonode.agents.base_agent import BaseAgent
from autonode.llms.base_llm import BaseLlm
from autonode.prompts.openai_prompt import AUTONODE_PLANNER_PROMPT_APOLLO


class PlanningAgent(BaseAgent):

    def __init__(self, llm_instance: BaseLlm):
        self.llm = llm_instance
        super().__init__(llm_instance)

    def execute(self, objective: str) -> str:

        prompt = AUTONODE_PLANNER_PROMPT_APOLLO.format(objective=objective)
        response = self.llm.chat_completion(messages=[{"role": "system", "content": prompt},
                                                      {"role": "user", "content": ""}])
        content = response["content"]
        return content

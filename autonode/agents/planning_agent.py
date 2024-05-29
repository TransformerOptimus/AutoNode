from autonode.agents.base_agent import BaseAgent
from autonode.llms.base_llm import BaseLlm
from autonode.prompts.openai_prompt import AUTONODE_PLANNER_PROMPT_APOLLO, AUTONODE_PLANNER_PROMPT_TWITTER


class PlanningAgent(BaseAgent):

    def __init__(self, planner_prompt: str, llm_instance: BaseLlm):
        self.llm = llm_instance
        self.prompt_hash = {
            "apollo": AUTONODE_PLANNER_PROMPT_APOLLO,
            "twitter": AUTONODE_PLANNER_PROMPT_TWITTER
        }
        self.prompt = self.prompt_hash.get(planner_prompt)
        super().__init__(llm_instance)

    def execute(self, objective: str) -> str:

        prompt = self.prompt.format(objective=objective)
        response = self.llm.chat_completion(messages=[{"role": "system", "content": prompt},
                                                      {"role": "user", "content": ""}])
        content = response["content"]
        return content

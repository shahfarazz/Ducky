from typing import Optional

import aitools_autogen.utils as utils
from aitools_autogen.agents import WebPageScraperAgent
from aitools_autogen.blueprint import Blueprint
from aitools_autogen.config import llm_config_openai as llm_config, config_list_openai as config_list, WORKING_DIR
from autogen import ConversableAgent

from typing import Optional
import aitools_autogen.utils as utils
from aitools_autogen.blueprint import Blueprint
from aitools_autogen.config import llm_config_openai as llm_config, config_list_openai as config_list, WORKING_DIR

class CoreClientProject8Example(Blueprint):

    def __init__(self, work_dir: Optional[str] = WORKING_DIR):
        super().__init__([], config_list=config_list, llm_config=llm_config)
        self._work_dir = work_dir or "code"
        self._summary_result: Optional[str] = None

    @property
    def summary_result(self) -> str | None:
        """The getter for the 'summary_result' attribute."""
        return self._summary_result

    @property
    def work_dir(self) -> str:
        """The getter for the 'work_dir' attribute."""
        return self._work_dir

    async def initiate_work(self, message: str):
        utils.clear_working_dir(self._work_dir)
        agent0 = ConversableAgent("a0",
                                  max_consecutive_auto_reply=0,
                                  llm_config=False,
                                  human_input_mode="NEVER")

        sklearn_agent = ConversableAgent("sklearn_agent",
                                         max_consecutive_auto_reply=6,
                                         llm_config=llm_config,
                                         human_input_mode="NEVER",
                                         code_execution_config=False,
                                         function_map=None,
                                         system_message="""
You are a Python developer expert in Scikit-learn.
You're writing a comprehensive Machine Learning model.

When you receive a message, you should expect that message to describe the ML model's requirements in detail.

Write a complete implementation covering all described steps. Each step should be encapsulated in its own function for modularity and ease of testing. The steps might include but are not limited to:
- Data loading
- Data preprocessing
- Feature extraction
- Model training
- Model evaluation
- Model saving

Use multiple Python files in a directory structure that makes sense. Each file should correspond to a logical part of the ML pipeline.

Use Scikit-learn for the ML framework.

You must indicate the script type in the code block.
Do not suggest incomplete code which requires users to modify.
Always put `# filename: aitools_autogen/coding/<filename>` as the first line of each code block.

Feel free to include multiple code blocks in one response. Do not ask users to copy and paste the result.

After the code, provide a summary explanation of the generated code, including the purpose of each function and how they work together to form the complete ML pipeline.
""")

        agent0.initiate_chat(sklearn_agent, True, True, message=message)

        llm_message = agent0.last_message(sklearn_agent)["content"]
        utils.save_code_files(llm_message, self.work_dir)

        self._summary_result = utils.summarize_files(self.work_dir)

if __name__ == "__main__":
    import asyncio

    task = """
     I want to create a basic Machine Learning model using Scikit-learn.
     The model should include the following steps:
     - Data preprocessing
     - Model training
     - Model evaluation
    """
    # Create an instance of MLModelBlueprint
    blueprint = CoreClientProject8Example()

    # Run the blueprint asynchronously
    asyncio.run(blueprint.initiate_work(task))

    print(blueprint.summary_result)
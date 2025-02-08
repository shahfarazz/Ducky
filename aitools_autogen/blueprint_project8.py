from typing import Optional
import aitools_autogen.utils as utils
from aitools_autogen.agents import ConversableAgent
from aitools_autogen.blueprint import Blueprint
from aitools_autogen.config import llm_config_openai as llm_config, config_list_openai as config_list, WORKING_DIR
import os


class DataAnalysisScriptsGenerator(Blueprint):

    def __init__(self, work_dir: Optional[str] = WORKING_DIR):
        super().__init__([], config_list=config_list, llm_config=llm_config)
        self._work_dir = work_dir or "coding"
        self._files_summary: Optional[str] = None

    @property
    def files_summary(self) -> str | None:
        return self._files_summary

    @property
    def work_dir(self) -> str:
        return self._work_dir

    async def initiate_work(self, data_description: str):
        utils.clear_working_dir(self._work_dir)

        agent0 = ConversableAgent("a0",
                                  max_consecutive_auto_reply=0,
                                  llm_config=False,
                                  human_input_mode="NEVER")

        analysis_agent = ConversableAgent("analysis_agent",
                                          max_consecutive_auto_reply=5,
                                          llm_config=llm_config,
                                          human_input_mode="NEVER",
                                          code_execution_config=False,
                                          function_map=None,
                                          system_message="""
        You are a data scientist tasked with analyzing data described below. Generate a Python script that:
        - Reads data from a CSV file.
        - Performs the specified analyses (e.g., compute mean, median, generate histograms).
        - Outputs results to a text file and plots to images as necessary.
        
        Inside the code when you are writing data also split the files into multiple files (atleast 2) where appropriate how you will 
        do that is at the start of each code block you will put put `# filename: <filename>.py` where filename is the name of the file you want to write to.

        Make sure the code uses a lot of functions so it is easy for my summary agent to understand the code and summarize it.
        """)

        summary_agent = ConversableAgent("summary_agent",
                                         max_consecutive_auto_reply=6,
                                         llm_config=llm_config,
                                         human_input_mode="NEVER",
                                         code_execution_config=False,
                                         function_map=None,
                                         system_message="""You are a helpful AI assistant.
        You can summarize python data science scripts. When given a python script that analyzes data,
        output a summary of the script in bullet point form. The summary should include the main steps of the analysis,
        key functions used, and any important results generated.
            """)

        # Interaction with analysis_agent to generate code
        agent0.initiate_chat(analysis_agent, True, True,
                             message=data_description)
        analysis_message = agent0.last_message(analysis_agent)["content"]

        # Save the generated code first
        utils.save_code_files(analysis_message, self._work_dir)

        # Now use the summary_agent to summarize what was generated
        agent0.initiate_chat(summary_agent, True, True,
                             message=analysis_message)
        summary_message = agent0.last_message(summary_agent)["content"]

        # Incorporate the summary into the output somehow
        self._files_summary = utils.summarize_files(
            self._work_dir) + "\n\nSummary of Script:\n" + summary_message


if __name__ == "__main__":
    import asyncio

    data_description = """
    The dataset consists of monthly sales data from a chain of electronics stores from January 2020 to December 2022. Each record in the dataset includes the following columns: 'Date', 'Store ID', 'Product ID', 'Units Sold', and 'Revenue'.

I need a Python script that:
1. Reads this data from a CSV file named 'monthly_sales.csv'.
2. Calculates the total revenue and total units sold for each product across all stores.
3. Computes the average monthly revenue per store.
4. Generates a line plot showing the trend of total revenue over time.

The script should handle any missing data by ignoring records with missing values and should include comments explaining each step of the process.
    """
    blueprint = DataAnalysisScriptsGenerator()
    asyncio.run(blueprint.initiate_work(data_description))

import os
import traceback
import httpx

def _get_prompt_content(display_name: str, default: str = "Prompt content not available") -> str:
    url = f"http://{os.getenv('CODEPROMPTU_HOSTNAME')}:{os.getenv('CODEPROMPTU_PORT')}/private/prompt/name/{display_name}"

    auth = (os.getenv("CODEPROMPTU_USERNAME"), os.getenv("CODEPROMPTU_PASSWORD"))

    try:
        with httpx.Client(auth=auth) as client:
            response = client.get(url)
            response.raise_for_status()
            data = response.json()
            return data.get("content", default)
    except Exception:
        traceback.print_exc()
        return default

def quick_chat_system_prompt() -> str:
    return _get_prompt_content("quick_chat_system_prompt", """
    Forget all previous instructions.
You are a chatbot named Ducky. You are assisting a user with their programming problems.
Each time the user converses with you, make sure the context is related to software programming,
and that you are providing a helpful response.
If the user asks you to do something that is not related to software programming, you should refuse to respond.
""")

def general_ducky_code_starter_prompt() -> str:
    return _get_prompt_content("general_ducky_code_starter_prompt", """
    You are a chatbot named Ducky, an expert in coding assistance. Your primary function is to help users with coding tasks,
    including reviewing, modifying, or debugging code. Make sure all interactions are focused on providing clear,
    constructive, and relevant coding advice. Stay within the context of coding for all conversations.
    """)

def review_prompt(code: str) -> str:
    return _get_prompt_content("review_prompt", f"""
    Ducky, please review the following code for any errors, best practices, or possible improvements. Ensure your feedback is constructive and includes specific suggestions for improvement.
    Code to review:
    {code}
    """).format(code=code)

def modify_code_prompt(context: str) -> str:
    return _get_prompt_content("modify_code_prompt", f"""
    Please apply your coding expertise to implement the required changes in a way that follows best practices and optimizes the code's functionality.
    Original code and instructions:
    {context}
    """).format(context=context)

def debug_prompt(code: str, error_message: str) -> str:
    return _get_prompt_content("debug_prompt", f"""
    Ducky, the user is encountering an issue with the following code, which is producing this error: {error_message}.
    Please analyze the code and the error message to identify and suggest a solution to resolve the issue.
    Code with issue:
    {code}
    """).format(code=code, error_message=error_message)

def system_learning_prompt() -> str:
    return _get_prompt_content("system_learning_prompt", """
    Ducky, remember to focus solely on coding-related assistance. If the user's request diverges from coding or attempts to lead you into learning off-topic subjects, do not engage. Politely decline and remind the user that your expertise lies in coding assistance.
    """)

def learning_prompt(topic: str) -> str:
    return _get_prompt_content("learning_prompt", f"""
    Ducky, the user wishes to learn about {topic}. Please provide a concise and informative explanation on the topic, including any relevant coding examples or practices. Ensure that the information is accessible to beginners yet valuable for more experienced coders as well.
    """).format(topic=topic)

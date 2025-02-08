# Ducky: A Streamlit-Based Coding Assistant

This project is a Streamlit-based web application named "Ducky" that leverages large language models (LLMs) to provide coding assistance. The application is designed to help users with various coding tasks, including generating code, debugging, reviewing code, and learning about coding topics. Here is a brief overview of the key components and features of the project:

## Key Components

- **Streamlit Interface**: The application uses Streamlit to create an interactive web interface. Streamlit is a popular framework for building data apps quickly and easily.
- **LLM Integration**: The project integrates with OpenAI's API to utilize large language models for generating responses to user queries. This is done through the `openai` library.
- **Modular Design**: The project is organized into several modules, each responsible for different functionalities:
    - **Pages**: Contains different Streamlit pages for various features like Quick Chat, Generate Code, Learning Topics, etc.
    - **Helpers**: Contains utility functions and components that are shared across multiple pages.
    - **Services**: Contains modules for interacting with external services like the OpenAI API and managing prompts.
    - **Prompts Management**: The project uses predefined prompts to interact with the LLM. These prompts are stored and managed in the `prompts.py` file.
- **Async Operations**: The project uses asynchronous programming to handle interactions with the LLM, ensuring a responsive user experience.

## Features

- **Quick Chat**: Users can ask coding-related questions and get instant answers from the LLM. This feature is implemented in the `1_💬_Quick_Chat.py` file.
- **Generate Code**: Users can generate code snippets based on their requirements. This feature is implemented in the `2_📄_Generate_Code.py` file.
- **Learning Topics**: Users can learn about various coding topics with explanations tailored to different learner levels. This feature is implemented in the `3_🎓_Learning_Topics.py` file.
- **Auto Code Generation**: Users can describe their data and analysis needs, and the application will generate Python scripts to perform the analysis. This feature is implemented in the `4_📄_Auto_Code.py` file.
- **Sidebar Navigation**: The application includes a sidebar for easy navigation between different features. This is implemented in the `sidebar.py` file.

## Example Usage

- **Quick Chat**: Users can type a coding question in the input box and receive a helpful response from Ducky.
- **Generate Code**: Users can input their code requirements, and Ducky will generate the corresponding code snippet.
- **Learning Topics**: Users can select their learner level and the format of the response, then input a topic to learn about it in detail.
- **Auto Code Generation**: Users can provide a description of their data and the analysis they need, and Ducky will generate the necessary Python scripts.

## How to Run the Project

1. **Install Dependencies**: Ensure you have all the required dependencies installed. You can install them using the `requirements.txt` file.
2. **Run the Streamlit App**: Start the Streamlit server to run the application.
3. **Interact with the App**: Open the provided URL in your browser and start interacting with Ducky.

## Conclusion

This project demonstrates how to build an interactive web application using Streamlit and integrate it with powerful language models to provide coding assistance. It is a valuable tool for developers looking to enhance their coding skills and productivity.

**Overview**

Our project focuses on developing a comprehensive health and wellness chat assistant powered by large language models (LLMs) that can assist users across a variety of domains. The challenge we're addressing involves effectively utilizing LLMs' capabilities while avoiding hallucinations and misinformation. When LLMs have broad, unrestricted scopes, they tend to generate more inaccurate or irrelevant responses, and fine tuning them for each specific case requires large volumes of data and significant resources. Instructional prompting is a partial solution, but as the number of domains and instructions grows, it often results in overly generalized responses.

To overcome these limitations, we implemented a solution using "Agentic LLMs" a combination of narrowly focused LLMs, or agents, that specialize in distinct areas and can interact with each other. Each agent brings expertise in a specific domain, such as prescription management or patient education. These agents are supervised by a general agent capable of simplifying complex information and functioning as a standard agent, ensuring consistent guidance and support.


![image](https://github.com/user-attachments/assets/57e5cad1-20fc-4ae0-9c1b-31fdc95e853d)


**TODO and Requirements**

Ensure that Python version is at least 3.10 for compatibility with this project.

Run the following command to install all required dependencies: pip install -r requirements.txt

Download the serviceAccountKey.json file into the project repository from google cloud. This file is necessary for accessing Google Cloud resources, such as connecting to Google Cloud SQL databases, using Gemini services, and other Google Cloud functionalities.

Run the Chainlit Application: chainlit run chainlit_app.py



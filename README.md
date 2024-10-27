Overview
Our project focuses on developing a comprehensive health and wellness chat assistant powered by large language models (LLMs) that can assist users across a variety of domains. The challenge we're addressing involves effectively utilizing LLMs' capabilities while avoiding hallucinations and misinformation. When LLMs have broad, unrestricted scopes, they tend to generate more inaccurate or irrelevant responses, and fine tuning them for each specific case requires large volumes of data and significant resources. Instructional prompting is a partial solution, but as the number of domains and instructions grows, it often results in overly generalized responses.

To overcome these limitations, we implemented a solution using "Agentic LLMs" a combination of narrowly focused LLMs, or agents, that specialize in distinct areas and can interact with each other. Each agent brings expertise in a specific domain, such as prescription management or patient education. These agents are supervised by a general agent capable of simplifying complex information and functioning as a standard agent, ensuring consistent guidance and support.


![image](https://github.com/user-attachments/assets/57e5cad1-20fc-4ae0-9c1b-31fdc95e853d)


Python >= 3.10

pip install -r requirements.txt

chainlit run chainlit_app.py



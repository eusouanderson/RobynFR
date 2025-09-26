from langchain_community.llms import OpenAI


def answer_question(text: str, question: str) -> str:
    llm = OpenAI(temperature=0)
    prompt = f'Texto do documento:\n{text}\n\nPergunta: {question}\nResposta:'
    return llm(prompt)

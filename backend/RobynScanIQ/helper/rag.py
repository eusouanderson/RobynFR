from google import genai

client = genai.Client()

def answer_question(text: str, question: str) -> str:
    """Responde a uma pergunta com base no texto fornecido usando o modelo Gemini."""
    system_prompt = "Você é um assistente útil. Responda perguntas com base no texto fornecido."
    user_prompt = f"Texto do documento:\n{text}\n\nPergunta: {question}\nResposta:"

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{system_prompt}\n\n{user_prompt}"
        )
        return response.text or "Nenhuma resposta gerada."

    except Exception as e:
        return f"Ocorreu um erro ao consultar o modelo Gemini: {str(e)}"


# Teste
# resposta = answer_question(
#     "Este é um texto de exemplo. A migração de LLM foi bem-sucedida.",
#     "Qual é o conteúdo do texto?"
# )
# print("Resposta do modelo:", resposta)

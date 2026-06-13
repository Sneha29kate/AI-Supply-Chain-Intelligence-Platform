import google.generativeai as genai

genai.configure(
    api_key="AQ.Ab8RN6J16kc-IjMxW-y07g0yc6wT3McIrdNjHCFCgoemeHRylA"
)

model = genai.GenerativeModel(
    "models/gemini-2.5-flash"
)

def ask_gemini(question, context):

    prompt = f"""
    Context:
    {context}

    Question:
    {question}

    Answer using the context above.
    """

    response = model.generate_content(prompt)

    return response.text
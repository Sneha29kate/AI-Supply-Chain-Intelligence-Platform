import google.generativeai as genai

genai.configure(
    api_key="YOUR_GEMINI_API_KEY"
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
import google.generativeai as genai

genai.configure(api_key="AQ.Ab8RN6J16kc-IjMxW-y07g0yc6wT3McIrdNjHCFCgoemeHRylA")

for model in genai.list_models():
    print(model.name)
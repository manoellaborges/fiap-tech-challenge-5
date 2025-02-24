import google.generativeai as genai

GEMINI_API_KEY = "AIzaSyCp0LgV00zXvpa7-N8DlKWLGPEW_A5FMVs"
genai.configure(api_key=GEMINI_API_KEY)

def extracts_keywords(text):
    """
    Envia o texto da notícia para a API do Gemini e retorna palavras-chave primárias e secundárias.
    """
    model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-01-21") #10RPM - API permite 10 requisições por minuto
    prompt = (
            "Extraia deste texto palavras chaves, separadas em palavras-chaves primárias e e palavras-chave secundárias, "
            "e as retorne no seguinte formato: \n"
            "Primárias: palavra1, palavra2, palavra3 \n"
            "Secundárias: palavra4, palavra5, palavra6 \n\n"
            f"Texto: {text}"
    )
    try:
        response = model.generate_content(prompt)
        if response and response.text:
            lines = response.text.split("\n")
            primary_keywords = []
            secondary_keywords = []

            for line in lines:
                if line.startswith("Primárias:"):
                    primary_keywords = [kw.strip() for kw in line.replace("Primárias:", "").split(",")]
                elif line.startswith("Secundárias:"):
                    secondary_keywords = [kw.strip() for kw in line.replace("Secundárias:", "").split(",")]
            return primary_keywords, secondary_keywords
    except Exception as e:
        print(f"Erro ao processar texto: {e}")
        return [], []
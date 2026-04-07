import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
from groq import Groq

# 1. CARREGAR VARIÁVEIS
load_dotenv(override=True)
api_key = os.getenv("GROQ_API_KEY")

# 2. TESTE DE SEGURANÇA (VER NO TERMINAL)
print("--- TESTE DE CONEXÃO ---")
if api_key:
    print(f"Chave detectada: {api_key[:10]}...{api_key[-4:]}")
else:
    print("ERRO CRÍTICO: Chave GROQ_API_KEY não encontrada no .env!")
print("------------------------")

# 3. INICIALIZAR CLIENTE E APP (ORDEM CORRETA)
client = Groq(api_key=api_key)
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

def extract_text_from_pdf(file):
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        print(f"Erro ao ler PDF: {e}")
        return ""

@app.route('/analyze', methods=['POST'])
def analyze():
    if 'resume' not in request.files:
        return jsonify({"error": "Currículo não enviado"}), 400
    
    job_description = request.form.get('job_description', '')
    resume_file = request.files['resume']
    resume_text = extract_text_from_pdf(resume_file)

    if not resume_text:
        return jsonify({"error": "Não foi possível extrair texto do PDF"}), 400

    prompt = f"""
    Atue como um Especialista em Recrutamento Tech e Auditor de ATS.
    Analise o currículo abaixo para a vaga: {job_description}
    Currículo: {resume_text}

    REGRAS: Retorne APENAS um JSON seguindo esta estrutura exata:
    {{
        "score_ats_geral": 0,
        "score_match_vaga": 0,
        "metricas_detalhadas": {{
            "otimizacao_palavras_chave": 0,
            "relevancia_competencias": 0,
            "legibilidade_ats": 0,
            "formatacao_estrutura": 0,
            "qualidade_experiencia": 0,
            "completude_secao": 0
        }},
        "analise_ats": {{
            "pontos_fortes": [],
            "pontos_melhoria": [],
            "o_que_remover": []
        }},
        "analise_vaga": {{
            "requisitos_atendidos": [],
            "requisitos_faltantes": [],
            "sugestao_tecnica": ""
        }},
        "curriculo_otimizado": {{
            "cabecalho": {{"nome": "", "contato": ""}},
            "resumo_profissional": "",
            "experiencia": [{{ "cargo": "", "empresa": "", "conquistas": [] }}],
            "educacao": [{{ "curso": "", "instituicao": "" }}],
            "certificacoes": [],
            "competencias_tecnicas": []
        }}
    }}
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"},
            max_tokens=4000
        )
        return completion.choices[0].message.content, 200, {'Content-Type': 'application/json'}
        
    except Exception as e:
        print(f"Erro na Groq: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)
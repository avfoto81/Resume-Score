import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
from groq import Groq

# 1. CARREGAR VARIÁVEIS (Ordem segura para Nuvem)
load_dotenv() 
api_key = os.getenv("GROQ_API_KEY")

# 2. TESTE DE SEGURANÇA (O print ajuda a debugar nos Logs do Space)
print("--- INICIANDO SERVIDOR ---")
if api_key:
    print(f"API Key carregada com sucesso!")
else:
    print("AVISO: GROQ_API_KEY não encontrada no .env ou Environment Variables!")
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
    Atue como um Especialista em Recrutamento Tech. 
    Sua tarefa é ser justo e preciso na calibração dos scores.

    CRITÉRIOS DE PONTUAÇÃO (Seja um Especialista Humano):
    1. ANÁLISE SEMÂNTICA: Não busque apenas palavras idênticas. Se a vaga pede 'Experiência com APIs' e o candidato cita 'Axios, Fetch ou REST', considere match total.
    2. PESO BASE: Se o candidato possui a stack principal (tecnologia chave), o score base deve ser entre 60% e 70%. 
    3. PONTOS EXTRAS: Use os 30% restantes para diferenciais como soft skills, tempo de experiência e certificações.

    Analise o currículo: {resume_text}
    Para a vaga: {job_description}

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
    max_tokens=4000,
    temperature=0.2  # <--- Adicione isso! 0.2 deixa a IA mais técnica e menos "criativa"
)
        return completion.choices[0].message.content, 200, {'Content-Type': 'application/json'}
        
    except Exception as e:
        print(f"Erro na Groq: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Ele tenta pegar a porta do sistema (Hugging Face usa 7860), se não achar, usa 8000
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
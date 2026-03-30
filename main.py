import os
from dotenv import load_dotenv # Precisa instalar: pip install python-dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import PyPDF2
from groq import Groq

load_dotenv() # Carrega as variáveis do arquivo .env
client = Groq(api_key=os.getenv("GROQ_API_KEY")) # Puxa o nome exato que está no .env

app = Flask(__name__)
# Configuração robusta de CORS
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

    # PROMPT CORRIGIDO (USANDO CHAVES DUPLAS PARA O JSON)
    # PROMPT DE ENGENHARIA CALIBRADO
    prompt = f"""
    Atue como um Especialista em Recrutamento Tech e Auditor de ATS (Sistemas de Rastreamento de Candidatos).
    Sua análise deve seguir os critérios de auditoria do mercado (como Evalzz e Jobscan).

    CRITÉRIOS DE AUDITORIA RIGOROSOS:
    1. Score ATS Geral (Estrutura):
       - Verifique se existem seções padrão: Experiência, Educação, Competências.
       - Penalize se houver tabelas, colunas complexas, imagens ou gráficos (ATS não lê bem).
       - Avalie a densidade: Currículos muito curtos ou "enrolados" perdem pontos.
    
    2. Score Match Vaga (Semântica):
       - Não busque apenas palavras idênticas. Busque SINÔNIMOS técnicos.
       - Ex: Se a vaga pede "React", e o currículo tem "Next.js" ou "Hooks", o match é alto.
       - Avalie o nível de senioridade: Se a vaga pede "Sênior" e o currículo é "Júnior", o match deve baixar drasticamente.

    3. Métricas Detalhadas (Calibração Evalzz):
       - otimizacao_palavras_chave: Frequência de termos técnicos da vaga no currículo.
       - qualidade_experiencia: Presença de NÚMEROS e RESULTADOS (ex: "aumentei em 20%", "reduzi custo"). Se não houver números, a nota não passa de 60%.
       - legibilidade_ats: Uso de fontes padrão e ausência de elementos gráficos.

    VAGA: {job_description}
    CURRÍCULO: {resume_text}

    REGRAS DE RETORNO:
    - Retorne APENAS o JSON.
    - Se a 'qualidade_experiencia' for baixa, justifique em 'pontos_melhoria'.
    - DIRETRIZES DE REESCRITA (CURRÍCULO IDEAL):
    1. Resumo Profissional: Deve ser um parágrafo de 3-4 linhas focado em RESULTADOS e com as 5 principais Keywords da vaga integradas organicamente.
    2. Experiência Profissional (MÉTODO STAR): 
       - Cada conquista DEVE começar com um Verbo de Ação forte (Ex: Desenvolvi, Liderança, Otimizei, Alavanquei).
       - Transforme tarefas em resultados quantificáveis. Se não houver números no original, use estimativas realistas (Ex: 'Melhoria na performance' vira 'Otimização de 30% na velocidade de carregamento').
    3. Competências Técnicas: Agrupe por categorias (Ex: Linguagens, Frameworks, Ferramentas) e coloque as mais relevantes da vaga NO INÍCIO da lista.
    4. Formatação: Use apenas texto limpo, sem caracteres especiais complexos que confundem o parser do ATS.
    REGRAS DE INTEGRIDADE DE DADOS:
    1. PROIBIDO OMITIR: Não remova nenhuma experiência profissional, formação acadêmica ou certificação que conste no currículo original.
    2. EXPANSÃO, NÃO SUPRESSÃO: O objetivo é melhorar a escrita, não deletar informações. Se o currículo original tem 5 experiências, o otimizado DEVE ter as mesmas 5.
    3. DETALHAMENTO DE CONQUISTAS: Se o usuário listou 3 responsabilidades em um cargo, transforme essas 3 em 3 conquistas no formato STAR. 
    4. PRESERVAÇÃO DE DATAS E LOCAIS: Mantenha exatamente as mesmas datas, empresas e instituições de ensino.

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
            "experiencia": [
                {{
                    "cargo": "",
                    "empresa": "",
                    "conquistas": []
                }}
            ],
            "educacao": [
                {{
                    "curso": "",
                    "instituicao": ""
                }}
            ],
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
            max_tokens=4000  # Garante que o JSON não seja cortado no meio
        )
        
        # Retornamos como Response do Flask para garantir o Header de JSON
        return completion.choices[0].message.content, 200, {'Content-Type': 'application/json'}
        
    except Exception as e:
        print(f"Erro na Groq: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=8000, debug=True)
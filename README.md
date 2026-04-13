![Astro](https://img.shields.io/badge/Astro-0D1117?style=for-the-badge&logo=astro&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Hugging Face](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-yellow)



📝 Resume Score AI - Analisador de Currículos com IA
O Resume Score AI é uma aplicação Full Stack de alta performance que utiliza Inteligência Artificial para realizar a triagem técnica de currículos. O sistema compara o perfil do candidato (PDF) com os requisitos de uma vaga de emprego, gerando scores de compatibilidade, análise de palavras-chave e sugestões de otimização para ATS (Applicant Tracking Systems).

🚀 Tecnologias Utilizadas
Frontend
Astro: Framework para performance e entrega de conteúdo otimizado.

React: Componentização da interface e gerenciamento de estados.

TypeScript: Garantia de tipagem e segurança no desenvolvimento.

Tailwind CSS: Estilização moderna e responsiva.

Vercel: Hospedagem e CI/CD do frontend.

Backend (API)
Python / Flask: API REST ágil e escalável para processamento de dados.

Groq Cloud (Llama-3.3-70b): Processamento de linguagem natural de baixíssima latência para análise semântica.

PyPDF2: Biblioteca para extração de texto de documentos PDF.

Gunicorn: Servidor de produção para o ambiente Python.

Docker: Containerização para garantir paridade entre ambientes.

Hugging Face Spaces: Infraestrutura de nuvem para o backend.

🛠️ Funcionalidades
Extração de Texto via PDF: Processamento automático de currículos.

Cálculo de Match Semântico: Avaliação baseada em contexto e não apenas em palavras idênticas.

Métricas de ATS: Pontuação detalhada sobre legibilidade, estrutura e competências.

Dicas de Otimização: Sugestões geradas pela IA para melhorar o alinhamento com a vaga.

Dashboard de Resultados: Visualização clara dos pontos fortes e gaps do candidato.

🏗️ Arquitetura do Sistema
O projeto foi estruturado seguindo boas práticas de desenvolvimento moderno:

Frontend: Desacoplado, consome a API de forma assíncrona.

Segurança: Uso de Variáveis de Ambiente e Secrets para proteção de chaves de API (evitando exposição no GitHub).

Escalabilidade: Backend containerizado com Docker, facilitando migrações e deploys.

💻 Como Rodar o Projeto
Backend
Clone o repositório.

Instale as dependências: pip install -r requirements.txt.

Configure a sua GROQ_API_KEY no arquivo .env.

Execute: python main.py.

Frontend
Instale as dependências: npm install.

Configure a PUBLIC_API_URL com o endereço do seu backend.

Inicie o projeto: npm run dev.

🛡️ Segurança e Boas Práticas
Este projeto implementa:

Git Push Protection para prevenir vazamento de credenciais.

CORS Policies para controle de acesso à API.

Clean Code com separação de responsabilidades.

👨‍💻 Autor
André Luiz Desenvolvedor Full Stack apaixonado por IA e automação. [https://www.linkedin.com/in/andreluizas/] | [https://meu-portfolio-dun-two.vercel.app/]
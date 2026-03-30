import React, { useState } from 'react';
import {
  CheckCircle2, AlertCircle, Target, Trash2, Zap,
  FileText, ArrowRight, ShieldCheck, Search, Printer, Loader2, BarChart3
} from 'lucide-react';

const Analyzer: React.FC = () => {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [jobDescription, setJobDescription] = useState('');
  const [file, setFile] = useState<File | null>(null);

  const handleAnalyze = async () => {
    if (!file || !jobDescription) {
      alert("Por favor, preencha a vaga e envie o PDF.");
      return;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_description', jobDescription);

    try {
      const response = await fetch('http://127.0.0.1:8000/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) throw new Error('Erro no servidor');

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Erro de conexão:", error);
      alert("Erro ao conectar. Verifique se o terminal do Python mostra erros.");
    } finally {
      setLoading(false);
    }
  };
  const style = (
  <style>
    {`
      @media print {
        /* Esconde absolutamente TUDO na página */
        body * {
          visibility: hidden !important;
        }
        /* Mostra apenas o que tiver a classe 'printable-cv' e seus filhos */
        .printable-cv, .printable-cv * {
          visibility: visible !important;
        }
        /* Posiciona o currículo no topo esquerdo da folha */
        .printable-cv {
          position: absolute !important;
          left: 0 !important;
          top: 0 !important;
          width: 100% !important;
          margin: 0 !important;
          padding: 0 !important;
          border: none !important;
          box-shadow: none !important;
        }
        /* Remove cabeçalhos e rodapés automáticos do navegador (título da página, data, etc) */
        @page {
          margin: 0;
        }
      }
    `}
  </style>
);

  if (!result) {
    return (
      <div className="max-w-3xl mx-auto bg-white p-10 rounded-[3rem] shadow-xl border border-slate-200 mt-10">
        <div className="space-y-6">
          <textarea
            className="w-full p-6 rounded-3xl border border-slate-100 bg-slate-50 outline-none focus:ring-2 focus:ring-blue-500 h-40 text-sm"
            placeholder="Cole a descrição da vaga aqui..."
            onChange={(e) => setJobDescription(e.target.value)}
          />
          <input
            type="file" accept=".pdf"
            onChange={(e) => setFile(e.target.files?.[0] || null)}
            className="w-full text-sm text-slate-500 file:mr-4 file:py-3 file:px-6 file:rounded-full file:border-0 file:bg-slate-900 file:text-white cursor-pointer"
          />
          <button
            onClick={handleAnalyze} disabled={loading}
            className="w-full bg-blue-600 text-white py-5 rounded-2xl font-black uppercase tracking-widest hover:bg-blue-700 transition-all flex items-center justify-center gap-2"
          >
            {loading ? <Loader2 className="animate-spin" /> : "Analisar Currículo"}
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto p-4 md:p-8 space-y-8 animate-in fade-in duration-700">
      {style} {/* Injeta o estilo de impressão aqui */}
      {/* ADICIONE 'print:hidden' AQUI */}
      <button
        onClick={() => setResult(null)}
        className="print:hidden text-[10px] font-black uppercase text-slate-400 hover:text-blue-600"
      >
        ← Nova Análise
      </button>

      {/* 1. SCORES PRINCIPAIS */}
      <div className="print:hidden grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white p-8 rounded-[2.5rem] border border-slate-200 relative overflow-hidden shadow-sm">
          <p className="text-slate-400 text-[10px] font-black uppercase tracking-widest mb-2">Saúde do Currículo (ATS)</p>
          <div className="flex items-baseline gap-2">
            <span className="text-7xl font-black text-slate-900">{result.score_ats_geral}</span>
            <span className="text-2xl font-bold text-slate-300">%</span>
          </div>
          <div className="mt-4 flex items-center gap-2 text-emerald-600 text-xs font-bold">
            <ShieldCheck size={16} /> Estrutura validada por IA
          </div>
        </div>

        <div className="bg-slate-900 p-8 rounded-[2.5rem] shadow-2xl relative overflow-hidden border border-slate-800">
          <p className="text-blue-400 text-[10px] font-black uppercase tracking-widest mb-2">Match com a Vaga</p>
          <div className="flex items-baseline gap-2 text-white">
            <span className="text-7xl font-black">{result.score_match_vaga}</span>
            <span className="text-2xl font-bold text-slate-500">%</span>
          </div>
          <p className="mt-4 text-xs text-slate-400 italic">"{result.analise_vaga?.sugestao_tecnica}"</p>
        </div>
      </div>

      {/* 2. OS 6 CARDS DETALHADOS */}
      <div className="print:hidden grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {[
          { label: "Palavras-Chave", val: result.metricas_detalhadas?.otimizacao_palavras_chave, icon: <Search size={14} /> },
          { label: "Competências", val: result.metricas_detalhadas?.relevancia_competencias, icon: <Zap size={14} /> },
          { label: "Legibilidade", val: result.metricas_detalhadas?.legibilidade_ats, icon: <FileText size={14} /> },
          { label: "Estrutura", val: result.metricas_detalhadas?.formatacao_estrutura, icon: <ShieldCheck size={14} /> },
          { label: "Experiência", val: result.metricas_detalhadas?.qualidade_experiencia, icon: <Target size={14} /> },
          { label: "Completude", val: result.metricas_detalhadas?.completude_secao, icon: <CheckCircle2 size={14} /> },
        ].map((m, i) => (
          <div key={i} className="bg-white p-5 rounded-[2rem] border border-slate-100 shadow-sm flex flex-col items-center text-center transition-all hover:shadow-md">
            <div className="text-blue-500 mb-3 bg-blue-50 p-2 rounded-xl">{m.icon}</div>
            <span className="text-xl font-black text-slate-900">{m.val ?? 0}%</span>
            <p className="text-[9px] font-black uppercase text-slate-400 tracking-tighter mt-1 leading-tight">{m.label}</p>
            <div className="w-full h-1.5 bg-slate-100 rounded-full mt-4 overflow-hidden">
              <div className="h-full bg-blue-500" style={{ width: `${m.val ?? 0}%` }} />
            </div>
          </div>
        ))}
      </div>

      {/* 3. PONTOS FORTES E FRACOS */}
      <div className="print:hidden grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-emerald-50/50 border border-emerald-100 p-8 rounded-[2.5rem]">
          <h4 className="text-emerald-800 font-black text-[10px] uppercase mb-4 tracking-widest">O que manter</h4>
          <ul className="space-y-3">
            {result.analise_ats?.pontos_fortes?.map((p: string, i: number) => (
              <li key={i} className="text-xs text-emerald-700 flex items-start gap-2 font-medium"><span>•</span> {p}</li>
            ))}
          </ul>
        </div>
        <div className="bg-red-50/50 border border-red-100 p-8 rounded-[2.5rem]">
          <h4 className="text-red-800 font-black text-[10px] uppercase mb-4 tracking-widest">O que ajustar</h4>
          <ul className="space-y-3">
            {result.analise_ats?.pontos_melhoria?.map((p: string, i: number) => (
              <li key={i} className="text-xs text-red-700 flex items-start gap-2 font-medium"><span>!</span> {p}</li>
            ))}
          </ul>
        </div>
      </div>

      {/* 4. CURRÍCULO REESCRITO (IDEAL) */}
      <div className="bg-white rounded-[3rem] border border-slate-200 p-10 md:p-16 shadow-sm relative mb-20 print:shadow-none print:border-0 print:p-0 print:m-0 print:rounded-none">
        <div className="absolute top-10 right-10 print:hidden">
          <button onClick={() => window.print()} className="p-3 bg-slate-100 rounded-full hover:bg-slate-200 transition-all">
          <Printer size={20} />
        </button>
        </div>

        <div className="max-w-2xl mx-auto">
          <h2 className="text-3xl font-bold text-center mb-2">{result.curriculo_otimizado?.cabecalho?.nome}</h2>
          <p className="text-center text-slate-500 text-sm mb-10 pb-10 border-b">{result.curriculo_otimizado?.cabecalho?.contato}</p>

          <section className="mb-8" print:break-inside-avoid>
            <h3 className="text-blue-600 font-black text-[10px] uppercase tracking-widest mb-3">Resumo Otimizado</h3>
            <p className="text-sm leading-relaxed text-slate-700 italic">
              {result.curriculo_otimizado?.resumo_profissional}
            </p>
          </section>

          <section className="mb-8" print:break-inside-avoid>
            <h3 className="text-blue-600 font-black text-[10px] uppercase tracking-widest mb-4">Experiência Profissional</h3>
            <div className="space-y-6">
              {result.curriculo_otimizado?.experiencia?.map((exp: any, i: number) => (
                <div key={i} className="group">
                  <p className="font-bold text-slate-900 text-sm">{exp.cargo} | <span className="font-medium text-slate-400">{exp.empresa}</span></p>
                  <ul className="mt-3 space-y-2">
                    {exp.conquistas?.map((c: string, j: number) => (
                      <li key={j} className="text-[13px] text-slate-600 leading-relaxed flex items-start gap-2">
                        <span className="text-blue-500 font-bold mt-1">•</span>
                        {c}
                      </li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </section>

          {/* Seção de Educação e Certificados */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mt-8 border-t pt-8">
            <section>
              <h3 className="text-blue-600 font-black text-[10px] uppercase tracking-widest mb-4">Educação</h3>
              {result.curriculo_otimizado?.educacao?.map((edu: any, i: number) => (
                <div key={i} className="mb-3">
                  <p className="font-bold text-slate-900 text-[13px]">{edu.curso}</p>
                  <p className="text-slate-500 text-xs">{edu.instituicao}</p>
                </div>
              ))}
            </section>

            <section>
              <h3 className="text-blue-600 font-black text-[10px] uppercase tracking-widest mb-4">Certificações</h3>
              <ul className="space-y-1">
                {result.curriculo_otimizado?.certificacoes?.map((cert: string, i: number) => (
                  <li key={i} className="text-[13px] text-slate-600">• {cert}</li>
                ))}
              </ul>
            </section>
          </div>

          {/* Seção extra de Skills que o Evalzz adora */}
          <section>
            <h3 className="text-blue-600 font-black text-[10px] uppercase tracking-widest mb-4">Competências Técnicas</h3>
            <div className="flex flex-wrap gap-2">
              {result.curriculo_otimizado?.competencias_tecnicas?.map((skill: string, i: number) => (
                <span key={i} className="px-3 py-1 bg-slate-50 border border-slate-100 rounded-lg text-[11px] font-bold text-slate-600">
                  {skill}
                </span>
              ))}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};

export default Analyzer;
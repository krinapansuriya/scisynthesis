import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../lib/api';

const ProjectAdvancedPage: React.FC = () => {
  const { projectId } = useParams<{ projectId: string }>();
  const [activeTab, setActiveTab] = useState('chat');
  const [papers, setPapers] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  
  // Chat state
  const [chatQuery, setChatQuery] = useState('');
  const [chatHistory, setChatHistory] = useState<any[]>([]);

  // Citations state
  const [citationPaperId, setCitationPaperId] = useState<number | ''>('');
  const [citationStyle, setCitationStyle] = useState('APA');
  const [citationResult, setCitationResult] = useState<string>('');

  // Keywords state
  const [keywordPaperId, setKeywordPaperId] = useState<number | ''>('');
  const [keywordResult, setKeywordResult] = useState<any>(null);

  // Similar Papers state
  const [similarPaperId, setSimilarPaperId] = useState<number | ''>('');
  const [similarResult, setSimilarResult] = useState<any[]>([]);

  useEffect(() => {
    fetchProject();
  }, [projectId]);

  const fetchProject = async () => {
    try {
      const res = await api.get(`/projects/${projectId}`);
      setPapers(res.data.papers || []);
    } catch {
      console.error('Failed to fetch project');
    }
  };

  const handleChat = async () => {
    if (!chatQuery) return;
    const currentQ = chatQuery;
    setChatQuery('');
    setChatHistory([...chatHistory, { type: 'user', text: currentQ }]);
    setLoading(true);
    try {
      const res = await api.post('/analysis/query', {
        query: currentQ,
        paper_ids: papers.map(p => p.id)
      });
      setChatHistory(prev => [...prev, { type: 'ai', data: res.data }]);
    } catch {
      console.error('Request failed');
      setChatHistory(prev => [...prev, { type: 'error', text: 'Failed to fetch response' }]);
    }
    setLoading(false);
  };

  const handleCompare = async () => {
    setLoading(true);
    try {
      const res = await api.post('/analysis/advanced/compare-papers', {
        paper_ids: papers.map(p => p.id)
      });
      setResult(res.data);
    } catch {
      console.error('Request failed');
      alert('Requires at least 2 papers');
    }
    setLoading(false);
  };

  const handleHypothesis = async () => {
    setLoading(true);
    try {
      const res = await api.post('/analysis/advanced/generate-hypothesis', {
        topic: 'General findings from this project',
        paper_ids: papers.map(p => p.id)
      });
      setResult(res.data);
    } catch {
      console.error('Request failed');
    }
    setLoading(false);
  };

  const handleIdeas = async () => {
    setLoading(true);
    try {
      const res = await api.post('/analysis/advanced/project-ideas', {
        paper_ids: papers.map(p => p.id)
      });
      setResult(res.data);
    } catch {
      console.error('Request failed');
    }
    setLoading(false);
  };

  const handleCitation = async () => {
    if (!citationPaperId) return;
    setLoading(true);
    setCitationResult('');
    try {
      const paper = papers.find(p => p.id === citationPaperId);
      const res = await api.post('/analysis/advanced/citation', {
        paper_id: citationPaperId,
        title: paper?.title || 'Unknown Title',
        style: citationStyle
      });
      setCitationResult(res.data.citation || JSON.stringify(res.data));
    } catch {
      console.error('Request failed');
      alert('Citation generation failed');
    }
    setLoading(false);
  };

  const handleKeywords = async () => {
    if (!keywordPaperId) return;
    setLoading(true);
    setKeywordResult(null);
    try {
      const res = await api.get(`/analysis/advanced/keywords/${keywordPaperId}`);
      setKeywordResult(res.data);
    } catch {
      console.error('Request failed');
      alert('Keyword extraction failed');
    }
    setLoading(false);
  };

  const handleSimilar = async () => {
    if (!similarPaperId) return;
    setLoading(true);
    setSimilarResult([]);
    try {
      const res = await api.get(`/analysis/advanced/similar/${similarPaperId}`);
      const recs = res.data.recommendations || res.data.similar_papers || res.data || [];
      if (recs.length === 0) {
        alert('No similar papers found. Upload more papers to this project to enable similarity search.');
      }
      setSimilarResult(recs);
    } catch (err) {
      const e = err as { response?: { data?: { detail?: string } } };
      const msg = e?.response?.data?.detail || 'Similar paper search failed';
      alert(msg);
    }
    setLoading(false);
  };

  const handleCluster = async () => {
    setLoading(true);
    try {
      const res = await api.post('/analysis/advanced/cluster-papers', {
        paper_ids: papers.map(p => p.id),
        n_clusters: 3
      });
      setResult(res.data);
    } catch {
      console.error('Request failed');
      alert('Requires at least 3 papers');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex">
      {/* Sidebar */}
      <div className="w-64 bg-white border-r p-4 flex flex-col gap-2">
        <Link to={`/projects/${projectId}`} className="text-blue-600 mb-4 hover:underline">
          &larr; Back to Project
        </Link>
        <h2 className="font-bold text-lg mb-2">Advanced Tools</h2>
        <button type="button" className={`p-2 text-left rounded ${activeTab === 'chat' ? 'bg-blue-100 text-blue-800' : 'hover:bg-gray-100'}`} onClick={() => { setActiveTab('chat'); setResult(null); }}>
          RAG Chat
        </button>
        <button type="button" className={`p-2 text-left rounded ${activeTab === 'compare' ? 'bg-blue-100 text-blue-800' : 'hover:bg-gray-100'}`} onClick={() => { setActiveTab('compare'); setResult(null); }}>
          Compare Papers
        </button>
        <button type="button" className={`p-2 text-left rounded ${activeTab === 'hypothesis' ? 'bg-blue-100 text-blue-800' : 'hover:bg-gray-100'}`} onClick={() => { setActiveTab('hypothesis'); setResult(null); }}>
          Hypothesis Generator
        </button>
        <button type="button" className={`p-2 text-left rounded ${activeTab === 'ideas' ? 'bg-blue-100 text-blue-800' : 'hover:bg-gray-100'}`} onClick={() => { setActiveTab('ideas'); setResult(null); }}>
          Project Ideas
        </button>
        <button type="button" className={`p-2 text-left rounded ${activeTab === 'cluster' ? 'bg-blue-100 text-blue-800' : 'hover:bg-gray-100'}`} onClick={() => { setActiveTab('cluster'); setResult(null); }}>
          Semantic Clustering
        </button>
        <div className="border-t border-gray-200 my-2" />
        <p className="text-[10px] font-bold text-gray-400 uppercase tracking-widest px-2 mb-1">Advanced</p>
        <button type="button" className={`p-2 text-left rounded ${activeTab === 'citations' ? 'bg-blue-100 text-blue-800' : 'hover:bg-gray-100'}`} onClick={() => { setActiveTab('citations'); setResult(null); setCitationResult(''); }}>
          Citations
        </button>
        <button type="button" className={`p-2 text-left rounded ${activeTab === 'keywords' ? 'bg-blue-100 text-blue-800' : 'hover:bg-gray-100'}`} onClick={() => { setActiveTab('keywords'); setResult(null); setKeywordResult(null); }}>
          Keywords
        </button>
        <button type="button" className={`p-2 text-left rounded ${activeTab === 'similar' ? 'bg-blue-100 text-blue-800' : 'hover:bg-gray-100'}`} onClick={() => { setActiveTab('similar'); setResult(null); setSimilarResult([]); }}>
          Similar Papers
        </button>
      </div>

      {/* Main Content */}
      <div className="flex-1 p-8 overflow-y-auto">
        {activeTab === 'chat' && (
          <div className="max-w-3xl mx-auto flex flex-col h-full">
            <h1 className="text-2xl font-bold mb-4">Project RAG Chat</h1>
            <div className="flex-1 bg-white p-4 rounded-lg shadow-sm border mb-4 overflow-y-auto min-h-[400px]">
              {chatHistory.length === 0 && <p className="text-gray-500 text-center mt-10">Ask a question about your project's papers.</p>}
              {chatHistory.map((msg, i) => (
                <div key={i} className={`mb-4 ${msg.type === 'user' ? 'text-right' : 'text-left'}`}>
                  <div className={`inline-block p-3 rounded-lg max-w-[80%] ${msg.type === 'user' ? 'bg-blue-600 text-white' : msg.type === 'error' ? 'bg-red-100 text-red-800' : 'bg-gray-100 text-gray-800'}`}>
                    {msg.type === 'user' || msg.type === 'error' ? msg.text : (
                      <div>
                        <p className="whitespace-pre-wrap">{msg.data.answer}</p>
                        {msg.data.sources && msg.data.sources.length > 0 && (
                          <div className="mt-3 text-xs border-t border-gray-300 pt-2">
                            <span className="font-semibold text-green-700">Confidence: {(msg.data.confidence * 100).toFixed(1)}%</span>
                            <p className="italic mt-1 text-gray-600 mb-2">"{msg.data.explanation}"</p>
                            <span className="font-bold">Sources:</span>
                            <ul className="list-disc pl-4 mt-1">
                              {msg.data.sources.map((src: any, idx: number) => (
                                <li key={idx} className="mb-1" title={src.text_snippet}>
                                  [ChunkID: {src.chunk_id}] (Paper {src.paper_id}, Pg {src.page_number}) - Match: {(src.relevance_score * 100).toFixed(1)}%
                                </li>
                              ))}
                            </ul>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {loading && <div className="text-center text-gray-500">AI is thinking...</div>}
            </div>
            <div className="flex gap-2">
              <input type="text" value={chatQuery} onChange={(e) => setChatQuery(e.target.value)} onKeyDown={(e) => e.key === 'Enter' && handleChat()} className="flex-1 border p-3 rounded-lg" placeholder="Ask about methods, findings, etc..." />
              <button type="button" onClick={handleChat} disabled={loading} className="bg-blue-600 text-white px-6 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50">Send</button>
            </div>
          </div>
        )}

        {activeTab === 'citations' && (
          <div className="max-w-2xl mx-auto">
            <h1 className="text-2xl font-bold mb-6">Citation Generator</h1>
            <div className="bg-white p-6 rounded-lg border shadow-sm space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Select Paper</label>
                <select
                  title="Select paper for citation"
                  value={citationPaperId}
                  onChange={e => setCitationPaperId(Number(e.target.value) || '')}
                  className="w-full border p-2 rounded-lg bg-gray-50 text-sm"
                >
                  <option value="">-- Choose a paper --</option>
                  {papers.map(p => <option key={p.id} value={p.id}>{p.title}</option>)}
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Citation Style</label>
                <div className="flex gap-2">
                  {['APA', 'IEEE', 'MLA'].map(style => (
                    <button
                      type="button"
                      key={style}
                      onClick={() => setCitationStyle(style)}
                      className={`px-4 py-2 rounded-lg text-sm font-semibold border transition-colors ${citationStyle === style ? 'bg-blue-600 text-white border-blue-600' : 'bg-white text-gray-600 border-gray-200 hover:border-blue-400'}`}
                    >
                      {style}
                    </button>
                  ))}
                </div>
              </div>
              <button
                type="button"
                onClick={handleCitation}
                disabled={loading || !citationPaperId}
                className="w-full bg-blue-600 text-white py-2 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Generating...' : `Generate ${citationStyle} Citation`}
              </button>
              {citationResult && (
                <div className="mt-4 p-4 bg-gray-50 border rounded-lg relative">
                  <p className="text-sm font-mono text-gray-800 whitespace-pre-wrap leading-relaxed">{citationResult}</p>
                  <button
                    type="button"
                    onClick={() => navigator.clipboard.writeText(citationResult)}
                    className="mt-3 text-xs text-blue-600 hover:underline font-medium"
                  >
                    Copy to clipboard
                  </button>
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'keywords' && (
          <div className="max-w-2xl mx-auto">
            <h1 className="text-2xl font-bold mb-6">Keyword Extraction</h1>
            <div className="bg-white p-6 rounded-lg border shadow-sm space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Select Paper</label>
                <select
                  title="Select paper for keyword extraction"
                  value={keywordPaperId}
                  onChange={e => setKeywordPaperId(Number(e.target.value) || '')}
                  className="w-full border p-2 rounded-lg bg-gray-50 text-sm"
                >
                  <option value="">-- Choose a paper --</option>
                  {papers.map(p => <option key={p.id} value={p.id}>{p.title}</option>)}
                </select>
              </div>
              <button
                type="button"
                onClick={handleKeywords}
                disabled={loading || !keywordPaperId}
                className="w-full bg-blue-600 text-white py-2 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Extracting...' : 'Extract Keywords'}
              </button>
              {keywordResult && (
                <div className="mt-4 space-y-4">
                  {keywordResult.keywords && (
                    <div>
                      <h3 className="font-semibold text-gray-800 mb-2">Keywords</h3>
                      <div className="flex flex-wrap gap-2">
                        {keywordResult.keywords.map((kw: string, i: number) => (
                          <span key={i} className="px-3 py-1 bg-blue-100 text-blue-800 text-sm rounded-full font-medium">{kw}</span>
                        ))}
                      </div>
                    </div>
                  )}
                  {keywordResult.themes && (
                    <div>
                      <h3 className="font-semibold text-gray-800 mb-2">Themes</h3>
                      <div className="flex flex-wrap gap-2">
                        {keywordResult.themes.map((t: string, i: number) => (
                          <span key={i} className="px-3 py-1 bg-gray-100 text-gray-700 text-sm rounded-full font-medium">{t}</span>
                        ))}
                      </div>
                    </div>
                  )}
                  {keywordResult.technical_terms && (
                    <div>
                      <h3 className="font-semibold text-gray-800 mb-2">Technical Terms</h3>
                      <div className="flex flex-wrap gap-2">
                        {keywordResult.technical_terms.map((t: string, i: number) => (
                          <span key={i} className="px-3 py-1 bg-green-100 text-green-800 text-sm rounded-full font-medium">{t}</span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        {activeTab === 'similar' && (
          <div className="max-w-2xl mx-auto">
            <h1 className="text-2xl font-bold mb-6">Similar Papers</h1>
            <div className="bg-white p-6 rounded-lg border shadow-sm space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Select Source Paper</label>
                <select
                  title="Select paper to find similar papers"
                  value={similarPaperId}
                  onChange={e => setSimilarPaperId(Number(e.target.value) || '')}
                  className="w-full border p-2 rounded-lg bg-gray-50 text-sm"
                >
                  <option value="">-- Choose a paper --</option>
                  {papers.map(p => <option key={p.id} value={p.id}>{p.title}</option>)}
                </select>
              </div>
              <button
                type="button"
                onClick={handleSimilar}
                disabled={loading || !similarPaperId}
                className="w-full bg-blue-600 text-white py-2 rounded-lg font-medium hover:bg-blue-700 disabled:opacity-50"
              >
                {loading ? 'Searching...' : 'Find Similar Papers'}
              </button>
              {similarResult.length > 0 && (
                <div className="mt-4 space-y-3">
                  <h3 className="font-semibold text-gray-800">Semantically Similar Papers</h3>
                  {similarResult.map((paper: any, i: number) => (
                    <div key={i} className="p-4 border rounded-lg bg-gray-50 hover:bg-white transition-colors">
                      <div className="flex items-start justify-between gap-2">
                        <p className="font-medium text-gray-800 text-sm">{paper.title || `Paper ID: ${paper.id}`}</p>
                        {paper.similarity_score !== undefined && (
                          <span className="shrink-0 text-xs font-bold text-blue-600 bg-blue-100 px-2 py-1 rounded-full">
                            {(paper.similarity_score * 100).toFixed(1)}% match
                          </span>
                        )}
                      </div>
                      {paper.research_topic && <p className="text-xs text-gray-500 mt-1">{paper.research_topic}</p>}
                    </div>
                  ))}
                </div>
              )}
              {!loading && similarResult.length === 0 && similarPaperId && (
                <p className="text-center text-gray-400 text-sm py-4">Run the search to find similar papers.</p>
              )}
            </div>
          </div>
        )}

        {activeTab !== 'chat' && activeTab !== 'citations' && activeTab !== 'keywords' && activeTab !== 'similar' && (
          <div className="max-w-4xl mx-auto">
            <div className="flex justify-between items-center mb-6">
              <h1 className="text-2xl font-bold capitalize">{activeTab.replace('-', ' ')}</h1>
              <button type="button" onClick={() => {
                if (activeTab === 'compare') handleCompare();
                if (activeTab === 'hypothesis') handleHypothesis();
                if (activeTab === 'ideas') handleIdeas();
                if (activeTab === 'cluster') handleCluster();
              }} disabled={loading || papers.length === 0} className="bg-blue-600 text-white px-4 py-2 rounded shadow hover:bg-blue-700 disabled:opacity-50">
                {loading ? 'Processing...' : 'Run Analysis'}
              </button>
            </div>

            {loading && <p className="text-gray-500">Generating advanced insights, please wait...</p>}

            {!loading && result && (
              <div className="bg-white p-6 rounded-lg shadow-sm border">
                {activeTab === 'compare' && (
                  <div>
                    <h3 className="font-bold text-xl mb-4">Comparison Table</h3>
                    <div className="overflow-x-auto">
                      <table className="w-full text-left border-collapse">
                        <thead>
                          <tr className="bg-gray-100">
                            <th className="p-2 border">Paper</th>
                            <th className="p-2 border">Methodology</th>
                            <th className="p-2 border">Results</th>
                            <th className="p-2 border">Contributions</th>
                          </tr>
                        </thead>
                        <tbody>
                          {result.comparison_table?.map((row: any, i: number) => (
                            <tr key={i}>
                              <td className="p-2 border font-medium">{row.paper_title}</td>
                              <td className="p-2 border text-sm">{row.methodology}</td>
                              <td className="p-2 border text-sm">{row.results}</td>
                              <td className="p-2 border text-sm">{row.key_contributions}</td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                    <h3 className="font-bold text-xl mt-6 mb-2">Key Insights</h3>
                    <ul className="list-disc pl-5">
                      {result.bullet_insights?.map((bullet: string, i: number) => <li key={i} className="mb-1">{bullet}</li>)}
                    </ul>
                  </div>
                )}

                {activeTab === 'hypothesis' && (
                  <div>
                    <h3 className="font-bold text-xl mb-4">Novel Hypotheses</h3>
                    <div className="grid gap-4 mb-6">
                      {result.hypotheses?.map((hyp: any, i: number) => (
                        <div key={i} className="bg-blue-50 p-4 rounded border border-blue-100">
                          <p className="font-bold text-lg text-blue-900">{hyp.hypothesis}</p>
                          <p className="mt-2 text-sm"><strong>Reasoning:</strong> {hyp.reasoning}</p>
                          <p className="mt-2 text-sm"><strong>How to Test:</strong> {hyp.how_to_test}</p>
                        </div>
                      ))}
                    </div>
                    <h3 className="font-bold text-xl mb-2">Research Gaps</h3>
                    <ul className="list-disc pl-5 mb-6">
                      {result.research_gaps?.map((gap: string, i: number) => <li key={i} className="mb-1">{gap}</li>)}
                    </ul>
                    <h3 className="font-bold text-xl mb-2">Future Directions</h3>
                    <ul className="list-disc pl-5">
                      {result.future_directions?.map((dir: string, i: number) => <li key={i} className="mb-1">{dir}</li>)}
                    </ul>
                  </div>
                )}

                {activeTab === 'ideas' && (
                  <div className="grid gap-6">
                    {result.ideas?.map((idea: any, i: number) => (
                      <div key={i} className="border p-5 rounded-lg shadow-sm">
                        <h3 className="font-bold text-xl text-gray-800">{idea.title}</h3>
                        <span className="inline-block bg-gray-200 text-gray-800 text-xs px-2 py-1 rounded mt-1 mb-3">For {idea.target_audience}</span>
                        <p className="mb-2"><strong>Problem:</strong> {idea.problem}</p>
                        <p className="mb-2"><strong>Architecture:</strong> {idea.architecture}</p>
                        <p className="mb-2"><strong>Tech Stack:</strong> {idea.tech_stack?.join(', ')}</p>
                        <div>
                          <strong>Implementation Steps:</strong>
                          <ol className="list-decimal pl-5 mt-1 text-sm">
                            {idea.implementation_steps?.map((step: string, j: number) => <li key={j}>{step}</li>)}
                          </ol>
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {activeTab === 'cluster' && (
                  <div>
                    <h3 className="font-bold text-xl mb-4">Semantic Clusters</h3>
                    <div className="grid gap-4 grid-cols-1 md:grid-cols-2">
                      {result.clusters?.map((cluster: any, i: number) => (
                        <div key={i} className="border p-4 rounded-lg bg-green-50 border-green-200">
                          <h4 className="font-bold text-lg text-green-900 mb-2">{cluster.label}</h4>
                          <ul className="list-disc pl-4 text-sm">
                            {cluster.paper_ids.map((pid: number) => {
                              const p = papers.find(x => x.id === pid);
                              return <li key={pid} className="mb-1">{p ? p.title : `Paper ID: ${pid}`}</li>
                            })}
                          </ul>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default ProjectAdvancedPage;

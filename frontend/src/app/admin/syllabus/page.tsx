'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { BrainCircuit, ChevronRight, Upload, Plus, CheckCircle2 } from 'lucide-react';

export default function AdminSyllabusPage() {
  const [tree, setTree] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [importModal, setImportModal] = useState(false);
  const [jsonInput, setJsonInput] = useState('');
  const [importing, setImporting] = useState(false);

  const fetchTree = () => {
    apiRequest('/syllabus/tree')
      .then((res) => setTree(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchTree();
  }, []);

  const handleImport = async (e: React.FormEvent) => {
    e.preventDefault();
    setImporting(true);

    try {
      const parsed = JSON.parse(jsonInput);
      await apiRequest('/syllabus/import', {
        method: 'POST',
        body: JSON.stringify(Array.isArray(parsed) ? parsed : [parsed]),
      });
      alert('Imported syllabus nodes successfully!');
      setImportModal(false);
      fetchTree();
    } catch (err: any) {
      alert(err.message || 'Invalid JSON format');
    } finally {
      setImporting(false);
    }
  };

  const renderNode = (node: any, level = 0) => {
    return (
      <div key={node.id} className="space-y-2">
        <div 
          className="p-3 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-between text-xs hover:border-slate-700 transition-colors"
          style={{ marginLeft: `${level * 20}px` }}
        >
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-800 text-teal-300 border border-slate-700 font-mono">
              {node.type}
            </span>
            <span className="font-bold text-white">{node.title}</span>
            <span className="text-slate-500 font-mono">({node.code})</span>
          </div>

          {node.prerequisites && node.prerequisites.length > 0 && (
            <div className="text-[11px] text-amber-300">
              Prereqs: {node.prerequisites.join(', ')}
            </div>
          )}
        </div>

        {node.children && node.children.map((child: any) => renderNode(child, level + 1))}
      </div>
    );
  };

  return (
    <div className="flex-1 pb-16">
      <Navbar title="Curriculum &amp; DAG Hierarchy" subtitle="Hierarchical syllabus architecture and prerequisite dependency graph" />

      <div className="p-6 max-w-5xl mx-auto space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-lg font-bold text-white">Curriculum Knowledge Graph</h2>
            <p className="text-xs text-slate-400">Board &gt; Class &gt; Subject &gt; Chapter &gt; Topic (with Directed Acyclic Graph prerequisites)</p>
          </div>

          <button
            onClick={() => setImportModal(true)}
            className="py-2 px-3.5 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 text-xs flex items-center gap-1.5"
          >
            <Upload className="h-3.5 w-3.5" /> Import JSON / CSV
          </button>
        </div>

        {loading ? (
          <div className="p-12 text-center text-slate-400 text-sm">Loading syllabus tree...</div>
        ) : tree.length === 0 ? (
          <div className="p-12 rounded-2xl bg-[#162235] border border-slate-800 text-center text-slate-400 text-sm">
            No curriculum nodes defined.
          </div>
        ) : (
          <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-3">
            {tree.map((node) => renderNode(node))}
          </div>
        )}

        {/* Modal */}
        {importModal && (
          <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-[#162235] border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-base font-bold text-white">Import Curriculum Nodes</h3>
                <button onClick={() => setImportModal(false)} className="text-slate-400 hover:text-white">✕</button>
              </div>

              <form onSubmit={handleImport} className="space-y-4">
                <textarea
                  rows={8}
                  required
                  value={jsonInput}
                  onChange={(e) => setJsonInput(e.target.value)}
                  placeholder='[{"type": "TOPIC", "title": "...", "code": "TOP-1", "prerequisites": []}]'
                  className="w-full p-3 bg-slate-900 border border-slate-700 rounded-xl font-mono text-xs text-white focus:outline-none focus:border-teal-500"
                />

                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setImportModal(false)}
                    className="w-1/2 py-2 rounded-xl border border-slate-700 text-xs text-slate-300 hover:bg-slate-800"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={importing}
                    className="w-1/2 py-2 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 text-xs"
                  >
                    {importing ? 'Importing...' : 'Confirm Import'}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

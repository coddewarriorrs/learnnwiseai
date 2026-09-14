'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { BrainCircuit, ChevronRight, CheckCircle2, AlertTriangle, ArrowRight } from 'lucide-react';
import Link from 'next/link';

export default function StudentSyllabusPage() {
  const [tree, setTree] = useState<any[]>([]);
  const [masteries, setMasteries] = useState<Record<number, any>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      apiRequest('/syllabus/tree'),
      apiRequest('/students/me/mastery').catch(() => ({ topics: [] }))
    ])
      .then(([treeData, masteryData]) => {
        setTree(treeData);
        const map: Record<number, any> = {};
        if (masteryData && masteryData.topics) {
          masteryData.topics.forEach((t: any) => {
            map[t.topic_id] = t;
          });
        }
        setMasteries(map);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const renderNode = (node: any, level = 0) => {
    const isTopic = node.type === 'TOPIC';
    const mastery = isTopic ? masteries[node.id] : null;

    return (
      <div key={node.id} className="space-y-2">
        <div 
          className={`p-4 rounded-xl border transition-all flex items-center justify-between text-xs ${
            level === 0 ? 'bg-[#162235] border-slate-700' : 'bg-slate-900 border-slate-800'
          }`}
          style={{ marginLeft: `${level * 16}px` }}
        >
          <div className="flex items-center gap-3">
            <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-slate-800 text-teal-300 border border-slate-700 font-mono">
              {node.type}
            </span>
            <span className="font-bold text-white text-sm">{node.title}</span>
            <span className="text-slate-500 font-mono text-[11px]">({node.code})</span>
          </div>

          <div className="flex items-center gap-3">
            {mastery ? (
              <div className="flex items-center gap-2">
                <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${
                  mastery.status === 'CRITICAL' ? 'bg-rose-500/15 text-rose-300 border-rose-500/30' :
                  mastery.status === 'STRONG' ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30' :
                  'bg-amber-500/15 text-amber-300 border-amber-500/30'
                }`}>
                  {mastery.mastery_score}% {mastery.status.replace('_', ' ')}
                </span>
                <Link
                  href="/student/practice"
                  className="py-1 px-2.5 rounded-lg bg-teal-500/15 text-teal-300 border border-teal-500/30 font-semibold text-[11px] hover:bg-teal-500/25"
                >
                  Practice
                </Link>
              </div>
            ) : isTopic ? (
              <Link
                href="/student/practice"
                className="py-1 px-2.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 font-semibold text-[11px]"
              >
                Diagnostic Quiz
              </Link>
            ) : null}
          </div>
        </div>

        {node.children && node.children.map((child: any) => renderNode(child, level + 1))}
      </div>
    );
  };

  return (
    <div className="flex-1 pb-16">
      <Navbar title="Curriculum Syllabus &amp; Mastery Map" subtitle="Full syllabus breakdown aligned with your concept mastery" />

      <div className="p-6 max-w-5xl mx-auto space-y-6">
        {loading ? (
          <div className="p-12 text-center text-slate-400 text-sm">Loading curriculum syllabus...</div>
        ) : tree.length === 0 ? (
          <div className="p-12 rounded-2xl bg-[#162235] border border-slate-800 text-center text-slate-400 text-sm">
            No syllabus data available.
          </div>
        ) : (
          <div className="space-y-3">
            {tree.map((node) => renderNode(node))}
          </div>
        )}
      </div>
    </div>
  );
}

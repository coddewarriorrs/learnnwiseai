'use client';

import React, { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { apiRequest } from '@/lib/api';
import { ShieldCheck, CheckCircle2 } from 'lucide-react';

export default function ParentProgressPage() {
  const { id } = useParams();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!id) return;
    apiRequest(`/students/parent/progress/${id}`)
      .then((res) => setData(res))
      .catch((err) => setError(err.message || 'Unable to load progress record'))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div className="min-h-screen bg-[#0B1220] flex items-center justify-center text-slate-400 text-sm">
        Loading student progress report...
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="min-h-screen bg-[#0B1220] flex items-center justify-center p-6 text-center text-slate-400 text-sm">
        {error || 'Student report not found.'}
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0B1220] text-slate-100 py-10 px-6">
      <div className="max-w-3xl mx-auto space-y-6">
        <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <ShieldCheck className="h-5 w-5 text-teal-400" />
              <span className="text-xs font-bold uppercase tracking-wider text-teal-400">Parent Portal</span>
            </div>
            <h1 className="text-2xl font-bold text-white">{data.student_name}'s Progress</h1>
            <p className="text-xs text-slate-400 mt-0.5">{data.grade} Academic Insights & Concept Tracking</p>
          </div>
          <div className="text-right">
            <span className="text-xs text-slate-400 block">Overall Mastery</span>
            <span className="text-3xl font-extrabold text-teal-400">{data.overall_progress_score}%</span>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="p-5 rounded-xl bg-[#162235] border border-slate-800">
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Academic Status</h3>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                data.risk_level === 'HIGH' ? 'bg-rose-500/20 text-rose-300 border-rose-500/30' :
                data.risk_level === 'MEDIUM' ? 'bg-amber-500/20 text-amber-300 border-amber-500/30' :
                'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
              }`}>
                {data.risk_level} ATTENTION
              </span>
            </div>
            <ul className="space-y-1.5 mt-3">
              {data.risk_summary.map((r: string, idx: number) => (
                <li key={idx} className="text-xs text-slate-300 flex items-start gap-2">
                  <span className="text-teal-400 font-bold">•</span> {r}
                </li>
              ))}
            </ul>
          </div>

          <div className="p-5 rounded-xl bg-[#162235] border border-slate-800">
            <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider mb-2">Strengths & Mastered Concepts</h3>
            <div className="flex flex-wrap gap-1.5 mt-3">
              {data.strengths.map((s: string, idx: number) => (
                <span key={idx} className="text-xs bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 px-2.5 py-1 rounded-lg flex items-center gap-1.5">
                  <CheckCircle2 className="h-3 w-3" /> {s}
                </span>
              ))}
            </div>
          </div>
        </div>

        <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800">
          <h3 className="text-sm font-bold text-white mb-3">Teacher Interventions & Action Plan</h3>
          {data.active_interventions.length === 0 ? (
            <p className="text-xs text-slate-400">No active interventions required. Learning pace is steady!</p>
          ) : (
            <div className="space-y-3">
              {data.active_interventions.map((item: any, idx: number) => (
                <div key={idx} className="p-3.5 rounded-lg bg-slate-900 border border-slate-800">
                  <div className="flex justify-between items-center mb-1">
                    <span className="text-xs font-semibold text-teal-300">{item.action}</span>
                    <span className="text-[10px] text-slate-400 capitalize">{item.status.toLowerCase()}</span>
                  </div>
                  <p className="text-xs text-slate-400">{item.reason}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        <p className="text-center text-[11px] text-slate-500">
          This portal provides parent-authorized progress summaries. Private student Socratic tutor dialogues remain strictly confidential.
        </p>
      </div>
    </div>
  );
}

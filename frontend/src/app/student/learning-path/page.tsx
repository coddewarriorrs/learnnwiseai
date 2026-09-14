'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { BrainCircuit, CheckCircle2, AlertTriangle, ArrowRight, BookOpen, Target, Sparkles } from 'lucide-react';
import Link from 'next/link';

export default function LearningPathPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiRequest('/students/me/learning-path')
      .then((res) => setData(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex-1">
        <Navbar title="Personalized Learning Path" subtitle="Synthesizing prerequisite DAG sequence..." />
        <div className="p-8 text-center text-slate-400 text-sm">Computing adaptive recovery sequence...</div>
      </div>
    );
  }

  return (
    <div className="flex-1 pb-16">
      <Navbar 
        title="Personalized Learning Path" 
        subtitle="Dynamic curriculum graph sequence tailored to your prerequisite gap diagnosis" 
      />

      <div className="p-6 max-w-4xl mx-auto space-y-6">
        {/* Header telemetry */}
        <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-1.5">
              <BrainCircuit className="h-5 w-5 text-teal-400" />
              <span className="text-xs font-bold uppercase tracking-wider text-teal-400">Target Focus</span>
            </div>
            <h2 className="text-xl font-bold text-white">{data?.current_focus_topic}</h2>
            <p className="text-xs text-slate-400 mt-0.5">Subject: {data?.subject} • Baseline Mastery: {data?.current_mastery}%</p>
          </div>

          {data?.recovery_mode_active && (
            <div className="px-3.5 py-2 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-center gap-2.5">
              <AlertTriangle className="h-4 w-4 text-amber-400 shrink-0" />
              <div>
                <span className="text-xs font-bold text-amber-300 block">Adaptive Recovery Active</span>
                <span className="text-[11px] text-slate-300 block">Prerequisite steps prioritized to rebuild foundations.</span>
              </div>
            </div>
          )}
        </div>

        {/* Path Sequence */}
        <div className="space-y-4">
          <h3 className="text-sm font-bold text-white uppercase tracking-wider">Step-by-Step Recovery Sequence</h3>

          <div className="relative border-l-2 border-slate-800 ml-4 space-y-6 pl-6 py-2">
            {data?.path?.map((step: any, idx: number) => {
              const isPrereq = step.type === 'PREREQUISITE_REVIEW';
              const isPractice = step.type === 'PRACTICE';
              
              return (
                <div key={step.step_number} className="relative group">
                  {/* Timeline node */}
                  <span className={`absolute -left-[35px] top-1 h-6 w-6 rounded-full flex items-center justify-center font-bold text-xs border ${
                    step.is_completed 
                      ? 'bg-emerald-500 text-slate-950 border-emerald-400' 
                      : isPrereq 
                      ? 'bg-amber-500/20 text-amber-300 border-amber-500/40' 
                      : 'bg-teal-500/20 text-teal-300 border-teal-500/40'
                  }`}>
                    {step.step_number}
                  </span>

                  <div className="p-5 rounded-xl bg-[#162235] border border-slate-800 group-hover:border-slate-700 transition-all">
                    <div className="flex items-center justify-between mb-2">
                      <div className="flex items-center gap-2">
                        <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                          isPrereq 
                            ? 'bg-amber-500/10 text-amber-300 border-amber-500/30' 
                            : 'bg-teal-500/10 text-teal-300 border-teal-500/30'
                        }`}>
                          {step.type.replace('_', ' ')}
                        </span>
                        <h4 className="text-sm font-bold text-white">{step.title}</h4>
                      </div>

                      {step.is_completed ? (
                        <span className="flex items-center gap-1 text-xs text-emerald-400 font-semibold">
                          <CheckCircle2 className="h-3.5 w-3.5" /> Completed
                        </span>
                      ) : (
                        <Link
                          href="/student/practice"
                          className="py-1.5 px-3 rounded-lg font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 text-xs flex items-center gap-1 transition-all"
                        >
                          Start <ArrowRight className="h-3 w-3" />
                        </Link>
                      )}
                    </div>

                    <p className="text-xs text-slate-400 leading-relaxed">{step.recommendation_reason}</p>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

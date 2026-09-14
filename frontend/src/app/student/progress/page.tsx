'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { TrendingUp, CheckCircle2, AlertTriangle, XCircle, ArrowRight } from 'lucide-react';
import Link from 'next/link';

export default function ProgressPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiRequest('/students/me/mastery')
      .then((res) => setData(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex-1">
        <Navbar title="Mastery & Learning Telemetry" subtitle="Loading metrics..." />
        <div className="p-8 text-center text-slate-400 text-sm">Computing topic masteries...</div>
      </div>
    );
  }

  return (
    <div className="flex-1 pb-16">
      <Navbar title="Concept Mastery Matrix" subtitle="Granular topic-level telemetry and historical accuracy" />

      <div className="p-6 max-w-6xl mx-auto space-y-6">
        {/* Metric Summary */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div className="p-5 rounded-2xl bg-[#162235] border border-slate-800">
            <span className="text-xs text-slate-400 font-semibold uppercase">Overall Average</span>
            <p className="text-3xl font-extrabold text-white mt-1">{data?.overall_mastery}%</p>
          </div>
          <div className="p-5 rounded-2xl bg-[#162235] border border-slate-800">
            <span className="text-xs text-slate-400 font-semibold uppercase">Topics Mastered</span>
            <p className="text-3xl font-extrabold text-emerald-400 mt-1">{data?.topics_mastered}</p>
          </div>
          <div className="p-5 rounded-2xl bg-[#162235] border border-slate-800">
            <span className="text-xs text-slate-400 font-semibold uppercase">Critical Topics</span>
            <p className="text-3xl font-extrabold text-rose-400 mt-1">{data?.critical_topics}</p>
          </div>
        </div>

        {/* Mastery Table */}
        <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 shadow-xl overflow-x-auto">
          <h3 className="text-sm font-bold text-white mb-4">Topic Mastery Records</h3>
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 uppercase tracking-wider">
                <th className="pb-3 font-semibold">Topic</th>
                <th className="pb-3 font-semibold">Mastery Score</th>
                <th className="pb-3 font-semibold">Status</th>
                <th className="pb-3 font-semibold">Accuracy</th>
                <th className="pb-3 font-semibold">Attempts</th>
                <th className="pb-3 font-semibold text-right">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {data?.topics?.map((t: any) => {
                const isCritical = t.status === 'CRITICAL';
                const isStrong = t.status === 'STRONG';

                return (
                  <tr key={t.topic_id} className="hover:bg-slate-900/40 transition-colors">
                    <td className="py-4 font-semibold text-white">{t.topic_title}</td>
                    <td className="py-4 font-bold text-teal-400">{t.mastery_score}%</td>
                    <td className="py-4">
                      <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${
                        isCritical ? 'bg-rose-500/15 text-rose-300 border-rose-500/30' :
                        isStrong ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30' :
                        'bg-amber-500/15 text-amber-300 border-amber-500/30'
                      }`}>
                        {t.status.replace('_', ' ')}
                      </span>
                    </td>
                    <td className="py-4 text-slate-300">{t.accuracy_percentage}%</td>
                    <td className="py-4 text-slate-400">{t.correct_attempts} / {t.total_attempts}</td>
                    <td className="py-4 text-right">
                      <Link
                        href="/student/practice"
                        className="inline-flex items-center gap-1 text-teal-400 hover:underline font-semibold"
                      >
                        Practice <ArrowRight className="h-3 w-3" />
                      </Link>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

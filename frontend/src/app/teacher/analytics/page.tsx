'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { BarChart3, TrendingUp, AlertTriangle, CheckCircle2 } from 'lucide-react';

export default function TeacherAnalyticsPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiRequest('/teacher/dashboard')
      .then((res) => setData(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex-1">
        <Navbar title="Class Analytics" subtitle="Loading telemetry..." />
        <div className="p-8 text-center text-slate-400 text-sm">Computing class metrics...</div>
      </div>
    );
  }

  const { metrics, topic_weaknesses } = data || {};

  return (
    <div className="flex-1 pb-16">
      <Navbar title="Class Telemetry & Analytics" subtitle="Cohort concept heatmaps, mastery curves & learning gap trends" />

      <div className="p-6 max-w-6xl mx-auto space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-5 rounded-2xl bg-[#162235] border border-slate-800">
            <span className="text-xs text-slate-400 font-semibold uppercase">Enrolled Students</span>
            <p className="text-3xl font-extrabold text-white mt-1">{metrics?.total_students || 0}</p>
          </div>
          <div className="p-5 rounded-2xl bg-[#162235] border border-slate-800">
            <span className="text-xs text-slate-400 font-semibold uppercase">Class Average Mastery</span>
            <p className="text-3xl font-extrabold text-teal-400 mt-1">{metrics?.average_mastery || 0}%</p>
          </div>
          <div className="p-5 rounded-2xl bg-[#162235] border border-slate-800">
            <span className="text-xs text-slate-400 font-semibold uppercase">Critical Concept Alerts</span>
            <p className="text-3xl font-extrabold text-rose-400 mt-1">{metrics?.high_risk_count || 0}</p>
          </div>
        </div>

        {/* Concept Heatmap Table */}
        <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 shadow-xl overflow-x-auto">
          <h3 className="text-sm font-bold text-white mb-4">Syllabus Concept Weakness Heatmap</h3>
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 uppercase tracking-wider">
                <th className="pb-3 font-semibold">Concept Topic</th>
                <th className="pb-3 font-semibold">Cohort Mastery</th>
                <th className="pb-3 font-semibold">Students Needing Support</th>
                <th className="pb-3 font-semibold">Recommended Remedy</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {topic_weaknesses?.map((tw: any, idx: number) => (
                <tr key={idx} className="hover:bg-slate-900/40">
                  <td className="py-4 font-bold text-white">{tw.topic}</td>
                  <td className="py-4 font-mono font-bold text-teal-400">{tw.average_mastery}%</td>
                  <td className="py-4">
                    <span className="text-rose-400 font-semibold">
                      {tw.students_critical} student(s) at &lt;40%
                    </span>
                  </td>
                  <td className="py-4 text-slate-300">
                    Review prerequisite foundations before proceeding to complex exam problems.
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}

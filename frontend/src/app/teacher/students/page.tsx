'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { Users, ArrowRight, AlertTriangle, ShieldCheck, Search } from 'lucide-react';
import Link from 'next/link';

export default function TeacherStudentsPage() {
  const [students, setStudents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    apiRequest('/teacher/students')
      .then((res) => setStudents(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const filtered = students.filter((s) => 
    s.name.toLowerCase().includes(search.toLowerCase()) || 
    s.email.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="flex-1 pb-16">
      <Navbar title="Student Directory & Diagnostics" subtitle="Class rosters and individual concept mastery telemetry" />

      <div className="p-6 max-w-6xl mx-auto space-y-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div>
            <h2 className="text-lg font-bold text-white">All Enrolled Students</h2>
            <p className="text-xs text-slate-400">Select any student to view prerequisite gaps and issue interventions</p>
          </div>

          <div className="relative w-full sm:w-64">
            <Search className="h-4 w-4 absolute left-3 top-3 text-slate-500" />
            <input
              type="text"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search students..."
              className="w-full pl-9 pr-3 py-2 bg-slate-900 border border-slate-700 rounded-xl text-xs text-white focus:outline-none focus:border-teal-500"
            />
          </div>
        </div>

        {loading ? (
          <div className="p-12 text-center text-slate-400 text-sm">Loading student diagnostics...</div>
        ) : filtered.length === 0 ? (
          <div className="p-12 rounded-2xl bg-[#162235] border border-slate-800 text-center text-slate-400 text-sm">
            No students found.
          </div>
        ) : (
          <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 shadow-xl overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead>
                <tr className="border-b border-slate-800 text-slate-400 uppercase tracking-wider">
                  <th className="pb-3 font-semibold">Student</th>
                  <th className="pb-3 font-semibold">Classes</th>
                  <th className="pb-3 font-semibold">Average Mastery</th>
                  <th className="pb-3 font-semibold">Predicted Risk</th>
                  <th className="pb-3 font-semibold text-right">Action</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-800/60">
                {filtered.map((s) => {
                  const isHigh = s.risk_level === 'HIGH';
                  const isMed = s.risk_level === 'MEDIUM';

                  return (
                    <tr key={s.id} className="hover:bg-slate-900/40 transition-colors">
                      <td className="py-4">
                        <p className="font-bold text-white">{s.name}</p>
                        <p className="text-[11px] text-slate-400">{s.email}</p>
                      </td>
                      <td className="py-4 text-slate-300">
                        {s.classes.join(', ') || 'General'}
                      </td>
                      <td className="py-4 font-bold text-teal-400">{s.average_mastery}%</td>
                      <td className="py-4">
                        <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${
                          isHigh ? 'bg-rose-500/15 text-rose-300 border-rose-500/30' :
                          isMed ? 'bg-amber-500/15 text-amber-300 border-amber-500/30' :
                          'bg-emerald-500/15 text-emerald-300 border-emerald-500/30'
                        }`}>
                          {s.risk_score} / 100 ({s.risk_level})
                        </span>
                      </td>
                      <td className="py-4 text-right">
                        <Link
                          href={`/teacher/students/${s.id}`}
                          className="py-1.5 px-3 rounded-lg bg-slate-900 border border-slate-700 hover:bg-slate-800 text-teal-300 font-semibold inline-flex items-center gap-1.5"
                        >
                          Diagnostic Profile <ArrowRight className="h-3 w-3" />
                        </Link>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}

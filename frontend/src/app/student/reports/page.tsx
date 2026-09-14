'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { FileText, Download, Printer, Award, ShieldCheck, Target } from 'lucide-react';

export default function StudentReportsPage() {
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiRequest('/reports/student')
      .then((res) => setReport(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleDownloadCsv = async () => {
    try {
      const csvText = await apiRequest('/reports/student/download');
      const blob = new Blob([csvText], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', `student_report_${report.student_name}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch {
      alert('Failed to download CSV');
    }
  };

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="flex-1 pb-16">
      <Navbar title="Academic Progress Report" subtitle="Official diagnostic summary and exportable performance record" />

      <div className="p-6 max-w-4xl mx-auto space-y-6">
        <div className="flex justify-end gap-3 print:hidden">
          <button
            onClick={handleDownloadCsv}
            className="py-2 px-3.5 rounded-xl border border-slate-700 bg-slate-900 hover:bg-slate-800 text-slate-200 text-xs font-semibold flex items-center gap-2"
          >
            <Download className="h-3.5 w-3.5" /> Download CSV
          </button>
          <button
            onClick={handlePrint}
            className="py-2 px-3.5 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 hover:from-teal-400 hover:to-cyan-300 text-xs flex items-center gap-2"
          >
            <Printer className="h-3.5 w-3.5" /> Print Report
          </button>
        </div>

        {/* Printable Card */}
        <div className="p-8 rounded-2xl bg-[#162235] border border-slate-800 shadow-2xl space-y-6">
          <div className="border-b border-slate-800 pb-6 flex justify-between items-center">
            <div>
              <span className="text-[10px] font-bold uppercase tracking-widest text-teal-400 block mb-1">
                LearnWise AI Official Telemetry Record
              </span>
              <h2 className="text-2xl font-bold text-white">{report?.student_name}</h2>
              <p className="text-xs text-slate-400">{report?.grade_level} • {report?.email}</p>
            </div>
            <div className="text-right">
              <span className="text-xs text-slate-400 block">Overall Mastery</span>
              <span className="text-3xl font-extrabold text-teal-400">{report?.overall_mastery}%</span>
            </div>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
              <span className="text-[11px] text-slate-400 block">Predicted Risk</span>
              <span className={`text-sm font-bold block mt-1 ${
                report?.risk_level === 'HIGH' ? 'text-rose-400' : report?.risk_level === 'MEDIUM' ? 'text-amber-400' : 'text-emerald-400'
              }`}>
                {report?.risk_score} / 100 ({report?.risk_level})
              </span>
            </div>
            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
              <span className="text-[11px] text-slate-400 block">Topics Assessed</span>
              <span className="text-sm font-bold text-white block mt-1">{report?.topics_assessed} Concepts</span>
            </div>
            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
              <span className="text-[11px] text-slate-400 block">Assessment Avg</span>
              <span className="text-sm font-bold text-white block mt-1">{report?.average_assessment_score}%</span>
            </div>
            <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
              <span className="text-[11px] text-slate-400 block">Total Activities</span>
              <span className="text-sm font-bold text-white block mt-1">{report?.total_activities} Sessions</span>
            </div>
          </div>

          <div>
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 mb-2">Risk Drivers & Observations</h3>
            <ul className="space-y-1.5">
              {report?.risk_reasons?.map((r: string, idx: number) => (
                <li key={idx} className="text-xs text-slate-300 flex items-center gap-2">
                  <span className="text-teal-400 font-bold">•</span> {r}
                </li>
              ))}
            </ul>
          </div>

          <div className="p-4 rounded-xl bg-teal-500/10 border border-teal-500/20 text-xs">
            <span className="font-bold text-teal-300 block mb-1">Recommended Pedagogical Action:</span>
            <p className="text-slate-300">{report?.recommended_action}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

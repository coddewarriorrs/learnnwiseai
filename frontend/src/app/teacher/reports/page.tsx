'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { FileText, Download, Users, BookOpen } from 'lucide-react';

export default function TeacherReportsPage() {
  const [classes, setClasses] = useState<any[]>([]);
  const [selectedClass, setSelectedClass] = useState<number | null>(null);
  const [report, setReport] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiRequest('/classes')
      .then((cls) => {
        setClasses(cls);
        if (cls.length > 0) {
          setSelectedClass(cls[0].id);
          fetchClassReport(cls[0].id);
        } else {
          setLoading(false);
        }
      })
      .catch(() => setLoading(false));
  }, []);

  const fetchClassReport = (cid: number) => {
    setLoading(true);
    apiRequest(`/reports/class/${cid}`)
      .then((res) => setReport(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  const handleClassChange = (cid: number) => {
    setSelectedClass(cid);
    fetchClassReport(cid);
  };

  const handleDownloadCsv = async () => {
    if (!selectedClass) return;
    try {
      const csvText = await apiRequest(`/reports/class/${selectedClass}/download`);
      const blob = new Blob([csvText], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', `class_report_${selectedClass}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    } catch {
      alert('Failed to download CSV');
    }
  };

  return (
    <div className="flex-1 pb-16">
      <Navbar title="Class Reports & Export" subtitle="Exportable class performance telemetry and roster diagnostics" />

      <div className="p-6 max-w-4xl mx-auto space-y-6">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div className="flex items-center gap-2">
            <span className="text-xs text-slate-400">Select Class:</span>
            <select
              value={selectedClass || ''}
              onChange={(e) => handleClassChange(Number(e.target.value))}
              className="bg-slate-900 border border-slate-700 rounded-xl px-3 py-1.5 text-xs text-white focus:outline-none focus:border-teal-500"
            >
              {classes.map((c) => (
                <option key={c.id} value={c.id}>{c.name}</option>
              ))}
            </select>
          </div>

          <button
            onClick={handleDownloadCsv}
            disabled={!selectedClass}
            className="py-2 px-4 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 text-xs flex items-center gap-2"
          >
            <Download className="h-3.5 w-3.5" /> Export Class Roster CSV
          </button>
        </div>

        {report && (
          <div className="p-8 rounded-2xl bg-[#162235] border border-slate-800 shadow-2xl space-y-6">
            <div className="border-b border-slate-800 pb-4">
              <h2 className="text-xl font-bold text-white">{report.class_name}</h2>
              <p className="text-xs text-slate-400">Subject: {report.subject} • Grade {report.grade}</p>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-3 gap-4">
              <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                <span className="text-xs text-slate-400 block">Total Students</span>
                <span className="text-2xl font-bold text-white mt-1 block">{report.student_count}</span>
              </div>
              <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                <span className="text-xs text-slate-400 block">Average Mastery</span>
                <span className="text-2xl font-bold text-teal-400 mt-1 block">{report.average_mastery}%</span>
              </div>
              <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                <span className="text-xs text-slate-400 block">High Risk Students</span>
                <span className="text-2xl font-bold text-rose-400 mt-1 block">{report.risk_breakdown?.HIGH || 0}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

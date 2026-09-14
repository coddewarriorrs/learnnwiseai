'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { AlertTriangle, ShieldAlert, ArrowRight, CheckCircle2, User, Plus } from 'lucide-react';
import Link from 'next/link';

export default function EarlyWarningDashboardPage() {
  const [students, setStudents] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedStudent, setSelectedStudent] = useState<any>(null);
  const [actionModal, setActionModal] = useState(false);
  const [interventionAction, setInterventionAction] = useState('Assign targeted prerequisite review and guided practice');
  const [submitting, setSubmitting] = useState(false);

  const fetchStudents = () => {
    apiRequest('/risk/early-warning')
      .then((res) => setStudents(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchStudents();
  }, []);

  const handleCreateIntervention = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedStudent) return;
    setSubmitting(true);

    try {
      await apiRequest('/interventions', {
        method: 'POST',
        body: JSON.stringify({
          student_id: selectedStudent.student_id,
          reason: `Early Warning Triage: ${selectedStudent.reasons[0] || 'Academic Risk'}`,
          action: interventionAction,
          type: 'PREREQUISITE_REVIEW'
        }),
      });
      alert('Intervention assigned successfully!');
      setActionModal(false);
      fetchStudents();
    } catch (err: any) {
      alert(err.message || 'Error assigning intervention');
    } finally {
      setSubmitting(false);
    }
  };

  const highRisk = students.filter((s) => s.risk_level === 'HIGH');
  const medRisk = students.filter((s) => s.risk_level === 'MEDIUM');
  const lowRisk = students.filter((s) => s.risk_level === 'LOW');

  return (
    <div className="flex-1 pb-16">
      <Navbar 
        title="Early Warning & Risk Triage" 
        subtitle="Predicted academic risk telemetry categorized by urgent intervention priority" 
      />

      <div className="p-6 max-w-6xl mx-auto space-y-6">
        {/* Triage Summary */}
        <div className="grid grid-cols-3 gap-4">
          <div className="p-5 rounded-2xl bg-rose-500/10 border border-rose-500/30">
            <span className="text-xs font-bold text-rose-400 uppercase tracking-wider block">High Priority</span>
            <p className="text-3xl font-extrabold text-white mt-1">{highRisk.length}</p>
            <span className="text-[11px] text-rose-300 mt-1 block">Immediate prerequisite intervention</span>
          </div>
          <div className="p-5 rounded-2xl bg-amber-500/10 border border-amber-500/30">
            <span className="text-xs font-bold text-amber-400 uppercase tracking-wider block">Medium Attention</span>
            <p className="text-3xl font-extrabold text-white mt-1">{medRisk.length}</p>
            <span className="text-[11px] text-amber-300 mt-1 block">Guided practice recommended</span>
          </div>
          <div className="p-5 rounded-2xl bg-emerald-500/10 border border-emerald-500/30">
            <span className="text-xs font-bold text-emerald-400 uppercase tracking-wider block">On Track</span>
            <p className="text-3xl font-extrabold text-white mt-1">{lowRisk.length}</p>
            <span className="text-[11px] text-emerald-300 mt-1 block">Steady concept mastery</span>
          </div>
        </div>

        {/* Student Cards grouped by Priority */}
        <div className="space-y-6">
          {/* HIGH RISK */}
          <div className="space-y-3">
            <h3 className="text-sm font-bold text-rose-400 uppercase tracking-wider flex items-center gap-2">
              <ShieldAlert className="h-4 w-4" /> High Risk Priority (Score &gt; 70/100)
            </h3>

            {highRisk.length === 0 ? (
              <p className="text-xs text-slate-500 p-4 rounded-xl bg-slate-900/50">No students currently in High Risk status.</p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {highRisk.map((s) => (
                  <div key={s.student_id} className="p-5 rounded-2xl bg-[#162235] border border-rose-500/40 shadow-lg space-y-3">
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="text-base font-bold text-white">{s.student_name}</h4>
                        <p className="text-xs text-slate-400">{s.class_name} • {s.student_email}</p>
                      </div>
                      <span className="text-xs font-mono font-bold text-rose-300 bg-rose-500/20 px-2.5 py-1 rounded-lg border border-rose-500/30">
                        {s.risk_score} / 100
                      </span>
                    </div>

                    <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-xs space-y-1">
                      <span className="text-slate-400 block font-medium">Root Drivers:</span>
                      {s.reasons.map((r: string, i: number) => (
                        <p key={i} className="text-rose-200 flex items-start gap-1.5">
                          <span className="text-rose-400">•</span> {r}
                        </p>
                      ))}
                    </div>

                    <div className="text-xs text-slate-400">
                      Primary Gap: <span className="font-semibold text-white">{s.top_weak_topic}</span>
                    </div>

                    <div className="pt-2 border-t border-slate-800 flex items-center justify-between">
                      <button
                        onClick={() => { setSelectedStudent(s); setActionModal(true); }}
                        className="py-1.5 px-3 rounded-lg font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 text-xs flex items-center gap-1.5"
                      >
                        <Plus className="h-3.5 w-3.5" /> Assign Intervention
                      </button>
                      <Link
                        href={`/teacher/students/${s.student_id}`}
                        className="text-xs font-semibold text-teal-400 hover:underline flex items-center gap-1"
                      >
                        Deep Dive <ArrowRight className="h-3 w-3" />
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* MEDIUM RISK */}
          <div className="space-y-3 pt-4">
            <h3 className="text-sm font-bold text-amber-400 uppercase tracking-wider flex items-center gap-2">
              <AlertTriangle className="h-4 w-4" /> Medium Risk (Score 40-69/100)
            </h3>

            {medRisk.length === 0 ? (
              <p className="text-xs text-slate-500 p-4 rounded-xl bg-slate-900/50">No students currently in Medium Risk status.</p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {medRisk.map((s) => (
                  <div key={s.student_id} className="p-5 rounded-2xl bg-[#162235] border border-amber-500/30 space-y-3">
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="text-base font-bold text-white">{s.student_name}</h4>
                        <p className="text-xs text-slate-400">{s.class_name} • {s.student_email}</p>
                      </div>
                      <span className="text-xs font-mono font-bold text-amber-300 bg-amber-500/20 px-2.5 py-1 rounded-lg border border-amber-500/30">
                        {s.risk_score} / 100
                      </span>
                    </div>

                    <div className="p-3 rounded-xl bg-slate-900/80 border border-slate-800 text-xs space-y-1">
                      {s.reasons.map((r: string, i: number) => (
                        <p key={i} className="text-amber-200 flex items-start gap-1.5">
                          <span className="text-amber-400">•</span> {r}
                        </p>
                      ))}
                    </div>

                    <div className="pt-2 border-t border-slate-800 flex items-center justify-between">
                      <button
                        onClick={() => { setSelectedStudent(s); setActionModal(true); }}
                        className="py-1.5 px-3 rounded-lg font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 text-xs flex items-center gap-1.5"
                      >
                        <Plus className="h-3.5 w-3.5" /> Assign Intervention
                      </button>
                      <Link
                        href={`/teacher/students/${s.student_id}`}
                        className="text-xs font-semibold text-teal-400 hover:underline flex items-center gap-1"
                      >
                        Deep Dive <ArrowRight className="h-3 w-3" />
                      </Link>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        {/* Modal for Assigning Intervention */}
        {actionModal && selectedStudent && (
          <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-[#162235] border border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-base font-bold text-white">Create Targeted Intervention</h3>
                <button onClick={() => setActionModal(false)} className="text-slate-400 hover:text-white">✕</button>
              </div>

              <p className="text-xs text-slate-400">
                Assigning intervention for <strong>{selectedStudent.student_name}</strong> based on early warning telemetry.
              </p>

              <form onSubmit={handleCreateIntervention} className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                    Action Plan / Assignment
                  </label>
                  <textarea
                    rows={4}
                    required
                    value={interventionAction}
                    onChange={(e) => setInterventionAction(e.target.value)}
                    className="w-full p-3 bg-slate-900 border border-slate-700 rounded-xl text-xs text-white focus:outline-none focus:border-teal-500"
                  />
                </div>

                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setActionModal(false)}
                    className="w-1/2 py-2 rounded-xl border border-slate-700 text-xs text-slate-300 hover:bg-slate-800"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={submitting}
                    className="w-1/2 py-2 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 text-xs"
                  >
                    {submitting ? 'Assigning...' : 'Confirm Intervention'}
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

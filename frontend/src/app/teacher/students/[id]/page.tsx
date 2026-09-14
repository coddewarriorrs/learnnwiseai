'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { useParams } from 'next/navigation';
import { apiRequest } from '@/lib/api';
import { 
  User, Award, AlertTriangle, CheckCircle2, Clock, Plus, 
  ArrowLeft, FileText, Send, Sparkles, BrainCircuit, ShieldAlert, 
  Lightbulb, Lock
} from 'lucide-react';
import Link from 'next/link';

export default function StudentProfilePage() {
  const { id } = useParams();
  const [data, setData] = useState<any>(null);
  const [twinData, setTwinData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newNote, setNewNote] = useState('');
  const [addingNote, setAddingNote] = useState(false);
  const [interventionModal, setInterventionModal] = useState(false);
  const [interventionAction, setInterventionAction] = useState('Prerequisite review and guided practice set');
  const [interventionReason, setInterventionReason] = useState('Foundational gap detected in Indefinite Integrals');

  const fetchProfile = () => {
    apiRequest(`/teacher/students/${id}`)
      .then((res) => setData(res))
      .catch((err) => setError(err.message || 'Error loading profile'))
      .finally(() => setLoading(false));

    apiRequest(`/twin/student/${id}`)
      .then((t) => setTwinData(t))
      .catch(() => setTwinData(null));
  };

  useEffect(() => {
    if (!id) return;
    fetchProfile();
  }, [id]);

  const handleAddNote = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newNote.trim()) return;
    setAddingNote(true);

    try {
      await apiRequest('/teacher/notes', {
        method: 'POST',
        body: JSON.stringify({ student_id: Number(id), note: newNote }),
      });
      setNewNote('');
      fetchProfile();
    } catch {
      alert('Failed to save note');
    } finally {
      setAddingNote(false);
    }
  };

  const handleCreateIntervention = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiRequest('/interventions', {
        method: 'POST',
        body: JSON.stringify({
          student_id: Number(id),
          reason: interventionReason,
          action: interventionAction,
          type: 'PREREQUISITE_REVIEW'
        }),
      });
      alert('Intervention assigned successfully!');
      setInterventionModal(false);
      fetchProfile();
    } catch (err: any) {
      alert(err.message || 'Error creating intervention');
    }
  };

  if (loading) {
    return (
      <div className="flex-1">
        <Navbar title="Student Diagnostic Profile" subtitle="Loading..." />
        <div className="p-8 text-center text-slate-400 text-sm">Aggregating diagnostic telemetry...</div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex-1">
        <Navbar title="Student Diagnostic Profile" subtitle="Access Denied" />
        <div className="p-8 text-center text-rose-400 text-sm">{error || 'Access denied.'}</div>
      </div>
    );
  }

  const { student, risk, masteries, interventions, notes, recent_activity } = data;

  return (
    <div className="flex-1 pb-16">
      <Navbar title={student.name} subtitle="Granular diagnostic telemetry, risk decomposition & intervention logs" />

      <div className="p-6 max-w-6xl mx-auto space-y-6">
        <Link href="/teacher/students" className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-white">
          <ArrowLeft className="h-3.5 w-3.5" /> Back to Student Roster
        </Link>

        {/* Student Summary Banner */}
        <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center gap-4">
            <div className="h-12 w-12 rounded-2xl bg-teal-500/10 border border-teal-500/20 text-teal-400 flex items-center justify-center font-bold text-base">
              {student.name.slice(0, 2).toUpperCase()}
            </div>
            <div>
              <h2 className="text-xl font-bold text-white">{student.name}</h2>
              <p className="text-xs text-slate-400">{student.email} • {student.grade || 'Grade 11'}</p>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={() => setInterventionModal(true)}
              className="py-2.5 px-4 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 hover:from-teal-400 hover:to-cyan-300 text-xs flex items-center gap-2"
            >
              <Plus className="h-4 w-4" /> Assign Intervention
            </button>
          </div>
        </div>

        {/* Risk Decomposition Card */}
        <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-sm font-bold text-white uppercase tracking-wider">Multi-Factor Risk Breakdown</h3>
            <span className={`text-xs font-mono font-bold px-2.5 py-1 rounded-lg border ${
              risk.level === 'HIGH' ? 'bg-rose-500/20 text-rose-300 border-rose-500/30' :
              risk.level === 'MEDIUM' ? 'bg-amber-500/20 text-amber-300 border-amber-500/30' :
              'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
            }`}>
              Composite Score: {risk.score} / 100 ({risk.level})
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
              <span className="text-slate-400 block">Performance Risk (35%)</span>
              <span className="font-bold text-white text-sm mt-0.5 block">{risk.performance_risk}%</span>
            </div>
            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
              <span className="text-slate-400 block">Attendance Risk (25%)</span>
              <span className="font-bold text-white text-sm mt-0.5 block">{risk.attendance_risk}%</span>
            </div>
            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
              <span className="text-slate-400 block">Assignment Risk (20%)</span>
              <span className="font-bold text-white text-sm mt-0.5 block">{risk.assignment_risk}%</span>
            </div>
            <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
              <span className="text-slate-400 block">Engagement Risk (20%)</span>
              <span className="font-bold text-white text-sm mt-0.5 block">{risk.engagement_risk}%</span>
            </div>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-900/60 border border-slate-800 text-xs">
            <span className="font-semibold text-slate-300 block mb-1">Explainable Telemetry Drivers:</span>
            <ul className="space-y-1">
              {risk.reasons.map((r: string, i: number) => (
                <li key={i} className="text-slate-300 flex items-start gap-2">
                  <span className="text-amber-400">•</span> {r}
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Topic Mastery Matrix */}
        <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 shadow-xl overflow-x-auto">
          <h3 className="text-sm font-bold text-white mb-4">Topic Mastery Breakdown</h3>
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 text-slate-400 uppercase tracking-wider">
                <th className="pb-3 font-semibold">Topic</th>
                <th className="pb-3 font-semibold">Mastery Score</th>
                <th className="pb-3 font-semibold">Status</th>
                <th className="pb-3 font-semibold">Correct / Attempts</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {masteries.map((m: any) => (
                <tr key={m.topic_id} className="hover:bg-slate-900/40">
                  <td className="py-3 font-semibold text-white">{m.topic}</td>
                  <td className="py-3 font-bold text-teal-400">{m.score}%</td>
                  <td className="py-3">
                    <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${
                      m.status === 'CRITICAL' ? 'bg-rose-500/15 text-rose-300 border-rose-500/30' :
                      m.status === 'STRONG' ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30' :
                      'bg-amber-500/15 text-amber-300 border-amber-500/30'
                    }`}>
                      {m.status.replace('_', ' ')}
                    </span>
                  </td>
                  <td className="py-3 text-slate-400">{m.correct_attempts} / {m.total_attempts}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Personal Learning Twin Diagnostic Telemetry (Teacher View) */}
        {twinData && (
          <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-5 shadow-xl">
            <div className="flex flex-wrap items-center justify-between border-b border-slate-800 pb-3 gap-3">
              <div className="flex items-center gap-2.5">
                <div className="h-9 w-9 rounded-xl bg-purple-500/15 border border-purple-500/30 text-purple-400 flex items-center justify-center">
                  <Sparkles className="h-5 w-5" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                    Personal Learning Twin Cognitive Profile
                  </h3>
                  <p className="text-[11px] text-slate-400">
                    Live telemetry on recurring mistake archetypes, DAG prerequisite gaps & struggle signals
                  </p>
                </div>
              </div>

              {/* Privacy Notice */}
              <div className="flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-900 border border-slate-800 text-[11px] text-slate-400">
                <Lock className="h-3 w-3 text-teal-400" />
                <span>AI Tutor Transcripts Protected (Private to Student)</span>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
              {/* Misconception Fingerprint */}
              <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
                <div className="flex items-center gap-1.5 font-bold text-purple-300">
                  <ShieldAlert className="h-4 w-4 text-purple-400" />
                  <span>Misconception Fingerprint</span>
                </div>
                {twinData.misconception_fingerprint && twinData.misconception_fingerprint.length > 0 ? (
                  <div className="space-y-2 pt-1">
                    {twinData.misconception_fingerprint.map((mf: any, idx: number) => (
                      <div key={idx} className="p-2.5 rounded-lg bg-purple-500/10 border border-purple-500/20 text-[11px] space-y-1">
                        <div className="flex justify-between font-bold text-purple-200 uppercase">
                          <span>{mf.mistake_type.replace(/_/g, ' ')}</span>
                          <span>{mf.count}x</span>
                        </div>
                        <p className="text-slate-300 text-[10px]">{mf.remedy_advice}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-slate-500 text-[11px] pt-1">No repeated misconception patterns exhibited.</p>
                )}
              </div>

              {/* Recovery Mode & Struggle Signal */}
              <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
                <div className="flex items-center gap-1.5 font-bold text-rose-300">
                  <BrainCircuit className="h-4 w-4 text-rose-400" />
                  <span>Recovery Mode & Struggle</span>
                </div>
                <div className="space-y-2 pt-1 text-[11px]">
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400">Struggle Signal:</span>
                    <span className={`font-bold px-2 py-0.5 rounded ${
                      twinData.struggle_signal?.detected 
                        ? 'bg-rose-500/20 text-rose-300 border border-rose-500/40' 
                        : 'bg-emerald-500/15 text-emerald-300'
                    }`}>
                      {twinData.struggle_signal?.detected ? 'DETECTED' : 'CLEAR'}
                    </span>
                  </div>
                  {twinData.struggle_signal?.reason && (
                    <p className="text-slate-300 bg-slate-800/80 p-2 rounded border border-slate-700">
                      {twinData.struggle_signal.reason}
                    </p>
                  )}
                  <div className="flex items-center justify-between pt-1 border-t border-slate-800">
                    <span className="text-slate-400">Recovery Mode:</span>
                    <span className="font-semibold text-slate-200">
                      {twinData.recovery_mode?.active ? `Step ${twinData.recovery_mode.step}/7 Active` : 'Inactive'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Prerequisite Gaps & Memory Decay */}
              <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 space-y-2">
                <div className="flex items-center gap-1.5 font-bold text-amber-300">
                  <AlertTriangle className="h-4 w-4 text-amber-400" />
                  <span>Foundational Gaps & Decay</span>
                </div>
                <div className="space-y-2 pt-1 text-[11px]">
                  {twinData.prerequisite_gaps && twinData.prerequisite_gaps.length > 0 ? (
                    twinData.prerequisite_gaps.slice(0, 2).map((g: any, i: number) => (
                      <div key={i} className="p-2 rounded bg-amber-500/10 border border-amber-500/20">
                        <span className="font-semibold text-amber-200 block">{g.topic_name}</span>
                        <span className="text-[10px] text-slate-400">Prereq: {g.root_prerequisite_name}</span>
                      </div>
                    ))
                  ) : (
                    <p className="text-slate-500 text-[11px]">No prerequisite gaps identified.</p>
                  )}
                  {twinData.decayed_topics && twinData.decayed_topics.length > 0 && (
                    <p className="text-[10px] text-cyan-300 pt-1">
                      {twinData.decayed_topics.length} topic(s) due for spaced review.
                    </p>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Interventions & Teacher Notes */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Interventions */}
          <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-4">
            <h3 className="text-sm font-bold text-white">Active Interventions</h3>
            {interventions.length === 0 ? (
              <p className="text-xs text-slate-500">No interventions assigned yet.</p>
            ) : (
              <div className="space-y-3">
                {interventions.map((item: any) => (
                  <div key={item.id} className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 text-xs space-y-1">
                    <div className="flex justify-between items-center">
                      <span className="font-semibold text-teal-300">{item.action}</span>
                      <span className="text-[10px] text-slate-400 capitalize">{item.status.toLowerCase()}</span>
                    </div>
                    <p className="text-slate-400">{item.reason}</p>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Private Notes */}
          <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-4">
            <h3 className="text-sm font-bold text-white">Private Teacher Notes</h3>
            <form onSubmit={handleAddNote} className="space-y-2">
              <textarea
                rows={2}
                value={newNote}
                onChange={(e) => setNewNote(e.target.value)}
                placeholder="Add a confidential pedagogical note..."
                className="w-full p-2.5 bg-slate-900 border border-slate-700 rounded-xl text-xs text-white focus:outline-none focus:border-teal-500"
              />
              <button
                type="submit"
                disabled={addingNote || !newNote.trim()}
                className="py-1.5 px-3 rounded-lg font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 text-xs flex items-center gap-1.5 disabled:opacity-50"
              >
                <Send className="h-3 w-3" /> Save Note
              </button>
            </form>

            <div className="space-y-2.5 max-h-48 overflow-y-auto">
              {notes.map((n: any) => (
                <div key={n.id} className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-xs">
                  <p className="text-slate-300">{n.note}</p>
                  <span className="text-[10px] text-slate-500 mt-1 block">
                    {new Date(n.created_at).toLocaleDateString()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Modal */}
        {interventionModal && (
          <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-[#162235] border border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-base font-bold text-white">Assign Intervention</h3>
                <button onClick={() => setInterventionModal(false)} className="text-slate-400 hover:text-white">✕</button>
              </div>

              <form onSubmit={handleCreateIntervention} className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                    Pedagogical Reason
                  </label>
                  <input
                    type="text"
                    required
                    value={interventionReason}
                    onChange={(e) => setInterventionReason(e.target.value)}
                    className="w-full p-2.5 bg-slate-900 border border-slate-700 rounded-xl text-xs text-white focus:outline-none focus:border-teal-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                    Action Plan / Assignment
                  </label>
                  <textarea
                    rows={4}
                    required
                    value={interventionAction}
                    onChange={(e) => setInterventionAction(e.target.value)}
                    className="w-full p-2.5 bg-slate-900 border border-slate-700 rounded-xl text-xs text-white focus:outline-none focus:border-teal-500"
                  />
                </div>

                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setInterventionModal(false)}
                    className="w-1/2 py-2 rounded-xl border border-slate-700 text-xs text-slate-300 hover:bg-slate-800"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="w-1/2 py-2 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 text-xs"
                  >
                    Assign
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

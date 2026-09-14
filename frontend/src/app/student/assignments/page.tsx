'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { FileCheck, CheckCircle2, Clock, Upload, AlertCircle } from 'lucide-react';

export default function StudentAssignmentsPage() {
  const [assignments, setAssignments] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeModal, setActiveModal] = useState<any>(null);
  const [submissionContent, setSubmissionContent] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [success, setSuccess] = useState('');

  const fetchAssignments = () => {
    apiRequest('/assignments')
      .then((res) => setAssignments(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchAssignments();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!submissionContent || !activeModal) return;
    setSubmitting(true);
    setSuccess('');

    try {
      await apiRequest(`/assignments/${activeModal.id}/submit`, {
        method: 'POST',
        body: JSON.stringify({ content: submissionContent }),
      });
      setSuccess('Submitted successfully! Telemetry updated.');
      fetchAssignments();
      setTimeout(() => {
        setActiveModal(null);
        setSubmissionContent('');
        setSuccess('');
      }, 1500);
    } catch (err: any) {
      alert(err.message || 'Error submitting');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex-1 pb-16">
      <Navbar title="Assignments" subtitle="Class coursework and targeted practice tasks" />

      <div className="p-6 max-w-5xl mx-auto space-y-6">
        {loading ? (
          <div className="p-12 text-center text-slate-400 text-sm">Loading assignments...</div>
        ) : assignments.length === 0 ? (
          <div className="p-12 rounded-2xl bg-[#162235] border border-slate-800 text-center text-slate-400 text-sm">
            No coursework assigned yet.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {assignments.map((a) => {
              const isDone = a.submission_status === 'COMPLETED';
              return (
                <div key={a.id} className="p-6 rounded-2xl bg-[#162235] border border-slate-800 flex flex-col justify-between">
                  <div>
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full border bg-slate-800 text-slate-300 border-slate-700">
                        {a.class_name || 'Classwork'}
                      </span>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                        isDone ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30' : 'bg-amber-500/15 text-amber-300 border-amber-500/30'
                      }`}>
                        {a.submission_status || 'ASSIGNED'}
                      </span>
                    </div>

                    <h3 className="text-base font-bold text-white mb-2">{a.title}</h3>
                    <p className="text-xs text-slate-300 leading-relaxed mb-4">{a.instructions}</p>
                  </div>

                  <div className="pt-4 border-t border-slate-800 flex items-center justify-between text-xs">
                    <span className="text-slate-400">Total Points: {a.total_points}</span>
                    {isDone ? (
                      <span className="text-emerald-400 font-semibold flex items-center gap-1">
                        <CheckCircle2 className="h-3.5 w-3.5" /> Submitted
                      </span>
                    ) : (
                      <button
                        onClick={() => setActiveModal(a)}
                        className="py-1.5 px-3 rounded-lg font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 text-xs"
                      >
                        Submit Response
                      </button>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}

        {/* Modal */}
        {activeModal && (
          <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-[#162235] border border-slate-800 rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-base font-bold text-white">Submit: {activeModal.title}</h3>
                <button onClick={() => setActiveModal(null)} className="text-slate-400 hover:text-white">✕</button>
              </div>

              {success && (
                <div className="p-3 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4" /> {success}
                </div>
              )}

              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                    Your Solution / Explanation
                  </label>
                  <textarea
                    rows={6}
                    required
                    value={submissionContent}
                    onChange={(e) => setSubmissionContent(e.target.value)}
                    placeholder="Provide your step-by-step mathematical reasoning or answer here..."
                    className="w-full p-3 bg-slate-900 border border-slate-700 rounded-xl text-xs text-white focus:outline-none focus:border-teal-500"
                  />
                </div>

                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setActiveModal(null)}
                    className="w-1/2 py-2 rounded-xl border border-slate-700 text-xs text-slate-300 hover:bg-slate-800"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={submitting}
                    className="w-1/2 py-2 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 text-xs"
                  >
                    {submitting ? 'Submitting...' : 'Confirm Submission'}
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

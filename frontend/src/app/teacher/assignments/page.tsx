'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { FileCheck, Plus, ArrowRight, CheckCircle2 } from 'lucide-react';

export default function TeacherAssignmentsPage() {
  const [assignments, setAssignments] = useState<any[]>([]);
  const [classes, setClasses] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);

  const [title, setTitle] = useState('');
  const [classId, setClassId] = useState<number | null>(null);
  const [instructions, setInstructions] = useState('');
  const [points, setPoints] = useState(50);
  const [submitting, setSubmitting] = useState(false);

  const fetchData = () => {
    Promise.all([apiRequest('/assignments'), apiRequest('/classes')])
      .then(([asgns, cls]) => {
        setAssignments(asgns);
        setClasses(cls);
        if (cls.length > 0) setClassId(cls[0].id);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleCreateAssignment = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!classId) return;
    setSubmitting(true);

    try {
      await apiRequest('/assignments', {
        method: 'POST',
        body: JSON.stringify({
          class_id: classId,
          title,
          instructions,
          total_points: points,
        }),
      });
      setShowModal(false);
      setTitle('');
      setInstructions('');
      fetchData();
    } catch (err: any) {
      alert(err.message || 'Failed to create assignment');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex-1 pb-16">
      <Navbar title="Class Assignments" subtitle="Create homework and evaluate submissions" />

      <div className="p-6 max-w-6xl mx-auto space-y-6">
        <div className="flex justify-between items-center">
          <div>
            <h2 className="text-lg font-bold text-white">Coursework Management</h2>
            <p className="text-xs text-slate-400">Assignments created here are instantly distributed to all enrolled class members</p>
          </div>
          <button
            onClick={() => setShowModal(true)}
            className="py-2.5 px-4 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 text-xs flex items-center gap-2"
          >
            <Plus className="h-4 w-4" /> Create Assignment
          </button>
        </div>

        {loading ? (
          <div className="p-12 text-center text-slate-400 text-sm">Loading assignments...</div>
        ) : assignments.length === 0 ? (
          <div className="p-12 rounded-2xl bg-[#162235] border border-slate-800 text-center text-slate-400 text-sm">
            No assignments created yet.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {assignments.map((a) => (
              <div key={a.id} className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full border bg-slate-800 text-teal-300 border-slate-700">
                    {a.class_name || 'Cohort'}
                  </span>
                  <span className="text-xs text-slate-400">{a.total_points} Points</span>
                </div>
                <h3 className="text-base font-bold text-white">{a.title}</h3>
                <p className="text-xs text-slate-400 leading-relaxed">{a.instructions}</p>
              </div>
            ))}
          </div>
        )}

        {/* Create Modal */}
        {showModal && (
          <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-[#162235] border border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-base font-bold text-white">New Assignment</h3>
                <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-white">✕</button>
              </div>

              <form onSubmit={handleCreateAssignment} className="space-y-4">
                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Target Class</label>
                  <select
                    value={classId || ''}
                    onChange={(e) => setClassId(Number(e.target.value))}
                    className="w-full p-2.5 bg-slate-900 border border-slate-700 rounded-xl text-xs text-white focus:outline-none focus:border-teal-500"
                  >
                    {classes.map((c) => (
                      <option key={c.id} value={c.id}>{c.name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Title</label>
                  <input
                    type="text"
                    required
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    placeholder="e.g. Calculus Practice Set 4"
                    className="w-full p-2.5 bg-slate-900 border border-slate-700 rounded-xl text-xs text-white focus:outline-none focus:border-teal-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">Instructions</label>
                  <textarea
                    rows={4}
                    required
                    value={instructions}
                    onChange={(e) => setInstructions(e.target.value)}
                    placeholder="Describe problems to solve..."
                    className="w-full p-2.5 bg-slate-900 border border-slate-700 rounded-xl text-xs text-white focus:outline-none focus:border-teal-500"
                  />
                </div>

                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setShowModal(false)}
                    className="w-1/2 py-2 rounded-xl border border-slate-700 text-xs text-slate-300 hover:bg-slate-800"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={submitting}
                    className="w-1/2 py-2 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 text-xs"
                  >
                    {submitting ? 'Creating...' : 'Distribute Assignment'}
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

'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { BookOpen, Plus, CheckCircle2, AlertCircle, Users, ArrowRight } from 'lucide-react';
import Link from 'next/link';

export default function StudentClassesPage() {
  const [classes, setClasses] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [joinCode, setJoinCode] = useState('');
  const [joining, setJoining] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);

  const fetchClasses = () => {
    apiRequest('/classes')
      .then((res) => setClasses(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchClasses();
  }, []);

  const handleJoin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!joinCode) return;
    setJoining(true);
    setError('');
    setMessage('');

    try {
      const res = await apiRequest('/classes/join', {
        method: 'POST',
        body: JSON.stringify({ class_code: joinCode }),
      });
      setMessage(res.message || 'Joined class successfully!');
      setJoinCode('');
      fetchClasses();
      setTimeout(() => setShowModal(false), 1500);
    } catch (err: any) {
      setError(err.message || 'Failed to join class.');
    } finally {
      setJoining(false);
    }
  };

  return (
    <div className="flex-1 pb-16">
      <Navbar title="My Enrolled Classes" subtitle="Classes and curriculum syllabi you are registered in" />

      <div className="p-6 max-w-6xl mx-auto space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-white">Active Cohorts</h2>
            <p className="text-xs text-slate-400">Join new classes using your teacher's class code</p>
          </div>
          <button
            onClick={() => setShowModal(true)}
            className="py-2.5 px-4 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 hover:from-teal-400 hover:to-cyan-300 text-xs flex items-center gap-2 transition-all cursor-pointer shadow-md shadow-teal-500/20"
          >
            <Plus className="h-4 w-4" /> Join Class with Code
          </button>
        </div>

        {loading ? (
          <div className="p-12 text-center text-slate-400 text-sm">Loading classes...</div>
        ) : classes.length === 0 ? (
          <div className="p-12 rounded-2xl bg-[#162235] border border-slate-800 text-center space-y-3">
            <BookOpen className="h-8 w-8 text-slate-500 mx-auto" />
            <h3 className="text-sm font-bold text-white">No Classes Enrolled</h3>
            <p className="text-xs text-slate-400">Ask your teacher for a class code or invite link to join your first class.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {classes.map((c) => (
              <div key={c.id} className="p-6 rounded-2xl bg-[#162235] border border-slate-800 hover:border-slate-700 transition-all flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-[11px] font-semibold text-teal-400 bg-teal-500/10 px-2.5 py-0.5 rounded-full border border-teal-500/20">
                      Grade {c.grade} • {c.board}
                    </span>
                    <span className="text-xs font-mono text-slate-500">Code: {c.class_code}</span>
                  </div>
                  <h3 className="text-base font-bold text-white mb-1">{c.name}</h3>
                  <p className="text-xs text-slate-400">Subject: {c.subject}</p>
                </div>

                <div className="mt-6 pt-4 border-t border-slate-800 flex items-center justify-between">
                  <div className="flex items-center gap-1.5 text-xs text-slate-400">
                    <Users className="h-3.5 w-3.5" />
                    <span>{c.student_count || 1} classmates</span>
                  </div>
                  <Link
                    href="/student/practice"
                    className="inline-flex items-center gap-1 text-xs font-semibold text-teal-400 hover:underline"
                  >
                    Practice <ArrowRight className="h-3 w-3" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Join Modal */}
        {showModal && (
          <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
            <div className="bg-[#162235] border border-slate-800 rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
              <div className="flex justify-between items-center">
                <h3 className="text-base font-bold text-white">Join a Class</h3>
                <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-white text-sm">✕</button>
              </div>

              <p className="text-xs text-slate-400">Enter the 6-character class code provided by your teacher (e.g. MATH11).</p>

              {error && (
                <div className="p-3 rounded-lg bg-rose-500/15 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
                  <AlertCircle className="h-4 w-4 shrink-0" />
                  <span>{error}</span>
                </div>
              )}

              {message && (
                <div className="p-3 rounded-lg bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 shrink-0" />
                  <span>{message}</span>
                </div>
              )}

              <form onSubmit={handleJoin} className="space-y-4">
                <input
                  type="text"
                  required
                  value={joinCode}
                  onChange={(e) => setJoinCode(e.target.value.toUpperCase())}
                  placeholder="MATH11"
                  className="w-full p-3 bg-slate-900 border border-slate-700 rounded-xl text-center text-lg font-mono font-bold tracking-widest text-white uppercase focus:outline-none focus:border-teal-500"
                />

                <div className="flex gap-2.5">
                  <button
                    type="button"
                    onClick={() => setShowModal(false)}
                    className="w-1/2 py-2.5 rounded-xl border border-slate-700 text-xs text-slate-300 hover:bg-slate-800"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    disabled={joining}
                    className="w-1/2 py-2.5 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 hover:from-teal-400 hover:to-cyan-300 text-xs disabled:opacity-50"
                  >
                    {joining ? 'Joining...' : 'Confirm & Join'}
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

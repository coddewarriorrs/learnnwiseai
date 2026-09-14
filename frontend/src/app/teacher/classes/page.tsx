'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { BookOpen, Plus, Copy, CheckCircle2, RefreshCw, ToggleLeft, ToggleRight, Users, ExternalLink } from 'lucide-react';
import Link from 'next/link';

export default function TeacherClassesPage() {
  const [classes, setClasses] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [copiedId, setCopiedId] = useState<number | null>(null);

  const fetchClasses = () => {
    apiRequest('/classes')
      .then((res) => setClasses(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchClasses();
  }, []);

  const handleCopyInvite = (c: any) => {
    const inviteUrl = `${window.location.origin}/join/${c.invite_token}`;
    navigator.clipboard.writeText(inviteUrl);
    setCopiedId(c.id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleRegenerate = async (classId: number) => {
    if (!confirm('Regenerating will invalidate previous invite links. Continue?')) return;
    try {
      await apiRequest(`/classes/${classId}/regenerate-invite`, { method: 'POST' });
      fetchClasses();
    } catch {
      alert('Failed to regenerate invite token');
    }
  };

  const handleToggle = async (classId: number) => {
    try {
      await apiRequest(`/classes/${classId}/toggle-invite`, { method: 'PATCH' });
      fetchClasses();
    } catch {
      alert('Failed to toggle invite status');
    }
  };

  return (
    <div className="flex-1 pb-16">
      <Navbar title="Class Management" subtitle="Manage class rosters, codes, and secure invite tokens" />

      <div className="p-6 max-w-6xl mx-auto space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-lg font-bold text-white">Class Roster</h2>
            <p className="text-xs text-slate-400">Invite students via class code or direct secure invite link</p>
          </div>
          <Link
            href="/teacher/classes/create"
            className="py-2.5 px-4 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 hover:from-teal-400 hover:to-cyan-300 text-xs flex items-center gap-2 transition-all shadow-md shadow-teal-500/20"
          >
            <Plus className="h-4 w-4" /> Create New Class
          </Link>
        </div>

        {loading ? (
          <div className="p-12 text-center text-slate-400 text-sm">Loading classes...</div>
        ) : classes.length === 0 ? (
          <div className="p-12 rounded-2xl bg-[#162235] border border-slate-800 text-center space-y-3">
            <BookOpen className="h-8 w-8 text-slate-500 mx-auto" />
            <h3 className="text-sm font-bold text-white">No Classes Created Yet</h3>
            <p className="text-xs text-slate-400">Create your first class cohort to start inviting students.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
            {classes.map((c) => (
              <div key={c.id} className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-semibold text-teal-400 bg-teal-500/10 px-2.5 py-0.5 rounded-full border border-teal-500/20">
                    Grade {c.grade} • {c.board}
                  </span>
                  <div className="flex items-center gap-1.5 text-xs text-slate-400">
                    <Users className="h-3.5 w-3.5" />
                    <span>{c.student_count || 0} enrolled</span>
                  </div>
                </div>

                <div>
                  <h3 className="text-base font-bold text-white">{c.name}</h3>
                  <p className="text-xs text-slate-400">Subject: {c.subject} • Academic Year: {c.academic_year}</p>
                </div>

                {/* Class Code & Invite Link Box */}
                <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 space-y-2.5 text-xs">
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400">Class Code:</span>
                    <span className="font-mono font-bold text-teal-400 tracking-wider text-sm bg-teal-500/10 px-2 py-0.5 rounded border border-teal-500/20">
                      {c.class_code}
                    </span>
                  </div>

                  <div className="flex items-center justify-between pt-1 border-t border-slate-800/80">
                    <span className="text-slate-400">Direct Invite Link:</span>
                    <button
                      onClick={() => handleCopyInvite(c)}
                      className="inline-flex items-center gap-1 font-semibold text-teal-300 hover:text-teal-200 cursor-pointer"
                    >
                      {copiedId === c.id ? <CheckCircle2 className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
                      {copiedId === c.id ? 'Copied URL' : 'Copy Link'}
                    </button>
                  </div>
                </div>

                {/* Controls */}
                <div className="pt-2 flex items-center justify-between text-xs">
                  <div className="flex items-center gap-2">
                    <button
                      onClick={() => handleToggle(c.id)}
                      className="text-slate-400 hover:text-white flex items-center gap-1"
                    >
                      {c.invite_active ? <ToggleRight className="h-4 w-4 text-emerald-400" /> : <ToggleLeft className="h-4 w-4 text-slate-600" />}
                      <span>{c.invite_active ? 'Active' : 'Disabled'}</span>
                    </button>
                    <button
                      onClick={() => handleRegenerate(c.id)}
                      title="Regenerate invite token"
                      className="p-1.5 text-slate-400 hover:text-amber-400 transition-colors"
                    >
                      <RefreshCw className="h-3.5 w-3.5" />
                    </button>
                  </div>

                  <Link
                    href={`/teacher/classes/${c.id}`}
                    className="font-bold text-teal-400 hover:underline flex items-center gap-1"
                  >
                    View Roster <ExternalLink className="h-3 w-3" />
                  </Link>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

'use client';

import React from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { useAuth } from '@/lib/auth';
import { Settings, User, ShieldCheck } from 'lucide-react';

export default function TeacherSettingsPage() {
  const { user } = useAuth();

  return (
    <div className="flex-1 pb-16">
      <Navbar title="Teacher Settings" subtitle="Account details and pedagogical telemetry options" />

      <div className="p-6 max-w-3xl mx-auto space-y-6">
        <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-4">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-teal-500/10 border border-teal-500/20 text-teal-400 flex items-center justify-center">
              <User className="h-5 w-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">{user?.full_name}</h3>
              <p className="text-xs text-slate-400">{user?.email} • Instructor Role</p>
            </div>
          </div>
        </div>

        <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-3 text-xs">
          <div className="flex items-center gap-2">
            <ShieldCheck className="h-4 w-4 text-teal-400" />
            <span className="font-bold text-white">Pedagogical Guardrails Active</span>
          </div>
          <p className="text-slate-400 leading-relaxed">
            LearnWise AI enforces strict student data isolation. You can only view students enrolled in your designated classes. Private student Socratic tutor chat transcripts remain confidential; safe aggregated learning telemetry is reported instead.
          </p>
        </div>
      </div>
    </div>
  );
}

'use client';

import React, { useState } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { useAuth } from '@/lib/auth';
import { Settings, Copy, CheckCircle2, ShieldCheck, User } from 'lucide-react';

export default function StudentSettingsPage() {
  const { user } = useAuth();
  const [copied, setCopied] = useState(false);

  const parentUrl = typeof window !== 'undefined' 
    ? `${window.location.origin}/parent/progress/${user?.parent_access_token}` 
    : '';

  const handleCopy = () => {
    navigator.clipboard.writeText(parentUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex-1 pb-16">
      <Navbar title="Student Account Settings" subtitle="Profile telemetry and parent progress access tokens" />

      <div className="p-6 max-w-3xl mx-auto space-y-6">
        {/* Profile Card */}
        <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-4">
          <div className="flex items-center gap-3">
            <div className="h-10 w-10 rounded-xl bg-teal-500/10 border border-teal-500/20 text-teal-400 flex items-center justify-center">
              <User className="h-5 w-5" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">{user?.full_name}</h3>
              <p className="text-xs text-slate-400">{user?.email} • {user?.grade_level || 'Grade 11'}</p>
            </div>
          </div>
        </div>

        {/* Parent Link Portal Card */}
        <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-4">
          <div className="flex items-center gap-2">
            <ShieldCheck className="h-5 w-5 text-teal-400" />
            <h3 className="text-sm font-bold text-white">Parent Progress Access Link</h3>
          </div>
          <p className="text-xs text-slate-400 leading-relaxed">
            Share this secure, read-only link with your parent or guardian. They will be able to monitor your concept mastery and teacher interventions in plain English, while your private AI Tutor chats remain strictly confidential.
          </p>

          <div className="flex gap-2">
            <input
              type="text"
              readOnly
              value={parentUrl}
              className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs font-mono text-slate-300 focus:outline-none"
            />
            <button
              onClick={handleCopy}
              className="py-2 px-4 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 hover:from-teal-400 hover:to-cyan-300 text-xs flex items-center gap-1.5 cursor-pointer"
            >
              {copied ? <CheckCircle2 className="h-3.5 w-3.5" /> : <Copy className="h-3.5 w-3.5" />}
              {copied ? 'Copied' : 'Copy'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

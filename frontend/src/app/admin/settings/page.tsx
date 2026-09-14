'use client';

import React from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { ShieldCheck, Server, Key, Database } from 'lucide-react';

export default function AdminSettingsPage() {
  return (
    <div className="flex-1 pb-16">
      <Navbar title="System Settings" subtitle="Platform configuration and infrastructure telemetry" />

      <div className="p-6 max-w-3xl mx-auto space-y-6">
        <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-4 text-xs">
          <div className="flex items-center gap-2 text-teal-400 font-bold">
            <Server className="h-4 w-4" />
            <span>Infrastructure Status</span>
          </div>

          <div className="space-y-2 text-slate-300">
            <div className="flex justify-between py-2 border-b border-slate-800">
              <span className="text-slate-400">Backend API Engine:</span>
              <span className="font-mono text-emerald-400 font-semibold">FastAPI 0.110 (Online)</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-800">
              <span className="text-slate-400">Database Engine:</span>
              <span className="font-mono text-emerald-400 font-semibold">PostgreSQL / SQLite ORM (Connected)</span>
            </div>
            <div className="flex justify-between py-2 border-b border-slate-800">
              <span className="text-slate-400">Real-time Service:</span>
              <span className="font-mono text-emerald-400 font-semibold">WebSocket Connection Manager (Active)</span>
            </div>
            <div className="flex justify-between py-2">
              <span className="text-slate-400">AI Pedagogical Engine:</span>
              <span className="font-mono text-teal-400 font-semibold">Configurable LLM Provider + Socratic Rule Fallback</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

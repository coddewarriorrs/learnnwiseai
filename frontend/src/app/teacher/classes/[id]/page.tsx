'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { useParams } from 'next/navigation';
import { apiRequest } from '@/lib/api';
import { BookOpen, Users, ArrowLeft, ArrowRight, User } from 'lucide-react';
import Link from 'next/link';

export default function ClassDetailPage() {
  const { id } = useParams();
  const [classData, setClassData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!id) return;
    apiRequest(`/classes/${id}`)
      .then((res) => setClassData(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div className="flex-1">
        <Navbar title="Class Roster" subtitle="Loading..." />
        <div className="p-8 text-center text-slate-400 text-sm">Loading roster...</div>
      </div>
    );
  }

  if (!classData) {
    return (
      <div className="flex-1">
        <Navbar title="Class Roster" subtitle="Error" />
        <div className="p-8 text-center text-rose-400 text-sm">Class not found.</div>
      </div>
    );
  }

  return (
    <div className="flex-1 pb-16">
      <Navbar title={classData.name} subtitle={`Subject: ${classData.subject} • Grade ${classData.grade}`} />

      <div className="p-6 max-w-5xl mx-auto space-y-6">
        <Link href="/teacher/classes" className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-white">
          <ArrowLeft className="h-3.5 w-3.5" /> Back to Classes
        </Link>

        {/* Header Telemetry */}
        <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 flex justify-between items-center">
          <div>
            <h2 className="text-xl font-bold text-white">{classData.name}</h2>
            <p className="text-xs text-slate-400 mt-1">Class Code: <span className="font-mono text-teal-400 font-bold">{classData.class_code}</span></p>
          </div>
          <div className="text-right">
            <span className="text-xs text-slate-400 block">Enrolled Students</span>
            <span className="text-2xl font-bold text-teal-400">{classData.students?.length || 0}</span>
          </div>
        </div>

        {/* Student List */}
        <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 shadow-xl">
          <h3 className="text-sm font-bold text-white mb-4">Student Members</h3>

          {(!classData.students || classData.students.length === 0) ? (
            <p className="text-xs text-slate-500">No students enrolled yet. Share the invite link with your students!</p>
          ) : (
            <div className="divide-y divide-slate-800/60">
              {classData.students.map((s: any) => (
                <div key={s.id} className="py-3.5 flex items-center justify-between text-xs hover:bg-slate-900/30 px-2 rounded-lg transition-colors">
                  <div className="flex items-center gap-3">
                    <div className="h-8 w-8 rounded-full bg-slate-800 border border-slate-700 flex items-center justify-center font-bold text-teal-400">
                      {s.full_name.slice(0, 2).toUpperCase()}
                    </div>
                    <div>
                      <p className="font-bold text-white">{s.full_name}</p>
                      <p className="text-[11px] text-slate-400">{s.email}</p>
                    </div>
                  </div>

                  <Link
                    href={`/teacher/students/${s.id}`}
                    className="py-1.5 px-3 rounded-lg bg-slate-900 border border-slate-700 hover:bg-slate-800 text-teal-300 font-semibold flex items-center gap-1.5"
                  >
                    Diagnostic Deep Dive <ArrowRight className="h-3 w-3" />
                  </Link>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { BookOpen, Users } from 'lucide-react';

export default function AdminClassesPage() {
  const [classes, setClasses] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiRequest('/classes')
      .then((res) => setClasses(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="flex-1 pb-16">
      <Navbar title="Platform Classes Overview" subtitle="All institution-wide cohorts and class rosters" />

      <div className="p-6 max-w-6xl mx-auto space-y-6">
        {loading ? (
          <div className="p-12 text-center text-slate-400 text-sm">Loading platform classes...</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {classes.map((c) => (
              <div key={c.id} className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded-full border bg-slate-800 text-teal-300 border-slate-700">
                    Grade {c.grade} • {c.board}
                  </span>
                  <span className="text-xs text-slate-400">{c.student_count || 0} students</span>
                </div>
                <h3 className="text-base font-bold text-white">{c.name}</h3>
                <p className="text-xs text-slate-400">Subject: {c.subject} • Code: <span className="font-mono text-teal-400">{c.class_code}</span></p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { CheckSquare, CheckCircle2, Clock, RotateCcw, AlertTriangle } from 'lucide-react';

export default function TeacherInterventionsPage() {
  const [interventions, setInterventions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchInterventions = () => {
    apiRequest('/interventions')
      .then((res) => setInterventions(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchInterventions();
  }, []);

  const handleUpdateStatus = async (id: number, newStatus: string) => {
    try {
      await apiRequest(`/interventions/${id}/status`, {
        method: 'PATCH',
        body: JSON.stringify({ status: newStatus }),
      });
      fetchInterventions();
    } catch {
      alert('Failed to update status');
    }
  };

  return (
    <div className="flex-1 pb-16">
      <Navbar 
        title="Interventions Command Board" 
        subtitle="Active pedagogical interventions, targeted remediation & reassessment triggers" 
      />

      <div className="p-6 max-w-6xl mx-auto space-y-6">
        {loading ? (
          <div className="p-12 text-center text-slate-400 text-sm">Loading interventions...</div>
        ) : interventions.length === 0 ? (
          <div className="p-12 rounded-2xl bg-[#162235] border border-slate-800 text-center text-slate-400 text-sm">
            No interventions assigned. Use the Early Warning dashboard or Student Diagnostics to issue remedial action plans.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
            {interventions.map((item) => {
              const isCompleted = item.status === 'COMPLETED';

              return (
                <div key={item.id} className="p-6 rounded-2xl bg-[#162235] border border-slate-800 flex flex-col justify-between space-y-4">
                  <div>
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-[10px] font-bold px-2 py-0.5 rounded-full border bg-slate-800 text-slate-300 border-slate-700">
                        {item.type.replace('_', ' ')}
                      </span>
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                        isCompleted ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30' : 'bg-amber-500/15 text-amber-300 border-amber-500/30'
                      }`}>
                        {item.status}
                      </span>
                    </div>

                    <h4 className="text-sm font-bold text-white mb-1">Student: {item.student_name}</h4>
                    <p className="text-xs text-teal-300 font-medium mb-2">{item.action}</p>
                    <p className="text-xs text-slate-400">{item.reason}</p>
                  </div>

                  <div className="pt-3 border-t border-slate-800 flex items-center justify-between text-xs">
                    <span className="text-slate-500">{new Date(item.created_at).toLocaleDateString()}</span>

                    {!isCompleted ? (
                      <button
                        onClick={() => handleUpdateStatus(item.id, 'COMPLETED')}
                        className="py-1 px-3 rounded-lg font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 text-xs flex items-center gap-1"
                      >
                        <CheckCircle2 className="h-3 w-3" /> Mark Completed & Reassess
                      </button>
                    ) : (
                      <span className="text-emerald-400 font-semibold flex items-center gap-1">
                        <CheckCircle2 className="h-3.5 w-3.5" /> Reassessment Triggered
                      </span>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}

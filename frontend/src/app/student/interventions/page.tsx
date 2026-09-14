'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { 
  CheckSquare, Clock, CheckCircle2, ArrowRight, 
  MessageSquareCode, Target, User, Calendar, Sparkles 
} from 'lucide-react';

export default function StudentInterventionsPage() {
  const [interventions, setInterventions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState<'ALL' | 'ACTIVE' | 'COMPLETED'>('ALL');
  const [updatingId, setUpdatingId] = useState<number | null>(null);

  const fetchInterventions = () => {
    apiRequest('/interventions')
      .then((res) => setInterventions(res || []))
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchInterventions();
  }, []);

  const handleUpdateStatus = async (id: number, newStatus: string) => {
    setUpdatingId(id);
    try {
      await apiRequest(`/interventions/${id}/status`, {
        method: 'PATCH',
        body: JSON.stringify({ status: newStatus }),
      });
      fetchInterventions();
    } catch (err: any) {
      alert(err.message || 'Failed to update intervention status');
    } finally {
      setUpdatingId(null);
    }
  };

  const activeInterventions = interventions.filter(
    (i) => i.status === 'ASSIGNED' || i.status === 'IN_PROGRESS' || i.status === 'RECOMMENDED'
  );
  const completedInterventions = interventions.filter(
    (i) => i.status === 'COMPLETED'
  );

  const displayedList = filter === 'ACTIVE' 
    ? activeInterventions 
    : filter === 'COMPLETED' 
    ? completedInterventions 
    : interventions;

  const getTypeBadge = (type: string) => {
    switch (type) {
      case 'PREREQUISITE_REVIEW':
        return { label: 'Prerequisite Review', bg: 'bg-amber-500/10 text-amber-300 border-amber-500/30' };
      case 'EXTRA_PRACTICE':
        return { label: 'Targeted Practice', bg: 'bg-cyan-500/10 text-cyan-300 border-cyan-500/30' };
      case 'ONE_TO_ONE':
        return { label: '1-on-1 Tutoring Session', bg: 'bg-purple-500/10 text-purple-300 border-purple-500/30' };
      case 'TARGETED_QUIZ':
        return { label: 'Targeted Quiz', bg: 'bg-blue-500/10 text-blue-300 border-blue-500/30' };
      case 'CONCEPT_EXPLANATION':
        return { label: 'Concept Deep-Dive', bg: 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30' };
      default:
        return { label: type.replace(/_/g, ' '), bg: 'bg-slate-800 text-slate-300 border-slate-700' };
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'COMPLETED':
        return { label: 'Completed', bg: 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30' };
      case 'IN_PROGRESS':
        return { label: 'In Progress', bg: 'bg-cyan-500/20 text-cyan-300 border-cyan-500/30' };
      default:
        return { label: 'Action Required', bg: 'bg-amber-500/20 text-amber-300 border-amber-500/30' };
    }
  };

  return (
    <div className="flex-1 pb-16">
      <Navbar 
        title="Teacher Action Plans & Interventions" 
        subtitle="Remedial tasks, guided reviews, and personalized interventions assigned by your teachers" 
      />

      <div className="p-6 max-w-6xl mx-auto space-y-6">
        {/* Metric Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-5 rounded-2xl bg-[#162235] border border-slate-800 flex items-center justify-between">
            <div>
              <p className="text-xs text-[#94A3B8] font-medium uppercase tracking-wider">Total Action Plans</p>
              <h3 className="text-2xl font-bold text-[#F8FAFC] mt-1">{interventions.length}</h3>
              <p className="text-[11px] text-[#94A3B8] mt-0.5">Assigned by course instructors</p>
            </div>
            <div className="h-12 w-12 rounded-xl bg-cyan-500/10 text-[#22D3EE] flex items-center justify-center">
              <CheckSquare className="h-6 w-6" />
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-[#162235] border border-slate-800 flex items-center justify-between">
            <div>
              <p className="text-xs text-[#94A3B8] font-medium uppercase tracking-wider">Active & Pending</p>
              <h3 className="text-2xl font-bold text-amber-400 mt-1">{activeInterventions.length}</h3>
              <p className="text-[11px] text-[#94A3B8] mt-0.5">Requiring your focus & practice</p>
            </div>
            <div className="h-12 w-12 rounded-xl bg-amber-500/10 text-amber-400 flex items-center justify-center">
              <Clock className="h-6 w-6" />
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-[#162235] border border-slate-800 flex items-center justify-between">
            <div>
              <p className="text-xs text-[#94A3B8] font-medium uppercase tracking-wider">Resolved & Completed</p>
              <h3 className="text-2xl font-bold text-emerald-400 mt-1">{completedInterventions.length}</h3>
              <p className="text-[11px] text-[#94A3B8] mt-0.5">Risk mitigated & verified</p>
            </div>
            <div className="h-12 w-12 rounded-xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center">
              <CheckCircle2 className="h-6 w-6" />
            </div>
          </div>
        </div>

        {/* Filter Navigation */}
        <div className="flex flex-wrap items-center justify-between gap-3 border-b border-slate-800 pb-4">
          <div className="flex items-center gap-2">
            <button
              onClick={() => setFilter('ALL')}
              className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                filter === 'ALL'
                  ? 'bg-[#22D3EE] text-[#0B1220] shadow-md shadow-cyan-500/20'
                  : 'bg-[#162235] text-[#94A3B8] hover:bg-[#1C2B42] hover:text-[#F8FAFC]'
              }`}
            >
              All Plans ({interventions.length})
            </button>
            <button
              onClick={() => setFilter('ACTIVE')}
              className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                filter === 'ACTIVE'
                  ? 'bg-amber-400 text-[#0B1220] shadow-md shadow-amber-500/20'
                  : 'bg-[#162235] text-[#94A3B8] hover:bg-[#1C2B42] hover:text-[#F8FAFC]'
              }`}
            >
              Active ({activeInterventions.length})
            </button>
            <button
              onClick={() => setFilter('COMPLETED')}
              className={`px-4 py-2 rounded-xl text-xs font-semibold transition-all ${
                filter === 'COMPLETED'
                  ? 'bg-emerald-400 text-[#0B1220] shadow-md shadow-emerald-500/20'
                  : 'bg-[#162235] text-[#94A3B8] hover:bg-[#1C2B42] hover:text-[#F8FAFC]'
              }`}
            >
              Completed ({completedInterventions.length})
            </button>
          </div>

          <span className="text-xs text-[#94A3B8]">
            Showing {displayedList.length} action {displayedList.length === 1 ? 'plan' : 'plans'}
          </span>
        </div>

        {/* List of Interventions */}
        {loading ? (
          <div className="p-12 text-center text-[#94A3B8] text-sm">
            Loading your teacher action plans...
          </div>
        ) : displayedList.length === 0 ? (
          <div className="p-12 rounded-2xl bg-[#162235] border border-slate-800 text-center space-y-3">
            <div className="h-12 w-12 rounded-2xl bg-emerald-500/10 text-emerald-400 flex items-center justify-center mx-auto">
              <CheckCircle2 className="h-6 w-6" />
            </div>
            <h4 className="text-base font-bold text-[#F8FAFC]">No Action Plans in this Category</h4>
            <p className="text-xs text-[#94A3B8] max-w-md mx-auto">
              {filter === 'COMPLETED' 
                ? 'You have not completed any action plans yet. Tackle your active interventions to reduce academic risk!' 
                : 'Great job! You currently have no pending teacher interventions. Your learning cadence is on track.'}
            </p>
            <Link
              href="/student/practice"
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs font-semibold text-[#F8FAFC] mt-2 transition-colors"
            >
              Continue Adaptive Practice
              <ArrowRight className="h-3.5 w-3.5" />
            </Link>
          </div>
        ) : (
          <div className="space-y-4">
            {displayedList.map((item) => {
              const typeBadge = getTypeBadge(item.type);
              const statusBadge = getStatusBadge(item.status);
              const isDone = item.status === 'COMPLETED';

              return (
                <div
                  key={item.id}
                  className={`p-6 rounded-2xl border transition-all ${
                    isDone 
                      ? 'bg-[#162235]/60 border-slate-800/80' 
                      : 'bg-[#162235] border-amber-500/30 shadow-lg shadow-black/20'
                  }`}
                >
                  <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
                    <div className="space-y-3 flex-1">
                      {/* Top Badges */}
                      <div className="flex flex-wrap items-center gap-2">
                        <span className={`text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${typeBadge.bg}`}>
                          {typeBadge.label}
                        </span>
                        <span className={`text-[11px] font-bold px-2.5 py-0.5 rounded-full border ${statusBadge.bg}`}>
                          {statusBadge.label}
                        </span>
                        {item.topic_title && (
                          <span className="text-[11px] text-[#94A3B8] bg-slate-900 px-2.5 py-0.5 rounded-full border border-slate-800">
                            Topic: {item.topic_title}
                          </span>
                        )}
                      </div>

                      {/* Instructor & Date Info */}
                      <div className="flex flex-wrap items-center gap-4 text-xs text-[#94A3B8]">
                        <span className="flex items-center gap-1.5">
                          <User className="h-3.5 w-3.5 text-[#22D3EE]" />
                          <span>Assigned by: <strong className="text-[#F8FAFC]">{item.teacher_name || 'Instructor'}</strong></span>
                        </span>
                        <span className="flex items-center gap-1.5">
                          <Calendar className="h-3.5 w-3.5 text-slate-500" />
                          <span>{item.created_at ? new Date(item.created_at).toLocaleDateString(undefined, { dateStyle: 'medium' }) : 'Recently'}</span>
                        </span>
                      </div>

                      {/* Pedagogical Reason */}
                      <div className="p-3 rounded-xl bg-[#101827] border border-slate-800 text-xs space-y-1">
                        <span className="text-[#94A3B8] font-medium block">Reason for Intervention:</span>
                        <p className="text-[#F8FAFC] leading-relaxed">{item.reason}</p>
                      </div>

                      {/* Prescribed Action Plan */}
                      <div className="p-3.5 rounded-xl bg-gradient-to-r from-amber-500/10 via-[#101827] to-[#101827] border border-amber-500/20 text-xs space-y-1">
                        <span className="text-amber-300 font-bold block flex items-center gap-1.5">
                          <Sparkles className="h-3.5 w-3.5" />
                          Prescribed Action Plan:
                        </span>
                        <p className="text-[#F8FAFC] leading-relaxed font-medium">{item.action}</p>
                      </div>
                    </div>

                    {/* Interactive Action Controls */}
                    <div className="flex flex-col sm:flex-row md:flex-col gap-2 shrink-0 md:min-w-[180px]">
                      <Link
                        href="/student/practice"
                        className="inline-flex items-center justify-center gap-2 bg-[#22D3EE] hover:bg-cyan-400 text-[#0B1220] font-bold px-4 py-2.5 rounded-xl text-xs transition-all shadow-md shadow-cyan-500/20"
                      >
                        <Target className="h-3.5 w-3.5" />
                        Start Practice Set
                      </Link>

                      <Link
                        href="/student/tutor"
                        className="inline-flex items-center justify-center gap-2 bg-[#162235] hover:bg-[#1C2B42] border border-slate-700 text-[#F8FAFC] font-semibold px-4 py-2.5 rounded-xl text-xs transition-colors"
                      >
                        <MessageSquareCode className="h-3.5 w-3.5 text-[#22D3EE]" />
                        Ask AI Tutor
                      </Link>

                      {/* Status Toggle Buttons */}
                      {!isDone ? (
                        <>
                          {item.status !== 'IN_PROGRESS' && (
                            <button
                              onClick={() => handleUpdateStatus(item.id, 'IN_PROGRESS')}
                              disabled={updatingId === item.id}
                              className="px-4 py-2 rounded-xl bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-500/30 text-[#22D3EE] text-xs font-semibold transition-colors disabled:opacity-50"
                            >
                              {updatingId === item.id ? 'Updating...' : 'Mark In Progress'}
                            </button>
                          )}
                          <button
                            onClick={() => handleUpdateStatus(item.id, 'COMPLETED')}
                            disabled={updatingId === item.id}
                            className="px-4 py-2 rounded-xl bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/30 text-emerald-300 text-xs font-semibold transition-colors disabled:opacity-50"
                          >
                            {updatingId === item.id ? 'Updating...' : 'Mark Completed'}
                          </button>
                        </>
                      ) : (
                        <div className="p-2.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-center">
                          <span className="text-[11px] font-bold text-emerald-300 flex items-center justify-center gap-1.5">
                            <CheckCircle2 className="h-3.5 w-3.5" />
                            Completed
                          </span>
                        </div>
                      )}
                    </div>
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

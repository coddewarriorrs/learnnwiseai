'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { Navbar } from '@/components/layout/Navbar';
import { StatCard } from '@/components/ui/StatCard';
import { MasteryBarChart } from '@/components/charts/MasteryBarChart';
import { apiRequest } from '@/lib/api';
import { 
  Award, Target, AlertTriangle, Flame, ArrowRight, BrainCircuit, 
  BookOpen, CheckCircle2, Clock, Sparkles, CheckSquare 
} from 'lucide-react';

export default function StudentDashboardPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    apiRequest('/students/me/dashboard')
      .then((res) => setData(res))
      .catch((err) => setError(err.message || 'Failed to load dashboard'))
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex-1">
        <Navbar title="Student Workspace" subtitle="Loading your academic telemetry..." />
        <div className="p-8 text-center text-slate-400 text-sm">Loading learning metrics from database...</div>
      </div>
    );
  }

  if (error || !data) {
    return (
      <div className="flex-1">
        <Navbar title="Student Workspace" subtitle="Error loading data" />
        <div className="p-8 text-center text-rose-400 text-sm">{error || 'Unable to load dashboard'}</div>
      </div>
    );
  }

  const { metrics, next_best_action, topic_mastery, enrolled_classes, assignments, recent_activity, interventions } = data;
  const activeInterventions = interventions?.filter((i: any) => i.status !== 'COMPLETED') || [];

  return (
    <div className="flex-1 pb-12">
      <Navbar 
        title={`Welcome back, ${data.student.name}`} 
        subtitle="Adaptive Learning Telemetry & Concept Mastery" 
      />

      <div className="p-6 max-w-7xl mx-auto space-y-6">
        {/* Top Telemetry Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <StatCard
            title="Overall Mastery"
            value={`${metrics.overall_mastery}%`}
            subtitle={`${metrics.topics_mastered} of ${metrics.total_topics_tracked} topics mastered`}
            icon={Award}
            color="teal"
          />
          <StatCard
            title="Topics Needing Attention"
            value={metrics.topics_needing_attention + metrics.critical_topics}
            subtitle={`${metrics.critical_topics} at critical (<40%) mastery`}
            icon={AlertTriangle}
            color={metrics.critical_topics > 0 ? "rose" : "amber"}
          />
          <StatCard
            title="Predicted Academic Risk"
            value={`${metrics.risk_score}/100`}
            subtitle={`${metrics.risk_level} Risk Level`}
            icon={Target}
            color={metrics.risk_level === 'HIGH' ? 'rose' : metrics.risk_level === 'MEDIUM' ? 'amber' : 'teal'}
          />
          <StatCard
            title="Active Learning Streak"
            value={`${metrics.learning_streak_days} Days`}
            subtitle="Consistent practice cadence"
            icon={Flame}
            color="blue"
          />
        </div>

        {/* Teacher Action Plan / Intervention Banner */}
        {activeInterventions.length > 0 && (
          <div className="p-6 rounded-2xl bg-gradient-to-r from-amber-950/40 via-[#162235] to-[#162235] border border-amber-500/40 shadow-lg relative overflow-hidden">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div className="space-y-2">
                <div className="flex items-center gap-2">
                  <span className="p-1 rounded-md bg-amber-500/20 text-amber-400">
                    <CheckSquare className="h-4 w-4" />
                  </span>
                  <span className="text-xs font-bold uppercase tracking-wider text-amber-300">
                    Teacher Action Plan Assigned ({activeInterventions.length} Active)
                  </span>
                  <span className="text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30">
                    {activeInterventions[0].type.replace(/_/g, ' ')}
                  </span>
                </div>
                <h3 className="text-lg font-bold text-white">
                  {activeInterventions[0].reason}
                </h3>
                <p className="text-xs text-slate-300 max-w-2xl leading-relaxed">
                  <strong className="text-amber-300">Prescribed Plan: </strong>
                  {activeInterventions[0].action}
                </p>
                <p className="text-[11px] text-slate-400">
                  Assigned by <span className="text-white font-medium">{activeInterventions[0].teacher_name}</span>
                </p>
              </div>

              <div className="flex flex-wrap items-center gap-3 shrink-0">
                <Link
                  href="/student/practice"
                  className="inline-flex items-center gap-2 bg-amber-400 hover:bg-amber-300 text-slate-950 font-bold px-4 py-2.5 rounded-xl text-xs transition-all shadow-md shadow-amber-500/20"
                >
                  <Target className="h-3.5 w-3.5" />
                  Start Recommended Practice
                </Link>
                <Link
                  href="/student/interventions"
                  className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-xl border border-slate-700 bg-slate-900/80 hover:bg-slate-800 text-slate-200 text-xs font-semibold transition-colors"
                >
                  View All Action Plans ({interventions?.length || 0})
                  <ArrowRight className="h-3.5 w-3.5" />
                </Link>
              </div>
            </div>
          </div>
        )}

        {/* Next Best Action Banner & Risk Explainer */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Next Best Action */}
          <div className="lg:col-span-2 p-6 rounded-2xl bg-gradient-to-r from-teal-950/40 via-[#162235] to-[#162235] border border-teal-500/30 flex flex-col justify-between relative overflow-hidden">
            <div className="absolute right-0 top-0 translate-x-8 -translate-y-8 h-48 w-48 bg-teal-500/10 rounded-full blur-3xl pointer-events-none"></div>
            
            <div>
              <div className="flex items-center gap-2 mb-2">
                <span className="p-1 rounded-md bg-teal-500/20 text-teal-400">
                  <Sparkles className="h-4 w-4" />
                </span>
                <span className="text-xs font-bold uppercase tracking-wider text-teal-300">
                  AI Recommended Next Action
                </span>
              </div>
              <h3 className="text-xl font-bold text-white mt-1">{next_best_action.title}</h3>
              <p className="text-xs text-slate-300 mt-2 max-w-xl leading-relaxed">
                {next_best_action.description}
              </p>
            </div>

            <div className="mt-6 flex flex-wrap items-center gap-3">
              <Link
                href={next_best_action.type === 'PREREQUISITE_REVIEW' || next_best_action.type === 'PRACTICE' ? '/student/practice' : '/student/learning-path'}
                className="inline-flex items-center gap-2 bg-gradient-to-r from-teal-500 to-cyan-400 hover:from-teal-400 hover:to-cyan-300 text-slate-950 font-bold px-4 py-2.5 rounded-lg text-xs transition-all shadow-md shadow-teal-500/20"
              >
                Start Recommended Session
                <ArrowRight className="h-3.5 w-3.5" />
              </Link>
              <Link
                href="/student/learning-path"
                className="inline-flex items-center gap-1.5 px-4 py-2.5 rounded-lg border border-slate-700 bg-slate-900/60 hover:bg-slate-800 text-slate-300 text-xs font-semibold transition-colors"
              >
                View Full Path
              </Link>
            </div>
          </div>

          {/* Explainable Risk Card */}
          <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-3">
                <h3 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">Risk Telemetry</h3>
                <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full border ${
                  metrics.risk_level === 'HIGH' ? 'bg-rose-500/20 text-rose-300 border-rose-500/30' :
                  metrics.risk_level === 'MEDIUM' ? 'bg-amber-500/20 text-amber-300 border-amber-500/30' :
                  'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
                }`}>
                  {metrics.risk_level} RISK
                </span>
              </div>
              <p className="text-xs text-slate-400 font-medium mb-3">Why this score was calculated:</p>
              <ul className="space-y-2">
                {metrics.risk_reasons.map((reason: string, idx: number) => (
                  <li key={idx} className="text-xs text-slate-300 flex items-start gap-2">
                    <span className="text-amber-400 font-bold">•</span>
                    <span>{reason}</span>
                  </li>
                ))}
              </ul>
            </div>
            <p className="text-[11px] text-slate-500 mt-4 border-t border-slate-800/80 pt-3">
              Formula: 0.35 Perf + 0.25 Attend + 0.20 Assign + 0.20 Engage
            </p>
          </div>
        </div>

        {/* Topic Mastery Chart & Enrolled Classes */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 p-6 rounded-2xl bg-[#162235] border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-sm font-bold text-white">Topic Mastery Breakdown</h3>
                <p className="text-xs text-slate-400 mt-0.5">Calculated from recent practice & assessment accuracy</p>
              </div>
              <div className="flex items-center gap-3 text-[11px]">
                <span className="flex items-center gap-1 text-rose-400"><span className="h-2 w-2 rounded-full bg-rose-500"></span> &lt;40% Critical</span>
                <span className="flex items-center gap-1 text-amber-400"><span className="h-2 w-2 rounded-full bg-amber-500"></span> 40-70% Practice</span>
                <span className="flex items-center gap-1 text-emerald-400"><span className="h-2 w-2 rounded-full bg-emerald-500"></span> &gt;70% Strong</span>
              </div>
            </div>
            <MasteryBarChart data={topic_mastery} />
          </div>

          {/* Enrolled Classes */}
          <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-bold text-white">My Classes</h3>
                <Link href="/student/classes" className="text-xs text-teal-400 hover:underline">
                  Manage
                </Link>
              </div>
              {enrolled_classes.length === 0 ? (
                <p className="text-xs text-slate-500">Not enrolled in any class yet.</p>
              ) : (
                <div className="space-y-3">
                  {enrolled_classes.map((c: any) => (
                    <div key={c.id} className="p-3 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="h-8 w-8 rounded-lg bg-teal-500/10 text-teal-400 flex items-center justify-center font-bold text-xs">
                          {c.subject.slice(0, 2).toUpperCase()}
                        </div>
                        <div>
                          <h4 className="text-xs font-semibold text-white">{c.name}</h4>
                          <span className="text-[11px] text-slate-400">{c.subject}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="mt-6 pt-4 border-t border-slate-800/80">
              <Link
                href="/student/classes"
                className="w-full py-2 px-3 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors"
              >
                Join with Class Code
              </Link>
            </div>
          </div>
        </div>

        {/* Assignments & Recent Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Assignments */}
          <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-sm font-bold text-white">Active Assignments</h3>
              <Link href="/student/assignments" className="text-xs text-teal-400 hover:underline">
                View All
              </Link>
            </div>
            {assignments.length === 0 ? (
              <p className="text-xs text-slate-500">No pending assignments.</p>
            ) : (
              <div className="space-y-2.5">
                {assignments.map((a: any) => (
                  <div key={a.id} className="p-3 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-between text-xs">
                    <div>
                      <p className="font-semibold text-white">{a.title}</p>
                      <p className="text-[11px] text-slate-400">Due: {a.due_date ? new Date(a.due_date).toLocaleDateString() : 'No date'}</p>
                    </div>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      a.status === 'COMPLETED' ? 'bg-emerald-500/20 text-emerald-300' : 'bg-amber-500/20 text-amber-300'
                    }`}>
                      {a.status}
                    </span>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Recent Activity */}
          <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800">
            <h3 className="text-sm font-bold text-white mb-4">Recent Learning Telemetry</h3>
            {recent_activity.length === 0 ? (
              <p className="text-xs text-slate-500">No recorded activity yet. Complete a practice session!</p>
            ) : (
              <div className="space-y-2.5">
                {recent_activity.map((act: any) => (
                  <div key={act.id} className="p-3 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-between text-xs">
                    <div className="flex items-center gap-2.5">
                      <CheckCircle2 className="h-4 w-4 text-teal-400" />
                      <div>
                        <p className="font-medium text-slate-200">{act.title}</p>
                        <p className="text-[10px] text-slate-400">{new Date(act.timestamp).toLocaleString()}</p>
                      </div>
                    </div>
                    {act.score !== null && (
                      <span className="font-bold text-teal-400">{act.score}%</span>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

'use client';

import React, { useState, useEffect } from 'react';
import Link from 'next/link';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { 
  Sparkles, BrainCircuit, ShieldAlert, Target, TrendingUp, 
  RotateCcw, ArrowRight, CheckCircle2, Clock, AlertTriangle, 
  Layers, Lightbulb, Zap, ArrowUpRight, History
} from 'lucide-react';

export default function LearningTwinPage() {
  const [twin, setTwin] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [resetting, setResetting] = useState(false);

  const fetchTwinData = async () => {
    setLoading(true);
    try {
      const data = await apiRequest('/twin/me');
      setTwin(data);
    } catch (err) {
      console.error('Failed to load Personal Learning Twin profile:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTwinData();
  }, []);

  const handleResetProfile = async () => {
    const confirm = window.confirm(
      'Are you sure you want to reset your Learning Profile? This will wipe your practice attempts, scores, and mistake history to establish a clean diagnostic baseline. Your user account and enrolled classes will be safely preserved.'
    );
    if (!confirm) return;

    setResetting(true);
    try {
      await apiRequest('/twin/reset-profile', { method: 'POST' });
      alert('Learning profile successfully reset! You now have a clean slate.');
      await fetchTwinData();
    } catch (err: any) {
      alert(err.message || 'Failed to reset learning profile');
    } finally {
      setResetting(false);
    }
  };

  if (loading && !twin) {
    return (
      <div className="flex-1 flex flex-col h-screen">
        <Navbar title="Personal Learning Twin" subtitle="Synchronizing your dynamic cognitive model..." />
        <div className="flex-1 flex items-center justify-center text-slate-400 text-xs">
          <div className="flex items-center gap-2">
            <Sparkles className="h-5 w-5 text-teal-400 animate-spin" />
            <span>Assembling your Personal Learning Twin telemetry...</span>
          </div>
        </div>
      </div>
    );
  }

  const recoverySteps = [
    { step: 1, label: 'Diagnose Difficulty' },
    { step: 2, label: 'Intuitive Concept' },
    { step: 3, label: 'Worked Example' },
    { step: 4, label: 'Guided Micro-Task' },
    { step: 5, label: 'Easy Practice' },
    { step: 6, label: 'Medium Practice' },
    { step: 7, label: 'Final Reassessment' },
  ];

  return (
    <div className="flex-1 pb-16">
      <Navbar 
        title="Personal Learning Twin Hub" 
        subtitle="Real-time cognitive profile mapping practice telemetry, mistake archetypes & adaptive recovery" 
      />

      <div className="p-6 max-w-7xl mx-auto space-y-6">
        {/* Top Summary Banner */}
        <div className="p-6 sm:p-8 rounded-2xl bg-gradient-to-br from-[#162235] to-[#0D1525] border border-slate-800 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="flex items-center gap-2.5">
              <div className="h-10 w-10 rounded-xl bg-teal-500/10 border border-teal-500/20 text-teal-400 flex items-center justify-center shadow-md shadow-teal-500/10">
                <Sparkles className="h-5 w-5" />
              </div>
              <div>
                <h1 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
                  {twin?.student_name}&apos;s Cognitive Learning Twin
                </h1>
                <p className="text-xs text-slate-400">
                  Continuous multi-dimensional modeling of your conceptual strengths, misconceptions, and learning velocity.
                </p>
              </div>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-3">
            <button
              onClick={handleResetProfile}
              disabled={resetting}
              className="py-2.5 px-4 rounded-xl border border-rose-500/30 bg-rose-500/10 hover:bg-rose-500/20 text-rose-300 text-xs font-semibold flex items-center gap-1.5 transition-colors cursor-pointer"
            >
              <RotateCcw className="h-3.5 w-3.5" />
              <span>{resetting ? 'Resetting...' : 'Reset Learning Profile'}</span>
            </button>
          </div>
        </div>

        {/* 4 Key Metics Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="p-5 rounded-2xl bg-[#162235] border border-slate-800">
            <span className="text-xs text-slate-400 block font-medium">Overall Mastery</span>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-2xl sm:text-3xl font-bold text-teal-400">{twin?.overall_mastery || 0}%</span>
              <span className="text-[10px] text-slate-500">Live DB</span>
            </div>
            <div className="w-full bg-slate-800 h-1.5 rounded-full mt-3 overflow-hidden">
              <div 
                className="bg-teal-400 h-full rounded-full transition-all" 
                style={{ width: `${Math.min(100, twin?.overall_mastery || 0)}%` }} 
              />
            </div>
          </div>

          <div className="p-5 rounded-2xl bg-[#162235] border border-slate-800">
            <span className="text-xs text-slate-400 block font-medium">Academic Risk Level</span>
            <div className="flex items-center gap-2 mt-1">
              <span className={`text-xl sm:text-2xl font-bold ${
                twin?.risk_level === 'HIGH' ? 'text-rose-400' : (twin?.risk_level === 'MEDIUM' ? 'text-amber-400' : 'text-emerald-400')
              }`}>
                {twin?.risk_level || 'MEDIUM'}
              </span>
              <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono">
                {twin?.risk_score} score
              </span>
            </div>
            <p className="text-[10px] text-slate-500 mt-2">
              Steers question difficulty dynamically
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-[#162235] border border-slate-800">
            <span className="text-xs text-slate-400 block font-medium">Practice Items & Accuracy</span>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-2xl sm:text-3xl font-bold text-white">{twin?.total_questions_answered || 0}</span>
              <span className="text-xs text-teal-400 font-bold">({twin?.accuracy_rate || 0}%)</span>
            </div>
            <p className="text-[10px] text-slate-500 mt-2">
              Anti-repetition spaced repetition active
            </p>
          </div>

          <div className="p-5 rounded-2xl bg-[#162235] border border-slate-800">
            <span className="text-xs text-slate-400 block font-medium">Learning Velocity</span>
            <div className="flex items-baseline gap-2 mt-1">
              <span className="text-2xl sm:text-3xl font-bold text-cyan-400">{twin?.learning_velocity || 1.0}x</span>
              <span className="text-[10px] text-slate-500">adaptive rate</span>
            </div>
            <p className="text-[10px] text-slate-500 mt-2">
              Based on answer cadence & retention
            </p>
          </div>
        </div>

        {/* Next Best Action Card (Top Priority Action) */}
        {twin?.next_best_action && (
          <div className="p-6 rounded-2xl bg-gradient-to-r from-teal-500/10 via-cyan-500/10 to-transparent border border-teal-500/30 shadow-lg flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
            <div className="space-y-1">
              <div className="flex items-center gap-2 text-xs font-bold text-teal-400 uppercase tracking-wider">
                <Target className="h-4 w-4" />
                <span>Next Best Pedagogical Action</span>
              </div>
              <h2 className="text-base sm:text-lg font-bold text-white">
                {twin.next_best_action.title}
              </h2>
              <p className="text-xs text-slate-300 max-w-2xl leading-relaxed">
                {twin.next_best_action.description}
              </p>
            </div>

            <Link
              href={twin.next_best_action.cta_url || '/student/practice'}
              className="py-3 px-6 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 hover:from-teal-400 hover:to-cyan-300 text-xs flex items-center gap-2 shadow-lg shadow-teal-500/20 shrink-0 transition-transform hover:scale-102"
            >
              <span>{twin.next_best_action.cta_label || 'Start Now'}</span>
              <ArrowRight className="h-4 w-4" />
            </Link>
          </div>
        )}

        {/* 2-Column Main Section: Misconception Fingerprint & Recovery Mode */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Misconception Fingerprint */}
          <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <ShieldAlert className="h-5 w-5 text-purple-400" />
                <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                  Misconception Fingerprint
                </h3>
              </div>
              <span className="text-[10px] text-purple-400 font-mono">
                {twin?.misconception_fingerprint?.length || 0} Patterns
              </span>
            </div>

            {twin?.misconception_fingerprint && twin.misconception_fingerprint.length > 0 ? (
              <div className="space-y-3">
                {twin.misconception_fingerprint.map((item: any, i: number) => (
                  <div key={i} className="p-4 rounded-xl bg-purple-500/10 border border-purple-500/20 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-xs text-purple-300 uppercase">
                        {item.mistake_type.replace(/_/g, ' ')}
                      </span>
                      <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-purple-500/20 text-purple-200">
                        {item.count} occurrences ({item.frequency_pct}%)
                      </span>
                    </div>

                    <div className="text-[11px] text-slate-300 flex items-center gap-2">
                      <span className="text-slate-500">Detected in:</span>
                      <span className="font-medium text-slate-200">
                        {item.topics?.join(', ') || 'Topic Practice'}
                      </span>
                    </div>

                    <div className="p-2.5 rounded-lg bg-slate-900/80 border border-purple-500/10 text-[11px] text-slate-300 flex items-start gap-2">
                      <Lightbulb className="h-3.5 w-3.5 text-amber-400 shrink-0 mt-0.5" />
                      <span>{item.remedy_advice}</span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-6 rounded-xl bg-slate-900/60 border border-slate-800 text-center space-y-2">
                <CheckCircle2 className="h-8 w-8 text-teal-400 mx-auto opacity-70" />
                <p className="text-xs text-slate-300 font-medium">No active misconception patterns detected!</p>
                <p className="text-[11px] text-slate-500">
                  As you practice, recurring mistake patterns across the 8 error archetypes will appear here with tailored remedies.
                </p>
              </div>
            )}
          </div>

          {/* Learning Recovery Mode Status */}
          <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <BrainCircuit className="h-5 w-5 text-rose-400" />
                <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                  Learning Recovery Mode
                </h3>
              </div>
              <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                twin?.recovery_mode?.active 
                  ? 'bg-rose-500/20 text-rose-300 border border-rose-500/30 animate-pulse' 
                  : 'bg-slate-800 text-slate-400'
              }`}>
                {twin?.recovery_mode?.active ? `STEP ${twin.recovery_mode.step} ACTIVE` : 'STANDBY'}
              </span>
            </div>

            {twin?.recovery_mode?.active ? (
              <div className="space-y-4">
                <div className="p-3.5 rounded-xl bg-rose-500/10 border border-rose-500/25 space-y-1">
                  <span className="text-[11px] font-bold text-rose-300 block uppercase">
                    Scaffolding in progress: {twin.recovery_mode.topic_name}
                  </span>
                  <p className="text-xs text-slate-300">
                    {twin.recovery_mode.guidance}
                  </p>
                </div>

                {/* 7-Step Progression Tracker */}
                <div className="space-y-2">
                  <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider block">
                    7-Step Recovery Progression
                  </span>
                  <div className="grid grid-cols-7 gap-1">
                    {recoverySteps.map((s) => {
                      const isPast = s.step < twin.recovery_mode.step;
                      const isCurrent = s.step === twin.recovery_mode.step;
                      return (
                        <div key={s.step} className="flex flex-col items-center gap-1">
                          <div className={`h-8 w-full rounded-lg text-xs font-bold flex items-center justify-center transition-all ${
                            isCurrent
                              ? 'bg-rose-500 text-white shadow-lg shadow-rose-500/30 ring-2 ring-rose-400'
                              : isPast
                              ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                              : 'bg-slate-900 text-slate-600 border border-slate-800'
                          }`}>
                            {s.step}
                          </div>
                          <span className="text-[8px] text-center text-slate-500 truncate w-full hidden sm:block">
                            {s.label.split(' ')[0]}
                          </span>
                        </div>
                      );
                    })}
                  </div>
                </div>

                <Link
                  href={`/student/practice?topic_id=${twin.recovery_mode.topic_id}&difficulty=EASY`}
                  className="w-full py-2.5 rounded-xl bg-rose-500 hover:bg-rose-400 text-white font-bold text-xs flex items-center justify-center gap-2 transition-all shadow-md shadow-rose-500/20"
                >
                  <span>Resume Recovery Step {twin.recovery_mode.step}</span>
                  <ArrowRight className="h-4 w-4" />
                </Link>
              </div>
            ) : (
              <div className="p-6 rounded-xl bg-slate-900/60 border border-slate-800 text-center space-y-2">
                <CheckCircle2 className="h-8 w-8 text-teal-400 mx-auto opacity-70" />
                <p className="text-xs text-slate-300 font-medium">Concept Stability Normal</p>
                <p className="text-[11px] text-slate-500">
                  Recovery mode engages automatically when 3 consecutive mistakes occur on a single topic, shifting practice to step-by-step intuitive scaffolding.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* 2-Column Section: Prerequisite Knowledge Gaps & Knowledge Decay */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Prerequisite Knowledge Gaps */}
          <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <Layers className="h-5 w-5 text-amber-400" />
                <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                  Prerequisite Knowledge Gaps (DAG)
                </h3>
              </div>
              <span className="text-[10px] text-amber-400 font-mono">
                {twin?.prerequisite_gaps?.length || 0} Root Gaps
              </span>
            </div>

            {twin?.prerequisite_gaps && twin.prerequisite_gaps.length > 0 ? (
              <div className="space-y-3">
                {twin.prerequisite_gaps.map((gap: any, idx: number) => (
                  <div key={idx} className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-xs text-amber-200">{gap.topic_name}</span>
                      <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/20 text-amber-300">
                        {gap.gap_severity}
                      </span>
                    </div>

                    <div className="text-[11px] text-slate-300">
                      <span className="text-slate-400">Root Cause: </span>
                      <strong className="text-teal-300">{gap.root_prerequisite_name}</strong>
                    </div>

                    <p className="text-[11px] text-slate-400 leading-relaxed">
                      {gap.suggested_action}
                    </p>

                    <Link
                      href={`/student/practice?topic_id=${gap.root_prerequisite_id}&difficulty=EASY`}
                      className="text-[11px] text-teal-400 hover:text-teal-300 font-semibold inline-flex items-center gap-1 pt-1"
                    >
                      <span>Review prerequisite &quot;{gap.root_prerequisite_name}&quot;</span>
                      <ArrowUpRight className="h-3.5 w-3.5" />
                    </Link>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-6 rounded-xl bg-slate-900/60 border border-slate-800 text-center space-y-2">
                <CheckCircle2 className="h-8 w-8 text-teal-400 mx-auto opacity-70" />
                <p className="text-xs text-slate-300 font-medium">Prerequisite Foundations Solid</p>
                <p className="text-[11px] text-slate-500">
                  No foundational gaps identified along the curriculum dependency graph.
                </p>
              </div>
            )}
          </div>

          {/* Knowledge Decay / Spaced Memory Alerts */}
          <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div className="flex items-center gap-2">
                <Clock className="h-5 w-5 text-cyan-400" />
                <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                  Knowledge Decay & Spaced Review
                </h3>
              </div>
              <span className="text-[10px] text-cyan-400 font-mono">
                {twin?.decayed_topics?.length || 0} Topics Due
              </span>
            </div>

            {twin?.decayed_topics && twin.decayed_topics.length > 0 ? (
              <div className="space-y-3">
                {twin.decayed_topics.map((d: any, idx: number) => (
                  <div key={idx} className="p-4 rounded-xl bg-cyan-500/10 border border-cyan-500/20 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-xs text-cyan-200">{d.topic_name}</span>
                      <span className="text-[11px] font-mono text-cyan-400">
                        {d.days_since_last_practice} days elapsed
                      </span>
                    </div>

                    <div className="flex items-center justify-between text-[11px] text-slate-300">
                      <span>Peak Mastery: <strong>{d.highest_mastery}%</strong></span>
                      <span className="text-amber-300">Current Retention: <strong>{d.current_estimated_mastery}%</strong></span>
                    </div>

                    <Link
                      href={`/student/practice?topic_id=${d.topic_id}&difficulty=MEDIUM`}
                      className="w-full py-2 rounded-lg bg-cyan-500/20 hover:bg-cyan-500/30 text-cyan-200 text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors"
                    >
                      <span>Quick 5-Minute Refresher Practice</span>
                      <ArrowRight className="h-3.5 w-3.5" />
                    </Link>
                  </div>
                ))}
              </div>
            ) : (
              <div className="p-6 rounded-xl bg-slate-900/60 border border-slate-800 text-center space-y-2">
                <CheckCircle2 className="h-8 w-8 text-teal-400 mx-auto opacity-70" />
                <p className="text-xs text-slate-300 font-medium">Retention Curves Healthy</p>
                <p className="text-[11px] text-slate-500">
                  Topics previously mastered remain well within the memory retention half-life.
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Predictive What-If Simulations */}
        <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-4">
          <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
            <Zap className="h-5 w-5 text-amber-400" />
            <div>
              <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                What-If Predictive Simulations
              </h3>
              <p className="text-[11px] text-slate-400">
                Cognitive projection of how targeted study actions affect your overall mastery and risk.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {(twin?.what_if_simulations || []).map((sim: any, idx: number) => (
              <div key={idx} className="p-4 rounded-xl bg-slate-900/80 border border-slate-800 space-y-3">
                <span className="text-xs font-semibold text-slate-200 block leading-tight">
                  {sim.scenario}
                </span>

                <div className="flex items-center justify-between pt-2 border-t border-slate-800 text-xs">
                  <span className="text-slate-400">Projected Gain:</span>
                  <span className="font-bold text-teal-400">+{sim.projected_mastery_gain}%</span>
                </div>

                <div className="flex items-center justify-between text-xs">
                  <span className="text-slate-400">New Mastery:</span>
                  <span className="font-bold text-white">{sim.projected_new_mastery}%</span>
                </div>

                <div className="flex items-center justify-between text-[11px] text-slate-400">
                  <span>Target Time:</span>
                  <span className="font-mono text-cyan-300">{sim.recommended_time_minutes} mins</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Timeline Progression History */}
        {twin?.timeline && twin.timeline.length > 0 && (
          <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-800 pb-3">
              <History className="h-5 w-5 text-teal-400" />
              <h3 className="text-sm font-bold text-white uppercase tracking-wider">
                Personal Learning Twin Timeline Progression
              </h3>
            </div>

            <div className="space-y-3">
              {twin.timeline.map((event: any, idx: number) => (
                <div key={idx} className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="font-mono font-bold text-teal-400">{event.week_or_date}</span>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        event.status === 'MASTERED' 
                          ? 'bg-emerald-500/20 text-emerald-300' 
                          : (event.status === 'IMPROVING' ? 'bg-teal-500/20 text-teal-300' : 'bg-rose-500/20 text-rose-300')
                      }`}>
                        {event.status}
                      </span>
                    </div>
                    <p className="text-slate-300">{event.summary}</p>
                  </div>

                  <div className="flex items-center gap-4 text-slate-400 text-[11px] shrink-0">
                    <div>Questions: <strong className="text-white">{event.questions_attempted}</strong></div>
                    <div>Mistakes: <strong className="text-amber-300">{event.mistakes_made}</strong></div>
                    <div>Avg Mastery: <strong className="text-teal-400">{event.mastery_avg}%</strong></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

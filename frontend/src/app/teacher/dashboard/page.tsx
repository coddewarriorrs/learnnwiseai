'use client';

import React, { useState, useEffect, useCallback } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { StatCard } from '@/components/ui/StatCard';
import { RiskDonutChart } from '@/components/charts/RiskDonutChart';
import { useAuth } from '@/lib/auth';
import { useTeacherWebSocket } from '@/lib/ws';
import { apiRequest } from '@/lib/api';
import { 
  Users, BookOpen, Award, AlertTriangle, Radio, ArrowRight, 
  CheckCircle2, Clock, Sparkles 
} from 'lucide-react';
import Link from 'next/link';

export default function TeacherDashboardPage() {
  const { user } = useAuth();
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [activityFeed, setActivityFeed] = useState<any[]>([]);

  const fetchDashboard = () => {
    apiRequest('/teacher/dashboard')
      .then((res) => {
        setData(res);
        setActivityFeed(res.activity_feed || []);
      })
      .catch(() => {})
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchDashboard();
  }, []);

  // Real-time WebSocket handler
  const handleWsEvent = useCallback((event: any) => {
    if (event.event === 'PRACTICE_COMPLETED' || event.event === 'ASSESSMENT_COMPLETED' || event.event === 'ASSIGNMENT_SUBMITTED') {
      const newEntry = {
        id: Date.now(),
        student_name: event.data.student_name,
        title: event.event === 'PRACTICE_COMPLETED' 
          ? `Completed practice: ${event.data.question_title}` 
          : event.event === 'ASSESSMENT_COMPLETED'
          ? `Submitted assessment: ${event.data.assessment_title} (${event.data.percentage}%)`
          : `Submitted assignment: ${event.data.assignment_title}`,
        type: event.event.split('_')[0],
        score: event.data.score || null,
        timestamp: new Date().toISOString(),
        isLive: true,
      };

      setActivityFeed((prev) => [newEntry, ...prev.slice(0, 14)]);
      // Silently refresh metrics in background
      apiRequest('/teacher/dashboard').then((res) => {
        setData((prevData: any) => ({
          ...prevData,
          metrics: res.metrics,
          risk_distribution: res.risk_distribution,
          topic_weaknesses: res.topic_weaknesses
        }));
      }).catch(() => {});
    }
  }, []);

  useTeacherWebSocket(user?.id, handleWsEvent);

  if (loading) {
    return (
      <div className="flex-1">
        <Navbar title="Teacher Command Center" subtitle="Connecting to live classroom telemetry..." />
        <div className="p-8 text-center text-slate-400 text-sm">Aggregating student diagnostic records...</div>
      </div>
    );
  }

  const { metrics, risk_distribution, topic_weaknesses, classes } = data || {};

  return (
    <div className="flex-1 pb-16">
      <Navbar 
        title="Teacher Command Center" 
        subtitle="Real-time class intelligence, prerequisite gap heatmaps, and early risk detection" 
      />

      <div className="p-6 max-w-7xl mx-auto space-y-6">
        {/* Top Telemetry Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <StatCard
            title="Total Students"
            value={metrics?.total_students || 0}
            subtitle={`Across ${metrics?.total_classes || 0} active classes`}
            icon={Users}
            color="teal"
          />
          <StatCard
            title="Class Average Mastery"
            value={`${metrics?.average_mastery || 0}%`}
            subtitle="Weighted across syllabus topics"
            icon={Award}
            color="blue"
          />
          <StatCard
            title="High Risk Students"
            value={metrics?.high_risk_count || 0}
            subtitle={`${metrics?.medium_risk_count || 0} medium risk`}
            icon={AlertTriangle}
            color={metrics?.high_risk_count > 0 ? "rose" : "amber"}
          />
          <StatCard
            title="Pending Interventions"
            value={metrics?.pending_interventions || 0}
            subtitle="Action plans assigned"
            icon={CheckCircle2}
            color="teal"
          />
        </div>

        {/* Risk Distribution & Live Activity Stream */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Risk Donut Chart */}
          <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-2">
                <h3 className="text-sm font-bold text-white">Cohort Risk Distribution</h3>
                <Link href="/teacher/early-warning" className="text-xs text-teal-400 hover:underline">
                  View Triage
                </Link>
              </div>
              <p className="text-xs text-slate-400 mb-4">Calculated via multi-factor academic risk engine</p>
              <RiskDonutChart data={risk_distribution || []} />
            </div>

            <div className="pt-4 border-t border-slate-800/80 mt-4">
              <Link
                href="/teacher/early-warning"
                className="w-full py-2 px-3 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors"
              >
                Open Early Warning Dashboard
              </Link>
            </div>
          </div>

          {/* Real-time Activity Feed */}
          <div className="lg:col-span-2 p-6 rounded-2xl bg-[#162235] border border-slate-800 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <h3 className="text-sm font-bold text-white">Live Activity & Telemetry Feed</h3>
                  <span className="flex items-center gap-1 px-2 py-0.5 rounded-full bg-teal-500/10 border border-teal-500/30 text-[10px] font-bold text-teal-300">
                    <Radio className="h-3 w-3 text-teal-400 animate-pulse" /> WebSocket Live
                  </span>
                </div>
                <span className="text-xs text-slate-500">No page refresh needed</span>
              </div>
              <p className="text-xs text-slate-400 mb-4">Real-time learning events broadcast directly from student browsers</p>

              {activityFeed.length === 0 ? (
                <div className="p-8 text-center text-slate-500 text-xs">Waiting for student submissions...</div>
              ) : (
                <div className="space-y-2.5 max-h-72 overflow-y-auto pr-1">
                  {activityFeed.map((act) => (
                    <div
                      key={act.id}
                      className={`p-3 rounded-xl border transition-all flex items-center justify-between text-xs ${
                        act.isLive 
                          ? 'bg-teal-500/10 border-teal-500/30 text-teal-200 animate-pulse' 
                          : 'bg-slate-900 border-slate-800 text-slate-300'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div className="h-7 w-7 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-teal-400 shrink-0 font-bold text-[10px]">
                          {act.student_name ? act.student_name.slice(0, 2).toUpperCase() : 'ST'}
                        </div>
                        <div>
                          <p className="font-semibold text-white">
                            {act.student_name}: <span className="font-normal text-slate-300">{act.title}</span>
                          </p>
                          <p className="text-[10px] text-slate-500">
                            {new Date(act.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                          </p>
                        </div>
                      </div>
                      {act.score !== null && (
                        <span className="font-bold text-teal-400 ml-2">{act.score}%</span>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Topic Gaps & Class List */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Class-wide Concept Gaps */}
          <div className="lg:col-span-2 p-6 rounded-2xl bg-[#162235] border border-slate-800">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-sm font-bold text-white">Class-wide Concept Learning Gaps</h3>
                <p className="text-xs text-slate-400">Lowest mastery topics requiring classroom intervention</p>
              </div>
              <Link href="/teacher/analytics" className="text-xs text-teal-400 hover:underline">
                Full Heatmap
              </Link>
            </div>

            <div className="space-y-3">
              {topic_weaknesses?.map((tw: any, idx: number) => (
                <div key={idx} className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 flex items-center justify-between text-xs">
                  <div>
                    <p className="font-bold text-white">{tw.topic}</p>
                    <span className="text-[11px] text-rose-400">
                      {tw.students_critical} student(s) at critical status (&lt;40%)
                    </span>
                  </div>
                  <div className="text-right">
                    <span className="text-sm font-bold text-white block">{tw.average_mastery}%</span>
                    <span className="text-[10px] text-slate-500">Class Average</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Classes Quick Links */}
          <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-bold text-white">My Classes</h3>
                <Link href="/teacher/classes/create" className="text-xs text-teal-400 hover:underline font-semibold">
                  + New Class
                </Link>
              </div>

              <div className="space-y-2.5">
                {classes?.map((c: any) => (
                  <Link
                    key={c.id}
                    href={`/teacher/classes/${c.id}`}
                    className="p-3 rounded-xl bg-slate-900 hover:bg-slate-800/80 border border-slate-800 flex items-center justify-between transition-colors block"
                  >
                    <div>
                      <h4 className="text-xs font-bold text-white">{c.name}</h4>
                      <p className="text-[11px] text-slate-400">{c.subject} • Code: <span className="font-mono text-teal-400">{c.code}</span></p>
                    </div>
                    <ArrowRight className="h-3.5 w-3.5 text-slate-500" />
                  </Link>
                ))}
              </div>
            </div>

            <div className="pt-4 border-t border-slate-800/80 mt-4">
              <Link
                href="/teacher/classes"
                className="w-full py-2 px-3 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors"
              >
                Manage Class Invites & Codes
              </Link>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

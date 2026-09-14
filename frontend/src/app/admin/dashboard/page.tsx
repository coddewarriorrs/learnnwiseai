'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { StatCard } from '@/components/ui/StatCard';
import { apiRequest } from '@/lib/api';
import { Users, BookOpen, BrainCircuit, HelpCircle, Award, Shield } from 'lucide-react';
import Link from 'next/link';

export default function AdminDashboardPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiRequest('/admin/dashboard')
      .then((res) => setData(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return (
      <div className="flex-1">
        <Navbar title="Platform Administration" subtitle="Loading metrics..." />
        <div className="p-8 text-center text-slate-400 text-sm">Aggregating platform health...</div>
      </div>
    );
  }

  const { metrics } = data || {};

  return (
    <div className="flex-1 pb-16">
      <Navbar title="Platform Administration" subtitle="System-wide telemetry, curriculum architecture, and user control" />

      <div className="p-6 max-w-7xl mx-auto space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <StatCard
            title="Total Registered Users"
            value={metrics?.total_users || 0}
            subtitle={`${metrics?.total_students || 0} students • ${metrics?.total_teachers || 0} teachers`}
            icon={Users}
            color="teal"
          />
          <StatCard
            title="Active Classes"
            value={metrics?.total_classes || 0}
            subtitle="Platform-wide cohorts"
            icon={BookOpen}
            color="blue"
          />
          <StatCard
            title="Curriculum Nodes"
            value={metrics?.total_curriculum_nodes || 0}
            subtitle="DAG topics with prerequisites"
            icon={BrainCircuit}
            color="teal"
          />
          <StatCard
            title="Questions Database"
            value={metrics?.total_questions || 0}
            subtitle="Mapped with explanations"
            icon={HelpCircle}
            color="amber"
          />
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link
            href="/admin/syllabus"
            className="p-6 rounded-2xl bg-[#131E32] border border-slate-800 hover:border-teal-500/40 transition-all block group"
          >
            <BrainCircuit className="h-8 w-8 text-teal-400 mb-3 group-hover:scale-105 transition-transform" />
            <h3 className="text-base font-bold text-white mb-1">Curriculum &amp; DAG Hierarchy</h3>
            <p className="text-xs text-slate-400">View and edit official syllabus structure, prerequisite mappings, and import nodes.</p>
          </Link>

          <Link
            href="/admin/users"
            className="p-6 rounded-2xl bg-[#131E32] border border-slate-800 hover:border-teal-500/40 transition-all block group"
          >
            <Users className="h-8 w-8 text-cyan-400 mb-3 group-hover:scale-105 transition-transform" />
            <h3 className="text-base font-bold text-white mb-1">User Directory</h3>
            <p className="text-xs text-slate-400">Manage teachers, students, and administrators with role-based access assignment.</p>
          </Link>

          <Link
            href="/admin/classes"
            className="p-6 rounded-2xl bg-[#131E32] border border-slate-800 hover:border-teal-500/40 transition-all block group"
          >
            <BookOpen className="h-8 w-8 text-amber-400 mb-3 group-hover:scale-105 transition-transform" />
            <h3 className="text-base font-bold text-white mb-1">Class Cohorts</h3>
            <p className="text-xs text-slate-400">Review all active classes, instructor assignments, and student membership rosters.</p>
          </Link>
        </div>
      </div>
    </div>
  );
}

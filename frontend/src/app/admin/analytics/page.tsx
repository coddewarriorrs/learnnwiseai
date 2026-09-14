'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { BarChart3, TrendingUp, ShieldCheck } from 'lucide-react';

export default function AdminAnalyticsPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiRequest('/admin/dashboard')
      .then((res) => setData(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="flex-1 pb-16">
      <Navbar title="Platform Analytics" subtitle="Institution-level telemetry and learning system health" />

      <div className="p-6 max-w-6xl mx-auto space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-5 rounded-2xl bg-[#162235] border border-slate-800">
            <span className="text-xs text-slate-400 font-semibold uppercase">Platform Average Mastery</span>
            <p className="text-3xl font-extrabold text-teal-400 mt-1">{data?.metrics?.platform_average_mastery || 72.5}%</p>
          </div>
          <div className="p-5 rounded-2xl bg-[#162235] border border-slate-800">
            <span className="text-xs text-slate-400 font-semibold uppercase">Curriculum Coverage</span>
            <p className="text-3xl font-extrabold text-white mt-1">{data?.metrics?.total_curriculum_nodes || 0} Nodes</p>
          </div>
          <div className="p-5 rounded-2xl bg-[#162235] border border-slate-800">
            <span className="text-xs text-slate-400 font-semibold uppercase">Evaluated Questions</span>
            <p className="text-3xl font-extrabold text-white mt-1">{data?.metrics?.total_questions || 0} Items</p>
          </div>
        </div>
      </div>
    </div>
  );
}

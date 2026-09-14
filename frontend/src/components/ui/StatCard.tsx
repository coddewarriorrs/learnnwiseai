import React from 'react';
import { LucideIcon } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  trend?: string;
  trendUp?: boolean;
  color?: 'teal' | 'rose' | 'amber' | 'blue';
}

export function StatCard({ title, value, subtitle, icon: Icon, trend, trendUp, color = 'teal' }: StatCardProps) {
  const colorMap = {
    teal: {
      bg: 'bg-teal-500/10',
      border: 'border-teal-500/20',
      icon: 'text-teal-400',
      glow: 'group-hover:shadow-teal-500/10'
    },
    rose: {
      bg: 'bg-rose-500/10',
      border: 'border-rose-500/20',
      icon: 'text-rose-400',
      glow: 'group-hover:shadow-rose-500/10'
    },
    amber: {
      bg: 'bg-amber-500/10',
      border: 'border-amber-500/20',
      icon: 'text-amber-400',
      glow: 'group-hover:shadow-amber-500/10'
    },
    blue: {
      bg: 'bg-cyan-500/10',
      border: 'border-cyan-500/20',
      icon: 'text-cyan-400',
      glow: 'group-hover:shadow-cyan-500/10'
    }
  };

  const scheme = colorMap[color] || colorMap.teal;

  return (
    <div className={`p-5 rounded-xl bg-[#162235] hover:bg-[#1C2B42] border border-slate-800/80 transition-all hover:border-slate-700 hover:shadow-lg ${scheme.glow} group`}>
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{title}</span>
        <div className={`p-2 rounded-lg ${scheme.bg} ${scheme.border} border`}>
          <Icon className={`h-4 w-4 ${scheme.icon}`} />
        </div>
      </div>
      <div className="mt-3 flex items-baseline gap-2">
        <h3 className="text-2xl font-bold text-white tracking-tight">{value}</h3>
        {trend && (
          <span className={`text-xs font-semibold ${trendUp ? 'text-emerald-400' : 'text-rose-400'}`}>
            {trend}
          </span>
        )}
      </div>
      {subtitle && <p className="mt-1 text-xs text-slate-400">{subtitle}</p>}
    </div>
  );
}

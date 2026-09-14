import React from 'react';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'critical' | 'warning' | 'success' | 'info' | 'neutral';
  className?: string;
}

export function Badge({ children, variant = 'info', className = '' }: BadgeProps) {
  const variantClasses = {
    critical: 'bg-rose-500/15 text-rose-300 border-rose-500/30',
    warning: 'bg-amber-500/15 text-amber-300 border-amber-500/30',
    success: 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30',
    info: 'bg-cyan-500/15 text-cyan-300 border-cyan-500/30',
    neutral: 'bg-slate-700/40 text-slate-300 border-slate-600/50',
  };

  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[11px] font-semibold border ${variantClasses[variant]} ${className}`}>
      {children}
    </span>
  );
}

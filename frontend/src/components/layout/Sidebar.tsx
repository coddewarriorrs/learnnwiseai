'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { 
  LayoutDashboard, BookOpen, BrainCircuit, Target, MessageSquareCode, 
  TrendingUp, FileCheck, FileText, Settings, Users, AlertTriangle, 
  BarChart3, Sparkles, LogOut, CheckSquare
} from 'lucide-react';

export function Sidebar() {
  const pathname = usePathname();
  const { user, logout } = useAuth();

  if (!user) return null;

  const studentLinks = [
    { href: '/student/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/student/learning-twin', label: 'Learning Twin', icon: Sparkles, badge: 'Twin' },
    { href: '/student/classes', label: 'My Classes', icon: BookOpen },
    { href: '/student/practice', label: 'Adaptive Practice', icon: Target },
    { href: '/student/learning-path', label: 'Learning Path', icon: BrainCircuit },
    { href: '/student/tutor', label: 'AI Multimodal Tutor', icon: MessageSquareCode },
    { href: '/student/progress', label: 'Mastery & Progress', icon: TrendingUp },
    { href: '/student/assignments', label: 'Assignments', icon: FileCheck },
    { href: '/student/interventions', label: 'Action Plans', icon: CheckSquare },
    { href: '/student/reports', label: 'Reports', icon: FileText },
    { href: '/student/settings', label: 'Settings', icon: Settings },
  ];

  const teacherLinks = [
    { href: '/teacher/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/teacher/classes', label: 'Classes', icon: BookOpen },
    { href: '/teacher/students', label: 'Student Diagnostic', icon: Users },
    { href: '/teacher/early-warning', label: 'Early Warning Risk', icon: AlertTriangle, badge: 'AI' },
    { href: '/teacher/analytics', label: 'Class Analytics', icon: BarChart3 },
    { href: '/teacher/assignments', label: 'Assignments', icon: FileCheck },
    { href: '/teacher/interventions', label: 'Interventions', icon: CheckSquare },
    { href: '/teacher/reports', label: 'Reports & Export', icon: FileText },
    { href: '/teacher/settings', label: 'Settings', icon: Settings },
  ];

  const adminLinks = [
    { href: '/admin/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/admin/users', label: 'User Directory', icon: Users },
    { href: '/admin/classes', label: 'Classes', icon: BookOpen },
    { href: '/admin/syllabus', label: 'Curriculum & DAG', icon: BrainCircuit },
    { href: '/admin/analytics', label: 'Platform Analytics', icon: BarChart3 },
    { href: '/admin/settings', label: 'System Settings', icon: Settings },
  ];

  const links = user.role === 'TEACHER' 
    ? teacherLinks 
    : user.role === 'ADMIN' 
    ? adminLinks 
    : studentLinks;

  return (
    <aside className="w-64 bg-[#101827] border-r border-slate-800 flex flex-col h-screen sticky top-0 z-30 select-none">
      {/* Brand Header */}
      <div className="p-5 border-b border-slate-800/80 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="h-9 w-9 rounded-xl bg-gradient-to-tr from-[#22D3EE] to-[#8B5CF6] flex items-center justify-center shadow-lg shadow-[#22D3EE]/20 group-hover:scale-105 transition-transform">
            <Sparkles className="h-5 w-5 text-slate-950 stroke-[2.5]" />
          </div>
          <div>
            <span className="text-lg font-bold tracking-tight text-[#F8FAFC] block leading-tight">
              LearnWise <span className="text-[#22D3EE]">AI</span>
            </span>
            <span className="text-[10px] tracking-wider uppercase font-semibold text-[#94A3B8] block">
              {user.role} PORTAL
            </span>
          </div>
        </Link>
      </div>

      {/* Navigation Links */}
      <div className="flex-1 overflow-y-auto px-3 py-4 space-y-1">
        {links.map((link) => {
          const Icon = link.icon;
          const isActive = pathname === link.href || pathname.startsWith(`${link.href}/`);
          return (
            <Link
              key={link.href}
              href={link.href}
              className={`flex items-center justify-between px-3.5 py-2.5 rounded-lg text-sm font-medium transition-all ${
                isActive
                  ? 'bg-[#162235] text-[#22D3EE] border border-[#22D3EE]/30 shadow-sm'
                  : 'text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-[#1C2B42]'
              }`}
            >
              <div className="flex items-center gap-3">
                <Icon className={`h-4 w-4 ${isActive ? 'text-[#22D3EE]' : 'text-[#94A3B8]'}`} />
                <span>{link.label}</span>
              </div>
              {link.badge && (
                <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#F59E0B]/20 text-[#F59E0B] border border-[#F59E0B]/40">
                  {link.badge}
                </span>
              )}
            </Link>
          );
        })}
      </div>

      {/* User Footer */}
      <div className="p-4 border-t border-slate-800/80 bg-[#101827]">
        <div className="flex items-center justify-between">
          <div className="overflow-hidden pr-2">
            <p className="text-xs font-semibold text-slate-200 truncate">{user.full_name}</p>
            <p className="text-[11px] text-slate-400 truncate">{user.email}</p>
          </div>
          <button
            onClick={logout}
            title="Sign Out"
            className="p-2 text-slate-400 hover:text-rose-400 hover:bg-slate-800 rounded-lg transition-colors"
          >
            <LogOut className="h-4 w-4" />
          </button>
        </div>
      </div>
    </aside>
  );
}

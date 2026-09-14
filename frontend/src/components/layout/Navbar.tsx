'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth';
import { Bell, Shield, Sparkles, User as UserIcon, MessageCircle } from 'lucide-react';

interface NavbarProps {
  title?: string;
  subtitle?: string;
}

export function Navbar({ title, subtitle }: NavbarProps) {
  const { user, logout } = useAuth();

  return (
    <header className="h-16 border-b border-slate-800 bg-[#101827]/90 backdrop-blur-md px-6 flex items-center justify-between sticky top-0 z-20">
      <div>
        {title && <h1 className="text-lg font-bold text-[#F8FAFC] tracking-tight leading-none">{title}</h1>}
        {subtitle && <p className="text-xs text-[#94A3B8] mt-0.5">{subtitle}</p>}
      </div>

      <div className="flex items-center gap-3.5">
        {/* WhatsApp Localhost Redirect Button */}
        <Link
          href="/whatsapp"
          target="_blank"
          title="Open WhatsApp via localhost"
          className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-[#22C55E]/10 hover:bg-[#22C55E]/20 border border-[#22C55E]/30 text-[11px] font-medium text-[#22C55E] transition-colors"
        >
          <MessageCircle className="h-3.5 w-3.5 text-[#22C55E]" />
          <span className="hidden sm:inline">WhatsApp</span>
        </Link>

        {/* Real-time status indicator */}
        <div className="flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-[#22D3EE]/10 border border-[#22D3EE]/30 text-[11px] font-medium text-[#22D3EE]">
          <span className="h-2 w-2 rounded-full bg-[#22D3EE] animate-pulse"></span>
          <span>Adaptive Engine Live</span>
        </div>

        {/* User Badge */}
        {user && (
          <div className="flex items-center gap-2.5 pl-2 border-l border-slate-800">
            <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-slate-700 to-slate-800 border border-slate-700 flex items-center justify-center text-[#22D3EE] font-bold text-xs">
              {user.full_name.slice(0, 2).toUpperCase()}
            </div>
            <div className="hidden md:block text-left">
              <p className="text-xs font-semibold text-[#F8FAFC] leading-none">{user.full_name}</p>
              <span className="text-[10px] text-[#94A3B8]">{user.role}</span>
            </div>
          </div>
        )}
      </div>
    </header>
  );
}

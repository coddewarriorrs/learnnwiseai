'use client';

import React, { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { Sidebar } from '@/components/layout/Sidebar';
import { FloatingChatbot } from '@/components/chat/FloatingChatbot';

export default function StudentLayout({ children }: { children: React.ReactNode }) {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading) {
      if (!user) {
        router.push('/login');
      } else if (user.role === 'TEACHER') {
        router.push('/teacher/dashboard');
      } else if (user.role === 'ADMIN') {
        router.push('/admin/dashboard');
      }
    }
  }, [user, loading, router]);

  if (loading || !user) {
    return (
      <div className="min-h-screen bg-[#0B1220] flex items-center justify-center text-slate-400 text-sm">
        Loading student workspace...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0B1220] flex relative">
      <Sidebar />
      <main className="flex-1 flex flex-col min-w-0 overflow-y-auto">
        {children}
      </main>
      <FloatingChatbot />
    </div>
  );
}

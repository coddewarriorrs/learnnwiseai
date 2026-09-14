'use client';

import React, { useEffect, useState } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { useAuth } from '@/lib/auth';
import { apiRequest } from '@/lib/api';
import { BookOpen, CheckCircle2, AlertCircle } from 'lucide-react';

export default function JoinClassPage() {
  const { token } = useParams();
  const { user, loading: authLoading } = useAuth();
  const router = useRouter();

  const [classInfo, setClassInfo] = useState<any>(null);
  const [error, setError] = useState('');
  const [joining, setJoining] = useState(false);
  const [joined, setJoined] = useState(false);

  useEffect(() => {
    if (!token) return;

    apiRequest(`/classes/join/verify/${token}`)
      .then((res) => {
        setClassInfo(res);
      })
      .catch((err) => {
        setError(err.message || 'Invalid or expired invite link.');
      });
  }, [token]);

  useEffect(() => {
    if (!authLoading && user && user.role === 'STUDENT' && classInfo && !joined && !joining) {
      setJoining(true);
      apiRequest('/classes/join', {
        method: 'POST',
        body: JSON.stringify({ invite_token: token }),
      })
        .then(() => {
          setJoined(true);
          setTimeout(() => router.push('/student/classes'), 2000);
        })
        .catch((err) => {
          if (err.message && err.message.includes('already enrolled')) {
            setJoined(true);
            setTimeout(() => router.push('/student/classes'), 1500);
          } else {
            setError(err.message);
          }
        })
        .finally(() => setJoining(false));
    }
  }, [authLoading, user, classInfo, joined, joining, token, router]);

  const handleSaveTokenAndAuth = (route: string) => {
    localStorage.setItem('pending_join_token', token as string);
    router.push(route);
  };

  return (
    <div className="min-h-screen bg-[#0B1220] flex flex-col justify-center py-12 px-6">
      <div className="max-w-md mx-auto w-full bg-[#162235] border border-slate-800 rounded-2xl p-8 shadow-2xl text-center">
        <div className="h-12 w-12 rounded-2xl bg-teal-500/10 border border-teal-500/20 text-teal-400 flex items-center justify-center mx-auto mb-4">
          <BookOpen className="h-6 w-6" />
        </div>

        <h2 className="text-xl font-bold text-white">Class Invitation</h2>

        {error && (
          <div className="mt-4 p-3 rounded-lg bg-rose-500/15 border border-rose-500/30 text-rose-300 text-xs flex items-center gap-2">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {classInfo && (
          <div className="mt-4 p-4 rounded-xl bg-slate-900 border border-slate-800 text-left">
            <h3 className="text-sm font-bold text-white">{classInfo.class_name}</h3>
            <p className="text-xs text-slate-400 mt-0.5">Subject: {classInfo.subject} • Grade {classInfo.grade}</p>
          </div>
        )}

        {joined ? (
          <div className="mt-6 p-4 rounded-xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-300 text-xs flex items-center justify-center gap-2">
            <CheckCircle2 className="h-4 w-4" /> Enrolled successfully! Redirecting to your classes...
          </div>
        ) : user ? (
          <div className="mt-6 text-xs text-slate-400">
            {joining ? 'Enrolling you into class...' : 'Confirming membership...'}
          </div>
        ) : (
          <div className="mt-6 space-y-3">
            <p className="text-xs text-slate-400">
              Please sign in or create an account. You will automatically join <strong>{classInfo?.class_name || 'this class'}</strong> upon authentication.
            </p>
            <button
              onClick={() => handleSaveTokenAndAuth('/login')}
              className="w-full py-2.5 px-4 rounded-lg font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 hover:from-teal-400 hover:to-cyan-300 text-xs transition-all cursor-pointer"
            >
              Sign In & Join Class
            </button>
            <button
              onClick={() => handleSaveTokenAndAuth('/register')}
              className="w-full py-2.5 px-4 rounded-lg font-semibold text-slate-300 bg-slate-900 border border-slate-700 hover:bg-slate-800 text-xs transition-all cursor-pointer"
            >
              Create New Account & Join
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

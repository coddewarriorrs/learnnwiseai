'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/lib/auth';
import { apiRequest } from '@/lib/api';
import { Sparkles, ArrowRight, Lock, Mail, AlertCircle } from 'lucide-react';

export default function LoginPage() {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = await apiRequest('/auth/login', {
        method: 'POST',
        body: JSON.stringify({ email, password }),
      });

      login(data.access_token, data.refresh_token, data.user);
    } catch (err: any) {
      setError(err.message || 'Login failed. Please check credentials.');
    } finally {
      setLoading(false);
    }
  };

  const fillDemo = (demoEmail: string) => {
    setEmail(demoEmail);
    setPassword('LearnWise@2026');
  };

  return (
    <div className="min-h-screen bg-[#0B1220] flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <Link href="/" className="inline-flex items-center gap-2.5">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-teal-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-teal-500/20">
            <Sparkles className="h-5 w-5 text-slate-950 stroke-[2.5]" />
          </div>
          <span className="text-2xl font-bold tracking-tight text-white">
            LearnWise <span className="text-teal-400">AI</span>
          </span>
        </Link>
        <h2 className="mt-4 text-xl font-bold tracking-tight text-slate-200">
          Sign in to your learning account
        </h2>
      </div>

      <div className="mt-6 sm:mx-auto sm:w-full sm:max-w-md px-4 sm:px-0">
        <div className="bg-[#162235] border border-slate-800 py-8 px-6 shadow-2xl rounded-2xl sm:px-10">
          {error && (
            <div className="mb-5 p-3 rounded-lg bg-rose-500/15 border border-rose-500/30 flex items-center gap-2.5 text-rose-300 text-xs">
              <AlertCircle className="h-4 w-4 shrink-0" />
              <span>{error}</span>
            </div>
          )}

          <form className="space-y-4" onSubmit={handleSubmit}>
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
                Email Address
              </label>
              <div className="mt-1 relative rounded-lg shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
                  <Mail className="h-4 w-4" />
                </div>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="name@learnwise.ai"
                  className="block w-full pl-9 pr-3 py-2.5 bg-slate-900 border border-slate-700 rounded-lg text-sm text-white placeholder-slate-500 focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500"
                />
              </div>
            </div>

            <div>
              <div className="flex justify-between items-center">
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">
                  Password
                </label>
                <Link href="/forgot-password" className="text-xs text-teal-400 hover:underline">
                  Forgot?
                </Link>
              </div>
              <div className="mt-1 relative rounded-lg shadow-sm">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-500">
                  <Lock className="h-4 w-4" />
                </div>
                <input
                  type="password"
                  required
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••••••"
                  className="block w-full pl-9 pr-3 py-2.5 bg-slate-900 border border-slate-700 rounded-lg text-sm text-white placeholder-slate-500 focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full flex justify-center items-center gap-2 py-2.5 px-4 rounded-lg shadow-sm text-sm font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 hover:from-teal-400 hover:to-cyan-300 focus:outline-none disabled:opacity-50 transition-all cursor-pointer"
            >
              {loading ? 'Authenticating...' : 'Sign In'}
              <ArrowRight className="h-4 w-4" />
            </button>
          </form>

          {/* Quick Demo Accounts */}
          <div className="mt-6 pt-6 border-t border-slate-800">
            <p className="text-xs text-slate-400 font-semibold mb-2.5 text-center">Quick Demo Fill (Password: LearnWise@2026):</p>
            <div className="grid grid-cols-2 gap-2 text-xs">
              <button 
                type="button"
                onClick={() => fillDemo('teacher@learnwise.ai')}
                className="px-2.5 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 transition-colors text-left"
              >
                <span className="block font-bold text-teal-400">Teacher</span>
                <span className="text-[10px] text-slate-400">Dr. Vance</span>
              </button>
              <button 
                type="button"
                onClick={() => fillDemo('arjun@learnwise.ai')}
                className="px-2.5 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 transition-colors text-left"
              >
                <span className="block font-bold text-rose-400">Student (High Risk)</span>
                <span className="text-[10px] text-slate-400">Arjun (Calculus gap)</span>
              </button>
              <button 
                type="button"
                onClick={() => fillDemo('rohit@learnwise.ai')}
                className="px-2.5 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 transition-colors text-left"
              >
                <span className="block font-bold text-emerald-400">Student (Strong)</span>
                <span className="text-[10px] text-slate-400">Rohit (Top score)</span>
              </button>
              <button 
                type="button"
                onClick={() => fillDemo('admin@learnwise.ai')}
                className="px-2.5 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-700 text-slate-200 transition-colors text-left"
              >
                <span className="block font-bold text-cyan-400">Administrator</span>
                <span className="text-[10px] text-slate-400">Platform Admin</span>
              </button>
            </div>
          </div>

          <div className="mt-5 text-center text-xs text-slate-400">
            Don't have an account?{' '}
            <Link href="/register" className="font-semibold text-teal-400 hover:underline">
              Register now
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

'use client';

import React, { useState } from 'react';
import Link from 'next/link';
import { apiRequest } from '@/lib/api';
import { Sparkles, ArrowLeft, Mail } from 'lucide-react';

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState('');
  const [submitted, setSubmitted] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiRequest('/auth/forgot-password', {
        method: 'POST',
        body: JSON.stringify({ email }),
      });
    } catch {
      // safe
    }
    setSubmitted(true);
  };

  return (
    <div className="min-h-screen bg-[#0B1220] flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <Link href="/" className="inline-flex items-center gap-2.5">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-teal-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-teal-500/20">
            <Sparkles className="h-5 w-5 text-slate-950 stroke-[2.5]" />
          </div>
          <span className="text-2xl font-bold tracking-tight text-white">LearnWise <span className="text-teal-400">AI</span></span>
        </Link>
      </div>

      <div className="mt-6 sm:mx-auto sm:w-full sm:max-w-md px-4 sm:px-0">
        <div className="bg-[#162235] border border-slate-800 py-8 px-6 shadow-2xl rounded-2xl sm:px-10">
          <h2 className="text-lg font-bold text-white mb-2">Reset Password</h2>
          <p className="text-xs text-slate-400 mb-6">Enter your email address and we will send instructions to reset your password.</p>

          {submitted ? (
            <div className="p-4 rounded-lg bg-teal-500/15 border border-teal-500/30 text-xs text-teal-300">
              Password reset link has been dispatched to your email if registered. Check your inbox!
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider">Email Address</label>
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
                    className="block w-full pl-9 pr-3 py-2.5 bg-slate-900 border border-slate-700 rounded-lg text-sm text-white focus:outline-none focus:border-teal-500"
                  />
                </div>
              </div>

              <button
                type="submit"
                className="w-full py-2.5 px-4 rounded-lg font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 hover:from-teal-400 hover:to-cyan-300 transition-all text-sm"
              >
                Send Reset Link
              </button>
            </form>
          )}

          <div className="mt-6 text-center">
            <Link href="/login" className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-slate-200">
              <ArrowLeft className="h-3.5 w-3.5" /> Back to Login
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

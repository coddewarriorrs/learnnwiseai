'use client';

import React, { useEffect, useState } from 'react';
import { MessageCircle, ExternalLink, ArrowRight, Sparkles } from 'lucide-react';
import Link from 'next/link';

export default function WhatsAppRedirectPage() {
  const [phone, setPhone] = useState('');
  const [text, setText] = useState('Hello from LearnWise AI - Education that adapts to every learner!');
  const [autoRedirected, setAutoRedirected] = useState(false);

  const getWhatsAppUrl = () => {
    const cleanPhone = phone.replace(/\D/g, '');
    const encodedText = encodeURIComponent(text);
    if (cleanPhone) {
      return `https://wa.me/${cleanPhone}?text=${encodedText}`;
    }
    return `https://web.whatsapp.com/send?text=${encodedText}`;
  };

  useEffect(() => {
    // Read query params if any
    if (typeof window !== 'undefined') {
      const params = new URLSearchParams(window.location.search);
      const qPhone = params.get('phone') || '';
      const qText = params.get('text') || 'Hello from LearnWise AI - Education that adapts to every learner!';
      if (qPhone) setPhone(qPhone);
      if (qText) setText(qText);

      const target = qPhone 
        ? `https://wa.me/${qPhone.replace(/\D/g, '')}?text=${encodeURIComponent(qText)}`
        : `https://web.whatsapp.com/send?text=${encodeURIComponent(qText)}`;

      // Automatically redirect after 1.5 seconds so user can see what is happening
      const timer = setTimeout(() => {
        setAutoRedirected(true);
        window.location.href = target;
      }, 1500);

      return () => clearTimeout(timer);
    }
  }, []);

  const targetUrl = getWhatsAppUrl();

  return (
    <div className="min-h-screen bg-[#0A0F1D] flex flex-col items-center justify-center p-6 text-slate-200">
      <div className="max-w-md w-full p-8 rounded-2xl bg-[#162235] border border-slate-800 shadow-2xl space-y-6 text-center">
        {/* Brand & WhatsApp Icon */}
        <div className="flex items-center justify-center gap-3">
          <div className="h-12 w-12 rounded-2xl bg-teal-500/10 border border-teal-500/20 text-teal-400 flex items-center justify-center">
            <Sparkles className="h-6 w-6" />
          </div>
          <ArrowRight className="h-4 w-4 text-slate-500" />
          <div className="h-12 w-12 rounded-2xl bg-emerald-500/15 border border-emerald-500/30 text-emerald-400 flex items-center justify-center shadow-lg shadow-emerald-500/20">
            <MessageCircle className="h-6 w-6" />
          </div>
        </div>

        <div>
          <h1 className="text-xl font-bold text-white tracking-tight">
            Redirecting to WhatsApp
          </h1>
          <p className="text-xs text-slate-400 mt-1">
            Connecting from LearnWise AI Localhost to WhatsApp Web / App
          </p>
        </div>

        {/* Status Indicator */}
        <div className="p-3.5 rounded-xl bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-xs flex items-center justify-center gap-2">
          <span className="h-2 w-2 rounded-full bg-emerald-400 animate-ping" />
          <span>Opening WhatsApp...</span>
        </div>

        {/* Optional Custom Phone or Message */}
        <div className="space-y-3 text-left pt-2 border-t border-slate-800 text-xs">
          <div>
            <label className="block text-slate-400 font-medium mb-1">
              Recipient Phone Number (Optional, with country code):
            </label>
            <input
              type="text"
              value={phone}
              onChange={(e) => setPhone(e.target.value)}
              placeholder="e.g. 919876543210"
              className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-emerald-500"
            />
          </div>

          <div>
            <label className="block text-slate-400 font-medium mb-1">
              Message Preview:
            </label>
            <textarea
              rows={2}
              value={text}
              onChange={(e) => setText(e.target.value)}
              className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-white focus:outline-none focus:border-emerald-500 resize-none text-xs"
            />
          </div>
        </div>

        {/* Manual Redirect Action Button */}
        <a
          href={targetUrl}
          target="_blank"
          rel="noopener noreferrer"
          className="w-full py-3.5 px-6 rounded-xl font-bold text-slate-950 bg-emerald-400 hover:bg-emerald-300 transition-all flex items-center justify-center gap-2 shadow-lg shadow-emerald-500/20 text-xs cursor-pointer"
        >
          <span>Open WhatsApp Directly</span>
          <ExternalLink className="h-4 w-4" />
        </a>

        <div className="pt-2">
          <Link href="/student/dashboard" className="text-xs text-slate-400 hover:text-white transition-colors">
            ← Return to LearnWise AI Dashboard
          </Link>
        </div>
      </div>
    </div>
  );
}

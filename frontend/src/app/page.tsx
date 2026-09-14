import React from 'react';
import Link from 'next/link';
import { 
  Sparkles, ArrowRight, BrainCircuit, AlertTriangle, ShieldCheck, 
  Target, Users, Award, LineChart, ChevronRight, CheckCircle2 
} from 'lucide-react';

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#0B1220] text-slate-100 flex flex-col selection:bg-teal-500 selection:text-white">
      {/* Navigation */}
      <nav className="border-b border-slate-800/80 bg-[#0B1220]/80 backdrop-blur-md sticky top-0 z-50 px-6 py-4 flex items-center justify-between max-w-7xl mx-auto w-full">
        <div className="flex items-center gap-2.5">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-teal-500 to-cyan-400 flex items-center justify-center shadow-lg shadow-teal-500/20">
            <Sparkles className="h-5 w-5 text-slate-950 stroke-[2.5]" />
          </div>
          <span className="text-xl font-bold tracking-tight text-white">
            LearnWise <span className="text-teal-400">AI</span>
          </span>
        </div>

        <div className="flex items-center gap-4">
          <Link 
            href="/login" 
            className="text-sm font-semibold text-slate-300 hover:text-white transition-colors px-3 py-2"
          >
            Sign In
          </Link>
          <Link 
            href="/register" 
            className="text-sm font-semibold bg-gradient-to-r from-teal-500 to-cyan-500 hover:from-teal-400 hover:to-cyan-400 text-slate-950 px-4 py-2 rounded-lg shadow-md shadow-teal-500/20 transition-all font-medium"
          >
            Get Started
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="max-w-6xl mx-auto px-6 pt-20 pb-16 text-center">
        <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-teal-500/10 border border-teal-500/30 text-teal-300 text-xs font-semibold mb-8">
          <span className="h-2 w-2 rounded-full bg-teal-400 animate-pulse"></span>
          Adaptive Smart Education & Pedagogical Intelligence
        </div>
        
        <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-tight md:leading-none">
          Education that adapts to <span className="text-transparent bg-clip-text bg-gradient-to-r from-teal-400 via-cyan-300 to-teal-200">every learner.</span>
        </h1>

        <p className="mt-6 text-lg md:text-xl text-slate-400 max-w-2xl mx-auto leading-relaxed">
          LearnWise AI understands where students struggle, explains why, and helps teachers take the right action at the right time.
        </p>

        <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
          <Link 
            href="/register" 
            className="inline-flex items-center gap-2 bg-gradient-to-r from-teal-500 to-cyan-500 hover:from-teal-400 hover:to-cyan-400 text-slate-950 font-bold px-6 py-3.5 rounded-xl shadow-lg shadow-teal-500/25 transition-all text-sm"
          >
            Get Started Free
            <ArrowRight className="h-4 w-4" />
          </Link>
          <Link 
            href="/login" 
            className="inline-flex items-center gap-2 bg-slate-900 border border-slate-700 hover:border-slate-500 text-slate-200 font-semibold px-6 py-3.5 rounded-xl transition-all text-sm"
          >
            Explore Demo Accounts
          </Link>
        </div>

        {/* Dashboard Preview */}
        <div className="mt-16 rounded-2xl border border-slate-800 bg-gradient-to-b from-slate-900/90 to-[#0B1220] p-4 shadow-2xl shadow-teal-950/30 max-w-5xl mx-auto text-left">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4 px-2">
            <div className="flex items-center gap-2">
              <div className="h-3 w-3 rounded-full bg-rose-500/80"></div>
              <div className="h-3 w-3 rounded-full bg-amber-500/80"></div>
              <div className="h-3 w-3 rounded-full bg-emerald-500/80"></div>
              <span className="text-xs font-mono text-slate-400 ml-2">learnwise.ai/student/dashboard</span>
            </div>
            <span className="text-[11px] font-semibold text-teal-400 bg-teal-500/10 px-2.5 py-0.5 rounded-full border border-teal-500/20">
              Live Diagnostic
            </span>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 p-2">
            <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
              <span className="text-xs text-slate-400 font-medium">Overall Mastery</span>
              <p className="text-3xl font-bold text-white mt-1">78.4%</p>
              <span className="text-xs text-emerald-400 font-semibold mt-2 block">↑ 6.2% since diagnostic</span>
            </div>
            <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
              <span className="text-xs text-slate-400 font-medium">Root-Cause Learning Gap</span>
              <p className="text-sm font-semibold text-rose-400 mt-1.5">Indefinite Integrals (36%)</p>
              <p className="text-xs text-slate-400 mt-1">Impacting Integration by Parts</p>
            </div>
            <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800">
              <span className="text-xs text-slate-400 font-medium">Predicted Risk</span>
              <p className="text-sm font-semibold text-amber-400 mt-1.5">MEDIUM RISK (42/100)</p>
              <p className="text-xs text-slate-400 mt-1">Guided review assigned</p>
            </div>
          </div>
        </div>
      </section>

      {/* Flow Section */}
      <section className="py-20 border-y border-slate-800/80 bg-[#0F172A]/50">
        <div className="max-w-6xl mx-auto px-6 text-center">
          <span className="text-xs font-bold text-teal-400 uppercase tracking-widest">Continuous Adaptive Loop</span>
          <h2 className="text-3xl md:text-4xl font-bold text-white mt-2">From marks to meaningful action</h2>
          <p className="text-slate-400 text-sm mt-2 max-w-xl mx-auto">Conventional tests simply give a score. LearnWise AI closes the loop.</p>

          <div className="mt-12 grid grid-cols-2 md:grid-cols-6 gap-3">
            {[
              { step: '1', title: 'Student Activity', desc: 'Practice & Quizzes' },
              { step: '2', title: 'Concept Diagnosis', desc: 'DAG Graph Traversal' },
              { step: '3', title: 'Risk Detection', desc: 'Explainable Multi-factor' },
              { step: '4', title: 'Personalized Path', desc: 'Prerequisite Recovery' },
              { step: '5', title: 'Teacher Action', desc: 'Targeted Intervention' },
              { step: '6', title: 'Student Growth', desc: 'Mastery Verified' },
            ].map((s) => (
              <div key={s.step} className="p-4 rounded-xl bg-[#162235] border border-slate-800 text-center hover:border-teal-500/40 transition-colors">
                <span className="h-6 w-6 rounded-full bg-teal-500/20 text-teal-300 font-bold text-xs flex items-center justify-center mx-auto mb-2 border border-teal-500/30">
                  {s.step}
                </span>
                <h4 className="text-xs font-bold text-white mb-1">{s.title}</h4>
                <p className="text-[11px] text-slate-400">{s.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stakeholders Section */}
      <section className="py-20 max-w-6xl mx-auto px-6">
        <div className="text-center mb-14">
          <span className="text-xs font-bold text-cyan-400 uppercase tracking-widest">Ecosystem Design</span>
          <h2 className="text-3xl md:text-4xl font-bold text-white mt-2">Built for every learning stakeholder</h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          {[
            {
              role: 'Student',
              icon: Target,
              desc: 'Personalized recovery paths, Socratic AI tutoring, and clear concept mastery visualization without high-stakes intimidation.'
            },
            {
              role: 'Teacher',
              icon: Users,
              desc: 'Early warning dashboard, real-time live activity stream, class prerequisite heatmaps, and one-click interventions.'
            },
            {
              role: 'Parent',
              icon: ShieldCheck,
              desc: 'Transparent, plain-English progress summaries showing strengths and areas needing support while preserving student privacy.'
            },
            {
              role: 'Institution',
              icon: Award,
              desc: 'Curriculum versioning, official syllabus alignment, and aggregate academic risk mitigation across departments.'
            },
          ].map((card) => {
            const Icon = card.icon;
            return (
              <div key={card.role} className="p-6 rounded-2xl bg-[#162235] border border-slate-800 hover:border-slate-700 transition-all flex flex-col justify-between">
                <div>
                  <div className="h-10 w-10 rounded-xl bg-teal-500/10 border border-teal-500/20 flex items-center justify-center text-teal-400 mb-4">
                    <Icon className="h-5 w-5" />
                  </div>
                  <h3 className="text-lg font-bold text-white">{card.role}</h3>
                  <p className="text-xs text-slate-400 mt-2 leading-relaxed">{card.desc}</p>
                </div>
              </div>
            );
          })}
        </div>
      </section>

      {/* Illustrative Growth Chart Section */}
      <section className="py-16 border-t border-slate-800 bg-[#0F172A]/40">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <span className="text-[10px] font-bold uppercase tracking-wider text-amber-400 bg-amber-500/10 border border-amber-500/20 px-2.5 py-1 rounded-full">
            Illustrative Model Validation
          </span>
          <h2 className="text-2xl md:text-3xl font-bold text-white mt-3">See learning differently</h2>
          <p className="text-xs text-slate-400 mt-1 max-w-lg mx-auto">
            Tracking prerequisite mastery closure vs. conventional rote re-testing across 8 weeks.
          </p>

          <div className="mt-8 p-6 rounded-xl bg-slate-900 border border-slate-800 text-left">
            <div className="flex justify-between items-center text-xs text-slate-400 mb-4">
              <span>Week 1 (Diagnostic): 32%</span>
              <span className="text-teal-400 font-semibold">Week 4 (Recovery Mode): 68%</span>
              <span className="text-emerald-400 font-bold">Week 8 (Mastery): 89%</span>
            </div>
            <div className="w-full bg-slate-800 h-3 rounded-full overflow-hidden">
              <div className="bg-gradient-to-r from-rose-500 via-amber-400 to-teal-400 h-full rounded-full transition-all duration-1000" style={{ width: '89%' }}></div>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-slate-800/80 py-8 px-6 mt-auto text-center text-xs text-slate-500">
        <p>© 2026 LearnWise AI. Education that adapts to every learner.</p>
        <p className="mt-1 text-[11px] text-slate-600">Built with Next.js, FastAPI, PostgreSQL, and Pedagogical AI Intelligence.</p>
      </footer>
    </div>
  );
}

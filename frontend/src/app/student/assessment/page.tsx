'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { 
  FileCheck, Clock, CheckCircle2, ArrowRight, RotateCcw, AlertTriangle 
} from 'lucide-react';
import Link from 'next/link';

export default function StudentAssessmentPage() {
  const [assessments, setAssessments] = useState<any[]>([]);
  const [activeAssessment, setActiveAssessment] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, string>>({});
  const [submitting, setSubmitting] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [timeSpent, setTimeSpent] = useState(0);

  useEffect(() => {
    apiRequest('/assessments')
      .then((res) => setAssessments(res))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const handleStart = async (aId: number) => {
    setLoading(true);
    try {
      const detail = await apiRequest(`/assessments/${aId}`);
      setActiveAssessment(detail);
      setCurrentIndex(0);
      setSelectedAnswers({});
      setResult(null);
      setTimeSpent(0);
    } catch {
      alert('Failed to load assessment');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    let interval: any;
    if (activeAssessment && !result) {
      interval = setInterval(() => setTimeSpent((t) => t + 1), 1000);
    }
    return () => clearInterval(interval);
  }, [activeAssessment, result]);

  const handleSubmit = async () => {
    if (!activeAssessment) return;
    setSubmitting(true);

    const answersPayload = activeAssessment.questions.map((q: any) => ({
      question_id: q.id,
      selected_answer: selectedAnswers[q.id] || '',
      time_taken_seconds: Math.round(timeSpent / activeAssessment.questions.length),
    }));

    try {
      const res = await apiRequest(`/assessments/${activeAssessment.id}/submit`, {
        method: 'POST',
        body: JSON.stringify({
          answers: answersPayload,
          time_taken_seconds: timeSpent,
        }),
      });
      setResult(res);
    } catch (err: any) {
      alert(err.message || 'Error submitting assessment');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="flex-1 pb-16">
      <Navbar title="Curriculum Assessments" subtitle="Formal evaluative tests with instant mastery update" />

      <div className="p-6 max-w-4xl mx-auto space-y-6">
        {!activeAssessment ? (
          /* List of Available Assessments */
          <div className="space-y-4">
            <h2 className="text-base font-bold text-white">Available Assessments</h2>
            {loading ? (
              <div className="p-12 text-center text-slate-400 text-sm">Loading assessments...</div>
            ) : assessments.length === 0 ? (
              <div className="p-12 rounded-2xl bg-[#162235] border border-slate-800 text-center text-slate-400 text-sm">
                No assessments scheduled currently.
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {assessments.map((a) => (
                  <div key={a.id} className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-3 flex flex-col justify-between">
                    <div>
                      <div className="flex justify-between items-center mb-2">
                        <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-slate-800 text-teal-300 border border-slate-700">
                          {a.duration_minutes} Mins
                        </span>
                        <span className="text-xs text-slate-400">{a.question_count || 3} Questions</span>
                      </div>
                      <h3 className="text-base font-bold text-white mb-1">{a.title}</h3>
                      <p className="text-xs text-slate-400">{a.description || 'Topic diagnostic evaluation'}</p>
                    </div>

                    <button
                      onClick={() => handleStart(a.id)}
                      className="w-full mt-4 py-2.5 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 hover:from-teal-400 hover:to-cyan-300 text-xs flex items-center justify-center gap-2 cursor-pointer"
                    >
                      Start Assessment <ArrowRight className="h-3.5 w-3.5" />
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>
        ) : result ? (
          /* Result Card */
          <div className="p-8 rounded-2xl bg-[#162235] border border-slate-800 text-center shadow-2xl space-y-6">
            <div className="h-16 w-16 rounded-2xl bg-teal-500/10 border border-teal-500/20 text-teal-400 flex items-center justify-center mx-auto">
              <CheckCircle2 className="h-8 w-8" />
            </div>

            <div>
              <h2 className="text-2xl font-bold text-white">Assessment Submitted</h2>
              <p className="text-xs text-slate-400 mt-1">{result.feedback}</p>
            </div>

            <div className="grid grid-cols-3 gap-3 max-w-md mx-auto text-center">
              <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                <span className="text-xs text-slate-400 block">Score</span>
                <span className="text-xl font-bold text-white">{result.score} / {result.max_score}</span>
              </div>
              <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                <span className="text-xs text-slate-400 block">Percentage</span>
                <span className="text-xl font-bold text-teal-400">{result.percentage}%</span>
              </div>
              <div className="p-4 rounded-xl bg-slate-900 border border-slate-800">
                <span className="text-xs text-slate-400 block">Status</span>
                <span className="text-xs font-bold text-emerald-400 block mt-1">{result.status}</span>
              </div>
            </div>

            <div className="flex justify-center gap-3 pt-4">
              <button
                onClick={() => setActiveAssessment(null)}
                className="py-2.5 px-5 rounded-xl bg-slate-900 border border-slate-700 hover:bg-slate-800 text-slate-200 text-xs font-semibold"
              >
                Back to Assessments
              </button>
              <Link
                href="/student/dashboard"
                className="py-2.5 px-5 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 text-xs"
              >
                View Updated Dashboard
              </Link>
            </div>
          </div>
        ) : (
          /* Active Exam Taker */
          <div className="space-y-6">
            <div className="flex items-center justify-between p-4 rounded-xl bg-[#162235] border border-slate-800">
              <span className="font-bold text-teal-400 text-xs">
                Question {currentIndex + 1} of {activeAssessment.questions?.length}
              </span>
              <div className="flex items-center gap-2 text-xs text-slate-400">
                <Clock className="h-3.5 w-3.5" />
                <span className="font-mono">{timeSpent}s</span>
              </div>
            </div>

            {activeAssessment.questions && activeAssessment.questions[currentIndex] && (
              <div className="p-6 rounded-2xl bg-[#162235] border border-slate-800 space-y-4">
                <h3 className="text-sm font-semibold text-white">
                  {activeAssessment.questions[currentIndex].prompt}
                </h3>

                <div className="space-y-2.5">
                  {activeAssessment.questions[currentIndex].options.map((opt: any) => {
                    const qId = activeAssessment.questions[currentIndex].id;
                    const isSelected = selectedAnswers[qId] === opt.id;

                    return (
                      <button
                        key={opt.id}
                        onClick={() => setSelectedAnswers((prev) => ({ ...prev, [qId]: opt.id }))}
                        className={`w-full text-left p-3.5 rounded-xl border text-xs sm:text-sm flex items-center gap-3 transition-all ${
                          isSelected
                            ? 'bg-teal-500/15 border-teal-500 text-white'
                            : 'bg-slate-900 border-slate-800 hover:border-slate-700 text-slate-300'
                        }`}
                      >
                        <span className="h-6 w-6 rounded bg-slate-800 border border-slate-700 flex items-center justify-center font-bold text-xs">
                          {opt.id}
                        </span>
                        <span>{opt.text}</span>
                      </button>
                    );
                  })}
                </div>

                <div className="flex justify-between items-center pt-4 border-t border-slate-800">
                  <button
                    disabled={currentIndex === 0}
                    onClick={() => setCurrentIndex((i) => i - 1)}
                    className="py-2 px-4 rounded-xl border border-slate-700 text-slate-400 hover:text-white text-xs disabled:opacity-30"
                  >
                    Previous
                  </button>

                  {currentIndex + 1 < activeAssessment.questions.length ? (
                    <button
                      onClick={() => setCurrentIndex((i) => i + 1)}
                      className="py-2 px-4 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 text-xs"
                    >
                      Next Question
                    </button>
                  ) : (
                    <button
                      disabled={submitting}
                      onClick={handleSubmit}
                      className="py-2 px-5 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 text-xs shadow-md shadow-teal-500/20"
                    >
                      {submitting ? 'Submitting...' : 'Submit Assessment'}
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

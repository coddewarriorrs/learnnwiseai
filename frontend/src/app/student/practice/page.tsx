'use client';

import React, { useState, useEffect, useMemo } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { 
  Target, Clock, AlertTriangle, CheckCircle2, XCircle, ArrowRight, 
  RotateCcw, Sparkles, BookOpen, HelpCircle, Layers, GraduationCap,
  Atom, Dna, FlaskConical, Calculator, ShieldAlert, Lightbulb, Check,
  Flame, BrainCircuit
} from 'lucide-react';

interface TopicItem {
  id: number;
  title: string;
  code: string;
  prerequisites: string[];
  chapter_id: number | null;
  chapter_title: string | null;
  subject_id: number | null;
  subject_title: string | null;
  grade: string | null;
}

interface ClassItem {
  id: number;
  name: string;
  class_code: string;
  subject: string;
  grade: string;
}

const SUBJECTS = [
  { id: 'ALL', label: 'All Subjects', icon: Layers, color: 'text-[#94A3B8]' },
  { id: 'Mathematics', label: 'Mathematics', icon: Calculator, color: 'text-[#22D3EE]' },
  { id: 'Physics', label: 'Physics', icon: Atom, color: 'text-[#F59E0B]' },
  { id: 'Chemistry', label: 'Chemistry', icon: FlaskConical, color: 'text-[#22C55E]' },
  { id: 'Biology', label: 'Biology', icon: Dna, color: 'text-[#F43F5E]' },
];

function cleanDisplay(text?: string | null): string {
  if (!text) return '';
  return text.replace(/[*#]/g, '').trim();
}

export default function PracticePage() {
  const [topics, setTopics] = useState<TopicItem[]>([]);
  const [classes, setClasses] = useState<ClassItem[]>([]);
  const [selectedSubject, setSelectedSubject] = useState<string>('ALL');
  const [selectedClassId, setSelectedClassId] = useState<number | null>(null);
  const [selectedChapter, setSelectedChapter] = useState<string>('ALL');
  const [selectedTopicId, setSelectedTopicId] = useState<number | null>(null);
  const [activeTopicName, setActiveTopicName] = useState<string>('');
  const [difficulty, setDifficulty] = useState<'ANY' | 'EASY' | 'MEDIUM' | 'HARD'>('ANY');
  const [numQuestions, setNumQuestions] = useState<number>(5);

  // Practice session state
  const [questions, setQuestions] = useState<any[]>([]);
  const [completedQuestionIds, setCompletedQuestionIds] = useState<number[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<string>('');
  const [sessionStarted, setSessionStarted] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [answerResult, setAnswerResult] = useState<any>(null);
  const [explanationMode, setExplanationMode] = useState<'brief' | 'full'>('brief');
  const [timeSpent, setTimeSpent] = useState(0);
  const [score, setScore] = useState(0);
  const [sessionFinished, setSessionFinished] = useState(false);
  const [loading, setLoading] = useState(false);

  // Load syllabus topics & enrolled classes on mount
  useEffect(() => {
    Promise.all([
      apiRequest('/syllabus/topics').catch(() => []),
      apiRequest('/classes').catch(() => [])
    ]).then(([topicsData, classesData]) => {
      if (Array.isArray(topicsData)) {
        setTopics(topicsData);
      }
      if (Array.isArray(classesData)) {
        setClasses(classesData);
      }
    });
  }, []);

  // Filtered chapters based on chosen subject/class
  const availableChapters = useMemo(() => {
    let filtered = topics;
    if (selectedSubject !== 'ALL') {
      filtered = filtered.filter((t) => t.subject_title?.toLowerCase() === selectedSubject.toLowerCase());
    }
    const chaptersMap = new Map<string, string>();
    filtered.forEach((t) => {
      if (t.chapter_title) {
        chaptersMap.set(t.chapter_title, t.chapter_title);
      }
    });
    return Array.from(chaptersMap.values());
  }, [topics, selectedSubject]);

  // Filtered topics based on chosen subject, class, and chapter
  const filteredTopics = useMemo(() => {
    let filtered = topics;
    if (selectedSubject !== 'ALL') {
      filtered = filtered.filter((t) => t.subject_title?.toLowerCase() === selectedSubject.toLowerCase());
    }
    if (selectedChapter !== 'ALL') {
      filtered = filtered.filter((t) => t.chapter_title === selectedChapter);
    }
    return filtered;
  }, [topics, selectedSubject, selectedChapter]);

  // Sync subject when a specific class is selected
  const handleClassChange = (classId: number | null) => {
    setSelectedClassId(classId);
    if (classId) {
      const cls = classes.find((c) => c.id === classId);
      if (cls && cls.subject) {
        const matchedSubj = SUBJECTS.find((s) => s.id.toLowerCase() === cls.subject.toLowerCase());
        if (matchedSubj) {
          setSelectedSubject(matchedSubj.id);
        }
      }
    }
    setSelectedChapter('ALL');
    setSelectedTopicId(null);
    setActiveTopicName('');
  };

  // Timer
  useEffect(() => {
    let interval: any;
    if (sessionStarted && !answerResult && !sessionFinished) {
      interval = setInterval(() => {
        setTimeSpent((t) => t + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [sessionStarted, answerResult, sessionFinished]);

  const handleStartPractice = async (continueWithExclusions = false, lockTopicId?: number) => {
    setLoading(true);
    try {
      const effectiveTopicId = lockTopicId !== undefined ? lockTopicId : selectedTopicId;
      const payload: any = {
        num_questions: numQuestions,
        difficulty: difficulty === 'ANY' ? undefined : difficulty,
      };

      if (effectiveTopicId) {
        payload.topic_id = effectiveTopicId;
        const found = topics.find(t => t.id === effectiveTopicId);
        if (found) {
          setActiveTopicName(found.title);
          setSelectedTopicId(effectiveTopicId);
        }
      } else if (selectedChapter !== 'ALL') {
        const topicInChap = filteredTopics.find((t) => t.chapter_title === selectedChapter);
        if (topicInChap && topicInChap.chapter_id) {
          payload.chapter_id = topicInChap.chapter_id;
          setActiveTopicName(selectedChapter);
        }
      } else if (selectedClassId) {
        payload.class_id = selectedClassId;
      } else if (selectedSubject !== 'ALL') {
        payload.subject = selectedSubject;
      }

      if (continueWithExclusions && completedQuestionIds.length > 0) {
        payload.exclude_ids = completedQuestionIds;
      }

      const qs = await apiRequest('/practice/start', {
        method: 'POST',
        body: JSON.stringify(payload),
      });

      if (!qs || qs.length === 0) {
        alert('No questions found for this topic/difficulty. Retrying with all difficulty levels...');
        setLoading(false);
        return;
      }

      setQuestions(qs);
      if (qs[0]?.topic_name) {
        setActiveTopicName(qs[0].topic_name);
        if (qs[0].topic_id && !selectedTopicId) {
          setSelectedTopicId(qs[0].topic_id);
        }
      }
      setCurrentIndex(0);
      setSessionStarted(true);
      setSessionFinished(false);
      setSelectedOption('');
      setAnswerResult(null);
      setTimeSpent(0);
      setScore(0);
    } catch (err: any) {
      alert(err.message || 'Failed to start practice session');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmitAnswer = async () => {
    if (!selectedOption) return;
    setSubmitting(true);

    try {
      const q = questions[currentIndex];
      const res = await apiRequest('/practice/submit-answer', {
        method: 'POST',
        body: JSON.stringify({
          question_id: q.id,
          selected_answer: selectedOption,
          time_taken_seconds: timeSpent,
        }),
      });

      setAnswerResult(res);
      setCompletedQuestionIds((prev) => Array.from(new Set([...prev, q.id])));
      if (res.is_correct) {
        setScore((s) => s + 1);
      }
    } catch (err: any) {
      alert(err.message || 'Error submitting answer');
    } finally {
      setSubmitting(false);
    }
  };

  const handleNextQuestion = () => {
    if (currentIndex + 1 < questions.length) {
      setCurrentIndex((i) => i + 1);
      setSelectedOption('');
      setAnswerResult(null);
      setTimeSpent(0);
    } else {
      setSessionFinished(true);
    }
  };

  const currentQ = questions[currentIndex];

  // Broadcast current practice question context for the AI Tutor
  useEffect(() => {
    if (sessionStarted && currentQ && !sessionFinished) {
      const ctx = {
        question_id: currentQ.id,
        prompt: currentQ.prompt,
        options: currentQ.options,
        subject_name: currentQ.subject_name,
        chapter_name: currentQ.chapter_name,
        topic_name: currentQ.topic_name,
        selected_option: selectedOption,
        is_answered: Boolean(answerResult),
        is_correct: answerResult?.is_correct,
        explanation: answerResult?.explanation_brief || answerResult?.explanation
      };
      try {
        sessionStorage.setItem('learnwise_practice_context', JSON.stringify(ctx));
      } catch {}
      if (typeof window !== 'undefined') {
        window.dispatchEvent(new CustomEvent('learnwise:practice-context', { detail: ctx }));
      }
    }
  }, [sessionStarted, currentQ, selectedOption, answerResult, sessionFinished]);

  const handleAskAITutor = () => {
    if (!currentQ) return;
    const ctx = {
      question_id: currentQ.id,
      prompt: currentQ.prompt,
      options: currentQ.options,
      subject_name: currentQ.subject_name,
      chapter_name: currentQ.chapter_name,
      topic_name: currentQ.topic_name,
      selected_option: selectedOption,
      is_answered: Boolean(answerResult),
      is_correct: answerResult?.is_correct,
      explanation: answerResult?.explanation_brief || answerResult?.explanation
    };
    try {
      sessionStorage.setItem('learnwise_practice_context', JSON.stringify(ctx));
    } catch {}
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('learnwise:open-tutor-question', { detail: ctx }));
    }
  };

  return (
    <div className="flex-1 pb-16 bg-[#0B1220] min-h-screen text-[#F8FAFC]">
      <Navbar 
        title="Adaptive Practice Engine" 
        subtitle="Syllabus-locked telemetry with root-cause prerequisite gap diagnosis" 
      />

      <div className="p-6 max-w-4xl mx-auto space-y-6">
        {!sessionStarted ? (
          /* Session Configuration Card */
          <div className="p-8 rounded-2xl bg-[#162235] border border-slate-800 shadow-2xl space-y-6">
            <div className="flex items-center justify-between pb-4 border-b border-slate-800">
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-xl bg-[#22D3EE]/10 border border-[#22D3EE]/20 text-[#22D3EE] flex items-center justify-center">
                  <Target className="h-5 w-5" />
                </div>
                <div>
                  <h2 className="text-lg font-bold text-[#F8FAFC]">Configure Practice Session</h2>
                  <p className="text-xs text-[#94A3B8]">Personalized adaptive questions locked to your chosen topic & syllabus</p>
                </div>
              </div>

              {completedQuestionIds.length > 0 && (
                <div className="px-3 py-1 rounded-full bg-[#101827] border border-slate-800 text-[11px] text-[#22D3EE] font-medium">
                  {completedQuestionIds.length} questions attempted today
                </div>
              )}
            </div>

            {/* 1. Subject Filter Tabs */}
            <div className="space-y-2">
              <label className="block text-xs font-semibold text-[#94A3B8] uppercase tracking-wider">
                Select Subject / Domain
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-5 gap-2">
                {SUBJECTS.map((s) => {
                  const Icon = s.icon;
                  const isSelected = selectedSubject === s.id;
                  return (
                    <button
                      key={s.id}
                      type="button"
                      onClick={() => {
                        setSelectedSubject(s.id);
                        setSelectedChapter('ALL');
                        setSelectedTopicId(null);
                        setActiveTopicName('');
                      }}
                      className={`p-3 rounded-xl border text-xs font-semibold flex flex-col items-center gap-1.5 transition-all cursor-pointer ${
                        isSelected 
                          ? 'bg-[#22D3EE]/20 border-[#22D3EE] text-[#22D3EE] shadow-lg shadow-[#22D3EE]/10' 
                          : 'bg-[#101827] border-slate-800 text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-[#1C2B42] hover:border-slate-700'
                      }`}
                    >
                      <Icon className={`h-4 w-4 ${isSelected ? 'text-[#22D3EE]' : s.color}`} />
                      <span>{s.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* 2. Enrolled Class Filter */}
            {classes.length > 0 && (
              <div className="space-y-2">
                <label className="block text-xs font-semibold text-[#94A3B8] uppercase tracking-wider flex items-center gap-1.5">
                  <GraduationCap className="h-3.5 w-3.5 text-[#22D3EE]" />
                  Filter by Enrolled Class Cohort (Optional)
                </label>
                <select
                  value={selectedClassId || ''}
                  onChange={(e) => handleClassChange(e.target.value ? Number(e.target.value) : null)}
                  className="w-full p-3 bg-[#101827] border border-slate-800 rounded-xl text-xs text-[#F8FAFC] focus:outline-none focus:border-[#22D3EE]"
                >
                  <option value="">All My Classes / Open Subject Practice</option>
                  {classes.map((c) => (
                    <option key={c.id} value={c.id}>
                      {c.name} ({c.class_code} • {c.subject})
                    </option>
                  ))}
                </select>
              </div>
            )}

            {/* 3. Cascading Chapter & Topic Dropdowns */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="block text-xs font-semibold text-[#94A3B8] uppercase tracking-wider">
                  Chapter / Unit
                </label>
                <select
                  value={selectedChapter}
                  onChange={(e) => {
                    setSelectedChapter(e.target.value);
                    setSelectedTopicId(null);
                    setActiveTopicName('');
                  }}
                  className="w-full p-3 bg-[#101827] border border-slate-800 rounded-xl text-xs text-[#F8FAFC] focus:outline-none focus:border-[#22D3EE]"
                >
                  <option value="ALL">All Chapters in {selectedSubject === 'ALL' ? 'Curriculum' : selectedSubject}</option>
                  {availableChapters.map((chap) => (
                    <option key={chap} value={chap}>{chap}</option>
                  ))}
                </select>
              </div>

              <div className="space-y-2">
                <label className="block text-xs font-semibold text-[#94A3B8] uppercase tracking-wider">
                  Specific Concept Topic (Locks Repeated Practice)
                </label>
                <select
                  value={selectedTopicId || ''}
                  onChange={(e) => {
                    const tid = e.target.value ? Number(e.target.value) : null;
                    setSelectedTopicId(tid);
                    if (tid) {
                      const tObj = topics.find(t => t.id === tid);
                      if (tObj) setActiveTopicName(tObj.title);
                    } else {
                      setActiveTopicName('');
                    }
                  }}
                  className="w-full p-3 bg-[#101827] border border-slate-800 rounded-xl text-xs text-[#F8FAFC] focus:outline-none focus:border-[#22D3EE]"
                >
                  <option value="">All Topics in Selected Scope</option>
                  {filteredTopics.map((t) => (
                    <option key={t.id} value={t.id}>
                      {t.title} ({t.code})
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* 4. Target Difficulty */}
            <div className="space-y-2">
              <label className="block text-xs font-semibold text-[#94A3B8] uppercase tracking-wider">
                Target Difficulty Level
              </label>
              <div className="grid grid-cols-4 gap-2.5">
                {[
                  { id: 'ANY', label: 'Adaptive (All)' },
                  { id: 'EASY', label: 'Easy' },
                  { id: 'MEDIUM', label: 'Medium' },
                  { id: 'HARD', label: 'Hard' },
                ].map((lvl) => (
                  <button
                    key={lvl.id}
                    type="button"
                    onClick={() => setDifficulty(lvl.id as any)}
                    className={`py-2.5 px-3 rounded-xl border text-xs font-bold transition-all cursor-pointer ${
                      difficulty === lvl.id
                        ? 'bg-[#22D3EE]/20 border-[#22D3EE] text-[#22D3EE] shadow-md shadow-[#22D3EE]/10'
                        : 'bg-[#101827] border-slate-800 text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-[#1C2B42]'
                    }`}
                  >
                    {lvl.label}
                  </button>
                ))}
              </div>
            </div>

            {/* 5. Number of Questions */}
            <div className="flex items-center justify-between pt-2">
              <span className="text-xs text-[#94A3B8]">Number of questions per round:</span>
              <div className="flex gap-2">
                {[5, 10, 20, 40].map((num) => (
                  <button
                    key={num}
                    type="button"
                    onClick={() => setNumQuestions(num)}
                    className={`px-3.5 py-1.5 rounded-lg text-xs font-semibold border cursor-pointer transition-all ${
                      numQuestions === num
                        ? 'bg-[#22D3EE] text-slate-950 border-[#22D3EE] font-bold shadow-md shadow-[#22D3EE]/20'
                        : 'bg-[#101827] text-[#94A3B8] border-slate-800 hover:text-[#F8FAFC] hover:bg-[#1C2B42]'
                    }`}
                  >
                    {num} Qs
                  </button>
                ))}
              </div>
            </div>

            <button
              onClick={() => handleStartPractice(false)}
              disabled={loading}
              className="w-full mt-2 py-3.5 px-6 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-[#22D3EE] to-[#8B5CF6] hover:opacity-95 transition-all flex items-center justify-center gap-2 shadow-lg shadow-[#22D3EE]/20 text-sm cursor-pointer disabled:opacity-50"
            >
              {loading ? (
                <span>Generating Adaptive Questions...</span>
              ) : (
                <>
                  <span>Launch Practice Session</span>
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </button>
          </div>
        ) : sessionFinished ? (
          /* Finished Screen */
          <div className="p-8 rounded-2xl bg-[#162235] border border-slate-800 text-center shadow-2xl space-y-6">
            <div className="h-16 w-16 rounded-2xl bg-[#22C55E]/10 border border-[#22C55E]/20 text-[#22C55E] flex items-center justify-center mx-auto">
              <CheckCircle2 className="h-8 w-8" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-[#F8FAFC]">Practice Round Complete!</h2>
              <p className="text-xs text-[#94A3B8] mt-1">
                Completed practice on <span className="text-[#22D3EE] font-bold">{activeTopicName || 'Selected Topic'}</span>. Your mastery and learning telemetry have updated.
              </p>
            </div>

            <div className="grid grid-cols-2 gap-4 max-w-sm mx-auto">
              <div className="p-4 rounded-xl bg-[#101827] border border-slate-800">
                <span className="text-xs text-[#94A3B8] block">Score</span>
                <span className="text-2xl font-bold text-[#F8FAFC]">{score} / {questions.length}</span>
              </div>
              <div className="p-4 rounded-xl bg-[#101827] border border-slate-800">
                <span className="text-xs text-[#94A3B8] block">Accuracy</span>
                <span className="text-2xl font-bold text-[#22C55E]">
                  {questions.length > 0 ? Math.round((score / questions.length) * 100) : 0}%
                </span>
              </div>
            </div>

            <div className="flex flex-col sm:flex-row justify-center gap-3 pt-4">
              {selectedTopicId && (
                <button
                  onClick={() => handleStartPractice(false, selectedTopicId)}
                  className="py-3 px-6 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-[#22D3EE] to-[#8B5CF6] hover:opacity-95 text-xs flex items-center justify-center gap-2 shadow-lg shadow-[#22D3EE]/20 cursor-pointer"
                >
                  <Sparkles className="h-4 w-4" /> Practice More: {activeTopicName || 'Same Topic'}
                </button>
              )}
              <button
                onClick={() => handleStartPractice(true)}
                className="py-3 px-5 rounded-xl font-bold text-[#F8FAFC] bg-[#1C2B42] hover:bg-[#223652] border border-slate-700 text-xs flex items-center justify-center gap-2 cursor-pointer"
              >
                <Sparkles className="h-4 w-4 text-[#22D3EE]" /> Practice Next Set (New Questions)
              </button>
              <button
                onClick={() => {
                  setSessionStarted(false);
                  setSessionFinished(false);
                }}
                className="py-3 px-5 rounded-xl bg-[#101827] border border-slate-800 hover:bg-[#1C2B42] text-[#94A3B8] hover:text-[#F8FAFC] text-xs font-semibold flex items-center justify-center gap-2 cursor-pointer"
              >
                <RotateCcw className="h-3.5 w-3.5" /> Change Subject / Topic
              </button>
            </div>
          </div>
        ) : currentQ ? (
          /* Active Question Card */
          <div className="space-y-5">
            {/* Header Telemetry */}
            <div className="flex flex-wrap items-center justify-between p-4 rounded-xl bg-[#162235] border border-slate-800 gap-3">
              <div className="flex items-center gap-2 text-xs text-[#94A3B8]">
                <span className="font-bold text-[#22D3EE]">Question {currentIndex + 1}</span> of {questions.length}
                <span className="text-slate-600">•</span>
                <span className="text-[#F8FAFC] font-semibold">{cleanDisplay(currentQ.subject_name || 'General')}</span>
                {currentQ.chapter_name && (
                  <>
                    <span className="text-slate-600">/</span>
                    <span className="text-[#94A3B8]">{cleanDisplay(currentQ.chapter_name)}</span>
                  </>
                )}
                <span className="text-slate-600">/</span>
                <span className="text-[#22D3EE] font-medium">{cleanDisplay(currentQ.topic_name)}</span>
              </div>

              <div className="flex items-center gap-3 text-xs">
                <span className={`px-2.5 py-0.5 rounded text-[11px] font-bold border ${
                  currentQ.difficulty === 'HARD'
                    ? 'bg-[#F43F5E]/10 text-[#F43F5E] border-[#F43F5E]/30'
                    : currentQ.difficulty === 'MEDIUM'
                    ? 'bg-[#F59E0B]/10 text-[#F59E0B] border-[#F59E0B]/30'
                    : 'bg-[#22C55E]/10 text-[#22C55E] border-[#22C55E]/30'
                }`}>
                  {currentQ.difficulty}
                </span>

                <div className="flex items-center gap-1.5 text-[#94A3B8] bg-[#101827] px-2.5 py-1 rounded-lg border border-slate-800">
                  <Clock className="h-3.5 w-3.5 text-[#22D3EE]" />
                  <span className="font-mono text-[#F8FAFC]">{timeSpent}s</span>
                </div>
              </div>
            </div>

            {/* Question Card */}
            <div className="p-6 sm:p-8 rounded-2xl bg-[#162235] border border-slate-800 shadow-xl space-y-6">
              <div className="space-y-1">
                <span className="text-[11px] font-mono text-[#22D3EE] uppercase tracking-widest block">
                  {cleanDisplay(currentQ.title)}
                </span>
                <h3 className="text-base sm:text-lg font-medium text-[#F8FAFC] leading-relaxed">
                  {cleanDisplay(currentQ.prompt)}
                </h3>
              </div>

              {/* Options */}
              <div className="space-y-3">
                {currentQ.options.map((opt: any) => {
                  const isSelected = selectedOption === opt.id;
                  let borderClass = 'border-slate-800 hover:border-slate-700 bg-[#101827] text-[#F8FAFC] hover:bg-[#1C2B42]';

                  if (answerResult) {
                    if (opt.id === answerResult.correct_answer) {
                      borderClass = 'border-[#22C55E] bg-[#22C55E]/15 text-[#22C55E] shadow-sm shadow-[#22C55E]/20';
                    } else if (isSelected && !answerResult.is_correct) {
                      borderClass = 'border-[#F43F5E] bg-[#F43F5E]/15 text-[#F43F5E]';
                    }
                  } else if (isSelected) {
                    borderClass = 'border-[#22D3EE] bg-[#22D3EE]/20 text-white shadow-sm shadow-[#22D3EE]/20';
                  }

                  return (
                    <button
                      key={opt.id}
                      type="button"
                      disabled={Boolean(answerResult)}
                      onClick={() => setSelectedOption(opt.id)}
                      className={`w-full p-4 rounded-xl border text-left text-sm font-medium transition-all flex items-start gap-3.5 cursor-pointer disabled:cursor-default ${borderClass}`}
                    >
                      <span className={`h-6 w-6 rounded-lg text-xs font-bold flex items-center justify-center shrink-0 mt-0.5 ${
                        isSelected 
                          ? 'bg-[#22D3EE] text-slate-950 font-bold' 
                          : 'bg-[#1C2B42] text-[#94A3B8] border border-slate-700'
                      }`}>
                        {opt.id}
                      </span>
                      <span className="leading-normal">{cleanDisplay(opt.text)}</span>
                    </button>
                  );
                })}
              </div>

              {/* Action Buttons */}
              <div className="flex flex-wrap items-center justify-between gap-3 pt-2">
                <div className="flex items-center gap-2">
                  {!answerResult ? (
                    <button
                      onClick={handleSubmitAnswer}
                      disabled={!selectedOption || submitting}
                      className="py-3 px-6 rounded-xl font-bold text-slate-950 bg-[#22D3EE] hover:bg-[#22D3EE]/90 disabled:opacity-40 transition-all text-xs flex items-center gap-2 cursor-pointer disabled:cursor-not-allowed shadow-md shadow-[#22D3EE]/15"
                    >
                      {submitting ? 'Evaluating...' : 'Submit Answer'}
                    </button>
                  ) : (
                    <button
                      onClick={handleNextQuestion}
                      className="py-3 px-6 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-[#22D3EE] to-[#8B5CF6] hover:opacity-95 transition-all text-xs flex items-center gap-2 shadow-lg shadow-[#22D3EE]/20 cursor-pointer"
                    >
                      <span>{currentIndex + 1 < questions.length ? 'Next Question (Same Topic)' : 'View Session Summary'}</span>
                      <ArrowRight className="h-4 w-4" />
                    </button>
                  )}
                </div>

                <button
                  type="button"
                  onClick={handleAskAITutor}
                  className="py-2.5 px-4 rounded-xl border border-[#22D3EE]/40 bg-[#101827] hover:bg-[#1C2B42] text-[#22D3EE] font-semibold text-xs flex items-center gap-2 transition-all cursor-pointer shadow-md"
                  title="Ask AI Tutor for a conceptual hint, formula, or mistake diagnostic"
                >
                  <Sparkles className="h-4 w-4 text-[#22D3EE]" />
                  <span>Ask AI Tutor</span>
                </button>
              </div>

              {/* Feedback / Clean Educational Explanation Box (Zero Asterisks) */}
              {answerResult && (
                <div className={`p-5 rounded-2xl border text-xs space-y-4 shadow-xl ${
                  answerResult.is_correct 
                    ? 'bg-[#22C55E]/10 border-[#22C55E]/30' 
                    : 'bg-[#F43F5E]/10 border-[#F43F5E]/30'
                }`}>
                  {/* Status header & Mistake Archetype Badge */}
                  <div className="flex flex-wrap items-center justify-between gap-2 pb-2 border-b border-slate-800/80">
                    <div className="flex items-center gap-2">
                      {answerResult.is_correct ? (
                        <>
                          <CheckCircle2 className="h-5 w-5 text-[#22C55E]" />
                          <span className="font-bold text-[#22C55E] text-sm">Correct Solution!</span>
                        </>
                      ) : (
                        <>
                          <XCircle className="h-5 w-5 text-[#F43F5E]" />
                          <span className="font-bold text-[#F43F5E] text-sm">
                            Incorrect. Correct Answer: Option {answerResult.correct_answer}
                          </span>
                        </>
                      )}
                    </div>

                    {/* Mistake Type Badge */}
                    {!answerResult.is_correct && answerResult.mistake_type && (
                      <span className="px-2.5 py-1 rounded-full text-[10px] font-mono font-bold bg-[#F59E0B]/20 text-[#F59E0B] border border-[#F59E0B]/40 uppercase tracking-wider flex items-center gap-1">
                        <AlertTriangle className="h-3 w-3" />
                        Mistake: {cleanDisplay(answerResult.mistake_type.replace(/_/g, ' '))}
                      </span>
                    )}
                  </div>

                  {/* Same-Topic Retention vs Advancement Banner */}
                  <div className={`p-3 rounded-xl border text-xs flex items-start gap-2.5 ${
                    answerResult.stay_on_topic
                      ? 'bg-[#22D3EE]/10 border-[#22D3EE]/30 text-[#22D3EE]'
                      : 'bg-[#8B5CF6]/15 border-[#8B5CF6]/30 text-[#8B5CF6]'
                  }`}>
                    {answerResult.stay_on_topic ? (
                      <Target className="h-4 w-4 text-[#22D3EE] shrink-0 mt-0.5" />
                    ) : (
                      <Sparkles className="h-4 w-4 text-[#8B5CF6] shrink-0 mt-0.5" />
                    )}
                    <div className="space-y-0.5">
                      <p className="font-semibold text-[11px] text-[#F8FAFC]">
                        {answerResult.stay_on_topic ? 'Personal Learning Twin: Topic Locked & Retention Mode' : 'Personal Learning Twin: Topic Solidified'}
                      </p>
                      <p className="text-[11px] opacity-90 leading-relaxed text-[#94A3B8]">
                        {cleanDisplay(answerResult.stay_on_topic_reason) || (
                          answerResult.stay_on_topic 
                            ? `Mastery is ${answerResult.updated_mastery_score}%. Solidifying this topic (Need 2 consecutive correct answers: ${answerResult.consecutive_successes}/2).`
                            : `Consistently strong understanding (${answerResult.updated_mastery_score}%). Advancement recommended!`
                        )}
                      </p>
                    </div>
                  </div>

                  {/* Misconception Fingerprint Alert */}
                  {answerResult.misconception_alert && (
                    <div className="p-3.5 rounded-xl bg-[#8B5CF6]/15 border border-[#8B5CF6]/40 text-[#F8FAFC] text-xs flex items-start gap-2.5">
                      <ShieldAlert className="h-4 w-4 text-[#8B5CF6] shrink-0 mt-0.5" />
                      <div className="space-y-1">
                        <span className="font-bold text-[#8B5CF6] block text-[11px] uppercase tracking-wider">
                          Misconception Fingerprint Detected
                        </span>
                        <p className="text-[11px] text-[#F8FAFC]/90 leading-relaxed">
                          {cleanDisplay(answerResult.misconception_alert)}
                        </p>
                      </div>
                    </div>
                  )}

                  {/* Recovery Mode Trigger Alert */}
                  {answerResult.recovery_mode_triggered && (
                    <div className="p-3.5 rounded-xl bg-[#F43F5E]/20 border border-[#F43F5E]/40 text-[#F8FAFC] text-xs flex items-start gap-2.5">
                      <BrainCircuit className="h-4 w-4 text-[#F43F5E] shrink-0 mt-0.5" />
                      <div>
                        <span className="font-bold text-[#F43F5E] block text-[11px] uppercase tracking-wider">
                          Learning Recovery Mode Activated
                        </span>
                        <p className="text-[11px] text-[#F8FAFC]/90 leading-relaxed">
                          Your Learning Twin detected consecutive struggles on this concept. We are shifting your path to step-by-step intuitive scaffolding to rebuild your mastery.
                        </p>
                      </div>
                    </div>
                  )}

                  {/* Dual Explanations Toggle */}
                  <div className="space-y-2 pt-1">
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-semibold text-[#94A3B8] uppercase tracking-wider">
                        Pedagogical Explanation:
                      </span>
                      <div className="flex items-center gap-1 p-0.5 bg-[#101827] rounded-lg border border-slate-800">
                        <button
                          type="button"
                          onClick={() => setExplanationMode('brief')}
                          className={`px-2.5 py-1 rounded text-[10px] font-bold transition-all cursor-pointer ${
                            explanationMode === 'brief'
                              ? 'bg-[#22D3EE] text-slate-950 shadow-sm'
                              : 'text-[#94A3B8] hover:text-[#F8FAFC]'
                          }`}
                        >
                          Brief Explanation
                        </button>
                        <button
                          type="button"
                          onClick={() => setExplanationMode('full')}
                          className={`px-2.5 py-1 rounded text-[10px] font-bold transition-all cursor-pointer ${
                            explanationMode === 'full'
                              ? 'bg-[#22D3EE] text-slate-950 shadow-sm'
                              : 'text-[#94A3B8] hover:text-[#F8FAFC]'
                          }`}
                        >
                          Full Step-by-Step
                        </button>
                      </div>
                    </div>

                    {/* Explanation Content Box (Clean, Clear BG, Zero Asterisks) */}
                    <div className="p-4 rounded-xl bg-[#101827] border border-slate-800 text-[#F8FAFC] text-xs leading-relaxed">
                      {explanationMode === 'brief' ? (
                        <p className="whitespace-pre-line">{cleanDisplay(answerResult.explanation_brief || answerResult.explanation)}</p>
                      ) : (
                        <div className="space-y-2 whitespace-pre-line font-sans">
                          {cleanDisplay(answerResult.explanation_full || answerResult.explanation)}
                        </div>
                      )}
                    </div>
                  </div>

                  {/* How to Avoid Advice */}
                  {answerResult.how_to_avoid && (
                    <div className="p-3 rounded-xl bg-[#101827] border border-[#F59E0B]/30 flex items-start gap-2.5 text-[11px]">
                      <Lightbulb className="h-4 w-4 text-[#F59E0B] shrink-0 mt-0.5" />
                      <div>
                        <strong className="text-[#F59E0B]">How to Avoid Next Time: </strong>
                        <span className="text-[#F8FAFC]">{cleanDisplay(answerResult.how_to_avoid)}</span>
                      </div>
                    </div>
                  )}

                  {/* Prerequisite Hint */}
                  {answerResult.prerequisite_hint && (
                    <div className="p-3 rounded-xl bg-[#101827] border border-[#22D3EE]/30 text-[11px] text-[#22D3EE] flex items-start gap-2">
                      <HelpCircle className="h-4 w-4 shrink-0 mt-0.5 text-[#22D3EE]" />
                      <span><strong className="text-[#F8FAFC]">Key Foundational Identity:</strong> {cleanDisplay(answerResult.prerequisite_hint)}</span>
                    </div>
                  )}

                  {/* Root-Cause Prerequisite Diagnostic Alert */}
                  {answerResult.root_cause_warning && (
                    <div className="p-3.5 rounded-lg bg-[#F59E0B]/15 border border-[#F59E0B]/30 text-[#F8FAFC] text-xs space-y-1">
                      <div className="flex items-center gap-2 font-bold text-[#F59E0B]">
                        <AlertTriangle className="h-4 w-4 text-[#F59E0B]" />
                        Root-Cause Diagnostic Alert
                      </div>
                      <p className="text-[11px] text-[#F8FAFC]/90 leading-relaxed">
                        {cleanDisplay(answerResult.root_cause_warning)}
                      </p>
                      {answerResult.recommended_remedy && (
                        <p className="text-[11px] text-[#22D3EE] font-medium pt-1">
                          Remedy: {cleanDisplay(answerResult.recommended_remedy)}
                        </p>
                      )}
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}

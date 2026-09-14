'use client';

import React, { useState, useEffect, useMemo } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { 
  Target, Clock, AlertTriangle, CheckCircle2, XCircle, ArrowRight, 
  RotateCcw, Sparkles, BookOpen, HelpCircle, Layers, GraduationCap,
  Atom, Dna, FlaskConical, Calculator, ShieldAlert, Lightbulb, Check,
  Flame, BrainCircuit, ChevronRight
} from 'lucide-react';

interface AcademicClass {
  id: number;
  class_number: number;
  title: string;
  code: string;
  subjects_count?: number;
}

interface SyllabusSubject {
  id: number;
  class_id: number;
  class_number: number;
  name: string;
  code: string;
  is_integrated_science: boolean;
  units_count?: number;
  chapters_count?: number;
}

interface SyllabusChapter {
  id: number;
  chapter_number: number;
  title: string;
  name?: string;
  code: string;
  domain?: string;
  topics_count?: number;
}

interface SyllabusUnit {
  id: number;
  unit_number: number;
  title: string;
  name?: string;
  code: string;
  chapters: SyllabusChapter[];
}

interface SyllabusTopic {
  id: number;
  title: string;
  code: string;
  subtopics?: Array<{ id: number; title: string; code: string }>;
  learning_outcomes?: Array<{ id: number; code: string; statement: string; bloom_level: string }>;
  questions_count?: number;
}

function cleanDisplay(text?: string | null): string {
  if (!text) return '';
  return text.replace(/[*#]/g, '').trim();
}

function getSubjectIcon(name: string) {
  const n = name.toLowerCase();
  if (n.includes('math')) return Calculator;
  if (n.includes('phys')) return Atom;
  if (n.includes('chem')) return FlaskConical;
  if (n.includes('bio')) return Dna;
  if (n.includes('sci')) return BrainCircuit;
  return Layers;
}

function getSubjectColor(name: string) {
  const n = name.toLowerCase();
  if (n.includes('math')) return 'text-[#22D3EE]';
  if (n.includes('phys')) return 'text-[#F59E0B]';
  if (n.includes('chem')) return 'text-[#22C55E]';
  if (n.includes('bio')) return 'text-[#F43F5E]';
  return 'text-[#38BDF8]';
}

export default function PracticePage() {
  // CBSE 2026-27 Dynamic Hierarchy States
  const [classesList, setClassesList] = useState<AcademicClass[]>([]);
  const [selectedClass, setSelectedClass] = useState<AcademicClass | null>(null);

  const [subjectsList, setSubjectsList] = useState<SyllabusSubject[]>([]);
  const [selectedSubject, setSelectedSubject] = useState<SyllabusSubject | null>(null);

  const [unitsList, setUnitsList] = useState<SyllabusUnit[]>([]);
  const [selectedChapterId, setSelectedChapterId] = useState<number | 'ALL'>('ALL');

  const [topicsList, setTopicsList] = useState<SyllabusTopic[]>([]);
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

  // 1. Fetch official CBSE classes on mount
  useEffect(() => {
    apiRequest('/syllabus/classes')
      .then((data: AcademicClass[]) => {
        if (Array.isArray(data) && data.length > 0) {
          setClassesList(data);
          // Default to Class 10 or the first class
          const defaultCls = data.find((c) => c.class_number === 10) || data[0];
          setSelectedClass(defaultCls);
        }
      })
      .catch((err) => console.error('Error fetching classes:', err));
  }, []);

  // 2. Fetch subjects when selectedClass changes
  useEffect(() => {
    if (!selectedClass) return;
    apiRequest(`/syllabus/classes/${selectedClass.id}/subjects`)
      .then((data: SyllabusSubject[]) => {
        if (Array.isArray(data) && data.length > 0) {
          setSubjectsList(data);
          setSelectedSubject(data[0]);
          setSelectedChapterId('ALL');
          setSelectedTopicId(null);
          setActiveTopicName('');
        } else {
          setSubjectsList([]);
          setSelectedSubject(null);
        }
      })
      .catch((err) => console.error('Error fetching subjects:', err));
  }, [selectedClass]);

  // 3. Fetch structured units & chapters when selectedSubject changes
  useEffect(() => {
    if (!selectedClass || !selectedSubject) {
      setUnitsList([]);
      return;
    }
    apiRequest(`/syllabus/classes/${selectedClass.id}/subjects/${selectedSubject.id}`)
      .then((data: any) => {
        if (data && Array.isArray(data.units)) {
          setUnitsList(data.units);
          setSelectedChapterId('ALL');
          setSelectedTopicId(null);
          setActiveTopicName('');
        } else {
          setUnitsList([]);
        }
      })
      .catch((err) => console.error('Error fetching subject structure:', err));
  }, [selectedClass, selectedSubject]);

  // Flatten available chapters
  const allChapters = useMemo(() => {
    const list: SyllabusChapter[] = [];
    unitsList.forEach((u) => {
      if (Array.isArray(u.chapters)) {
        list.push(...u.chapters);
      }
    });
    return list;
  }, [unitsList]);

  // 4. Fetch topics when a specific chapter is selected
  useEffect(() => {
    if (selectedChapterId === 'ALL') {
      setTopicsList([]);
      setSelectedTopicId(null);
      setActiveTopicName('');
      return;
    }
    apiRequest(`/syllabus/chapters/${selectedChapterId}/topics`)
      .then((data: any) => {
        if (data && Array.isArray(data.topics)) {
          setTopicsList(data.topics);
          setSelectedTopicId(null);
          setActiveTopicName('');
        } else {
          setTopicsList([]);
        }
      })
      .catch((err) => console.error('Error fetching chapter topics:', err));
  }, [selectedChapterId]);

  // Timer tick for active question
  useEffect(() => {
    let timer: any;
    if (sessionStarted && !answerResult && !sessionFinished) {
      timer = setInterval(() => {
        setTimeSpent((prev) => prev + 1);
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [sessionStarted, answerResult, sessionFinished, currentIndex]);

  // Handle class switch
  const handleClassChange = (c: AcademicClass) => {
    setSelectedClass(c);
    // Reset state immediately
    setSubjectsList([]);
    setSelectedSubject(null);
    setUnitsList([]);
    setSelectedChapterId('ALL');
    setTopicsList([]);
    setSelectedTopicId(null);
    setActiveTopicName('');
  };

  // Start Practice
  const handleStartPractice = async (isFollowup = false, customTopicId?: number) => {
    if (!selectedClass) return;
    setLoading(true);
    setSessionFinished(false);
    setAnswerResult(null);

    const targetTopicId = customTopicId || selectedTopicId;

    try {
      const payload: any = {
        academic_class_id: selectedClass.id,
        class_number: selectedClass.class_number,
        num_questions: numQuestions,
        exclude_ids: isFollowup ? completedQuestionIds : []
      };

      if (selectedSubject) {
        payload.subject_id = selectedSubject.id;
        payload.subject = selectedSubject.name;
      }

      if (selectedChapterId !== 'ALL') {
        payload.chapter_id = selectedChapterId;
      }

      if (targetTopicId) {
        payload.topic_id = targetTopicId;
        payload.hierarchy_topic_id = targetTopicId;
      }

      if (difficulty !== 'ANY') {
        payload.difficulty = difficulty;
      }

      const res = await apiRequest('/practice/start', {
        method: 'POST',
        body: JSON.stringify(payload)
      });

      if (Array.isArray(res) && res.length > 0) {
        setQuestions(res);
        setCurrentIndex(0);
        setSelectedOption('');
        setTimeSpent(0);
        setScore(0);
        setSessionStarted(true);

        if (res[0].topic_name) {
          setActiveTopicName(res[0].topic_name);
        }
      } else {
        alert('No practice questions found for the selected syllabus filter. Try selecting All Chapters or Adaptive Difficulty.');
      }
    } catch (err: any) {
      console.error('Error starting practice session:', err);
      alert(err.message || 'Failed to start practice session. Please verify your selection.');
    } finally {
      setLoading(false);
    }
  };

  const currentQ = questions[currentIndex];

  // Submit Answer
  const handleSubmitAnswer = async () => {
    if (!selectedOption || !currentQ || submitting) return;
    setSubmitting(true);

    try {
      const res = await apiRequest('/practice/submit-answer', {
        method: 'POST',
        body: JSON.stringify({
          question_id: currentQ.id,
          selected_answer: selectedOption,
          time_taken_seconds: Math.max(1, timeSpent)
        })
      });

      setAnswerResult(res);
      setCompletedQuestionIds((prev) => [...prev, currentQ.id]);

      if (res.is_correct) {
        setScore((prev) => prev + (currentQ.points || 10));
      }
    } catch (err: any) {
      console.error('Error submitting answer:', err);
      alert(err.message || 'Failed to submit answer.');
    } finally {
      setSubmitting(false);
    }
  };

  // Move to Next Question
  const handleNextQuestion = () => {
    if (currentIndex + 1 < questions.length) {
      setCurrentIndex((prev) => prev + 1);
      setSelectedOption('');
      setAnswerResult(null);
      setTimeSpent(0);
      setExplanationMode('brief');
    } else {
      setSessionFinished(true);
    }
  };

  return (
    <div className="flex-1 pb-16">
      <Navbar 
        title="Smart Adaptive Practice" 
        subtitle="CBSE/NCERT 2026-27 Syllabus Grounded Mastery Engine" 
      />

      <div className="p-4 sm:p-6 max-w-5xl mx-auto space-y-6">
        {!sessionStarted ? (
          /* Session Configuration Card */
          <div className="p-6 sm:p-8 rounded-2xl bg-[#162235] border border-slate-800 shadow-2xl space-y-6">
            <div className="flex flex-wrap items-center justify-between pb-4 border-b border-slate-800 gap-3">
              <div className="flex items-center gap-3">
                <div className="h-10 w-10 rounded-xl bg-[#22D3EE]/10 border border-[#22D3EE]/20 text-[#22D3EE] flex items-center justify-center">
                  <Target className="h-5 w-5" />
                </div>
                <div>
                  <h2 className="text-lg font-bold text-[#F8FAFC]">Configure Practice Session</h2>
                  <p className="text-xs text-[#94A3B8]">CBSE Academic Session 2026-2027 • Official NCERT Question Bank</p>
                </div>
              </div>

              {completedQuestionIds.length > 0 && (
                <div className="px-3 py-1 rounded-full bg-[#101827] border border-slate-800 text-[11px] text-[#22D3EE] font-medium">
                  {completedQuestionIds.length} questions attempted today
                </div>
              )}
            </div>

            {/* STEP 1: Academic Class Selector (Classes 8 - 12) */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <label className="block text-xs font-semibold text-[#94A3B8] uppercase tracking-wider flex items-center gap-1.5">
                  <GraduationCap className="h-4 w-4 text-[#22D3EE]" />
                  Select Academic Class
                </label>
                <span className="text-[11px] font-mono text-teal-400 bg-teal-500/10 px-2 py-0.5 rounded border border-teal-500/20">
                  CBSE 2026-27 Persistent Database
                </span>
              </div>
              <div className="grid grid-cols-5 gap-2">
                {classesList.map((c) => {
                  const isSelected = selectedClass?.id === c.id;
                  return (
                    <button
                      key={c.id}
                      type="button"
                      onClick={() => handleClassChange(c)}
                      className={`p-3 rounded-xl border text-xs font-bold transition-all cursor-pointer flex flex-col items-center gap-1 ${
                        isSelected
                          ? 'bg-[#22D3EE]/20 border-[#22D3EE] text-[#22D3EE] shadow-lg shadow-[#22D3EE]/10 scale-[1.02]'
                          : 'bg-[#101827] border-slate-800 text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-[#1C2B42]'
                      }`}
                    >
                      <span className="text-sm font-black">{c.title}</span>
                      <span className="text-[10px] font-mono opacity-70">Grade {c.class_number}</span>
                    </button>
                  );
                })}
              </div>
            </div>

            {/* STEP 2: Subject Selector */}
            <div className="space-y-2">
              <label className="block text-xs font-semibold text-[#94A3B8] uppercase tracking-wider flex items-center gap-1.5">
                <Layers className="h-3.5 w-3.5 text-[#22D3EE]" />
                Select Board Subject
                {selectedClass && selectedClass.class_number <= 10 && (
                  <span className="text-[10px] text-teal-300 font-normal ml-2">
                    (Classes 8–10 use Integrated Science with internal Physics, Chemistry & Biology)
                  </span>
                )}
              </label>
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                {subjectsList.map((s) => {
                  const Icon = getSubjectIcon(s.name);
                  const color = getSubjectColor(s.name);
                  const isSelected = selectedSubject?.id === s.id;
                  return (
                    <button
                      key={s.id}
                      type="button"
                      onClick={() => {
                        setSelectedSubject(s);
                        setSelectedChapterId('ALL');
                        setSelectedTopicId(null);
                        setActiveTopicName('');
                      }}
                      className={`p-3.5 rounded-xl border text-xs font-semibold flex flex-col items-center gap-1.5 transition-all cursor-pointer ${
                        isSelected
                          ? 'bg-[#22D3EE]/20 border-[#22D3EE] text-[#22D3EE] shadow-lg shadow-[#22D3EE]/10'
                          : 'bg-[#101827] border-slate-800 text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-[#1C2B42]'
                      }`}
                    >
                      <Icon className={`h-5 w-5 ${isSelected ? 'text-[#22D3EE]' : color}`} />
                      <span className="font-bold">{s.name}</span>
                      {s.is_integrated_science && (
                        <span className="text-[10px] text-teal-300 font-mono">Integrated</span>
                      )}
                    </button>
                  );
                })}
              </div>
            </div>

            {/* STEP 3: Chapter & Topic Dropdowns */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="space-y-2">
                <label className="block text-xs font-semibold text-[#94A3B8] uppercase tracking-wider">
                  Chapter
                </label>
                <select
                  value={selectedChapterId}
                  onChange={(e) => {
                    const val = e.target.value === 'ALL' ? 'ALL' : Number(e.target.value);
                    setSelectedChapterId(val);
                    setSelectedTopicId(null);
                    setActiveTopicName('');
                  }}
                  className="w-full p-3 bg-[#101827] border border-slate-800 rounded-xl text-xs text-[#F8FAFC] focus:outline-none focus:border-[#22D3EE]"
                >
                  <option value="ALL">All Chapters in {selectedSubject ? selectedSubject.name : 'Subject'}</option>
                  {unitsList.map((u) => (
                    <optgroup key={u.id} label={u.title || `Unit ${u.unit_number}`}>
                      {(u.chapters || []).map((ch) => (
                        <option key={ch.id} value={ch.id}>
                          {ch.title || ch.name} {ch.domain ? `[${ch.domain}]` : ''}
                        </option>
                      ))}
                    </optgroup>
                  ))}
                </select>
              </div>

              <div className="space-y-2">
                <label className="block text-xs font-semibold text-[#94A3B8] uppercase tracking-wider">
                  Specific Concept Topic
                </label>
                <select
                  value={selectedTopicId || ''}
                  disabled={selectedChapterId === 'ALL'}
                  onChange={(e) => {
                    const tid = e.target.value ? Number(e.target.value) : null;
                    setSelectedTopicId(tid);
                    if (tid) {
                      const tObj = topicsList.find((t) => t.id === tid);
                      if (tObj) setActiveTopicName(tObj.title);
                    } else {
                      setActiveTopicName('');
                    }
                  }}
                  className="w-full p-3 bg-[#101827] border border-slate-800 rounded-xl text-xs text-[#F8FAFC] focus:outline-none focus:border-[#22D3EE] disabled:opacity-50"
                >
                  <option value="">
                    {selectedChapterId === 'ALL' ? 'Select a specific chapter to choose a topic' : 'All Topics in Chapter'}
                  </option>
                  {topicsList.map((t) => (
                    <option key={t.id} value={t.id}>
                      {t.title} ({t.code})
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* STEP 4: Target Difficulty */}
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

            {/* STEP 5: Question Count */}
            <div className="space-y-2">
              <label className="block text-xs font-semibold text-[#94A3B8] uppercase tracking-wider">
                Session Length
              </label>
              <div className="grid grid-cols-3 gap-2.5">
                {[5, 10, 15].map((cnt) => (
                  <button
                    key={cnt}
                    type="button"
                    onClick={() => setNumQuestions(cnt)}
                    className={`py-2 px-3 rounded-xl border text-xs font-bold transition-all cursor-pointer ${
                      numQuestions === cnt
                        ? 'bg-[#22D3EE]/20 border-[#22D3EE] text-[#22D3EE]'
                        : 'bg-[#101827] border-slate-800 text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-[#1C2B42]'
                    }`}
                  >
                    {cnt} Questions
                  </button>
                ))}
              </div>
            </div>

            {/* Launch Button */}
            <button
              type="button"
              disabled={loading || !selectedClass}
              onClick={() => handleStartPractice(false)}
              className="w-full py-4 rounded-xl font-bold text-sm bg-gradient-to-r from-[#22D3EE] to-[#0EA5E9] hover:from-[#0EA5E9] hover:to-[#0284C7] text-[#0A0F1D] shadow-xl shadow-[#22D3EE]/20 flex items-center justify-center gap-2 cursor-pointer transition-all disabled:opacity-50"
            >
              {loading ? (
                <span>Loading Questions from Database...</span>
              ) : (
                <>
                  <Sparkles className="h-4 w-4" />
                  <span>Start Practice: {selectedClass?.title} • {selectedSubject?.name}</span>
                  <ArrowRight className="h-4 w-4" />
                </>
              )}
            </button>
          </div>
        ) : sessionFinished ? (
          /* Session Completed Summary */
          <div className="p-8 rounded-2xl bg-[#162235] border border-slate-800 shadow-2xl text-center space-y-6">
            <div className="h-16 w-16 rounded-full bg-[#22C55E]/10 border border-[#22C55E]/20 text-[#22C55E] flex items-center justify-center mx-auto">
              <CheckCircle2 className="h-8 w-8" />
            </div>

            <div className="space-y-2">
              <h2 className="text-2xl font-bold text-[#F8FAFC]">Practice Round Complete!</h2>
              <p className="text-sm text-[#94A3B8]">
                You scored <span className="text-[#22D3EE] font-bold">{score}</span> points in this adaptive round.
              </p>
            </div>

            <div className="flex flex-col sm:flex-row items-center justify-center gap-3 pt-4">
              <button
                onClick={() => handleStartPractice(true)}
                className="py-3 px-5 rounded-xl font-bold text-[#F8FAFC] bg-[#1C2B42] hover:bg-[#223652] border border-slate-700 text-xs flex items-center justify-center gap-2 cursor-pointer"
              >
                <Sparkles className="h-4 w-4 text-[#22D3EE]" /> Practice Next Set (Fresh Questions)
              </button>
              <button
                onClick={() => {
                  setSessionStarted(false);
                  setSessionFinished(false);
                }}
                className="py-3 px-5 rounded-xl bg-[#101827] border border-slate-800 hover:bg-[#1C2B42] text-[#94A3B8] hover:text-[#F8FAFC] text-xs font-semibold flex items-center justify-center gap-2 cursor-pointer"
              >
                <RotateCcw className="h-3.5 w-3.5" /> Change Class / Subject
              </button>
            </div>
          </div>
        ) : currentQ ? (
          /* Active Question Card */
          <div className="space-y-5">
            {/* Header Telemetry & Complete CBSE 2026-27 Syllabus Breadcrumb */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between p-4 rounded-xl bg-[#162235] border border-slate-800 gap-3">
              <div className="flex flex-wrap items-center gap-2 text-xs text-[#94A3B8]">
                <span className="font-bold text-[#22D3EE]">Question {currentIndex + 1}</span> of {questions.length}
                <span className="text-slate-600">•</span>
                <span className="px-2 py-0.5 rounded bg-teal-500/10 text-teal-300 font-bold border border-teal-500/30">
                  {currentQ.class_name || 'CBSE'}
                </span>
                <span className="text-[#F8FAFC] font-semibold">{cleanDisplay(currentQ.subject_name || 'General')}</span>
                {currentQ.domain && (
                  <span className="px-1.5 py-0.5 rounded bg-purple-500/10 text-purple-300 font-mono text-[10px] border border-purple-500/30">
                    {currentQ.domain}
                  </span>
                )}
                {currentQ.unit_name && (
                  <>
                    <span className="text-slate-600">/</span>
                    <span className="text-slate-400 text-[11px]">{cleanDisplay(currentQ.unit_name)}</span>
                  </>
                )}
                {currentQ.chapter_name && (
                  <>
                    <span className="text-slate-600">/</span>
                    <span className="text-[#94A3B8] font-medium">{cleanDisplay(currentQ.chapter_name)}</span>
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

            {/* Official NCERT Target Learning Outcome Banner */}
            {currentQ.learning_outcome && (
              <div className="px-4 py-2.5 rounded-xl bg-[#0f172a] border border-teal-500/20 text-xs text-teal-300 flex items-center gap-2">
                <Sparkles className="h-4 w-4 shrink-0 text-teal-400" />
                <span><strong>Target Learning Outcome:</strong> {cleanDisplay(currentQ.learning_outcome)}</span>
              </div>
            )}

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
                    borderClass = 'border-[#22D3EE] bg-[#22D3EE]/10 text-[#22D3EE] shadow-sm shadow-[#22D3EE]/20';
                  }

                  return (
                    <button
                      key={opt.id}
                      type="button"
                      disabled={!!answerResult || submitting}
                      onClick={() => setSelectedOption(opt.id)}
                      className={`w-full p-4 rounded-xl border text-left text-xs sm:text-sm font-medium transition-all flex items-center justify-between cursor-pointer ${borderClass} disabled:cursor-default`}
                    >
                      <div className="flex items-center gap-3">
                        <span className="h-6 w-6 rounded-lg bg-slate-800/80 border border-slate-700 flex items-center justify-center font-bold text-xs">
                          {opt.id}
                        </span>
                        <span>{cleanDisplay(opt.text)}</span>
                      </div>

                      {answerResult && opt.id === answerResult.correct_answer && (
                        <Check className="h-4 w-4 text-[#22C55E]" />
                      )}
                    </button>
                  );
                })}
              </div>

              {/* Submission / Continue Bar */}
              {!answerResult ? (
                <button
                  type="button"
                  disabled={!selectedOption || submitting}
                  onClick={handleSubmitAnswer}
                  className="w-full py-3.5 rounded-xl font-bold text-xs bg-gradient-to-r from-[#22D3EE] to-[#0EA5E9] hover:from-[#0EA5E9] hover:to-[#0284C7] text-[#0A0F1D] flex items-center justify-center gap-2 cursor-pointer transition-all disabled:opacity-50"
                >
                  {submitting ? 'Checking Answer...' : 'Submit Answer'}
                </button>
              ) : (
                /* Dual Explanation & Remediation Panel */
                <div className="space-y-4 pt-4 border-t border-slate-800">
                  {/* Result Status Banner */}
                  <div className={`p-4 rounded-xl border flex items-start gap-3 ${
                    answerResult.is_correct
                      ? 'bg-[#22C55E]/10 border-[#22C55E]/30 text-[#22C55E]'
                      : 'bg-[#F43F5E]/10 border-[#F43F5E]/30 text-[#F43F5E]'
                  }`}>
                    {answerResult.is_correct ? (
                      <CheckCircle2 className="h-5 w-5 shrink-0 mt-0.5" />
                    ) : (
                      <XCircle className="h-5 w-5 shrink-0 mt-0.5" />
                    )}
                    <div className="space-y-1">
                      <h4 className="font-bold text-sm">
                        {answerResult.is_correct ? 'Correct Answer!' : 'Incorrect Answer'}
                      </h4>
                      <p className="text-xs text-[#94A3B8]">
                        Topic Mastery: <strong className="text-[#F8FAFC]">{answerResult.updated_mastery_score}%</strong> ({answerResult.updated_mastery_status})
                      </p>
                    </div>
                  </div>

                  {/* Stay On Topic Reinforcement Alert */}
                  {answerResult.stay_on_topic && (
                    <div className="p-3.5 rounded-xl bg-amber-500/10 border border-amber-500/30 text-amber-300 text-xs flex items-start gap-2.5">
                      <ShieldAlert className="h-4 w-4 shrink-0 mt-0.5 text-amber-400" />
                      <div>
                        <span className="font-bold block">Reinforcement Topic Locked:</span>
                        <span className="text-[#94A3B8]">{cleanDisplay(answerResult.stay_on_topic_reason)}</span>
                      </div>
                    </div>
                  )}

                  {/* Dual Mode Switcher: Brief vs Full Derivation */}
                  <div className="flex items-center justify-between pt-2">
                    <div className="flex rounded-lg bg-[#101827] p-1 border border-slate-800 text-[11px]">
                      <button
                        type="button"
                        onClick={() => setExplanationMode('brief')}
                        className={`px-3 py-1 rounded-md font-semibold transition-all ${
                          explanationMode === 'brief' ? 'bg-[#1C2B42] text-[#22D3EE]' : 'text-[#94A3B8]'
                        }`}
                      >
                        Brief Core Reason
                      </button>
                      <button
                        type="button"
                        onClick={() => setExplanationMode('full')}
                        className={`px-3 py-1 rounded-md font-semibold transition-all ${
                          explanationMode === 'full' ? 'bg-[#1C2B42] text-[#22D3EE]' : 'text-[#94A3B8]'
                        }`}
                      >
                        Step-by-Step Derivation
                      </button>
                    </div>
                  </div>

                  {/* Explanation Box */}
                  <div className="p-4 rounded-xl bg-[#101827] border border-slate-800 text-xs leading-relaxed text-[#CBD5E1] whitespace-pre-line">
                    {cleanDisplay(
                      explanationMode === 'brief'
                        ? (answerResult.explanation_brief || answerResult.explanation)
                        : (answerResult.explanation_full || answerResult.explanation)
                    )}
                  </div>

                  {/* Action Button: Next Question or Remedial Set */}
                  <button
                    type="button"
                    onClick={handleNextQuestion}
                    className="w-full py-3.5 rounded-xl font-bold text-xs bg-[#22D3EE] hover:bg-[#0EA5E9] text-[#0A0F1D] flex items-center justify-center gap-2 cursor-pointer transition-all"
                  >
                    <span>{currentIndex + 1 < questions.length ? 'Next Question' : 'Finish Practice Round'}</span>
                    <ArrowRight className="h-4 w-4" />
                  </button>
                </div>
              )}
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
}

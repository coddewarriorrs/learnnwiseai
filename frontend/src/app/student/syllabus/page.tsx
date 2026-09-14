'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { 
  BrainCircuit, ChevronRight, CheckCircle2, AlertTriangle, ArrowRight,
  GraduationCap, Layers, BookOpen, Target, Sparkles, Atom, FlaskConical,
  Dna, Calculator, ChevronDown
} from 'lucide-react';
import Link from 'next/link';

interface AcademicClass {
  id: number;
  class_number: number;
  title: string;
  code: string;
}

interface SyllabusSubject {
  id: number;
  class_id: number;
  class_number: number;
  name: string;
  code: string;
  is_integrated_science: boolean;
  units_count: number;
  chapters_count: number;
}

interface SyllabusChapter {
  id: number;
  chapter_number: number;
  title: string;
  code: string;
  domain?: string;
  description?: string;
  topics_count?: number;
}

interface SyllabusUnit {
  id: number;
  unit_number: number;
  title: string;
  code: string;
  weightage_marks?: number;
  chapters: SyllabusChapter[];
}

interface SyllabusTopic {
  id: number;
  title: string;
  code: string;
  subtopics: Array<{ id: number; title: string; code: string }>;
  learning_outcomes: Array<{ id: number; code: string; statement: string; bloom_level: string }>;
  questions_count?: number;
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

function getDomainBadge(domain?: string) {
  if (!domain) return null;
  const d = domain.toLowerCase();
  let color = 'bg-purple-500/10 text-purple-300 border-purple-500/30';
  if (d.includes('bio')) color = 'bg-rose-500/10 text-rose-300 border-rose-500/30';
  if (d.includes('chem')) color = 'bg-emerald-500/10 text-emerald-300 border-emerald-500/30';
  if (d.includes('phys')) color = 'bg-amber-500/10 text-amber-300 border-amber-500/30';
  return (
    <span className={`px-2 py-0.5 rounded text-[10px] font-bold border font-mono ${color}`}>
      {domain}
    </span>
  );
}

export default function StudentSyllabusPage() {
  const [classesList, setClassesList] = useState<AcademicClass[]>([]);
  const [selectedClass, setSelectedClass] = useState<AcademicClass | null>(null);

  const [subjectsList, setSubjectsList] = useState<SyllabusSubject[]>([]);
  const [selectedSubject, setSelectedSubject] = useState<SyllabusSubject | null>(null);

  const [unitsList, setUnitsList] = useState<SyllabusUnit[]>([]);
  const [expandedChapters, setExpandedChapters] = useState<Record<number, boolean>>({});
  const [chapterTopics, setChapterTopics] = useState<Record<number, SyllabusTopic[]>>({});

  const [masteries, setMasteries] = useState<Record<number, any>>({});
  const [loading, setLoading] = useState(true);
  const [loadingSubject, setLoadingSubject] = useState(false);

  // 1. Initial Mount: Load Classes and Student Topic Mastery
  useEffect(() => {
    Promise.all([
      apiRequest('/syllabus/classes'),
      apiRequest('/students/me/mastery').catch(() => ({ topics: [] }))
    ])
      .then(([classesData, masteryData]) => {
        if (Array.isArray(classesData) && classesData.length > 0) {
          setClassesList(classesData);
          // Default to Class 10 or first
          const defaultCls = classesData.find((c: AcademicClass) => c.class_number === 10) || classesData[0];
          setSelectedClass(defaultCls);
        }

        const map: Record<number, any> = {};
        if (masteryData && masteryData.topics) {
          masteryData.topics.forEach((t: any) => {
            map[t.topic_id] = t;
            if (t.hierarchy_topic_id) {
              map[t.hierarchy_topic_id] = t;
            }
          });
        }
        setMasteries(map);
      })
      .catch((err) => console.error('Error initializing syllabus page:', err))
      .finally(() => setLoading(false));
  }, []);

  // 2. Fetch subjects when selectedClass changes
  useEffect(() => {
    if (!selectedClass) return;
    setLoadingSubject(true);
    apiRequest(`/syllabus/classes/${selectedClass.id}/subjects`)
      .then((data: SyllabusSubject[]) => {
        if (Array.isArray(data) && data.length > 0) {
          setSubjectsList(data);
          setSelectedSubject(data[0]);
        } else {
          setSubjectsList([]);
          setSelectedSubject(null);
        }
      })
      .catch((err) => console.error('Error fetching subjects:', err))
      .finally(() => setLoadingSubject(false));
  }, [selectedClass]);

  // 3. Fetch structured units and chapters when selectedSubject changes
  useEffect(() => {
    if (!selectedClass || !selectedSubject) {
      setUnitsList([]);
      return;
    }
    setLoadingSubject(true);
    apiRequest(`/syllabus/classes/${selectedClass.id}/subjects/${selectedSubject.id}`)
      .then((data: any) => {
        if (data && Array.isArray(data.units)) {
          setUnitsList(data.units);
          // Expand first chapter by default
          if (data.units.length > 0 && data.units[0].chapters?.length > 0) {
            const firstCh = data.units[0].chapters[0];
            toggleChapter(firstCh.id);
          }
        } else {
          setUnitsList([]);
        }
      })
      .catch((err) => console.error('Error fetching units:', err))
      .finally(() => setLoadingSubject(false));
  }, [selectedClass, selectedSubject]);

  // Expand / collapse chapter and fetch topics if not loaded
  const toggleChapter = async (chapterId: number) => {
    setExpandedChapters((prev) => ({ ...prev, [chapterId]: !prev[chapterId] }));

    if (!chapterTopics[chapterId]) {
      try {
        const res = await apiRequest(`/syllabus/chapters/${chapterId}/topics`);
        if (res && Array.isArray(res.topics)) {
          setChapterTopics((prev) => ({ ...prev, [chapterId]: res.topics }));
        }
      } catch (err) {
        console.error('Error loading topics for chapter:', err);
      }
    }
  };

  return (
    <div className="flex-1 pb-16">
      <Navbar 
        title="CBSE/NCERT Official Syllabus" 
        subtitle="CBSE Academic Session 2026-2027 • Standardized Curriculum Hierarchy & Learning Outcomes" 
      />

      <div className="p-4 sm:p-6 max-w-5xl mx-auto space-y-6">
        {/* Class Selection Tabs */}
        <div className="p-4 rounded-2xl bg-[#162235] border border-slate-800 space-y-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <GraduationCap className="h-5 w-5 text-[#22D3EE]" />
              <h2 className="text-sm font-bold text-[#F8FAFC]">Academic Class Hierarchy</h2>
            </div>
            <span className="text-[11px] font-mono text-teal-300 bg-teal-500/10 px-2.5 py-1 rounded-full border border-teal-500/20">
              CBSE 2026-27 Persistent DB
            </span>
          </div>

          <div className="grid grid-cols-5 gap-2">
            {classesList.map((c) => {
              const isSelected = selectedClass?.id === c.id;
              return (
                <button
                  key={c.id}
                  type="button"
                  onClick={() => setSelectedClass(c)}
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

        {/* Subject Selection Tabs */}
        <div className="space-y-2">
          <div className="flex items-center justify-between text-xs text-[#94A3B8]">
            <span className="font-semibold uppercase tracking-wider flex items-center gap-1.5">
              <Layers className="h-3.5 w-3.5 text-[#22D3EE]" />
              Board Subjects for {selectedClass?.title}
            </span>
            {selectedClass && selectedClass.class_number <= 10 ? (
              <span className="text-[11px] text-teal-300">
                Mathematics & Integrated Science (Internal Physics, Chemistry, Biology)
              </span>
            ) : (
              <span className="text-[11px] text-teal-300">
                Senior Secondary: Distinct Mathematics, Physics, Chemistry, Biology
              </span>
            )}
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
            {subjectsList.map((s) => {
              const Icon = getSubjectIcon(s.name);
              const color = getSubjectColor(s.name);
              const isSelected = selectedSubject?.id === s.id;
              return (
                <button
                  key={s.id}
                  type="button"
                  onClick={() => setSelectedSubject(s)}
                  className={`p-3.5 rounded-xl border text-xs font-semibold flex items-center gap-3 transition-all cursor-pointer ${
                    isSelected
                      ? 'bg-[#22D3EE]/20 border-[#22D3EE] text-[#22D3EE] shadow-lg shadow-[#22D3EE]/10'
                      : 'bg-[#101827] border-slate-800 text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-[#1C2B42]'
                  }`}
                >
                  <Icon className={`h-5 w-5 shrink-0 ${isSelected ? 'text-[#22D3EE]' : color}`} />
                  <div className="text-left">
                    <div className="font-bold text-sm">{s.name}</div>
                    <div className="text-[10px] text-slate-400 font-mono">
                      {s.units_count} Units • {s.chapters_count} Chapters
                    </div>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Structured Units & Chapters View */}
        {loading || loadingSubject ? (
          <div className="p-12 text-center text-slate-400 text-sm">
            Loading official CBSE/NCERT curriculum units...
          </div>
        ) : unitsList.length === 0 ? (
          <div className="p-12 rounded-2xl bg-[#162235] border border-slate-800 text-center text-slate-400 text-sm">
            No curriculum units registered for this subject.
          </div>
        ) : (
          <div className="space-y-4">
            {unitsList.map((u) => (
              <div key={u.id} className="rounded-2xl bg-[#162235] border border-slate-800 overflow-hidden shadow-xl">
                {/* Unit Header */}
                <div className="p-4 bg-[#101827]/80 border-b border-slate-800 flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="px-2 py-0.5 rounded bg-teal-500/10 text-teal-300 font-mono font-bold text-xs border border-teal-500/20">
                      Unit {u.unit_number}
                    </span>
                    <h3 className="text-sm font-bold text-[#F8FAFC]">{u.title}</h3>
                  </div>
                  <span className="text-[11px] font-mono text-slate-400">
                    {(u.chapters || []).length} Chapters
                  </span>
                </div>

                {/* Chapters list in unit */}
                <div className="divide-y divide-slate-800/60">
                  {(u.chapters || []).map((ch) => {
                    const isExpanded = !!expandedChapters[ch.id];
                    const topics = chapterTopics[ch.id] || [];

                    return (
                      <div key={ch.id} className="p-4 transition-all">
                        <div 
                          onClick={() => toggleChapter(ch.id)}
                          className="flex items-center justify-between cursor-pointer group"
                        >
                          <div className="flex items-center gap-3">
                            <span className="h-6 w-6 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-xs font-mono font-bold text-slate-300">
                              {ch.chapter_number}
                            </span>
                            <div>
                              <div className="flex items-center gap-2">
                                <span className="font-bold text-sm text-[#F8FAFC] group-hover:text-[#22D3EE] transition-colors">
                                  {ch.title}
                                </span>
                                {getDomainBadge(ch.domain)}
                              </div>
                              {ch.description && (
                                <p className="text-xs text-slate-400 mt-0.5 line-clamp-1">{ch.description}</p>
                              )}
                            </div>
                          </div>

                          <div className="flex items-center gap-2">
                            <span className="text-[11px] text-slate-400 font-mono">
                              {ch.topics_count || (topics.length ? topics.length : 'View')} Topics
                            </span>
                            <ChevronDown className={`h-4 w-4 text-slate-400 transition-transform ${isExpanded ? 'rotate-180 text-[#22D3EE]' : ''}`} />
                          </div>
                        </div>

                        {/* Expanded Topics and Learning Outcomes */}
                        {isExpanded && (
                          <div className="mt-4 pt-4 border-t border-slate-800/80 space-y-3 pl-4 sm:pl-8">
                            {topics.length === 0 ? (
                              <div className="text-xs text-slate-500 italic">Loading chapter topics & learning outcomes...</div>
                            ) : (
                              topics.map((top) => {
                                const mastery = masteries[top.id];
                                return (
                                  <div key={top.id} className="p-3.5 rounded-xl bg-[#0f172a] border border-slate-800 space-y-2.5">
                                    <div className="flex flex-wrap items-center justify-between gap-2">
                                      <div className="flex items-center gap-2">
                                        <BookOpen className="h-4 w-4 text-[#22D3EE]" />
                                        <span className="font-semibold text-xs sm:text-sm text-[#F8FAFC]">{top.title}</span>
                                        <span className="text-[10px] font-mono text-slate-500">({top.code})</span>
                                      </div>

                                      <div className="flex items-center gap-2">
                                        {mastery ? (
                                          <span className={`px-2 py-0.5 rounded-full text-[10px] font-bold border ${
                                            mastery.status === 'CRITICAL' ? 'bg-rose-500/15 text-rose-300 border-rose-500/30' :
                                            mastery.status === 'STRONG' ? 'bg-emerald-500/15 text-emerald-300 border-emerald-500/30' :
                                            'bg-amber-500/15 text-amber-300 border-amber-500/30'
                                          }`}>
                                            {mastery.mastery_score}% {mastery.status.replace('_', ' ')}
                                          </span>
                                        ) : null}

                                        <Link
                                          href={`/student/practice`}
                                          className="py-1 px-3 rounded-lg bg-[#22D3EE]/15 hover:bg-[#22D3EE]/25 text-[#22D3EE] border border-[#22D3EE]/30 font-bold text-xs transition-all flex items-center gap-1 cursor-pointer"
                                        >
                                          <span>Practice Topic</span>
                                          <ArrowRight className="h-3 w-3" />
                                        </Link>
                                      </div>
                                    </div>

                                    {/* Subtopics */}
                                    {top.subtopics && top.subtopics.length > 0 && (
                                      <div className="flex flex-wrap items-center gap-1.5 pt-1">
                                        <span className="text-[10px] text-slate-500 font-mono">Subtopics:</span>
                                        {top.subtopics.map((st) => (
                                          <span key={st.id} className="px-2 py-0.5 rounded bg-slate-800/90 text-slate-300 text-[10px] border border-slate-700">
                                            {st.title}
                                          </span>
                                        ))}
                                      </div>
                                    )}

                                    {/* Learning Outcomes */}
                                    {top.learning_outcomes && top.learning_outcomes.length > 0 && (
                                      <div className="pt-1.5 border-t border-slate-800/60 space-y-1">
                                        {top.learning_outcomes.map((lo) => (
                                          <div key={lo.id} className="text-[11px] text-teal-300 flex items-start gap-1.5">
                                            <Sparkles className="h-3.5 w-3.5 shrink-0 mt-0.5 text-teal-400" />
                                            <span><strong>Learning Outcome:</strong> {lo.statement}</span>
                                          </div>
                                        ))}
                                      </div>
                                    )}
                                  </div>
                                );
                              })
                            )}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

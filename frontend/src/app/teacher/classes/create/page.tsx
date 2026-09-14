'use client';

import React, { useState } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { useRouter } from 'next/navigation';
import { apiRequest } from '@/lib/api';
import { BookOpen, ArrowRight, ArrowLeft } from 'lucide-react';
import Link from 'next/link';

export default function CreateClassPage() {
  const router = useRouter();
  const [name, setName] = useState('');
  const [grade, setGrade] = useState('11');
  const [subject, setSubject] = useState('Mathematics');
  const [board, setBoard] = useState('CBSE');
  const [academicYear, setAcademicYear] = useState('2026-2027');
  const [submitting, setSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);

    try {
      await apiRequest('/classes', {
        method: 'POST',
        body: JSON.stringify({
          name,
          grade,
          subject,
          board,
          academic_year: academicYear,
        }),
      });
      router.push('/teacher/classes');
    } catch (err: any) {
      alert(err.message || 'Error creating class');
      setSubmitting(false);
    }
  };

  return (
    <div className="flex-1 pb-16">
      <Navbar title="Create New Class Cohort" subtitle="Generate class credentials and student enrollment links" />

      <div className="p-6 max-w-2xl mx-auto space-y-6">
        <Link href="/teacher/classes" className="inline-flex items-center gap-1.5 text-xs text-slate-400 hover:text-white">
          <ArrowLeft className="h-3.5 w-3.5" /> Back to Classes
        </Link>

        <div className="p-8 rounded-2xl bg-[#162235] border border-slate-800 shadow-2xl">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                Class Name
              </label>
              <input
                type="text"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="e.g. Grade 11 Advanced Mathematics"
                className="w-full p-3 bg-slate-900 border border-slate-700 rounded-xl text-sm text-white focus:outline-none focus:border-teal-500"
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                  Grade / Year
                </label>
                <select
                  value={grade}
                  onChange={(e) => setGrade(e.target.value)}
                  className="w-full p-3 bg-slate-900 border border-slate-700 rounded-xl text-sm text-white focus:outline-none focus:border-teal-500"
                >
                  <option value="9">Grade 9</option>
                  <option value="10">Grade 10</option>
                  <option value="11">Grade 11</option>
                  <option value="12">Grade 12</option>
                  <option value="College">College / Undergraduate</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                  Subject
                </label>
                <input
                  type="text"
                  required
                  value={subject}
                  onChange={(e) => setSubject(e.target.value)}
                  placeholder="Mathematics"
                  className="w-full p-3 bg-slate-900 border border-slate-700 rounded-xl text-sm text-white focus:outline-none focus:border-teal-500"
                />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                  Board / Curriculum
                </label>
                <input
                  type="text"
                  required
                  value={board}
                  onChange={(e) => setBoard(e.target.value)}
                  placeholder="CBSE"
                  className="w-full p-3 bg-slate-900 border border-slate-700 rounded-xl text-sm text-white focus:outline-none focus:border-teal-500"
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 uppercase tracking-wider mb-1">
                  Academic Year
                </label>
                <input
                  type="text"
                  required
                  value={academicYear}
                  onChange={(e) => setAcademicYear(e.target.value)}
                  placeholder="2026-2027"
                  className="w-full p-3 bg-slate-900 border border-slate-700 rounded-xl text-sm text-white focus:outline-none focus:border-teal-500"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={submitting}
              className="w-full mt-4 py-3 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-teal-500 to-cyan-400 hover:from-teal-400 hover:to-cyan-300 text-xs transition-all flex items-center justify-center gap-2 cursor-pointer shadow-md shadow-teal-500/20"
            >
              {submitting ? 'Creating class...' : 'Save & Generate Invite Link'}
              <ArrowRight className="h-4 w-4" />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}

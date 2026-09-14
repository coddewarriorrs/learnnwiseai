'use client';

import React from 'react';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell 
} from 'recharts';

interface MasteryBarChartProps {
  data: Array<{
    topic: string;
    mastery: number;
    status: string;
  }>;
}

export function MasteryBarChart({ data }: MasteryBarChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center text-slate-500 text-sm">
        No mastery data available yet. Start practicing to generate metrics!
      </div>
    );
  }

  const getColor = (score: number) => {
    if (score < 40) return '#EF4444'; // CRITICAL
    if (score <= 70) return '#F59E0B'; // NEEDS PRACTICE
    return '#10B981'; // STRONG
  };

  return (
    <div className="h-72 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
          <XAxis 
            dataKey="topic" 
            stroke="#64748b" 
            fontSize={11} 
            tickLine={false}
            interval={0}
            angle={-20}
            textAnchor="end"
          />
          <YAxis 
            stroke="#64748b" 
            fontSize={11} 
            tickLine={false}
            domain={[0, 100]}
            unit="%"
          />
          <Tooltip 
            content={({ active, payload }) => {
              if (active && payload && payload.length) {
                const item = payload[0].payload;
                return (
                  <div className="bg-slate-900 border border-slate-700 p-2.5 rounded-lg shadow-xl text-xs">
                    <p className="font-bold text-white mb-1">{item.topic}</p>
                    <p className="text-slate-300">Mastery: <span className="font-semibold text-teal-400">{item.mastery}%</span></p>
                    <p className="text-slate-400 capitalize">Status: {item.status.toLowerCase().replace('_', ' ')}</p>
                  </div>
                );
              }
              return null;
            }}
          />
          <Bar dataKey="mastery" radius={[4, 4, 0, 0]}>
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={getColor(entry.mastery)} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

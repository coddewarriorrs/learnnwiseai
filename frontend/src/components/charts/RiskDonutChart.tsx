'use client';

import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts';

interface RiskDonutChartProps {
  data: Array<{
    name: string;
    value: number;
    color: string;
  }>;
}

export function RiskDonutChart({ data }: RiskDonutChartProps) {
  const total = data.reduce((acc, curr) => acc + curr.value, 0);

  if (total === 0) {
    return (
      <div className="h-48 flex items-center justify-center text-slate-500 text-xs">
        No student risk data available.
      </div>
    );
  }

  return (
    <div className="h-48 w-full flex items-center justify-between">
      <div className="w-1/2 h-full">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={data}
              innerRadius={36}
              outerRadius={56}
              paddingAngle={4}
              dataKey="value"
            >
              {data.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip
              content={({ active, payload }) => {
                if (active && payload && payload.length) {
                  const item = payload[0].payload;
                  return (
                    <div className="bg-slate-900 border border-slate-700 px-2 py-1 rounded shadow text-xs text-white">
                      <span className="font-semibold">{item.name}:</span> {item.value} students
                    </div>
                  );
                }
                return null;
              }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="w-1/2 space-y-2 pr-2">
        {data.map((item) => (
          <div key={item.name} className="flex items-center justify-between text-xs">
            <div className="flex items-center gap-1.5">
              <span className="h-2.5 w-2.5 rounded-full" style={{ backgroundColor: item.color }}></span>
              <span className="text-slate-300">{item.name}</span>
            </div>
            <span className="font-bold text-white">{item.value}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

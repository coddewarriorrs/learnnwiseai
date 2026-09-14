import './globals.css';
import { AuthProvider } from '@/lib/auth';

export const metadata = {
  title: 'LearnWise AI — Education that adapts to every learner',
  description: 'Smart adaptive education platform diagnosing prerequisite learning gaps, predicting academic risk, and empowering teachers with real-time actionable interventions.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#0B1220] text-slate-100 antialiased selection:bg-teal-500 selection:text-white">
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}

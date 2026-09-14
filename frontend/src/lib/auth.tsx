'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { apiRequest } from './api';

export interface User {
  id: number;
  email: string;
  full_name: string;
  role: 'STUDENT' | 'TEACHER' | 'ADMIN';
  grade_level?: string;
  parent_access_token?: string;
}

interface AuthContextType {
  user: User | null;
  loading: boolean;
  login: (token: string, refreshToken: string, user: User) => void;
  logout: () => void;
  refreshUser: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    const savedUser = localStorage.getItem('learnwise_user');
    const token = localStorage.getItem('learnwise_token');
    if (savedUser && token) {
      try {
        setUser(JSON.parse(savedUser));
      } catch {
        localStorage.removeItem('learnwise_user');
      }
    }
    setLoading(false);
  }, []);

  const login = (token: string, refreshToken: string, userData: User) => {
    localStorage.setItem('learnwise_token', token);
    localStorage.setItem('learnwise_refresh_token', refreshToken);
    localStorage.setItem('learnwise_user', JSON.stringify(userData));
    setUser(userData);

    // Check if there was a pending join token saved
    const pendingJoin = localStorage.getItem('pending_join_token');
    if (pendingJoin) {
      localStorage.removeItem('pending_join_token');
      router.push(`/join/${pendingJoin}`);
      return;
    }

    if (userData.role === 'TEACHER') {
      router.push('/teacher/dashboard');
    } else if (userData.role === 'ADMIN') {
      router.push('/admin/dashboard');
    } else {
      router.push('/student/dashboard');
    }
  };

  const logout = () => {
    localStorage.removeItem('learnwise_token');
    localStorage.removeItem('learnwise_refresh_token');
    localStorage.removeItem('learnwise_user');
    setUser(null);
    router.push('/login');
  };

  const refreshUser = async () => {
    try {
      const me = await apiRequest('/auth/me');
      setUser(me);
      localStorage.setItem('learnwise_user', JSON.stringify(me));
    } catch {
      logout();
    }
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, refreshUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

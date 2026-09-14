'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Navbar } from '@/components/layout/Navbar';
import { apiRequest } from '@/lib/api';
import { 
  MessageSquareCode, Send, Sparkles, AlertTriangle, User, Bot, 
  HelpCircle, Image as ImageIcon, Mic, MicOff, Volume2, VolumeX, 
  X, CheckCircle2, XCircle, ArrowRight, BrainCircuit, ShieldAlert,
  Loader2
} from 'lucide-react';

interface StepAnalysis {
  step_number: number;
  step_content: string;
  is_correct: boolean;
  comment?: string;
}

interface ImageAnalysisData {
  is_readable: boolean;
  unreadable_reason?: string;
  problem_statement_detected?: string;
  steps: StepAnalysis[];
  first_incorrect_step?: number;
  where_error_occurred?: string;
  why_error_occurred?: string;
  how_to_correct?: string;
  correct_final_result?: string;
}

interface MessageItem {
  id?: string;
  sender: 'STUDENT' | 'AI';
  content: string;
  image_preview?: string;
  image_analysis?: ImageAnalysisData;
  time?: string;
}

function cleanText(text?: string | null): string {
  if (!text) return '';
  return text.replace(/[*#]/g, '').trim();
}

export default function TutorPage() {
  const [activeConversationId, setActiveConversationId] = useState<number | null>(null);
  const [messages, setMessages] = useState<MessageItem[]>([
    {
      sender: 'AI',
      content: "Hello! I'm your LearnWise AI Multi-Subject Tutor, powered like ChatGPT & Gemini. You can ask me any question across Mathematics, Physics, Chemistry, Biology, Computer Science, and Humanities, speak with your voice, or upload a photo of your handwritten notebook calculations for instant step-by-step diagnostic feedback. What would you like to explore today?",
    }
  ]);
  const [input, setInput] = useState('');
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [sending, setSending] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [currentlySpeakingIdx, setCurrentlySpeakingIdx] = useState<number | null>(null);
  const [twinProfile, setTwinProfile] = useState<any>(null);
  const [practiceContext, setPracticeContext] = useState<any | null>(null);

  const [suggested, setSuggested] = useState<string[]>([
    "What should I practice next?",
    "Explain how photosynthesis works and its chemical equation",
    "Solve the quadratic equation: x^2 - 5x + 6 = 0",
    "Explain Ohm's law and how to calculate resistance",
    "What are Newton's three laws of motion with examples?"
  ]);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const recognitionRef = useRef<any>(null);
  const isSendingRef = useRef<boolean>(false);
  const lastFailedMessageRef = useRef<string | null>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, sending]);

  // Load student's active conversation session & Personal Learning Twin context
  useEffect(() => {
    apiRequest('/ai/active-session')
      .then((data) => {
        if (data && data.conversation_id) {
          setActiveConversationId(data.conversation_id);
          if (data.messages && data.messages.length > 0) {
            setMessages(data.messages.map((m: any) => ({
              sender: m.sender,
              content: cleanText(m.content),
              image_preview: m.image_url,
              image_analysis: m.image_analysis,
              time: m.timestamp
            })));
          }
        }
      })
      .catch(() => {});

    apiRequest('/twin/me')
      .then((data) => setTwinProfile(data))
      .catch(() => setTwinProfile(null));

    try {
      const saved = sessionStorage.getItem('learnwise_practice_context');
      if (saved) {
        setPracticeContext(JSON.parse(saved));
      }
    } catch {}
  }, []);

  // Initialize Speech Recognition with proper Indian English language and error handling
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (SpeechRecognition) {
        const recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-IN';

        recognition.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript;
          setInput((prev) => (prev ? `${prev} ${transcript}` : transcript));
          setIsListening(false);
        };

        recognition.onerror = (e: any) => {
          setIsListening(false);
          if (e.error === 'not-allowed') {
            alert('Microphone permission was denied. Please allow microphone access in your browser settings.');
          } else if (e.error !== 'no-speech') {
            console.warn('Speech recognition notice:', e.error);
          }
        };

        recognition.onend = () => {
          setIsListening(false);
        };

        recognitionRef.current = recognition;
      }
    }
  }, []);

  const toggleVoiceInput = () => {
    if (!recognitionRef.current) {
      alert('Speech recognition is not supported in this browser. Please use Chrome, Edge, or Safari.');
      return;
    }
    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
    } else {
      try {
        recognitionRef.current.start();
        setIsListening(true);
      } catch {
        setIsListening(false);
      }
    }
  };

function getIndianEnglishFemaleVoice(): SpeechSynthesisVoice | null {
  if (typeof window === 'undefined' || !('speechSynthesis' in window)) return null;
  const voices = window.speechSynthesis.getVoices();
  if (!voices || voices.length === 0) return null;

  // 1. Highest Priority: Indian English Female voice (e.g. Heera, Neerja, Kalyani, Veena, en-IN female)
  const indianFemale = voices.find(v => 
    (v.lang === 'en-IN' || v.lang.toLowerCase().includes('en-in') || v.lang.toLowerCase().includes('en_in')) &&
    (v.name.toLowerCase().includes('female') || 
     v.name.toLowerCase().includes('heera') || 
     v.name.toLowerCase().includes('neerja') || 
     v.name.toLowerCase().includes('kalyani') || 
     v.name.toLowerCase().includes('veena') ||
     v.name.toLowerCase().includes('priya') ||
     v.name.toLowerCase().includes('online'))
  );
  if (indianFemale) return indianFemale;

  // 2. Any Indian English voice (en-IN)
  const anyIndian = voices.find(v => 
    v.lang === 'en-IN' || v.lang.toLowerCase().includes('en-in') || v.lang.toLowerCase().includes('en_in')
  );
  if (anyIndian) return anyIndian;

  // 3. Clear Natural English Female voices (e.g. Jenny, Aria, Sonia, Google UK English Female)
  const naturalFemale = voices.find(v =>
    v.lang.startsWith('en') && 
    (v.name.toLowerCase().includes('female') ||
     v.name.toLowerCase().includes('natural') ||
     v.name.toLowerCase().includes('heera') ||
     v.name.toLowerCase().includes('aria') ||
     v.name.toLowerCase().includes('jenny') ||
     v.name.toLowerCase().includes('sonia') ||
     v.name.toLowerCase().includes('zira'))
  );
  if (naturalFemale) return naturalFemale;

  // 4. Any English voice fallback
  return voices.find(v => v.lang.startsWith('en')) || voices[0] || null;
}

  const handleSpeakText = (text: string, idx: number) => {
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) {
      alert('Speech synthesis is not supported on this browser.');
      return;
    }

    if (isSpeaking && currentlySpeakingIdx === idx) {
      window.speechSynthesis.cancel();
      setIsSpeaking(false);
      setCurrentlySpeakingIdx(null);
      return;
    }

    window.speechSynthesis.cancel();
    const clean = cleanText(text).replace(/[`_$\\]/g, ' ');
    const utterance = new SpeechSynthesisUtterance(clean);

    // Apply Indian English female voice profile with natural pitch and rate
    const voice = getIndianEnglishFemaleVoice();
    if (voice) {
      utterance.voice = voice;
      utterance.lang = voice.lang || 'en-IN';
    } else {
      utterance.lang = 'en-IN';
    }
    utterance.pitch = 1.08; // Clear, pleasant female pitch
    utterance.rate = 0.95;  // Natural, articulate cadence

    utterance.onend = () => {
      setIsSpeaking(false);
      setCurrentlySpeakingIdx(null);
    };

    utterance.onerror = () => {
      setIsSpeaking(false);
      setCurrentlySpeakingIdx(null);
    };

    setIsSpeaking(true);
    setCurrentlySpeakingIdx(idx);
    window.speechSynthesis.speak(utterance);
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      setSelectedImage(reader.result as string);
    };
    reader.readAsDataURL(file);
  };

  const handleSend = async (textToSend?: string) => {
    const message = textToSend || input;
    if ((!message.trim() && !selectedImage) || sending || isSendingRef.current) return;

    isSendingRef.current = true;
    setSending(true);

    const clientMsgId = typeof crypto !== 'undefined' && crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    let rawBase64: string | undefined = undefined;
    if (selectedImage) {
      rawBase64 = selectedImage.includes(',') ? selectedImage.split(',')[1] : selectedImage;
    }

    const userMsg: MessageItem = {
      id: clientMsgId,
      sender: 'STUDENT',
      content: message || 'Please analyze this handwritten calculation from my notebook.',
      image_preview: selectedImage || undefined,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => {
      if (prev.some(m => m.id === clientMsgId)) return prev;
      return [...prev, userMsg];
    });

    if (!textToSend) setInput('');
    const imageToSend = rawBase64;
    setSelectedImage(null);

    try {
      const payload: any = {
        message: message || 'Please analyze my handwritten solution steps.',
        image_base64: imageToSend,
        topic_id: twinProfile?.current_focus_topic?.topic_id,
        conversation_id: activeConversationId,
        client_message_id: clientMsgId,
      };

      if (practiceContext) {
        payload.question_context = {
          question_id: practiceContext.question_id,
          prompt: practiceContext.prompt,
          options: practiceContext.options,
          subject_name: practiceContext.subject_name,
          chapter_name: practiceContext.chapter_name,
          topic_name: practiceContext.topic_name,
          student_answer: practiceContext.selected_option,
          is_answered: practiceContext.is_answered,
          is_correct: practiceContext.is_correct,
        };
      }

      const res = await apiRequest('/ai/tutor', {
        method: 'POST',
        body: JSON.stringify(payload),
      });

      if (res.conversation_id) {
        setActiveConversationId(res.conversation_id);
      }

      const aiMsgId = res.message_id ? String(res.message_id) : `${clientMsgId}-ai`;
      const aiMsg: MessageItem = {
        id: aiMsgId,
        sender: 'AI',
        content: cleanText(res.reply),
        image_analysis: res.image_analysis,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => {
        if (prev.some(m => m.id === aiMsgId)) return prev;
        return [...prev, aiMsg];
      });

      if (res.suggested_questions && res.suggested_questions.length > 0) {
        setSuggested(res.suggested_questions);
      }
      lastFailedMessageRef.current = null;
    } catch {
      lastFailedMessageRef.current = message;
      const errorMsgId = `${clientMsgId}-err`;
      setMessages((prev) => {
        if (prev.some(m => m.id === errorMsgId)) return prev;
        return [
          ...prev,
          {
            id: errorMsgId,
            sender: 'AI',
            content: "I ran into a temporary connection issue. Please click Retry below to send your question again.",
          }
        ];
      });
    } finally {
      isSendingRef.current = false;
      setSending(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col h-screen overflow-hidden bg-[#0B1220] text-[#F8FAFC]">
      <Navbar 
        title="Multimodal Socratic AI Tutor" 
        subtitle="Text, Voice & Handwritten Notebook Analysis grounded in your Personal Learning Twin" 
      />

      {/* Grounding Telemetry Bar */}
      {twinProfile && (
        <div className="bg-[#101827] border-b border-slate-800 px-6 py-3 flex flex-wrap items-center justify-between text-sm gap-3">
          <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-[#22D3EE] animate-pulse" />
            <span className="text-[#94A3B8] font-medium">Personal Learning Twin Synchronized:</span>
            <span className="text-[#22D3EE] font-bold">
              {cleanText(twinProfile.current_focus_topic?.title) || 'Active Curriculum'} ({twinProfile.overall_mastery}% Mastery)
            </span>
          </div>

          <div className="flex items-center gap-3">
            {twinProfile.misconception_fingerprint && twinProfile.misconception_fingerprint.length > 0 && (
              <span className="px-2.5 py-0.5 rounded-full bg-[#8B5CF6]/15 border border-[#8B5CF6]/30 text-[#8B5CF6] text-[11px] font-semibold flex items-center gap-1">
                <ShieldAlert className="h-3 w-3 text-[#8B5CF6]" />
                Misconception Alert: {cleanText(twinProfile.misconception_fingerprint[0].mistake_type.replace(/_/g, ' '))}
              </span>
            )}

            {twinProfile.recovery_mode?.active && (
              <span className="px-2.5 py-0.5 rounded-full bg-[#F43F5E]/15 border border-[#F43F5E]/30 text-[#F43F5E] text-[11px] font-semibold flex items-center gap-1">
                <BrainCircuit className="h-3 w-3 text-[#F43F5E]" />
                Recovery Mode Step {twinProfile.recovery_mode.step}/7
              </span>
            )}
          </div>
        </div>
      )}

      {/* Active Question Context Banner */}
      {practiceContext && (
        <div className="bg-[#162235] border-b border-[#22D3EE]/30 px-6 py-3 flex flex-wrap items-center justify-between text-sm gap-3 animate-in fade-in">
          <div className="flex items-center gap-2 overflow-hidden">
            <span className="text-[#22D3EE] font-bold">Active Question Context:</span>
            <span className="text-[#F8FAFC] font-semibold">{cleanText(practiceContext.topic_name || practiceContext.chapter_name || 'Practice Question')}</span>
            {practiceContext.prompt && (
              <span className="text-[#94A3B8] truncate max-w-lg hidden md:inline">
                - {cleanText(practiceContext.prompt)}
              </span>
            )}
          </div>
          <button
            type="button"
            onClick={() => {
              setPracticeContext(null);
              try { sessionStorage.removeItem('learnwise_practice_context'); } catch {}
            }}
            className="text-[11px] text-[#94A3B8] hover:text-[#F43F5E] px-2.5 py-1 rounded bg-[#101827] border border-slate-800 transition-colors cursor-pointer"
            title="Clear question context"
          >
            Clear Context
          </button>
        </div>
      )}

      {/* Messages Feed */}
      <div className="flex-1 overflow-y-auto p-6 max-w-4xl mx-auto w-full space-y-4">
        {messages.map((m, idx) => {
          const isUser = m.sender === 'STUDENT';
          return (
            <div key={idx} className={`flex gap-3 ${isUser ? 'justify-end' : 'justify-start'}`}>
              {!isUser && (
                <div className="h-8 w-8 rounded-xl bg-[#22D3EE]/10 border border-[#22D3EE]/20 text-[#22D3EE] flex items-center justify-center shrink-0 mt-0.5">
                  <Bot className="h-4 w-4" />
                </div>
              )}
              
              <div className={`p-5 rounded-2xl max-w-2xl text-base sm:text-[17px] leading-relaxed space-y-4 ${
                isUser 
                  ? 'bg-[#162235] text-[#F8FAFC] border border-slate-700/80 rounded-tr-none' 
                  : 'bg-[#162235] text-[#F8FAFC] border border-slate-800 rounded-tl-none shadow-md'
              }`}>
                {/* User Image Attachment */}
                {m.image_preview && (
                  <div className="rounded-xl overflow-hidden border border-[#22D3EE]/30 max-h-48 max-w-xs">
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img src={m.image_preview} alt="Attached calculation" className="object-cover w-full h-full" />
                  </div>
                )}

                <div className="whitespace-pre-wrap">{cleanText(m.content)}</div>

                {/* Structured Handwritten Image Diagnostic Breakdown */}
                {m.image_analysis && m.image_analysis.is_readable && (
                  <div className="mt-3 p-4 rounded-xl bg-[#101827] border border-slate-800 space-y-3 text-xs">
                    <div className="flex items-center justify-between border-b border-slate-800 pb-2">
                      <span className="font-bold text-[#22D3EE] uppercase tracking-wider text-[11px] flex items-center gap-1.5">
                        <Sparkles className="h-3.5 w-3.5 text-[#22D3EE]" />
                        Handwritten Step Breakdown
                      </span>
                      {m.image_analysis.first_incorrect_step && (
                        <span className="px-2 py-0.5 rounded bg-[#F43F5E]/20 text-[#F43F5E] border border-[#F43F5E]/40 font-bold text-[10px]">
                          Error in Step {m.image_analysis.first_incorrect_step}
                        </span>
                      )}
                    </div>

                    {/* Steps list */}
                    <div className="space-y-1.5">
                      {m.image_analysis.steps.map((s) => (
                        <div key={s.step_number} className={`p-2 rounded-lg flex items-start gap-2 text-[11px] ${
                          s.is_correct ? 'bg-[#22C55E]/10 border border-[#22C55E]/30 text-[#F8FAFC]' : 'bg-[#F43F5E]/10 border border-[#F43F5E]/30 text-[#F8FAFC]'
                        }`}>
                          {s.is_correct ? (
                            <CheckCircle2 className="h-4 w-4 text-[#22C55E] shrink-0 mt-0.5" />
                          ) : (
                            <XCircle className="h-4 w-4 text-[#F43F5E] shrink-0 mt-0.5" />
                          )}
                          <div className="flex-1">
                            <span className="font-semibold block text-[#F8FAFC]">Step {s.step_number}: {cleanText(s.step_content)}</span>
                            {s.comment && <span className="text-[10px] text-[#94A3B8] block pt-0.5">{cleanText(s.comment)}</span>}
                          </div>
                        </div>
                      ))}
                    </div>

                    {/* WHERE / WHY / HOW */}
                    {m.image_analysis.where_error_occurred && (
                      <div className="p-3 rounded-lg bg-[#162235] border border-slate-800 space-y-1.5 text-[11px]">
                        <div>
                          <strong className="text-[#F59E0B]">Where Error Occurred: </strong>
                          <span className="text-[#F8FAFC]">{cleanText(m.image_analysis.where_error_occurred)}</span>
                        </div>
                        <div>
                          <strong className="text-[#F43F5E]">Why It Occurred: </strong>
                          <span className="text-[#F8FAFC]">{cleanText(m.image_analysis.why_error_occurred)}</span>
                        </div>
                        <div>
                          <strong className="text-[#22D3EE]">How to Correct: </strong>
                          <span className="text-[#F8FAFC]">{cleanText(m.image_analysis.how_to_correct)}</span>
                        </div>
                        {m.image_analysis.correct_final_result && (
                          <div className="pt-1 border-t border-slate-800 font-semibold text-[#22C55E]">
                            Correct Expected Result: {cleanText(m.image_analysis.correct_final_result)}
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}

                {/* AI Audio Narration Button */}
                {!isUser && (
                  <div className="pt-1 border-t border-slate-800/60 flex items-center justify-between text-[11px] text-[#94A3B8]">
                    <button 
                      onClick={() => handleSpeakText(m.content, idx)}
                      className="flex items-center gap-1 hover:text-[#22D3EE] transition-colors cursor-pointer"
                    >
                      {currentlySpeakingIdx === idx ? (
                        <>
                          <VolumeX className="h-3.5 w-3.5 text-[#F43F5E]" />
                          <span className="text-[#F43F5E]">Stop Audio</span>
                        </>
                      ) : (
                        <>
                          <Volume2 className="h-3.5 w-3.5 text-[#22D3EE]" />
                          <span>Listen (Speech)</span>
                        </>
                      )}
                    </button>
                    <span className="text-[10px] text-[#94A3B8] flex items-center gap-1">
                      <Sparkles className="h-2.5 w-2.5 text-[#22D3EE]" /> Learning Twin Grounded
                    </span>
                  </div>
                )}
              </div>

              {isUser && (
                <div className="h-8 w-8 rounded-xl bg-[#162235] border border-slate-700 text-[#22D3EE] flex items-center justify-center shrink-0 mt-0.5 font-bold text-xs">
                  <User className="h-4 w-4" />
                </div>
              )}
            </div>
          );
        })}

        {sending && (
          <div className="flex gap-3 items-center text-xs text-[#94A3B8]">
            <div className="h-8 w-8 rounded-xl bg-[#22D3EE]/10 border border-[#22D3EE]/20 text-[#22D3EE] flex items-center justify-center shrink-0">
              <Loader2 className="h-4 w-4 animate-spin" />
            </div>
            <div className="p-3.5 rounded-2xl bg-[#162235] border border-slate-800 text-[#22D3EE]">
              Analyzing mathematical steps and checking for conceptual gaps...
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Questions Chips */}
      <div className="px-6 py-2 bg-[#101827] border-t border-slate-800 max-w-4xl mx-auto w-full">
        <div className="flex gap-2 overflow-x-auto no-scrollbar py-1">
          {suggested.map((sug, i) => (
            <button
              key={i}
              type="button"
              onClick={() => handleSend(sug)}
              className="whitespace-nowrap px-3.5 py-2 rounded-xl bg-[#162235] hover:bg-[#1C2B42] border border-slate-800 text-xs sm:text-sm text-[#94A3B8] hover:text-[#22D3EE] transition-all cursor-pointer flex items-center gap-1.5"
            >
              <Sparkles className="h-3 w-3 text-[#22D3EE]" />
              <span>{sug}</span>
            </button>
          ))}
        </div>
      </div>

      {/* Image Preview Strip */}
      {selectedImage && (
        <div className="px-6 py-2 bg-[#101827] border-t border-slate-800 max-w-4xl mx-auto w-full flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="h-12 w-12 rounded-lg overflow-hidden border border-[#22D3EE]/40 bg-slate-900">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img src={selectedImage} alt="Preview" className="h-full w-full object-cover" />
            </div>
            <div>
              <span className="text-xs text-[#22D3EE] font-medium block">Notebook photo selected</span>
              <span className="text-[10px] text-[#94A3B8]">Ready to diagnose calculation steps</span>
            </div>
          </div>
          <button 
            type="button" 
            onClick={() => setSelectedImage(null)}
            className="p-1.5 rounded-lg text-[#94A3B8] hover:text-[#F43F5E] hover:bg-[#162235] transition-colors cursor-pointer"
          >
            <X className="h-4 w-4" />
          </button>
        </div>
      )}

      {/* Chat Input Bar */}
      <div className="p-4 bg-[#101827] border-t border-slate-800">
        <div className="max-w-4xl mx-auto flex items-center gap-2">
          {/* File Input */}
          <input 
            type="file" 
            ref={fileInputRef} 
            onChange={handleImageUpload} 
            accept="image/*" 
            className="hidden" 
          />

          <button
            type="button"
            onClick={() => fileInputRef.current?.click()}
            className="p-3 rounded-xl bg-[#162235] hover:bg-[#1C2B42] border border-slate-800 text-[#94A3B8] hover:text-[#22D3EE] transition-all cursor-pointer"
            title="Upload notebook / calculation photo"
          >
            <ImageIcon className="h-5 w-5" />
          </button>

          <button
            type="button"
            onClick={toggleVoiceInput}
            className={`p-3 rounded-xl border transition-all cursor-pointer ${
              isListening 
                ? 'bg-[#F43F5E]/20 text-[#F43F5E] border-[#F43F5E]/40 animate-pulse' 
                : 'bg-[#162235] hover:bg-[#1C2B42] border-slate-800 text-[#94A3B8] hover:text-[#22D3EE]'
            }`}
            title={isListening ? 'Listening...' : 'Voice Input'}
          >
            {isListening ? <Mic className="h-5 w-5" /> : <MicOff className="h-5 w-5" />}
          </button>

          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            placeholder={selectedImage ? "Add question for this calculation or press Ask Tutor..." : "Ask any question (e.g. What is functional isomerism?), or upload a notebook photo..."}
            className="flex-1 p-4 bg-[#162235] border border-slate-800 rounded-xl text-sm sm:text-base text-[#F8FAFC] placeholder:text-slate-500 focus:outline-none focus:border-[#22D3EE]"
          />

          <button
            type="button"
            onClick={() => handleSend()}
            disabled={(!input.trim() && !selectedImage) || sending}
            className="p-3.5 px-5 rounded-xl font-bold text-slate-950 bg-gradient-to-r from-[#22D3EE] to-[#8B5CF6] hover:opacity-95 disabled:opacity-40 transition-all text-xs flex items-center gap-2 cursor-pointer disabled:cursor-not-allowed shadow-md shadow-[#22D3EE]/20"
          >
            {sending ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                <span>Thinking...</span>
              </>
            ) : (
              <>
                <Send className="h-4 w-4" />
                <span className="hidden sm:inline">Ask Tutor</span>
              </>
            )}
          </button>
        </div>
      </div>
    </div>
  );
}

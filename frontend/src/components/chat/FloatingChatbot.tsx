'use client';

import React, { useState, useEffect, useRef } from 'react';
import { 
  Sparkles, MessageSquare, X, Send, Image as ImageIcon, 
  Bot, User, AlertTriangle, CheckCircle2, ChevronDown, 
  Maximize2, Minimize2, Paperclip, Loader2, Mic, MicOff,
  Volume2, VolumeX, Lightbulb, Target
} from 'lucide-react';
import { apiRequest } from '@/lib/api';

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
  mistake_type?: string;
}

interface ChatMessage {
  id: string;
  sender: 'STUDENT' | 'AI';
  content: string;
  image_preview?: string;
  image_analysis?: ImageAnalysisData;
  timestamp: string;
}

function cleanText(text?: string | null): string {
  if (!text) return '';
  return text.replace(/[*#]/g, '').trim();
}

export function FloatingChatbot() {
  const [isOpen, setIsOpen] = useState(false);
  const [isMaximized, setIsMaximized] = useState(false);
  const [activeConversationId, setActiveConversationId] = useState<number | null>(null);
  const [practiceContext, setPracticeContext] = useState<any | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      sender: 'AI',
      content: "Hi! I'm your LearnWise AI Tutor, powered like ChatGPT & Gemini to answer questions from ANY subject (Mathematics, Physics, Chemistry, Biology, Computer Science, and Humanities). You can ask any question, request formula derivations or calculations, or upload a photo of your handwritten notebook calculations for instant step-by-step verification!",
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    },
  ]);
  const [input, setInput] = useState('');
  const [selectedImage, setSelectedImage] = useState<string | null>(null);
  const [sending, setSending] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [currentlySpeakingId, setCurrentlySpeakingId] = useState<string | null>(null);

  const fileInputRef = useRef<HTMLInputElement>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const recognitionRef = useRef<any>(null);
  const isSendingRef = useRef<boolean>(false);
  const lastFailedMessageRef = useRef<string | null>(null);

  const defaultQuickPrompts = [
    "What should I practice next?",
    "Explain how photosynthesis works step-by-step",
    "Solve the quadratic equation: x^2 - 5x + 6 = 0",
    "What is Ohm's law and how do you calculate resistance?",
    "Explain Python array time complexities with an example"
  ];

  const contextualQuickPrompts = [
    "Can you give me a conceptual hint for this question?",
    "What is the key formula or identity needed here?",
    "Explain step-by-step how to arrive at the solution",
    "What are common misconceptions to avoid on this topic?"
  ];

  const activeQuickPrompts = practiceContext ? contextualQuickPrompts : defaultQuickPrompts;

  useEffect(() => {
    if (isOpen) {
      messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages, isOpen, sending]);

  // Load persistent active session & listen for practice question context
  useEffect(() => {
    apiRequest('/ai/active-session')
      .then((session) => {
        if (session && session.conversation_id) {
          setActiveConversationId(session.conversation_id);
          if (session.messages && session.messages.length > 0) {
            const loaded: ChatMessage[] = session.messages.map((m: any) => ({
              id: m.id ? m.id.toString() : Math.random().toString(),
              sender: m.sender === 'STUDENT' ? 'STUDENT' : 'AI',
              content: cleanText(m.content),
              image_preview: m.image_url || undefined,
              image_analysis: m.image_analysis || m.metadata?.image_analysis || undefined,
              timestamp: m.timestamp 
                ? new Date(m.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                : new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            }));
            setMessages((prev) => {
              const existingIds = new Set(prev.map((x) => x.id));
              const uniqueIncoming = loaded.filter((x) => !existingIds.has(x.id));
              if (prev.length === 1 && prev[0].id === '1') {
                return loaded.length > 0 ? loaded : prev;
              }
              return [...prev, ...uniqueIncoming];
            });
          }
        }
      })
      .catch(() => {});

    // Try reading practice context from sessionStorage
    try {
      const saved = sessionStorage.getItem('learnwise_practice_context');
      if (saved) {
        setPracticeContext(JSON.parse(saved));
      }
    } catch {}

    // Listen to custom window events from the practice page
    const handlePracticeContext = (e: any) => {
      if (e.detail) {
        setPracticeContext(e.detail);
      }
    };

    const handleOpenTutorQuestion = (e: any) => {
      if (e.detail) {
        setPracticeContext(e.detail);
        setIsOpen(true);
      }
    };

    window.addEventListener('learnwise:practice-context', handlePracticeContext);
    window.addEventListener('learnwise:open-tutor-question', handleOpenTutorQuestion);

    // Warm up speech synthesis voices
    if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
      window.speechSynthesis.getVoices();
      window.speechSynthesis.onvoiceschanged = () => {
        window.speechSynthesis.getVoices();
      };
    }

    return () => {
      window.removeEventListener('learnwise:practice-context', handlePracticeContext);
      window.removeEventListener('learnwise:open-tutor-question', handleOpenTutorQuestion);
    };
  }, []);

  // Speech Recognition setup (en-IN)
  useEffect(() => {
    if (typeof window !== 'undefined') {
      const SpeechRec = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;
      if (SpeechRec) {
        const recognition = new SpeechRec();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-IN';

        recognition.onstart = () => {
          setIsListening(true);
        };

        recognition.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript;
          setInput((prev) => (prev ? `${prev} ${transcript}` : transcript));
          setIsListening(false);
        };

        recognition.onerror = (e: any) => {
          setIsListening(false);
          if (e.error === 'not-allowed') {
            alert('Microphone access was denied. Please allow microphone access in your browser.');
          }
        };

        recognition.onend = () => {
          setIsListening(false);
        };

        recognitionRef.current = recognition;
      }
    }
  }, []);

  const toggleVoice = () => {
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

    // 1. Indian English Female voice
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

    // 2. Any Indian English voice
    const anyIndian = voices.find(v => 
      v.lang === 'en-IN' || v.lang.toLowerCase().includes('en-in') || v.lang.toLowerCase().includes('en_in')
    );
    if (anyIndian) return anyIndian;

    // 3. Clear Natural English Female voice
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

  const handleSpeak = (text: string, msgId: string) => {
    if (typeof window === 'undefined' || !('speechSynthesis' in window)) return;

    if (currentlySpeakingId === msgId) {
      window.speechSynthesis.cancel();
      setCurrentlySpeakingId(null);
      return;
    }

    window.speechSynthesis.cancel();
    const clean = cleanText(text).replace(/[`_$\\\\]/g, ' ');
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

    utterance.onend = () => setCurrentlySpeakingId(null);
    utterance.onerror = () => setCurrentlySpeakingId(null);
    setCurrentlySpeakingId(msgId);
    window.speechSynthesis.speak(utterance);
  };

  const handleImageSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = () => {
      setSelectedImage(reader.result as string);
    };
    reader.readAsDataURL(file);
  };

  const handleSend = async (customMessage?: string) => {
    const textToSend = customMessage || input;
    if ((!textToSend.trim() && !selectedImage) || sending || isSendingRef.current) return;

    isSendingRef.current = true;
    setSending(true);

    const clientMsgId = typeof crypto !== 'undefined' && crypto.randomUUID ? crypto.randomUUID() : `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;

    let rawBase64: string | undefined = undefined;
    if (selectedImage) {
      rawBase64 = selectedImage.includes(',') ? selectedImage.split(',')[1] : selectedImage;
    }

    const newMsg: ChatMessage = {
      id: clientMsgId,
      sender: 'STUDENT',
      content: textToSend || 'Please analyze this handwritten calculation from my notebook.',
      image_preview: selectedImage || undefined,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
    };

    setMessages((prev) => {
      if (prev.some((m) => m.id === clientMsgId)) return prev;
      return [...prev, newMsg];
    });

    if (!customMessage) setInput('');
    const imageToSend = rawBase64;
    setSelectedImage(null);

    try {
      const payload: any = {
        message: textToSend || 'Please analyze my handwritten solution steps.',
        image_base64: imageToSend,
        conversation_id: activeConversationId || undefined,
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
      const aiMsg: ChatMessage = {
        id: aiMsgId,
        sender: 'AI',
        content: cleanText(res.reply) || "Here is the guidance for this concept.",
        image_analysis: res.image_analysis,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };

      setMessages((prev) => {
        if (prev.some((m) => m.id === aiMsgId)) return prev;
        return [...prev, aiMsg];
      });

      lastFailedMessageRef.current = null;
    } catch {
      lastFailedMessageRef.current = textToSend;
      const errorMsgId = `${clientMsgId}-err`;
      const errorMsg: ChatMessage = {
        id: errorMsgId,
        sender: 'AI',
        content: "I ran into a temporary connection issue. Please click Retry below to send your question again.",
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      };
      setMessages((prev) => {
        if (prev.some((m) => m.id === errorMsgId)) return prev;
        return [...prev, errorMsg];
      });
    } finally {
      isSendingRef.current = false;
      setSending(false);
    }
  };

  return (
    <div className={isOpen && isMaximized ? "fixed inset-0 z-50 p-2 sm:p-4 md:p-6 bg-black/75 backdrop-blur-sm flex items-center justify-center animate-in fade-in duration-200" : "fixed bottom-6 right-6 z-50 flex flex-col items-end"}>
      {/* Floating Chat Trigger Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="flex items-center gap-2.5 px-4 py-3 rounded-full bg-gradient-to-r from-[#22D3EE] to-[#8B5CF6] text-slate-950 font-bold text-sm shadow-xl shadow-[#22D3EE]/25 hover:scale-105 hover:shadow-2xl hover:shadow-[#22D3EE]/40 transition-all cursor-pointer group"
          title="Ask AI Tutor"
        >
          <div className="h-7 w-7 rounded-full bg-slate-950/20 flex items-center justify-center">
            <Sparkles className="h-4 w-4 text-slate-950 stroke-[2.5]" />
          </div>
          <span className="tracking-wide">AI Tutor & Multi-Subject Solver</span>
          <span className="flex h-2.5 w-2.5 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
          </span>
        </button>
      )}

      {/* Floating Chat Modal Panel */}
      {isOpen && (
        <div className={isMaximized ? "w-full h-full max-w-6xl bg-[#101827] border border-[#22D3EE]/40 rounded-2xl shadow-2xl flex flex-col overflow-hidden transition-all duration-300" : "w-[380px] sm:w-[460px] h-[600px] max-h-[85vh] bg-[#101827] border border-[#22D3EE]/30 rounded-2xl shadow-2xl flex flex-col overflow-hidden animate-in fade-in slide-in-from-bottom-5 duration-200"}>
          {/* Header */}
          <div className="p-4 bg-[#162235] border-b border-slate-800 flex items-center justify-between select-none">
            <div className="flex items-center gap-2.5">
              <div className="h-8 w-8 rounded-xl bg-gradient-to-tr from-[#22D3EE] to-[#8B5CF6] flex items-center justify-center text-slate-950 font-bold shadow-md shadow-[#22D3EE]/20">
                <Sparkles className="h-4 w-4" />
              </div>
              <div>
                <h3 className="text-base font-bold text-[#F8FAFC] flex items-center gap-2">
                  LearnWise AI Tutor
                  <span className="text-[10px] font-bold px-1.5 py-0.5 rounded bg-[#22C55E]/15 text-[#22C55E] border border-[#22C55E]/30">
                    Live
                  </span>
                </h3>
                <p className="text-xs text-[#94A3B8]">Multi-Subject AI Solver • Step-by-Step • Notebook Scan</p>
              </div>
            </div>

            <div className="flex items-center gap-1.5">
              <button
                onClick={() => setIsMaximized(!isMaximized)}
                className="p-1.5 rounded-lg text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-[#1C2B42] transition-colors cursor-pointer"
                title={isMaximized ? "Restore window" : "Maximize chat to full screen"}
              >
                {isMaximized ? <Minimize2 className="h-4 w-4" /> : <Maximize2 className="h-4 w-4" />}
              </button>
              <button
                onClick={() => { setIsOpen(false); setIsMaximized(false); }}
                className="p-1.5 rounded-lg text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-[#1C2B42] transition-colors cursor-pointer"
                title="Close chat"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          </div>

          {/* Active Question Context Banner */}
          {practiceContext && (
            <div className="px-3.5 py-2 bg-[#162235]/90 border-b border-[#22D3EE]/30 flex items-center justify-between text-xs animate-in fade-in">
              <div className="flex items-center gap-2 overflow-hidden">
                <Target className="h-3.5 w-3.5 text-[#22D3EE] shrink-0" />
                <span className="text-xs text-[#94A3B8] truncate">
                  Active Practice Context: <strong className="text-[#22D3EE]">{practiceContext.topic_name || practiceContext.chapter_name || 'Practice Question'}</strong>
                </span>
              </div>
              <button
                type="button"
                onClick={() => {
                  setPracticeContext(null);
                  try { sessionStorage.removeItem('learnwise_practice_context'); } catch {}
                }}
                className="text-[10px] text-[#94A3B8] hover:text-[#F43F5E] px-2 py-0.5 rounded bg-[#101827] border border-slate-800 shrink-0 ml-2 cursor-pointer transition-colors"
                title="Clear practice question context"
              >
                Clear Context
              </button>
            </div>
          )}

          {/* Messages Area */}
          <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-[#0B1220]/60">
            {messages.map((m) => (
              <div
                key={m.id}
                className={`flex gap-2.5 ${m.sender === 'STUDENT' ? 'justify-end' : 'justify-start'}`}
              >
                {m.sender === 'AI' && (
                  <div className="h-7 w-7 rounded-lg bg-[#22D3EE]/10 border border-[#22D3EE]/30 text-[#22D3EE] flex items-center justify-center shrink-0 mt-0.5">
                    <Bot className="h-4 w-4" />
                  </div>
                )}

                <div className={`max-w-[82%] space-y-2 ${m.sender === 'STUDENT' ? 'items-end' : 'items-start'}`}>
                  {/* Uploaded Image Preview if student uploaded image */}
                  {m.image_preview && (
                    <div className="rounded-xl overflow-hidden border border-slate-700 bg-slate-900 max-w-[220px]">
                      {/* eslint-disable-next-line @next/next/no-img-element */}
                      <img src={m.image_preview} alt="Uploaded notebook step" className="w-full h-auto object-cover" />
                    </div>
                  )}

                  {/* Message Bubble */}
                  <div
                    className={`p-4 rounded-2xl text-sm sm:text-base leading-relaxed ${
                      m.sender === 'STUDENT'
                        ? 'bg-[#162235] text-[#F8FAFC] border border-slate-700/80 rounded-tr-sm'
                        : 'bg-[#101827] text-[#F8FAFC] border border-slate-800 rounded-tl-sm shadow-md'
                    }`}
                  >
                    <p className="whitespace-pre-line text-sm sm:text-base leading-relaxed font-normal">{cleanText(m.content)}</p>

                    {/* Retry button if this message was an error */}
                    {m.content.includes("temporary connection issue") && (
                      <div className="pt-2">
                        <button
                          type="button"
                          onClick={() => handleSend(lastFailedMessageRef.current || undefined)}
                          className="px-2.5 py-1 rounded bg-[#22D3EE]/15 hover:bg-[#22D3EE]/25 border border-[#22D3EE]/30 text-[#22D3EE] text-[10px] font-semibold cursor-pointer transition-colors"
                        >
                          Retry Question
                        </button>
                      </div>
                    )}

                    {/* Speech synthesis trigger for AI messages */}
                    {m.sender === 'AI' && (
                      <div className="mt-2 pt-2 border-t border-slate-800/80 flex items-center justify-between text-[10px] text-[#94A3B8]">
                        <span>{m.timestamp}</span>
                        <button
                          onClick={() => handleSpeak(m.content, m.id)}
                          className="flex items-center gap-1 text-[#22D3EE] hover:underline cursor-pointer"
                        >
                          {currentlySpeakingId === m.id ? (
                            <>
                              <VolumeX className="h-3 w-3" /> Stop Voice
                            </>
                          ) : (
                            <>
                              <Volume2 className="h-3 w-3" /> Listen
                            </>
                          )}
                        </button>
                      </div>
                    )}
                  </div>

                  {/* Multimodal Notebook Step-by-Step Analysis Card */}
                  {m.image_analysis && (
                    <div className="p-4 rounded-xl bg-[#162235] border border-[#22D3EE]/30 text-sm space-y-3 mt-1">
                      <div className="flex items-center justify-between pb-1 border-b border-slate-800">
                        <div className="flex items-center gap-2 text-[#22D3EE] font-bold text-[11px]">
                          <CheckCircle2 className="h-3.5 w-3.5" />
                          Notebook Step Diagnostic
                        </div>
                        {m.image_analysis.mistake_type && (
                          <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-[#F59E0B]/20 text-[#F59E0B] border border-[#F59E0B]/30">
                            {cleanText(m.image_analysis.mistake_type)}
                          </span>
                        )}
                      </div>

                      {m.image_analysis.problem_statement_detected && (
                        <p className="text-[11px] text-[#94A3B8]">
                          <strong className="text-[#F8FAFC]">Problem:</strong> {cleanText(m.image_analysis.problem_statement_detected)}
                        </p>
                      )}

                      {/* Steps list */}
                      {m.image_analysis.steps && m.image_analysis.steps.length > 0 && (
                        <div className="space-y-1.5 pt-1">
                          {m.image_analysis.steps.map((st) => (
                            <div
                              key={st.step_number}
                              className={`p-2 rounded-lg border text-[11px] flex items-start gap-2 ${
                                st.is_correct
                                  ? 'bg-[#22C55E]/10 border-[#22C55E]/30 text-[#F8FAFC]'
                                  : 'bg-[#F43F5E]/10 border-[#F43F5E]/30 text-[#F8FAFC]'
                              }`}
                            >
                              <span className="font-bold text-[10px] px-1 rounded bg-slate-900 shrink-0">
                                Step {st.step_number}
                              </span>
                              <div className="space-y-0.5 flex-1">
                                <p>{cleanText(st.step_content)}</p>
                                {st.comment && (
                                  <p className={`text-[10px] ${st.is_correct ? 'text-[#22C55E]' : 'text-[#F43F5E]'}`}>
                                    {cleanText(st.comment)}
                                  </p>
                                )}
                              </div>
                            </div>
                          ))}
                        </div>
                      )}

                      {/* Where, Why, How */}
                      {m.image_analysis.where_error_occurred && (
                        <div className="p-2.5 rounded-lg bg-[#101827] border border-[#F59E0B]/30 text-[11px] space-y-1">
                          <p><strong className="text-[#F59E0B]">Where:</strong> {cleanText(m.image_analysis.where_error_occurred)}</p>
                          <p><strong className="text-[#F59E0B]">Why:</strong> {cleanText(m.image_analysis.why_error_occurred)}</p>
                          <p><strong className="text-[#22D3EE]">How to Fix:</strong> {cleanText(m.image_analysis.how_to_correct)}</p>
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {m.sender === 'STUDENT' && (
                  <div className="h-7 w-7 rounded-lg bg-[#162235] border border-slate-700 text-[#22D3EE] flex items-center justify-center shrink-0 mt-0.5 text-xs font-bold">
                    <User className="h-4 w-4" />
                  </div>
                )}
              </div>
            ))}

            {sending && (
              <div className="flex gap-2.5 items-center text-xs text-[#94A3B8]">
                <div className="h-7 w-7 rounded-lg bg-[#22D3EE]/10 border border-[#22D3EE]/30 text-[#22D3EE] flex items-center justify-center shrink-0">
                  <Loader2 className="h-4 w-4 animate-spin" />
                </div>
                <div className="p-3 rounded-2xl bg-[#101827] border border-slate-800 text-[11px] text-[#22D3EE]">
                  Analyzing concept & calculation steps...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Prompts */}
          <div className="px-3 py-2 bg-[#101827] border-t border-slate-800/80 flex gap-1.5 overflow-x-auto no-scrollbar">
            {activeQuickPrompts.map((qp, i) => (
              <button
                key={i}
                type="button"
                onClick={() => handleSend(qp)}
                className="whitespace-nowrap px-3 py-1.5 rounded-full bg-[#162235] hover:bg-[#1C2B42] border border-slate-800 text-xs text-[#94A3B8] hover:text-[#22D3EE] transition-all cursor-pointer"
              >
                {qp}
              </button>
            ))}
          </div>

          {/* Selected Image Thumbnail Bar */}
          {selectedImage && (
            <div className="px-4 py-2 bg-[#162235] border-t border-slate-800 flex items-center justify-between">
              <div className="flex items-center gap-2">
                <div className="h-10 w-10 rounded-lg overflow-hidden border border-[#22D3EE]/40 bg-slate-900">
                  {/* eslint-disable-next-line @next/next/no-img-element */}
                  <img src={selectedImage} alt="Preview" className="h-full w-full object-cover" />
                </div>
                <span className="text-[11px] text-[#22D3EE] font-medium">Notebook image ready to analyze</span>
              </div>
              <button
                type="button"
                onClick={() => setSelectedImage(null)}
                className="text-[#94A3B8] hover:text-[#F43F5E] p-1 rounded transition-colors cursor-pointer"
                title="Remove image"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
          )}

          {/* Input Footer */}
          <div className="p-3 bg-[#162235] border-t border-slate-800 flex items-center gap-2">
            <input
              type="file"
              ref={fileInputRef}
              accept="image/*"
              className="hidden"
              onChange={handleImageSelect}
            />

            {/* Image upload trigger */}
            <button
              type="button"
              onClick={() => fileInputRef.current?.click()}
              className="p-2 rounded-xl bg-[#101827] border border-slate-800 hover:border-[#22D3EE]/40 text-[#94A3B8] hover:text-[#22D3EE] transition-colors cursor-pointer"
              title="Upload notebook picture"
            >
              <ImageIcon className="h-4 w-4" />
            </button>

            {/* Voice input mic */}
            <button
              type="button"
              onClick={toggleVoice}
              className={`p-2 rounded-xl border transition-colors cursor-pointer ${
                isListening
                  ? 'bg-[#F43F5E]/20 text-[#F43F5E] border-[#F43F5E]/40 animate-pulse'
                  : 'bg-[#101827] border-slate-800 text-[#94A3B8] hover:text-[#22D3EE]'
              }`}
              title={isListening ? 'Listening...' : 'Voice Input'}
            >
              {isListening ? <Mic className="h-4 w-4" /> : <MicOff className="h-4 w-4" />}
            </button>

            {/* Text input */}
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
              placeholder={
                selectedImage 
                  ? 'Add question about this step or press Send...' 
                  : practiceContext 
                  ? `Ask tutor about ${practiceContext.topic_name || 'this question'}...`
                  : 'Ask any question from any subject (Math, Physics, Chemistry, Biology, CS)...'
              }
              className="flex-1 bg-[#101827] border border-slate-800 rounded-xl px-4 py-2.5 text-sm sm:text-base text-[#F8FAFC] placeholder:text-slate-500 focus:outline-none focus:border-[#22D3EE]"
            />

            {/* Send Button */}
            <button
              type="button"
              onClick={() => handleSend()}
              disabled={(!input.trim() && !selectedImage) || sending}
              className="p-2 rounded-xl bg-[#22D3EE] hover:bg-[#22D3EE]/90 disabled:opacity-40 text-slate-950 font-bold transition-all cursor-pointer shadow-md shadow-[#22D3EE]/20 flex items-center justify-center min-w-[36px]"
              title="Send message"
            >
              {sending ? (
                <Loader2 className="h-4 w-4 animate-spin text-slate-950" />
              ) : (
                <Send className="h-4 w-4" />
              )}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

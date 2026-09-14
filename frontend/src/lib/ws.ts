'use client';

import { useEffect, useRef } from 'react';

export function useTeacherWebSocket(teacherId: number | undefined, onEvent: (event: any) => void) {
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (!teacherId) return;

    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || `ws://localhost:8000/api/ws/teacher/${teacherId}`;
    let ws: WebSocket;

    try {
      ws = new WebSocket(wsUrl);
      wsRef.current = ws;

      ws.onopen = () => {
        // Send heartbeat ping every 25 seconds
        const pingInterval = setInterval(() => {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send('ping');
          }
        }, 25000);
        (ws as any).pingInterval = pingInterval;
      };

      ws.onmessage = (event) => {
        try {
          if (event.data === 'pong') return;
          const parsed = JSON.parse(event.data);
          onEvent(parsed);
        } catch {
          // Ignore non-json
        }
      };

      ws.onerror = () => {
        // Silently handle WS error
      };

      ws.onclose = () => {
        if ((ws as any).pingInterval) {
          clearInterval((ws as any).pingInterval);
        }
      };
    } catch {
      // WS fallback
    }

    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, [teacherId, onEvent]);
}

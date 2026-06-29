import { useCallback, useEffect, useRef, useState } from 'react';

export function useWebSocket(roomId, token, onMessage) {
  const ws = useRef(null);
  const [connected, setConnected] = useState(false);

  useEffect(() => {
    if (!roomId || !token) return;
    const wsUrl = process.env.REACT_APP_WS_URL || 'ws://localhost:8000';
    ws.current = new WebSocket(`${wsUrl}/ws/${roomId}?token=${token}`);

    ws.current.onopen = () => setConnected(true);
    ws.current.onclose = () => setConnected(false);
    ws.current.onmessage = (e) => {
      try { onMessage(JSON.parse(e.data)); } catch (_e) { /* ignore malformed frames */ }
    };

    return () => {
      ws.current?.close();
    };
  }, [roomId, token]); // onMessage intentionally excluded — callers pass inline functions

  const send = useCallback((payload) => {
    if (ws.current?.readyState === WebSocket.OPEN) {
      ws.current.send(JSON.stringify(payload));
    }
  }, []);

  const sendMessage = useCallback((content) => send({ type: 'message', content }), [send]);
  const sendTyping = useCallback(() => send({ type: 'typing' }), [send]);
  const sendStopTyping = useCallback(() => send({ type: 'stop_typing' }), [send]);

  return { connected, sendMessage, sendTyping, sendStopTyping };
}

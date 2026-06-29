import React, { useCallback, useEffect, useRef, useState } from 'react';
import { deleteRoom, getMessages, getRoomMembers, leaveRoom, searchMessages } from '../services/api';
import UserList from './UserList';
import { useWebSocket } from '../hooks/useWebSocket';

function Chat({ user, room, onLeave }) {
  const [messages, setMessages] = useState([]);
  const [members, setMembers] = useState([]);
  const [input, setInput] = useState('');
  const [search, setSearch] = useState('');
  const [searchResults, setSearchResults] = useState(null);
  const [typing, setTyping] = useState([]);
  const [error, setError] = useState('');
  const bottomRef = useRef(null);
  const typingTimer = useRef(null);

  const handleWsMessage = useCallback((event) => {
    if (event.type === 'message') {
      setMessages((prev) => [...prev, event]);
    } else if (event.type === 'join' || event.type === 'leave') {
      getRoomMembers(room.id).then((r) => setMembers(r.data)).catch(() => {});
    } else if (event.type === 'typing') {
      setTyping((prev) => prev.includes(event.username) ? prev : [...prev, event.username]);
    } else if (event.type === 'stop_typing') {
      setTyping((prev) => prev.filter((u) => u !== event.username));
    }
  }, [room.id]);

  const { sendMessage, sendTyping, sendStopTyping } = useWebSocket(room.id, user.token, handleWsMessage);

  useEffect(() => {
    getMessages(room.id)
      .then((r) => setMessages(r.data.map((m) => ({ ...m, type: 'message' }))))
      .catch(() => setError('Failed to load messages'));
    getRoomMembers(room.id)
      .then((r) => setMembers(r.data))
      .catch(() => {});
  }, [room.id]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    sendMessage(input.trim());
    setInput('');
    sendStopTyping();
  };

  const handleInputChange = (e) => {
    setInput(e.target.value);
    sendTyping();
    clearTimeout(typingTimer.current);
    typingTimer.current = setTimeout(() => sendStopTyping(), 2000);
  };

  const handleLeave = async () => {
    try {
      await leaveRoom(room.id);
      onLeave();
    } catch {
      setError('Failed to leave room');
    }
  };

  const handleDelete = async () => {
    if (!window.confirm(`Delete room "${room.name}"?`)) return;
    try {
      await deleteRoom(room.id);
      onLeave();
    } catch {
      setError('Failed to delete room');
    }
  };

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!search.trim()) { setSearchResults(null); return; }
    try {
      const resp = await searchMessages(room.id, search.trim());
      setSearchResults(resp.data.messages);
    } catch {
      setError('Search failed');
    }
  };

  const displayMessages = searchResults !== null ? searchResults : messages;

  const formatTime = (ts) => {
    const d = new Date(ts);
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="chat-layout">
      <aside className="sidebar">
        <div className="room-header">
          <h2>{room.name}</h2>
          <button className="btn-leave" onClick={handleLeave}>Leave</button>
          <button className="btn-delete" onClick={handleDelete}>Delete</button>
        </div>
        <UserList members={members} />
      </aside>

      <main className="chat-main">
        {error && <p className="error-msg">{error}</p>}

        <form className="search-form" onSubmit={handleSearch}>
          <input
            placeholder="Search messages…"
            value={search}
            onChange={(e) => { setSearch(e.target.value); if (!e.target.value) setSearchResults(null); }}
          />
          <button type="submit">Search</button>
          {searchResults !== null && (
            <button type="button" onClick={() => { setSearch(''); setSearchResults(null); }}>
              Clear
            </button>
          )}
        </form>

        <div className="messages">
          {displayMessages.map((m) => (
            <div key={m.id} className={`message ${m.username === user.username ? 'mine' : 'theirs'}`}>
              <span className="msg-username">{m.username}</span>
              <span className="msg-content">{m.content}</span>
              <span className="msg-time">{formatTime(m.timestamp)}</span>
            </div>
          ))}
          <div ref={bottomRef} />
        </div>

        {typing.filter((u) => u !== user.username).length > 0 && (
          <p className="typing-indicator">
            {typing.filter((u) => u !== user.username).join(', ')} is typing…
          </p>
        )}

        <form className="message-form" onSubmit={handleSend}>
          <input
            placeholder="Type a message…"
            value={input}
            onChange={handleInputChange}
          />
          <button type="submit">Send</button>
        </form>
      </main>
    </div>
  );
}

export default Chat;

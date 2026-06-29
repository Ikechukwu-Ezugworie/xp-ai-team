import React, { useEffect, useState } from 'react';
import Chat from './components/Chat';
import Login from './components/Login';
import RoomList from './components/RoomList';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [room, setRoom] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const username = localStorage.getItem('username');
    if (token && username) setUser({ token, username });
  }, []);

  const handleLogin = (userData) => setUser(userData);

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    setUser(null);
    setRoom(null);
  };

  if (!user) return <Login onLogin={handleLogin} />;
  if (!room) {
    return (
      <div className="app">
        <header className="app-header">
          <span>Welcome, {user.username}</span>
          <button onClick={handleLogout}>Logout</button>
        </header>
        <RoomList onJoin={setRoom} />
      </div>
    );
  }

  return (
    <div className="app">
      <Chat user={user} room={room} onLeave={() => setRoom(null)} />
    </div>
  );
}

export default App;

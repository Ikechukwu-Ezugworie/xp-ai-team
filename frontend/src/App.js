import React, { useState } from 'react';
import Login from './components/Login';
import Chat from './components/Chat';

function App() {
  const [user, setUser] = useState(null);
  return (
    <div className="App">
      {!user ? <Login onLogin={setUser} /> : <Chat user={user} />}
    </div>
  );
}
export default App;
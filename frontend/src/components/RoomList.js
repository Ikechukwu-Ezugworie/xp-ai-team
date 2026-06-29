import React, { useEffect, useState } from 'react';
import { createRoom, getRooms, joinRoom } from '../services/api';

function RoomList({ onJoin }) {
  const [rooms, setRooms] = useState([]);
  const [newRoomName, setNewRoomName] = useState('');
  const [error, setError] = useState('');

  const load = async () => {
    try {
      const resp = await getRooms();
      setRooms(resp.data);
    } catch {
      setError('Failed to load rooms');
    }
  };

  useEffect(() => { load(); }, []);

  const handleCreate = async (e) => {
    e.preventDefault();
    if (!newRoomName.trim()) return;
    try {
      const resp = await createRoom(newRoomName.trim());
      setNewRoomName('');
      onJoin(resp.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create room');
    }
  };

  const handleJoin = async (room) => {
    try {
      await joinRoom(room.id);
      onJoin(room);
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to join room');
    }
  };

  return (
    <div className="room-list">
      <h2>Chat Rooms</h2>
      {error && <p className="error-msg">{error}</p>}
      <form className="create-room-form" onSubmit={handleCreate}>
        <input
          placeholder="New room name"
          value={newRoomName}
          onChange={(e) => setNewRoomName(e.target.value)}
        />
        <button type="submit">Create</button>
      </form>
      <ul>
        {rooms.map((room) => (
          <li key={room.id} className="room-item">
            <span className="room-name">{room.name}</span>
            <span className="member-count">{room.member_count} members</span>
            <button onClick={() => handleJoin(room)}>Join</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default RoomList;

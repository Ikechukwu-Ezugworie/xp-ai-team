import axios from 'axios';

const API = axios.create({ baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000' });

API.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

export const register = (data) => API.post('/auth/register', data);
export const login = (data) => API.post('/auth/login', data);
export const logout = () => API.post('/auth/logout');

export const getRooms = () => API.get('/rooms/');
export const createRoom = (name) => API.post('/rooms/', { name });
export const joinRoom = (id) => API.post(`/rooms/${id}/join`);
export const leaveRoom = (id) => API.post(`/rooms/${id}/leave`);
export const getRoomMembers = (id) => API.get(`/rooms/${id}/members`);
export const deleteRoom = (id) => API.delete(`/rooms/${id}`);

export const getMessages = (roomId) => API.get(`/messages/${roomId}`);
export const sendMessage = (roomId, content) => API.post(`/messages/${roomId}`, { content });
export const searchMessages = (roomId, q) => API.get(`/messages/${roomId}/search`, { params: { q } });

export default API;

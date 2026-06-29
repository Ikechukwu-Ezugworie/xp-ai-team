import React, { useState } from 'react';
import { login, register } from '../services/api';

function Login({ onLogin }) {
  const [mode, setMode] = useState('login');
  const [form, setForm] = useState({ username: '', email: '', password: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      if (mode === 'register') {
        await register({ username: form.username, email: form.email, password: form.password });
        setMode('login');
        setError('Registered! Please log in.');
      } else {
        const resp = await login({ username: form.username, password: form.password });
        localStorage.setItem('token', resp.data.access_token);
        localStorage.setItem('username', resp.data.username);
        onLogin({ username: resp.data.username, token: resp.data.access_token });
      }
    } catch (err) {
      setError(err.response?.data?.detail || 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <h1>Chat App</h1>
      <div className="auth-box">
        <h2>{mode === 'login' ? 'Sign In' : 'Create Account'}</h2>
        {error && <p className="error-msg">{error}</p>}
        <form onSubmit={handleSubmit}>
          <input
            name="username" placeholder="Username" value={form.username}
            onChange={handleChange} required autoComplete="username"
          />
          {mode === 'register' && (
            <input
              name="email" type="email" placeholder="Email" value={form.email}
              onChange={handleChange} required autoComplete="email"
            />
          )}
          <input
            name="password" type="password" placeholder="Password" value={form.password}
            onChange={handleChange} required autoComplete="current-password"
          />
          <button type="submit" disabled={loading}>
            {loading ? 'Loading…' : mode === 'login' ? 'Sign In' : 'Register'}
          </button>
        </form>
        <button className="link-btn" onClick={() => setMode(mode === 'login' ? 'register' : 'login')}>
          {mode === 'login' ? 'Need an account? Register' : 'Have an account? Sign In'}
        </button>
      </div>
    </div>
  );
}

export default Login;

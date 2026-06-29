import React from 'react';
import { render, screen } from '@testing-library/react';
import App from '../App';

jest.mock('../services/api', () => ({
  getRooms: jest.fn().mockResolvedValue({ data: [] }),
  login: jest.fn(),
  register: jest.fn(),
  logout: jest.fn(),
}));

test('renders login page when no token is stored', () => {
  localStorage.clear();
  render(<App />);
  expect(screen.getByText('Chat App')).toBeInTheDocument();
  expect(screen.getByText('Sign In')).toBeInTheDocument();
});

test('placeholder', () => {
  expect(true).toBe(true);
});

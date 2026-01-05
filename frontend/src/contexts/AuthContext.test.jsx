/**
 * Comprehensive tests for AuthContext
 * Tests authentication state management, login, logout, and hooks
 */
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import { renderHook, act } from '@testing-library/react';
import { AuthProvider, useAuth } from './AuthContext';
import * as api from '../services/api';

// Mock the API module
vi.mock('../services/api', () => ({
  getApiKey: vi.fn(),
  setApiKey: vi.fn(),
  clearApiKey: vi.fn(),
}));

describe('AuthContext', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  describe('useAuth Hook', () => {
    it('should throw error when used outside AuthProvider', () => {
      // Suppress console.error for this test
      const originalError = console.error;
      console.error = vi.fn();

      expect(() => {
        renderHook(() => useAuth());
      }).toThrow('useAuth must be used within an AuthProvider');

      console.error = originalError;
    });

    it('should return context when used within AuthProvider', () => {
      const { result } = renderHook(() => useAuth(), {
        wrapper: AuthProvider,
      });

      expect(result.current).toHaveProperty('isAuthenticated');
      expect(result.current).toHaveProperty('isLoading');
      expect(result.current).toHaveProperty('login');
      expect(result.current).toHaveProperty('logout');
    });
  });

  describe('AuthProvider', () => {
    it('should render children', () => {
      render(
        <AuthProvider>
          <div>Test Child</div>
        </AuthProvider>
      );

      expect(screen.getByText('Test Child')).toBeInTheDocument();
    });

    it('should set isAuthenticated to false when no API key exists', async () => {
      api.getApiKey.mockReturnValue(null);

      const { result } = renderHook(() => useAuth(), {
        wrapper: AuthProvider,
      });

      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });

      expect(result.current.isAuthenticated).toBe(false);
    });

    it('should set isAuthenticated to true when API key exists', async () => {
      api.getApiKey.mockReturnValue('existing-key-123');

      const { result } = renderHook(() => useAuth(), {
        wrapper: AuthProvider,
      });

      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });

      expect(result.current.isAuthenticated).toBe(true);
    });
  });

  describe('login Function', () => {
    it('should save API key and set authenticated to true', async () => {
      api.getApiKey.mockReturnValue(null);

      const { result } = renderHook(() => useAuth(), {
        wrapper: AuthProvider,
      });

      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });

      act(() => {
        result.current.login('new-api-key-123');
      });

      expect(api.setApiKey).toHaveBeenCalledWith('new-api-key-123');
      expect(result.current.isAuthenticated).toBe(true);
    });

    it('should handle multiple login calls', async () => {
      api.getApiKey.mockReturnValue(null);

      const { result } = renderHook(() => useAuth(), {
        wrapper: AuthProvider,
      });

      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });

      act(() => {
        result.current.login('key1');
      });

      expect(api.setApiKey).toHaveBeenCalledWith('key1');

      act(() => {
        result.current.login('key2');
      });

      expect(api.setApiKey).toHaveBeenCalledWith('key2');
      expect(result.current.isAuthenticated).toBe(true);
    });
  });

  describe('logout Function', () => {
    it('should clear API key and set authenticated to false', async () => {
      api.getApiKey.mockReturnValue('existing-key');

      const { result } = renderHook(() => useAuth(), {
        wrapper: AuthProvider,
      });

      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });

      expect(result.current.isAuthenticated).toBe(true);

      act(() => {
        result.current.logout();
      });

      expect(api.clearApiKey).toHaveBeenCalled();
      expect(result.current.isAuthenticated).toBe(false);
    });

    it('should work when already logged out', async () => {
      api.getApiKey.mockReturnValue(null);

      const { result } = renderHook(() => useAuth(), {
        wrapper: AuthProvider,
      });

      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });

      act(() => {
        result.current.logout();
      });

      expect(api.clearApiKey).toHaveBeenCalled();
      expect(result.current.isAuthenticated).toBe(false);
    });
  });

  describe('Login/Logout Flow', () => {
    it('should handle complete login-logout flow', async () => {
      api.getApiKey.mockReturnValue(null);

      const { result } = renderHook(() => useAuth(), {
        wrapper: AuthProvider,
      });

      await waitFor(() => {
        expect(result.current.isLoading).toBe(false);
      });

      // Start logged out
      expect(result.current.isAuthenticated).toBe(false);

      // Login
      act(() => {
        result.current.login('test-key');
      });

      expect(result.current.isAuthenticated).toBe(true);

      // Logout
      act(() => {
        result.current.logout();
      });

      expect(result.current.isAuthenticated).toBe(false);
    });
  });
});

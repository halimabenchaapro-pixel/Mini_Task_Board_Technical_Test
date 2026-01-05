/**
 * Comprehensive tests for API service
 * Tests API key management and helper functions
 */
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { setApiKey, getApiKey, clearApiKey } from './api';

describe('API Service', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    localStorage.clear();
  });

  describe('API Key Management', () => {
    it('should set API key in localStorage', () => {
      setApiKey('test-key-123');
      expect(localStorage.setItem).toHaveBeenCalledWith('apiKey', 'test-key-123');
    });

    it('should get API key from localStorage', () => {
      localStorage.getItem.mockReturnValue('stored-key');
      const key = getApiKey();
      expect(localStorage.getItem).toHaveBeenCalledWith('apiKey');
      expect(key).toBe('stored-key');
    });

    it('should clear API key from localStorage', () => {
      clearApiKey();
      expect(localStorage.removeItem).toHaveBeenCalledWith('apiKey');
    });

    it('should return null when no key is stored', () => {
      localStorage.getItem.mockReturnValue(null);
      const key = getApiKey();
      expect(key).toBeNull();
    });

    it('should handle multiple set/get/clear cycles', () => {
      setApiKey('key1');
      expect(localStorage.setItem).toHaveBeenCalledWith('apiKey', 'key1');

      setApiKey('key2');
      expect(localStorage.setItem).toHaveBeenCalledWith('apiKey', 'key2');

      clearApiKey();
      expect(localStorage.removeItem).toHaveBeenCalledWith('apiKey');
    });
  });
});

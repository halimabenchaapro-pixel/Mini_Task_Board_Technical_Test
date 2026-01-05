/**
 * Comprehensive tests for Button component
 * Tests all props, variants, sizes, and interactions
 */
import { describe, it, expect, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Button from './Button';

describe('Button Component', () => {
  describe('Rendering', () => {
    it('should render with children text', () => {
      render(<Button>Click Me</Button>);
      expect(screen.getByText('Click Me')).toBeInTheDocument();
    });

    it('should render with complex children', () => {
      render(
        <Button>
          <span>Icon</span> Click Me
        </Button>
      );
      expect(screen.getByText('Icon')).toBeInTheDocument();
      expect(screen.getByText('Click Me')).toBeInTheDocument();
    });

    it('should render as button element by default', () => {
      render(<Button>Test</Button>);
      expect(screen.getByRole('button')).toBeInTheDocument();
    });
  });

  describe('Click Handling', () => {
    it('should call onClick when clicked', async () => {
      const handleClick = vi.fn();
      const user = userEvent.setup();

      render(<Button onClick={handleClick}>Click Me</Button>);

      await user.click(screen.getByRole('button'));

      expect(handleClick).toHaveBeenCalledTimes(1);
    });

    it('should not call onClick when disabled', async () => {
      const handleClick = vi.fn();
      const user = userEvent.setup();

      render(
        <Button onClick={handleClick} disabled>
          Click Me
        </Button>
      );

      await user.click(screen.getByRole('button'));

      expect(handleClick).not.toHaveBeenCalled();
    });

    it('should call onClick multiple times', async () => {
      const handleClick = vi.fn();
      const user = userEvent.setup();

      render(<Button onClick={handleClick}>Click Me</Button>);

      const button = screen.getByRole('button');
      await user.click(button);
      await user.click(button);
      await user.click(button);

      expect(handleClick).toHaveBeenCalledTimes(3);
    });
  });

  describe('Variants', () => {
    it('should apply primary variant by default', () => {
      render(<Button>Primary</Button>);
      const button = screen.getByRole('button');
      expect(button.className).toContain('bg-blue-600');
    });

    it('should apply secondary variant styles', () => {
      render(<Button variant="secondary">Secondary</Button>);
      const button = screen.getByRole('button');
      expect(button.className).toContain('bg-gray-200');
    });

    it('should apply danger variant styles', () => {
      render(<Button variant="danger">Danger</Button>);
      const button = screen.getByRole('button');
      expect(button.className).toContain('bg-red-600');
    });

    it('should apply success variant styles', () => {
      render(<Button variant="success">Success</Button>);
      const button = screen.getByRole('button');
      expect(button.className).toContain('bg-green-600');
    });
  });

  describe('Sizes', () => {
    it('should apply medium size by default', () => {
      render(<Button>Medium</Button>);
      const button = screen.getByRole('button');
      expect(button.className).toContain('px-4 py-2');
    });

    it('should apply small size styles', () => {
      render(<Button size="sm">Small</Button>);
      const button = screen.getByRole('button');
      expect(button.className).toContain('px-3 py-1.5 text-sm');
    });

    it('should apply large size styles', () => {
      render(<Button size="lg">Large</Button>);
      const button = screen.getByRole('button');
      expect(button.className).toContain('px-6 py-3 text-lg');
    });
  });

  describe('Type Attribute', () => {
    it('should have button type by default', () => {
      render(<Button>Test</Button>);
      expect(screen.getByRole('button')).toHaveAttribute('type', 'button');
    });

    it('should accept submit type', () => {
      render(<Button type="submit">Submit</Button>);
      expect(screen.getByRole('button')).toHaveAttribute('type', 'submit');
    });

    it('should accept reset type', () => {
      render(<Button type="reset">Reset</Button>);
      expect(screen.getByRole('button')).toHaveAttribute('type', 'reset');
    });
  });

  describe('Disabled State', () => {
    it('should not be disabled by default', () => {
      render(<Button>Test</Button>);
      expect(screen.getByRole('button')).not.toBeDisabled();
    });

    it('should be disabled when disabled prop is true', () => {
      render(<Button disabled>Test</Button>);
      expect(screen.getByRole('button')).toBeDisabled();
    });

    it('should apply disabled styles', () => {
      render(<Button disabled variant="primary">Test</Button>);
      const button = screen.getByRole('button');
      expect(button.className).toContain('disabled:bg-blue-300');
    });
  });

  describe('Custom ClassName', () => {
    it('should apply custom className', () => {
      render(<Button className="custom-class">Test</Button>);
      const button = screen.getByRole('button');
      expect(button.className).toContain('custom-class');
    });

    it('should merge custom className with default styles', () => {
      render(<Button className="mt-4">Test</Button>);
      const button = screen.getByRole('button');
      expect(button.className).toContain('mt-4');
      expect(button.className).toContain('font-medium');
      expect(button.className).toContain('rounded-lg');
    });
  });

  describe('Base Styles', () => {
    it('should always have base styles', () => {
      render(<Button>Test</Button>);
      const button = screen.getByRole('button');
      expect(button.className).toContain('font-medium');
      expect(button.className).toContain('rounded-lg');
      expect(button.className).toContain('transition');
    });
  });

  describe('Combined Props', () => {
    it('should handle all props together', async () => {
      const handleClick = vi.fn();
      const user = userEvent.setup();

      render(
        <Button
          variant="success"
          size="lg"
          type="submit"
          className="extra-class"
          onClick={handleClick}
        >
          Submit Form
        </Button>
      );

      const button = screen.getByRole('button');

      expect(button).toHaveAttribute('type', 'submit');
      expect(button.className).toContain('bg-green-600');
      expect(button.className).toContain('px-6 py-3 text-lg');
      expect(button.className).toContain('extra-class');

      await user.click(button);
      expect(handleClick).toHaveBeenCalled();
    });
  });
});

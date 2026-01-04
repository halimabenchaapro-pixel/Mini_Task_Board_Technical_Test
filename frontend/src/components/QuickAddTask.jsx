import { useState } from 'react';
import Button from './Button';

const QuickAddTask = ({ status, onAdd, onCancel }) => {
  const [title, setTitle] = useState('');
  const [isExpanded, setIsExpanded] = useState(false);
  const [priority, setPriority] = useState('MEDIUM');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!title.trim()) return;

    onAdd({
      title: title.trim(),
      status,
      priority,
    });

    setTitle('');
    setPriority('MEDIUM');
    setIsExpanded(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Escape') {
      setTitle('');
      setIsExpanded(false);
      onCancel?.();
    }
  };

  if (!isExpanded) {
    return (
      <button
        onClick={() => setIsExpanded(true)}
        className="w-full p-3 text-left text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg border-2 border-dashed border-gray-300 dark:border-gray-600 transition-all hover:border-blue-500 dark:hover:border-blue-400 group"
      >
        <div className="flex items-center gap-2">
          <svg
            className="w-5 h-5 text-gray-400 group-hover:text-blue-500 transition-colors"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 4v16m8-8H4"
            />
          </svg>
          <span className="text-sm font-medium">Quick add task</span>
        </div>
      </button>
    );
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white dark:bg-gray-700 rounded-lg p-3 shadow-sm border border-gray-200 dark:border-gray-600 animate-scale-in">
      <input
        type="text"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Task title (press Enter to add, Esc to cancel)"
        autoFocus
        className="w-full px-3 py-2 mb-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-600 dark:text-white rounded focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none text-sm transition-colors"
      />

      <div className="flex items-center gap-2 mb-2">
        <label className="text-xs text-gray-600 dark:text-gray-400">Priority:</label>
        <select
          value={priority}
          onChange={(e) => setPriority(e.target.value)}
          className="text-xs px-2 py-1 border border-gray-300 dark:border-gray-600 dark:bg-gray-600 dark:text-white rounded focus:ring-2 focus:ring-blue-500 outline-none transition-colors"
        >
          <option value="LOW">Low</option>
          <option value="MEDIUM">Medium</option>
          <option value="HIGH">High</option>
        </select>
      </div>

      <div className="flex gap-2">
        <Button type="submit" variant="primary" size="sm" className="flex-1" disabled={!title.trim()}>
          Add Task
        </Button>
        <Button
          type="button"
          variant="secondary"
          size="sm"
          onClick={() => {
            setTitle('');
            setIsExpanded(false);
            onCancel?.();
          }}
        >
          Cancel
        </Button>
      </div>
    </form>
  );
};

export default QuickAddTask;

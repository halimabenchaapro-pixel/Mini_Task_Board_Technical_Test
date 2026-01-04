import { useState, useEffect, useCallback } from 'react';
import { DragDropContext, Droppable, Draggable } from '@hello-pangea/dnd';
import { taskAPI } from '../services/api';
import { useAuth } from '../contexts/AuthContext';
import TaskCard from '../components/TaskCard';
import TaskForm from '../components/TaskForm';
import DeleteConfirmation from '../components/DeleteConfirmation';
import Modal from '../components/Modal';
import Button from '../components/Button';
import ThemeToggle from '../components/ThemeToggle';
import Toast from '../components/Toast';
import QuickAddTask from '../components/QuickAddTask';

const Board = () => {
  const [tasks, setTasks] = useState([]);
  const [filteredTasks, setFilteredTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('ALL');
  const [isTaskModalOpen, setIsTaskModalOpen] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [deletingTask, setDeletingTask] = useState(null);
  const [toast, setToast] = useState(null);
  const { logout } = useAuth();

  const showToast = useCallback((message, type = 'success') => {
    setToast({ message, type });
  }, []);

  const columns = {
    BACKLOG: { title: 'Backlog', color: 'bg-gray-100 dark:bg-gray-700' },
    IN_PROGRESS: { title: 'In Progress', color: 'bg-blue-100 dark:bg-blue-900' },
    DONE: { title: 'Done', color: 'bg-green-100 dark:bg-green-900' },
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  useEffect(() => {
    filterTasks();
  }, [tasks, searchQuery, priorityFilter]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyPress = (e) => {
      // Ctrl/Cmd + K to create new task
      if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
        e.preventDefault();
        openCreateModal();
      }
    };

    window.addEventListener('keydown', handleKeyPress);
    return () => window.removeEventListener('keydown', handleKeyPress);
  }, []);

  const fetchTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await taskAPI.getAll();
      setTasks(response.data);
    } catch (err) {
      if (err.response?.status === 401 || err.response?.status === 403) {
        setError('Invalid API key. Please login again.');
        setTimeout(() => logout(), 2000);
      } else {
        setError('Failed to fetch tasks. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  const filterTasks = () => {
    let filtered = [...tasks];

    // Search filter
    if (searchQuery.trim()) {
      filtered = filtered.filter((task) =>
        task.title.toLowerCase().includes(searchQuery.toLowerCase())
      );
    }

    // Priority filter
    if (priorityFilter !== 'ALL') {
      filtered = filtered.filter((task) => task.priority === priorityFilter);
    }

    setFilteredTasks(filtered);
  };

  const handleCreateTask = async (formData) => {
    try {
      await taskAPI.create(formData);
      setIsTaskModalOpen(false);
      fetchTasks();
      showToast('Task created successfully!', 'success');
    } catch (err) {
      showToast('Failed to create task. Please try again.', 'error');
    }
  };

  const handleQuickAddTask = async (formData) => {
    try {
      await taskAPI.create(formData);
      fetchTasks();
      showToast('Task added successfully!', 'success');
    } catch (err) {
      showToast('Failed to add task. Please try again.', 'error');
    }
  };

  const handleUpdateTask = async (formData) => {
    try {
      await taskAPI.update(editingTask.id, formData);
      setIsTaskModalOpen(false);
      setEditingTask(null);
      fetchTasks();
      showToast('Task updated successfully!', 'success');
    } catch (err) {
      showToast('Failed to update task. Please try again.', 'error');
    }
  };

  const handleDeleteTask = async () => {
    try {
      await taskAPI.delete(deletingTask.id);
      setDeletingTask(null);
      fetchTasks();
      showToast('Task deleted successfully!', 'success');
    } catch (err) {
      showToast('Failed to delete task. Please try again.', 'error');
    }
  };

  const handleQuickStatusChange = async (task, newStatus) => {
    const previousStatus = task.status;

    // Optimistic update
    setTasks((prevTasks) =>
      prevTasks.map((t) =>
        t.id === task.id ? { ...t, status: newStatus } : t
      )
    );

    try {
      await taskAPI.update(task.id, { status: newStatus });
      showToast(`Task moved to ${newStatus.replace('_', ' ')}!`, 'success');
    } catch (err) {
      // Revert on error
      setTasks((prevTasks) =>
        prevTasks.map((t) =>
          t.id === task.id ? { ...t, status: previousStatus } : t
        )
      );
      showToast('Failed to update task status. Please try again.', 'error');
    }
  };

  const handleDragEnd = async (result) => {
    if (!result.destination) return;

    const { source, destination, draggableId } = result;

    // If dropped in the same position
    if (source.droppableId === destination.droppableId && source.index === destination.index) {
      return;
    }

    const taskId = parseInt(draggableId);
    const newStatus = destination.droppableId;

    // Optimistic update
    setTasks((prevTasks) =>
      prevTasks.map((task) =>
        task.id === taskId ? { ...task, status: newStatus } : task
      )
    );

    try {
      await taskAPI.update(taskId, { status: newStatus });
      showToast('Task moved successfully!', 'success');
    } catch (err) {
      // Revert on error
      fetchTasks();
      showToast('Failed to move task. Please try again.', 'error');
    }
  };

  const openEditModal = (task) => {
    setEditingTask(task);
    setIsTaskModalOpen(true);
  };

  const openCreateModal = () => {
    setEditingTask(null);
    setIsTaskModalOpen(true);
  };

  const closeTaskModal = () => {
    setIsTaskModalOpen(false);
    setEditingTask(null);
  };

  const getTasksByStatus = (status) => {
    return filteredTasks.filter((task) => task.status === status);
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading tasks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-sm transition-colors duration-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white">Task Board</h1>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                Press <kbd className="px-2 py-0.5 bg-gray-200 dark:bg-gray-700 rounded text-xs">Ctrl+K</kbd> to quick add task
              </p>
            </div>
            <div className="flex gap-2">
              <ThemeToggle />
              <Button onClick={openCreateModal} variant="primary">
                + New Task
              </Button>
              <Button onClick={logout} variant="secondary">
                Logout
              </Button>
            </div>
          </div>

          {/* Filters */}
          <div className="mt-4 flex flex-col sm:flex-row gap-3">
            <input
              type="text"
              placeholder="Search tasks..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-colors duration-200"
            />
            <select
              value={priorityFilter}
              onChange={(e) => setPriorityFilter(e.target.value)}
              className="px-4 py-2 border border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-colors duration-200"
            >
              <option value="ALL">All Priorities</option>
              <option value="LOW">Low</option>
              <option value="MEDIUM">Medium</option>
              <option value="HIGH">High</option>
            </select>
          </div>
        </div>
      </header>

      {/* Error Message */}
      {error && (
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
            {error}
          </div>
        </div>
      )}

      {/* Board */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <DragDropContext onDragEnd={handleDragEnd}>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {Object.entries(columns).map(([status, { title, color }]) => (
              <div key={status} className="flex flex-col">
                <div className={`${color} rounded-t-lg px-4 py-3 transition-colors duration-200`}>
                  <h2 className="font-semibold text-gray-800 dark:text-gray-200">
                    {title}{' '}
                    <span className="text-sm font-normal text-gray-600 dark:text-gray-400">
                      ({getTasksByStatus(status).length})
                    </span>
                  </h2>
                </div>

                <Droppable droppableId={status}>
                  {(provided, snapshot) => (
                    <div
                      ref={provided.innerRef}
                      {...provided.droppableProps}
                      className={`flex-1 bg-gray-100 dark:bg-gray-800 rounded-b-lg p-4 min-h-[400px] transition-all duration-200 ${
                        snapshot.isDraggingOver ? 'bg-blue-50 dark:bg-blue-900' : ''
                      }`}
                    >
                      {/* Quick Add Task */}
                      <QuickAddTask
                        status={status}
                        onAdd={handleQuickAddTask}
                      />

                      {/* Task List */}
                      {getTasksByStatus(status).length === 0 ? (
                        <div className="text-center py-8 text-gray-500 dark:text-gray-400 mt-3">
                          <svg
                            className="mx-auto h-12 w-12 text-gray-400 dark:text-gray-600"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke="currentColor"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M9 13h6m-3-3v6m5 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                            />
                          </svg>
                          <p className="mt-2 text-sm">No tasks here yet...</p>
                          <p className="text-xs mt-1 text-gray-400">Use the quick add button above</p>
                        </div>
                      ) : (
                        <div className="mt-3 space-y-3">
                          {getTasksByStatus(status).map((task, index) => (
                            <Draggable
                              key={task.id}
                              draggableId={task.id.toString()}
                              index={index}
                            >
                              {(provided, snapshot) => (
                                <TaskCard
                                  task={task}
                                  onEdit={openEditModal}
                                  onDelete={setDeletingTask}
                                  onStatusChange={handleQuickStatusChange}
                                  provided={provided}
                                  snapshot={snapshot}
                                />
                              )}
                            </Draggable>
                          ))}
                        </div>
                      )}
                      {provided.placeholder}
                    </div>
                  )}
                </Droppable>
              </div>
            ))}
          </div>
        </DragDropContext>
      </main>

      {/* Task Modal */}
      <Modal
        isOpen={isTaskModalOpen}
        onClose={closeTaskModal}
        title={editingTask ? 'Edit Task' : 'Create New Task'}
      >
        <TaskForm
          task={editingTask}
          onSubmit={editingTask ? handleUpdateTask : handleCreateTask}
          onCancel={closeTaskModal}
        />
      </Modal>

      {/* Delete Confirmation */}
      <DeleteConfirmation
        isOpen={!!deletingTask}
        onClose={() => setDeletingTask(null)}
        onConfirm={handleDeleteTask}
        taskTitle={deletingTask?.title || ''}
      />

      {/* Toast Notifications */}
      {toast && (
        <Toast
          message={toast.message}
          type={toast.type}
          onClose={() => setToast(null)}
        />
      )}
    </div>
  );
};

export default Board;

const TaskCard = ({ task, onEdit, onDelete, provided, snapshot }) => {
  const priorityColors = {
    LOW: 'bg-green-100 text-green-800 border-green-200',
    MEDIUM: 'bg-yellow-100 text-yellow-800 border-yellow-200',
    HIGH: 'bg-red-100 text-red-800 border-red-200',
  };

  const formatDate = (dateString) => {
    if (!dateString) return null;
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  const priorityColor = priorityColors[task.priority] || priorityColors.MEDIUM;

  return (
    <div
      ref={provided?.innerRef}
      {...provided?.draggableProps}
      {...provided?.dragHandleProps}
      className={`bg-white rounded-lg shadow-sm border border-gray-200 p-4 mb-3 hover:shadow-md transition-shadow ${
        snapshot?.isDragging ? 'shadow-lg rotate-2' : ''
      }`}
    >
      {/* Priority Badge */}
      <div className="flex items-center justify-between mb-2">
        <span
          className={`px-2 py-1 rounded-md text-xs font-medium border ${priorityColor}`}
        >
          {task.priority}
        </span>
      </div>

      {/* Title */}
      <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">{task.title}</h3>

      {/* Description */}
      {task.description && (
        <p className="text-sm text-gray-600 mb-3 line-clamp-2">{task.description}</p>
      )}

      {/* Due Date */}
      {task.due_date && (
        <div className="flex items-center text-xs text-gray-500 mb-3">
          <svg className="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"
            />
          </svg>
          {formatDate(task.due_date)}
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-2 pt-2 border-t border-gray-100">
        <button
          onClick={() => onEdit(task)}
          className="flex-1 px-3 py-1.5 text-sm text-blue-600 hover:bg-blue-50 rounded-md transition"
        >
          Edit
        </button>
        <button
          onClick={() => onDelete(task)}
          className="flex-1 px-3 py-1.5 text-sm text-red-600 hover:bg-red-50 rounded-md transition"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TaskCard;

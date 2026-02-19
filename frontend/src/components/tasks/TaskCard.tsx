'use client';

import React from 'react';
import { Task } from '../../types';
import { useRouter } from 'next/dist/client/components/navigation';
import { format } from 'date-fns';

interface TaskCardProps {
  task: Task;
  onToggle?: (id: string, completed: boolean) => void;
  // onEdit?: (task: Task) => void;
  onDelete?: (id: string) => void;
}

const getPriorityColor = (priority?: string) => {
  switch (priority) {
    case 'Critical':
      return 'bg-red-100 text-red-800';
    case 'High':
      return 'bg-orange-100 text-orange-800';
    case 'Medium':
      return 'bg-yellow-100 text-yellow-800';
    case 'Low':
      return 'bg-green-100 text-green-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

const TaskCard: React.FC<TaskCardProps> = ({ task, onToggle, onDelete }) => {
  const handleToggle = () => {
    onToggle?.(task.id, !task.completed);
  };

  const router = useRouter();
  const handleEdit = () => {
    router.push(`/tasks/${task.id}/edit`);
  };

  const handleDelete = () => {
    onDelete?.(task.id);
  };

  // Check if task is overdue
  const isOverdue = task.dueDate && new Date(task.dueDate) < new Date() && !task.completed;

  return (
    <div className={`border rounded-lg shadow-md p-4 ${task.completed ? 'bg-green-50' : 'bg-white'} ${isOverdue ? 'border-red-300' : 'border-gray-200'}`}>
      <div className="flex justify-between items-start">
        <div className="flex-1">
          <div className="flex items-center gap-2 mb-2">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggle}
              className="h-5 w-5 text-blue-600 rounded focus:ring-blue-500 mt-1"
            />
            <h3 className={`font-bold text-lg ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
              {task.title}
            </h3>
            {task.priority && (
              <span className={`px-2 py-1 text-xs rounded-full ${getPriorityColor(task.priority)}`}>
                {task.priority}
              </span>
            )}
            {isOverdue && (
              <span className="px-2 py-1 text-xs rounded-full bg-red-100 text-red-800">
                Overdue
              </span>
            )}
          </div>

          {task.description && (
            <p className={`text-gray-600 mb-3 ${task.completed ? 'line-through' : ''}`}>
              {task.description}
            </p>
          )}

          <div className="flex flex-wrap gap-2 text-xs text-gray-500 mb-3">
            {task.dueDate && (
              <span>
                Due: {format(new Date(task.dueDate), 'MMM dd, yyyy HH:mm')}
              </span>
            )}
            {task.reminderTime && (
              <span>
                Remind: {format(new Date(task.reminderTime), 'MMM dd, yyyy HH:mm')}
              </span>
            )}
            {task.recurrenceType && (
              <span className="capitalize">
                Recurs: {task.recurrenceType}
              </span>
            )}
          </div>

          {task.tags && task.tags.length > 0 && (
            <div className="flex flex-wrap gap-1 mb-3">
              {task.tags.map((tag) => (
                <span key={tag.id} className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full">
                  {tag.name}
                </span>
              ))}
            </div>
          )}
        </div>
      </div>

      <div className="flex justify-end space-x-2">
        <button
          onClick={handleEdit}
          className="px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 text-sm"
        >
          Edit
        </button>
        <button
          onClick={handleDelete}
          className="px-3 py-1 bg-red-500 text-white rounded hover:bg-red-600 text-sm"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TaskCard;
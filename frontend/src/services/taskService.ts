import { Task, TaskFormData, ApiResponse } from '../types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

interface SearchParams {
  q?: string;
  status?: string;
  priority?: string;
  tag?: string;
  dueDateRange?: string;
  sortBy?: string;
  sortOrder?: 'asc' | 'desc';
}

export const searchTasks = async (
  userId: string,
  searchParams: SearchParams = {}
): Promise<ApiResponse<Task[]>> => {
  const { q, status, priority, tag, dueDateRange, sortBy, sortOrder } = searchParams;

  const url = new URL(`${API_BASE_URL}/tasks/${userId}`);

  // Add query parameters
  if (q) url.searchParams.append('q', q);
  if (status) url.searchParams.append('status', status);
  if (priority) url.searchParams.append('priority', priority);
  if (tag) url.searchParams.append('tag', tag);
  if (dueDateRange) url.searchParams.append('due_date_range', dueDateRange);
  if (sortBy) url.searchParams.append('sort_by', sortBy);
  if (sortOrder) url.searchParams.append('sort_order', sortOrder);

  const response = await fetch(url.toString(), {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to search tasks: ${response.statusText}`);
  }

  return response.json();
};

export const createTask = async (taskData: TaskFormData): Promise<ApiResponse<Task>> => {
  const response = await fetch(`${API_BASE_URL}/tasks`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    body: JSON.stringify(taskData),
  });

  if (!response.ok) {
    throw new Error(`Failed to create task: ${response.statusText}`);
  }

  return response.json();
};

export const updateTask = async (id: string, taskData: TaskFormData): Promise<ApiResponse<Task>> => {
  const response = await fetch(`${API_BASE_URL}/tasks/${id}`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    body: JSON.stringify(taskData),
  });

  if (!response.ok) {
    throw new Error(`Failed to update task: ${response.statusText}`);
  }

  return response.json();
};

export const deleteTask = async (id: string): Promise<ApiResponse<null>> => {
  const response = await fetch(`${API_BASE_URL}/tasks/${id}`, {
    method: 'DELETE',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to delete task: ${response.statusText}`);
  }

  return response.json();
};

export const toggleTaskCompletion = async (id: string, completed: boolean): Promise<ApiResponse<Task>> => {
  const response = await fetch(`${API_BASE_URL}/tasks/${id}/toggle`, {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
    body: JSON.stringify({ completed }),
  });

  if (!response.ok) {
    throw new Error(`Failed to update task completion: ${response.statusText}`);
  }

  return response.json();
};

export const getTaskById = async (id: string): Promise<ApiResponse<Task>> => {
  const response = await fetch(`${API_BASE_URL}/tasks/${id}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to get task: ${response.statusText}`);
  }

  return response.json();
};

export const getTasksByUser = async (userId: string): Promise<ApiResponse<Task[]>> => {
  const response = await fetch(`${API_BASE_URL}/tasks/${userId}`, {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${localStorage.getItem('token')}`,
    },
  });

  if (!response.ok) {
    throw new Error(`Failed to get tasks: ${response.statusText}`);
  }

  return response.json();
};
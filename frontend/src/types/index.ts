// Frontend Types for Todo App

export interface User {
  id: string;
  email: string;
  name?: string;
  createdAt: string;
  updatedAt?: string;
}

export interface Tag {
  id: number;
  name: string;
}

export interface Task {
  id: string; // UUID
  title: string;
  description?: string;
  completed: boolean;
  userId: string;
  createdAt: string;
  updatedAt?: string;
  priority?: string; // 'Low', 'Medium', 'High', 'Critical'
  dueDate?: string; // ISO string
  reminderTime?: string; // ISO string
  recurrenceType?: string; // 'daily', 'weekly', 'monthly'
  recurrenceMetadata?: string;
  tags?: Tag[];
}

export interface AuthResponse {
  user: User;
  token: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterData extends LoginCredentials {
  name?: string;
}

export interface TaskFormData {
  title: string;
  description?: string;
  priority?: string; // 'Low', 'Medium', 'High', 'Critical'
  dueDate?: string; // ISO string
  reminderTime?: string; // ISO string
  recurrenceType?: string; // 'daily', 'weekly', 'monthly'
  recurrenceMetadata?: string;
  tags?: string; // Comma-separated tags
}

export interface ApiResponse<T> {
  data: T;
  message?: string;
  success: boolean;
}

// JWT Token interface
export interface JwtPayload {
  userId: string;
  email: string;
  exp: number;
  iat: number;
}
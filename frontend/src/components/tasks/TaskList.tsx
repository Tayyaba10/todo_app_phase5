'use client';

import React, { useState, useMemo } from 'react';
import { Task } from '../../types';
import TaskItem from './TaskItem';
import TaskCard from './TaskCard';
import Skeleton from '../ui/Skeleton';
import SortControls from './SortControls';
import FilterPanel from './FilterPanel';

interface TaskListProps {
  tasks: Task[];
  viewMode?: 'list' | 'grid';
  loading?: boolean;
  onToggle?: (id: string, completed: boolean) => void;
  // onEdit?: (task: Task) => void;
  onDelete?: (id: string) => void;
}

const TaskList: React.FC<TaskListProps> = ({
  tasks,
  viewMode = 'list',
  loading = false,
  onToggle,
  // onEdit,
  onDelete
}) => {
  // State for sorting and filtering
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [sortBy, setSortBy] = useState<string>('createdAt');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [filterBy, setFilterBy] = useState({
    status: '',
    priority: '',
    tag: '',
    dueDateRange: ''
  });

  // Extract available tags from tasks
  const availableTags = useMemo(() => {
    const tagSet = new Set<string>();
    tasks.forEach(task => {
      if (task.tags && task.tags.length > 0) {
        task.tags.forEach(tag => tagSet.add(tag.name));
      }
    });
    return Array.from(tagSet);
  }, [tasks]);

  // Apply sorting and filtering
  const filteredAndSortedTasks = useMemo(() => {
    let filtered = tasks.filter(task => {
      // Search query filter
      if (searchQuery) {
        const query = searchQuery.toLowerCase();
        const matchesTitle = task.title.toLowerCase().includes(query);
        const matchesDescription = task.description && task.description.toLowerCase().includes(query);
        const matchesTags = task.tags && task.tags.some(tag =>
          tag.name.toLowerCase().includes(query)
        );

        if (!matchesTitle && !matchesDescription && !matchesTags) return false;
      }

      // Status filter
      if (filterBy.status) {
        if (filterBy.status === 'pending' && task.completed) return false;
        if (filterBy.status === 'completed' && !task.completed) return false;
      }

      // Priority filter
      if (filterBy.priority && task.priority !== filterBy.priority) return false;

      // Tag filter
      if (filterBy.tag) {
        const hasTag = task.tags && task.tags.some(tag => tag.name === filterBy.tag);
        if (!hasTag) return false;
      }

      // Due date range filter
      if (filterBy.dueDateRange && task.dueDate) {
        const dueDate = new Date(task.dueDate);
        const now = new Date();
        const todayStart = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        const weekEnd = new Date(todayStart);
        weekEnd.setDate(todayStart.getDate() + 6);
        const monthEnd = new Date(now.getFullYear(), now.getMonth() + 1, 0);

        switch (filterBy.dueDateRange) {
          case 'today':
            const todayEnd = new Date(todayStart);
            todayEnd.setDate(todayStart.getDate() + 1);
            todayEnd.setMilliseconds(-1);
            if (dueDate < todayStart || dueDate > todayEnd) return false;
            break;
          case 'week':
            if (dueDate < todayStart || dueDate > weekEnd) return false;
            break;
          case 'month':
            if (dueDate < todayStart || dueDate > monthEnd) return false;
            break;
          case 'overdue':
            if (dueDate >= now) return false;
            break;
        }
      } else if (filterBy.dueDateRange === 'no-due-date' && task.dueDate) {
        return false;
      }

      return true;
    });

    // Apply sorting
    return filtered.sort((a, b) => {
      let aValue: any, bValue: any;

      switch (sortBy) {
        case 'title':
          aValue = a.title.toLowerCase();
          bValue = b.title.toLowerCase();
          break;
        case 'priority':
          aValue = a.priority || '';
          bValue = b.priority || '';
          break;
        case 'completed':
          aValue = a.completed;
          bValue = b.completed;
          break;
        case 'dueDate':
          aValue = a.dueDate ? new Date(a.dueDate) : null;
          bValue = b.dueDate ? new Date(b.dueDate) : null;

          // Handle null values - tasks without due dates should come after those with due dates
          if (!aValue && !bValue) return 0;
          if (!aValue) return 1;
          if (!bValue) return -1;
          break;
        case 'createdAt':
        default:
          aValue = new Date(a.createdAt);
          bValue = new Date(b.createdAt);
          break;
      }

      // Handle null values in comparison
      if (aValue === null && bValue === null) return 0;
      if (aValue === null) return sortOrder === 'asc' ? 1 : -1;
      if (bValue === null) return sortOrder === 'asc' ? -1 : 1;

      if (aValue < bValue) return sortOrder === 'asc' ? -1 : 1;
      if (aValue > bValue) return sortOrder === 'asc' ? 1 : -1;
      return 0;
    });
  }, [tasks, sortBy, sortOrder, filterBy, searchQuery]);

  if (loading) {
    // Show skeleton loading state
    return (
      <div className="space-y-4">
        <div className="flex flex-col gap-2">
          <div className="flex flex-wrap gap-2 p-2">
            <div className="flex-1 min-w-[300px]">
              <input
                type="text"
                placeholder="Search tasks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                disabled
              />
            </div>
            <SortControls
              sortBy={sortBy}
              sortOrder={sortOrder}
              onSortChange={(newSortBy, newSortOrder) => {
                setSortBy(newSortBy);
                setSortOrder(newSortOrder);
              }}
            />
          </div>

          <FilterPanel
            filterBy={filterBy}
            onFilterChange={(filterType, value) => {
              setFilterBy(prev => ({
                ...prev,
                [filterType]: value
              }));
            }}
            availableTags={availableTags}
          />
        </div>

        <div className={viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4' : 'space-y-2'}>
          {Array.from({ length: 3 }).map((_, index) => (
            <div key={index} className="border rounded-lg p-4 bg-white">
              <Skeleton className="h-6 w-3/4 mb-2" />
              <Skeleton className="h-4 w-full mb-1" />
              <Skeleton className="h-4 w-2/3" />
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (filteredAndSortedTasks.length === 0) {
    return (
      <div className="space-y-4">
        <div className="flex flex-col gap-2">
          <div className="flex flex-wrap gap-2 p-2">
            <div className="flex-1 min-w-[300px]">
              <input
                type="text"
                placeholder="Search tasks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
              />
            </div>
            <SortControls
              sortBy={sortBy}
              sortOrder={sortOrder}
              onSortChange={(newSortBy, newSortOrder) => {
                setSortBy(newSortBy);
                setSortOrder(newSortOrder);
              }}
            />
          </div>

          <FilterPanel
            filterBy={filterBy}
            onFilterChange={(filterType, value) => {
              setFilterBy(prev => ({
                ...prev,
                [filterType]: value
              }));
            }}
            availableTags={availableTags}
          />
        </div>

        <div className="text-center py-8">
          <p className="text-gray-500">No tasks found matching your filters. Create your first task!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-2">
        <div className="flex flex-wrap gap-2 p-2">
          <div className="flex-1 min-w-[300px]">
            <input
              type="text"
              placeholder="Search tasks..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          <SortControls
            sortBy={sortBy}
            sortOrder={sortOrder}
            onSortChange={(newSortBy, newSortOrder) => {
              setSortBy(newSortBy);
              setSortOrder(newSortOrder);
            }}
          />
        </div>

        <FilterPanel
          filterBy={filterBy}
          onFilterChange={(filterType, value) => {
            setFilterBy(prev => ({
              ...prev,
              [filterType]: value
            }));
          }}
          availableTags={availableTags}
        />
      </div>

      <div className={viewMode === 'grid' ? 'grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4' : 'space-y-2'}>
        {filteredAndSortedTasks.map(task => (
          viewMode === 'list' ? (
            <TaskItem
              key={task.id}
              task={task}
              onToggle={onToggle}
              // onEdit={onEdit}
              onDelete={onDelete}
            />
          ) : (
            <TaskCard
              key={task.id}
              task={task}
              onToggle={onToggle}
              // onEdit={onEdit}
              onDelete={onDelete}
            />
          )
        ))}
      </div>
    </div>
  );
};

export default TaskList;
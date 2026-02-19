'use client';

import React from 'react';

interface FilterPanelProps {
  filterBy: {
    status: string;
    priority: string;
    tag: string;
    dueDateRange: string;
  };
  onFilterChange: (filterType: string, value: string) => void;
  availableTags: string[];
}

const FilterPanel: React.FC<FilterPanelProps> = ({
  filterBy,
  onFilterChange,
  availableTags
}) => {
  return (
    <div className="p-3 bg-gray-50 rounded border space-y-3">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
        {/* Status Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Status
          </label>
          <select
            value={filterBy.status}
            onChange={(e) => onFilterChange('status', e.target.value)}
            className="w-full px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            <option value="">All</option>
            <option value="pending">Pending</option>
            <option value="completed">Completed</option>
          </select>
        </div>

        {/* Priority Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Priority
          </label>
          <select
            value={filterBy.priority}
            onChange={(e) => onFilterChange('priority', e.target.value)}
            className="w-full px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            <option value="">All</option>
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
            <option value="Critical">Critical</option>
          </select>
        </div>

        {/* Tag Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Tag
          </label>
          <select
            value={filterBy.tag}
            onChange={(e) => onFilterChange('tag', e.target.value)}
            className="w-full px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            <option value="">All</option>
            {availableTags.map((tag, index) => (
              <option key={index} value={tag}>
                {tag}
              </option>
            ))}
          </select>
        </div>

        {/* Due Date Range Filter */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">
            Due Date
          </label>
          <select
            value={filterBy.dueDateRange}
            onChange={(e) => onFilterChange('dueDateRange', e.target.value)}
            className="w-full px-2 py-1 border border-gray-300 rounded text-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
          >
            <option value="">All</option>
            <option value="today">Due Today</option>
            <option value="week">Due This Week</option>
            <option value="month">Due This Month</option>
            <option value="overdue">Overdue</option>
            <option value="no-due-date">No Due Date</option>
          </select>
        </div>
      </div>
    </div>
  );
};

export default FilterPanel;
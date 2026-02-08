import React, { useState, useEffect } from 'react';
import { Task, Priority, FilterStatus, FilterPriority } from './types';
import { parseTags, getUniqueTags } from './utils';

const App: React.FC = () => {
  // State for tasks
  const [tasks, setTasks] = useState<Task[]>([]);
  
  // State for new task form
  const [newTaskTitle, setNewTaskTitle] = useState<string>('');
  const [newTaskDescription, setNewTaskDescription] = useState<string>('');
  const [newTaskPriority, setNewTaskPriority] = useState<Priority>('Medium');
  const [newTaskTags, setNewTaskTags] = useState<string>('');
  
  // State for filters and search
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<FilterStatus>('All');
  const [priorityFilter, setPriorityFilter] = useState<FilterPriority>('All');
  const [tagFilter, setTagFilter] = useState<string>('All');
  
  // State for sorting
  const [sortOption, setSortOption] = useState<string>('createdDate');
  const [sortDirection, setSortDirection] = useState<'asc' | 'desc'>('desc');

  // Load tasks from localStorage on component mount
  useEffect(() => {
    const savedTasks = localStorage.getItem('todo-app-tasks');
    if (savedTasks) {
      try {
        const parsedTasks = JSON.parse(savedTasks);
        // Convert date strings back to Date objects
        const tasksWithDates = parsedTasks.map((task: any) => ({
          ...task,
          createdAt: new Date(task.createdAt),
          dueDate: task.dueDate ? new Date(task.dueDate) : undefined
        }));
        setTasks(tasksWithDates);
      } catch (error) {
        console.error('Failed to parse tasks from localStorage:', error);
      }
    }
  }, []);

  // Save tasks to localStorage whenever tasks change
  useEffect(() => {
    localStorage.setItem('todo-app-tasks', JSON.stringify(tasks));
  }, [tasks]);

  // Function to add a new task
  const addTask = () => {
    if (!newTaskTitle.trim()) return;

    const newTask: Task = {
      id: Date.now().toString(),
      title: newTaskTitle,
      description: newTaskDescription || undefined,
      completed: false,
      priority: newTaskPriority,
      tags: parseTags(newTaskTags),
      createdAt: new Date(),
    };

    setTasks([...tasks, newTask]);
    
    // Reset form
    setNewTaskTitle('');
    setNewTaskDescription('');
    setNewTaskPriority('Medium');
    setNewTaskTags('');
  };

  // Function to toggle task completion
  const toggleComplete = (id: string) => {
    setTasks(
      tasks.map(task =>
        task.id === id ? { ...task, completed: !task.completed } : task
      )
    );
  };

  // Function to delete a task
  const deleteTask = (id: string) => {
    setTasks(tasks.filter(task => task.id !== id));
  };

  // State for editing tasks
  const [editingTaskId, setEditingTaskId] = useState<string | null>(null);
  const [editForm, setEditForm] = useState({
    title: '',
    description: '',
    priority: 'Medium' as Priority,
    tags: ''
  });

  // Function to start editing a task
  const startEditing = (task: Task) => {
    setEditingTaskId(task.id);
    setEditForm({
      title: task.title,
      description: task.description || '',
      priority: task.priority,
      tags: task.tags.join(', ')
    });
  };

  // Function to save edited task
  const saveEditedTask = () => {
    if (!editingTaskId) return;

    setTasks(tasks.map(task => 
      task.id === editingTaskId 
        ? { 
            ...task, 
            title: editForm.title,
            description: editForm.description || undefined,
            priority: editForm.priority,
            tags: parseTags(editForm.tags)
          } 
        : task
    ));

    setEditingTaskId(null);
  };

  // Function to cancel editing
  const cancelEditing = () => {
    setEditingTaskId(null);
  };

  // Function to get filtered and sorted tasks
  const getFilteredAndSortedTasks = (): Task[] => {
    let filteredTasks = [...tasks];

    // Apply search filter
    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filteredTasks = filteredTasks.filter(
        task =>
          task.title.toLowerCase().includes(term) ||
          (task.description && task.description.toLowerCase().includes(term))
      );
    }

    // Apply status filter
    if (statusFilter !== 'All') {
      filteredTasks = filteredTasks.filter(task => {
        if (statusFilter === 'Pending') return !task.completed;
        if (statusFilter === 'Completed') return task.completed;
        return true;
      });
    }

    // Apply priority filter
    if (priorityFilter !== 'All') {
      filteredTasks = filteredTasks.filter(task => task.priority === priorityFilter);
    }

    // Apply tag filter
    if (tagFilter !== 'All') {
      filteredTasks = filteredTasks.filter(task => task.tags.includes(tagFilter));
    }

    // Apply sorting
    filteredTasks.sort((a, b) => {
      let comparison = 0;

      switch (sortOption) {
        case 'priority':
          // Define priority order: High > Medium > Low
          const priorityOrder: Record<Priority, number> = { High: 3, Medium: 2, Low: 1 };
          comparison = priorityOrder[b.priority] - priorityOrder[a.priority];
          break;
        case 'createdDate':
          comparison = sortDirection === 'asc' 
            ? a.createdAt.getTime() - b.createdAt.getTime()
            : b.createdAt.getTime() - a.createdAt.getTime();
          break;
        case 'alphabetical':
          comparison = sortDirection === 'asc'
            ? a.title.localeCompare(b.title)
            : b.title.localeCompare(a.title);
          break;
        case 'dueDate':
          if (a.dueDate && b.dueDate) {
            comparison = sortDirection === 'asc'
              ? a.dueDate.getTime() - b.dueDate.getTime()
              : b.dueDate.getTime() - a.dueDate.getTime();
          } else if (a.dueDate) {
            comparison = sortDirection === 'asc' ? -1 : 1;
          } else if (b.dueDate) {
            comparison = sortDirection === 'asc' ? 1 : -1;
          } else {
            comparison = 0;
          }
          break;
        default:
          break;
      }

      return comparison;
    });

    return filteredTasks;
  };

  // Get unique tags for the tag filter dropdown
  const uniqueTags = getUniqueTags(tasks);

  // Render the app
  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <h1 className="text-3xl font-bold text-center text-gray-800 mb-8">Intermediate Todo App</h1>
        
        {/* Add Task Form */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Add New Task</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <input
                type="text"
                value={newTaskTitle}
                onChange={(e) => setNewTaskTitle(e.target.value)}
                placeholder="Task title"
                className="w-full p-2 border border-gray-300 rounded mb-2"
              />
              <textarea
                value={newTaskDescription}
                onChange={(e) => setNewTaskDescription(e.target.value)}
                placeholder="Description (optional)"
                className="w-full p-2 border border-gray-300 rounded mb-2"
                rows={2}
              />
            </div>
            <div>
              <select
                value={newTaskPriority}
                onChange={(e) => setNewTaskPriority(e.target.value as Priority)}
                className="w-full p-2 border border-gray-300 rounded mb-2"
              >
                <option value="High">High Priority</option>
                <option value="Medium">Medium Priority</option>
                <option value="Low">Low Priority</option>
              </select>
              <input
                type="text"
                value={newTaskTags}
                onChange={(e) => setNewTaskTags(e.target.value)}
                placeholder="Tags (comma-separated)"
                className="w-full p-2 border border-gray-300 rounded mb-2"
              />
              <button
                onClick={addTask}
                className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600 transition-colors"
              >
                Add Task
              </button>
            </div>
          </div>
        </div>

        {/* Controls Section */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-6">
          <h2 className="text-xl font-semibold mb-4">Filters & Sorting</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Search</label>
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Search tasks..."
                className="w-full p-2 border border-gray-300 rounded"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Status</label>
              <select
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value as FilterStatus)}
                className="w-full p-2 border border-gray-300 rounded"
              >
                <option value="All">All</option>
                <option value="Pending">Pending</option>
                <option value="Completed">Completed</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Priority</label>
              <select
                value={priorityFilter}
                onChange={(e) => setPriorityFilter(e.target.value as FilterPriority)}
                className="w-full p-2 border border-gray-300 rounded"
              >
                <option value="All">All</option>
                <option value="High">High</option>
                <option value="Medium">Medium</option>
                <option value="Low">Low</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Tag</label>
              <select
                value={tagFilter}
                onChange={(e) => setTagFilter(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded"
              >
                <option value="All">All</option>
                {uniqueTags.map(tag => (
                  <option key={tag} value={tag}>{tag}</option>
                ))}
              </select>
            </div>
          </div>
          <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Sort By</label>
              <select
                value={sortOption}
                onChange={(e) => setSortOption(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded"
              >
                <option value="createdDate">Created Date</option>
                <option value="priority">Priority</option>
                <option value="alphabetical">Alphabetical</option>
                <option value="dueDate">Due Date</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Direction</label>
              <select
                value={sortDirection}
                onChange={(e) => setSortDirection(e.target.value as 'asc' | 'desc')}
                className="w-full p-2 border border-gray-300 rounded"
              >
                <option value="asc">Ascending</option>
                <option value="desc">Descending</option>
              </select>
            </div>
          </div>
        </div>

        {/* Task List */}
        <div>
          <h2 className="text-xl font-semibold mb-4">
            Tasks ({getFilteredAndSortedTasks().length} shown of {tasks.length})
          </h2>
          
          {getFilteredAndSortedTasks().length === 0 ? (
            <div className="bg-white rounded-lg shadow-md p-6 text-center">
              <p className="text-gray-500">
                {tasks.length === 0 
                  ? "No tasks yet. Add a task to get started!" 
                  : "No tasks match your current filters."}
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {getFilteredAndSortedTasks().map(task => (
                <div 
                  key={task.id} 
                  className={`bg-white rounded-lg shadow-md p-4 border-l-4 ${
                    task.priority === 'High' ? 'border-red-500' :
                    task.priority === 'Medium' ? 'border-yellow-500' : 'border-green-500'
                  } ${task.completed ? 'opacity-75' : ''}`}
                >
                  {editingTaskId === task.id ? (
                    // Edit form
                    <div className="space-y-3">
                      <input
                        type="text"
                        value={editForm.title}
                        onChange={(e) => setEditForm({...editForm, title: e.target.value})}
                        className="w-full p-2 border border-gray-300 rounded mb-2"
                      />
                      <textarea
                        value={editForm.description}
                        onChange={(e) => setEditForm({...editForm, description: e.target.value})}
                        className="w-full p-2 border border-gray-300 rounded mb-2"
                        rows={2}
                      />
                      <div className="grid grid-cols-2 gap-2">
                        <select
                          value={editForm.priority}
                          onChange={(e) => setEditForm({...editForm, priority: e.target.value as Priority})}
                          className="p-2 border border-gray-300 rounded"
                        >
                          <option value="High">High Priority</option>
                          <option value="Medium">Medium Priority</option>
                          <option value="Low">Low Priority</option>
                        </select>
                        <input
                          type="text"
                          value={editForm.tags}
                          onChange={(e) => setEditForm({...editForm, tags: e.target.value})}
                          placeholder="Tags (comma-separated)"
                          className="p-2 border border-gray-300 rounded"
                        />
                      </div>
                      <div className="flex space-x-2">
                        <button
                          onClick={saveEditedTask}
                          className="bg-green-500 text-white py-1 px-3 rounded hover:bg-green-600"
                        >
                          Save
                        </button>
                        <button
                          onClick={cancelEditing}
                          className="bg-gray-500 text-white py-1 px-3 rounded hover:bg-gray-600"
                        >
                          Cancel
                        </button>
                      </div>
                    </div>
                  ) : (
                    // Display task
                    <div className="flex items-start">
                      <input
                        type="checkbox"
                        checked={task.completed}
                        onChange={() => toggleComplete(task.id)}
                        className="mt-1 mr-3 h-5 w-5"
                      />
                      <div className="flex-1">
                        <div className="flex justify-between">
                          <h3 className={`text-lg font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-800'}`}>
                            {task.title}
                          </h3>
                          <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                            task.priority === 'High' ? 'bg-red-100 text-red-800' :
                            task.priority === 'Medium' ? 'bg-yellow-100 text-yellow-800' : 'bg-green-100 text-green-800'
                          }`}>
                            {task.priority}
                          </span>
                        </div>
                        
                        {task.description && (
                          <p className="text-gray-600 mt-1">{task.description}</p>
                        )}
                        
                        <div className="mt-2 flex flex-wrap gap-2">
                          {task.tags.map(tag => (
                            <span 
                              key={`${task.id}-${tag}`} 
                              className="px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-xs"
                            >
                              {tag}
                            </span>
                          ))}
                        </div>
                      </div>
                      <div className="flex flex-col space-y-2">
                        <button
                          onClick={() => startEditing(task)}
                          className="text-blue-500 hover:text-blue-700"
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => deleteTask(task.id)}
                          className="text-red-500 hover:text-red-700"
                        >
                          Delete
                        </button>
                      </div>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default App;
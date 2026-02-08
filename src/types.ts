export type Priority = 'High' | 'Medium' | 'Low';

export interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: Priority;
  tags: string[];
  createdAt: Date;
  dueDate?: Date;
}

export type FilterStatus = 'All' | 'Pending' | 'Completed';
export type FilterPriority = 'All' | 'High' | 'Medium' | 'Low';
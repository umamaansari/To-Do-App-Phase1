/**
 * Parses a comma-separated string of tags into an array of trimmed, non-empty tags
 * @param tagString - String containing comma-separated tags
 * @returns Array of trimmed, non-empty tags
 */
export const parseTags = (tagString: string): string[] => {
  if (!tagString || typeof tagString !== 'string') {
    return [];
  }

  return tagString
    .split(',')
    .map(tag => tag.trim())
    .filter(tag => tag.length > 0);
};

/**
 * Gets all unique tags from an array of tasks
 * @param tasks - Array of Task objects
 * @returns Array of unique tag strings
 */
export const getUniqueTags = (tasks: any[]): string[] => {
  const allTags: string[] = [];
  
  tasks.forEach(task => {
    if (task.tags && Array.isArray(task.tags)) {
      allTags.push(...task.tags);
    }
  });
  
  // Return unique tags only
  return Array.from(new Set(allTags));
};
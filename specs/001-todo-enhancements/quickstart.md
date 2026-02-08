# Quickstart Guide: Intermediate Todo App

## Prerequisites
- Node.js (v14 or later)
- npm or yarn package manager
- Modern web browser

## Setup Instructions

1. Clone or download the project files
2. Navigate to the project directory in terminal
3. Install dependencies:
   ```
   npm install
   ```
   or
   ```
   yarn install
   ```
4. Start the development server:
   ```
   npm start
   ```
   or
   ```
   yarn start
   ```

## Key Features Overview

### Adding Tasks
- Enter task title in the input field
- Optionally add a description
- Select priority level (High/Medium/Low)
- Add tags as comma-separated values
- Click "Add Task" button

### Managing Tasks
- Toggle completion status using the checkbox
- Edit existing tasks by clicking the edit icon
- Delete tasks using the delete button

### Filtering & Searching
- Use the search bar to filter tasks by title/description
- Apply status filters (All/Pending/Completed)
- Apply priority filters (All/High/Medium/Low)
- Apply tag filters (select from available tags)

### Sorting
- Choose from various sorting options:
  - Created date (newest/oldest)
  - Priority (High→Low or Low→High)
  - Alphabetical (A→Z or Z→A)

## File Structure
- `App.tsx` - Main application component
- `types.ts` - Type definitions
- `utils.ts` - Utility functions (tag parsing, etc.)

## Development Notes
- All data is persisted in localStorage
- State is managed using React hooks (useState, useEffect)
- Styling uses Tailwind CSS classes
- Responsive design for mobile and desktop
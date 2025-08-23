# Professor Nihil PKM Application Design Document

## Overview

This document outlines the design for an integrated Personal Knowledge Management (PKM) application with the Professor Nihil AI Philosopher chatbot embedded in the sidebar. The application combines markdown editing, note organization, and advanced AI capabilities in an efficient, minimalist interface.

## Key Requirements

1. **Integrated Sidebar Chatbot**
   - Professor Nihil AI Philosopher accessible from the right sidebar
   - Expandable/collapsible for space efficiency
   - Maintains philosophical depth and capabilities of the original chatbot

2. **Markdown Editor with Preview**
   - Clean, distraction-free writing environment
   - Live markdown preview
   - Expandable/collapsible preview panel

3. **AI Feature Dropdown Menu**
   - Replaces the #DEEPRESEARCH button with a dropdown menu
   - Includes options: Summarize, Expand, Analyze, Deep Research, Rewrite, Brainstorm
   - Accessible from the left sidebar

4. **Efficient Layout**
   - Minimizes buttons under the note area
   - Three-panel layout (left sidebar, main content, right sidebar)
   - Responsive design for different screen sizes

## UI Components

### Left Sidebar
- App title and branding
- Search notes functionality
- New note button
- AI Features dropdown menu (replacing #DEEPRESEARCH button)
- Note list with filtering capabilities
- Tags/folders navigation

### Main Content Area
- Note title input
- Tags input
- Markdown editor
- Minimal button row (Save, Clear, Delete)
- Toggle buttons for Preview and AI Sidebar
- Word/character counter

### Right Sidebar (AI Philosopher)
- Collapsible panel with toggle button
- Professor Nihil header with minimize/expand button
- Chat history display area
- Input field for questions
- Send button
- Mode selector for different philosophical approaches

## Interaction Flow

1. **Note Creation and Editing**
   - Create new note from left sidebar
   - Edit in main content area
   - Save with minimal button or keyboard shortcut

2. **AI Assistance**
   - Select AI feature from dropdown in left sidebar
   - AI processes current note content
   - Results appear in right sidebar
   - Conversation can continue in the sidebar

3. **Philosophical Exploration**
   - Toggle right sidebar for Professor Nihil
   - Select philosophical mode if desired
   - Ask questions and receive responses
   - Minimize when not needed

## Technical Architecture

### Frontend
- HTML5, CSS3, JavaScript (ES6+)
- Responsive design using CSS Grid and Flexbox
- Dark theme with consistent styling
- Local storage for note persistence

### AI Integration
- Professor Nihil chatbot integration
- OpenAI API for processing
- Client-side API key management
- Multiple philosophical modes

### Data Management
- LocalStorage/IndexedDB for notes
- Session management for chat history
- Export/import functionality

## Visual Design

- **Color Scheme**: Dark theme with accent colors
  - Background: #121212
  - Panels: #1a1a1a
  - Text: #e0e0e0
  - Accent: #6f4dff (violet)

- **Typography**:
  - Primary font: "Inter" or system sans-serif
  - Monospace for code blocks
  - Comfortable line height and spacing

- **Layout**:
  - Three-column responsive grid
  - Collapsible panels for space efficiency
  - Clean visual hierarchy

## Optimizations

- Keyboard shortcuts for common actions
- Collapsible panels to maximize working space
- Minimal button usage with context-appropriate controls
- Efficient AI feature access through dropdown menu
- Responsive design for various screen sizes

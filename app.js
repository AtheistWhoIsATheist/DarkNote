// Enhanced functionality for the PKM app with Professor Nihil integration

// DOM Elements
document.addEventListener('DOMContentLoaded', function() {
  const appContainer = document.querySelector('.app-container');
  const togglePreviewBtn = document.getElementById('toggle-preview');
  const previewPanel = document.getElementById('preview-panel');
  const toggleAiSidebarBtn = document.getElementById('toggle-ai-sidebar');
  const minimizeAiBtn = document.getElementById('minimize-ai');
  const editorTextarea = document.querySelector('.editor-textarea');
  const wordCount = document.querySelector('.word-count');
  const titleInput = document.querySelector('.title-input');
  const tagsInput = document.querySelector('.tags-input');
  const aiInput = document.querySelector('.ai-input');
  const aiSendBtn = document.querySelector('.ai-input-container .button');
  const aiChatContainer = document.querySelector('.ai-chat-container');
  const aiModeSelector = document.querySelector('.ai-mode-selector');
  const saveNoteBtn = document.querySelector('.button-row .button:nth-child(1)');
  const clearBtn = document.querySelector('.button-row .button:nth-child(2)');
  const deleteBtn = document.querySelector('.button-row .button:nth-child(3)');
  const newNoteBtn = document.querySelector('.button.primary.full-width');
  const searchInput = document.querySelector('.search-input');
  const notesList = document.querySelector('.notes-list');
  const aiFeatureLinks = document.querySelectorAll('.dropdown-content a');
  
  // Notes storage
  let notes = JSON.parse(localStorage.getItem('notes')) || [];
  let currentNoteId = null;
  
  // Initialize marked for markdown rendering
  const marked = window.marked || {
    parse: function(text) {
      return text
        .replace(/^### (.*$)/gim, '<h3>$1</h3>')
        .replace(/^## (.*$)/gim, '<h2>$1</h2>')
        .replace(/^# (.*$)/gim, '<h1>$1</h1>')
        .replace(/\*\*(.*)\*\*/gim, '<strong>$1</strong>')
        .replace(/\*(.*)\*/gim, '<em>$1</em>')
        .replace(/\n/gim, '<br>');
    }
  };
  
  // Toggle preview panel
  togglePreviewBtn.addEventListener('click', () => {
    previewPanel.classList.toggle('visible');
    if (previewPanel.classList.contains('visible')) {
      renderMarkdownPreview();
    }
  });
  
  // Toggle AI sidebar
  toggleAiSidebarBtn.addEventListener('click', () => {
    appContainer.classList.toggle('sidebar-collapsed');
  });
  
  // Minimize AI sidebar
  minimizeAiBtn.addEventListener('click', () => {
    appContainer.classList.add('sidebar-collapsed');
  });
  
  // Update word count
  editorTextarea.addEventListener('input', () => {
    updateWordCount();
    renderMarkdownPreview();
  });
  
  // Render markdown preview
  function renderMarkdownPreview() {
    if (previewPanel.classList.contains('visible')) {
      const markdown = editorTextarea.value;
      previewPanel.innerHTML = marked.parse(markdown);
    }
  }
  
  function updateWordCount() {
    const text = editorTextarea.value;
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    const chars = text.length;
    wordCount.textContent = `${words} words, ${chars} characters`;
  }
  
  // Save note
  saveNoteBtn.addEventListener('click', saveNote);
  
  function saveNote() {
    const title = titleInput.value.trim() || 'Untitled Note';
    const content = editorTextarea.value;
    const tags = tagsInput.value.split(',').map(tag => tag.trim()).filter(Boolean);
    
    if (currentNoteId) {
      // Update existing note
      const noteIndex = notes.findIndex(note => note.id === currentNoteId);
      if (noteIndex !== -1) {
        notes[noteIndex] = {
          ...notes[noteIndex],
          title,
          content,
          tags,
          updatedAt: new Date().toISOString()
        };
      }
    } else {
      // Create new note
      const newNote = {
        id: Date.now(),
        title,
        content,
        tags,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };
      notes.push(newNote);
      currentNoteId = newNote.id;
    }
    
    localStorage.setItem('notes', JSON.stringify(notes));
    renderNotesList();
    
    // Show temporary save confirmation
    const saveConfirm = document.createElement('div');
    saveConfirm.textContent = 'Note saved!';
    saveConfirm.style.position = 'fixed';
    saveConfirm.style.bottom = '20px';
    saveConfirm.style.right = '20px';
    saveConfirm.style.backgroundColor = 'var(--accent-color)';
    saveConfirm.style.color = 'white';
    saveConfirm.style.padding = '10px 20px';
    saveConfirm.style.borderRadius = 'var(--radius)';
    saveConfirm.style.zIndex = '1000';
    document.body.appendChild(saveConfirm);
    
    setTimeout(() => {
      document.body.removeChild(saveConfirm);
    }, 2000);
  }
  
  // Clear form
  clearBtn.addEventListener('click', clearForm);
  
  function clearForm() {
    titleInput.value = '';
    editorTextarea.value = '';
    tagsInput.value = '';
    currentNoteId = null;
    updateWordCount();
    previewPanel.innerHTML = '';
  }
  
  // Delete note
  deleteBtn.addEventListener('click', deleteNote);
  
  function deleteNote() {
    if (!currentNoteId) return;
    
    if (confirm('Are you sure you want to delete this note? This action cannot be undone.')) {
      notes = notes.filter(note => note.id !== currentNoteId);
      localStorage.setItem('notes', JSON.stringify(notes));
      clearForm();
      renderNotesList();
    }
  }
  
  // Create new note
  newNoteBtn.addEventListener('click', () => {
    clearForm();
    titleInput.focus();
  });
  
  // Render notes list
  function renderNotesList() {
    notesList.innerHTML = '';
    
    const filteredNotes = filterNotes(searchInput.value);
    
    filteredNotes.forEach(note => {
      const noteItem = document.createElement('div');
      noteItem.className = `note-item${note.id === currentNoteId ? ' active' : ''}`;
      noteItem.dataset.id = note.id;
      
      const noteTitle = document.createElement('div');
      noteTitle.className = 'note-title';
      noteTitle.textContent = note.title;
      
      const notePreview = document.createElement('div');
      notePreview.className = 'note-preview';
      notePreview.textContent = note.content.substring(0, 60) + (note.content.length > 60 ? '...' : '');
      
      noteItem.appendChild(noteTitle);
      noteItem.appendChild(notePreview);
      notesList.appendChild(noteItem);
      
      noteItem.addEventListener('click', () => loadNote(note.id));
    });
  }
  
  // Filter notes
  function filterNotes(query) {
    if (!query) return [...notes].sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt));
    
    query = query.toLowerCase();
    return notes.filter(note => 
      note.title.toLowerCase().includes(query) || 
      note.content.toLowerCase().includes(query) ||
      note.tags.some(tag => tag.toLowerCase().includes(query))
    ).sort((a, b) => new Date(b.updatedAt) - new Date(a.updatedAt));
  }
  
  // Search notes
  searchInput.addEventListener('input', () => {
    renderNotesList();
  });
  
  // Load note
  function loadNote(id) {
    const note = notes.find(note => note.id === id);
    if (!note) return;
    
    currentNoteId = note.id;
    titleInput.value = note.title;
    editorTextarea.value = note.content;
    tagsInput.value = note.tags.join(', ');
    
    updateWordCount();
    renderMarkdownPreview();
    renderNotesList(); // Update active state
  }
  
  // Professor Nihil AI Integration
  aiSendBtn.addEventListener('click', sendToAI);
  aiInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendToAI();
    }
  });
  
  function sendToAI() {
    const message = aiInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addChatMessage(message, 'user');
    aiInput.value = '';
    
    // Get selected philosophical mode
    const mode = aiModeSelector.value;
    
    // Simulate AI response (in a real app, this would call an API)
    setTimeout(() => {
      const response = generatePhilosophicalResponse(message, mode);
      addChatMessage(response, 'bot');
    }, 1000);
  }
  
  function addChatMessage(message, sender) {
    const messageEl = document.createElement('div');
    messageEl.className = `ai-message ${sender}`;
    messageEl.textContent = message;
    
    aiChatContainer.appendChild(messageEl);
    aiChatContainer.scrollTop = aiChatContainer.scrollHeight;
  }
  
  function generatePhilosophicalResponse(message, mode) {
    // This is a simplified simulation of Professor Nihil's responses
    // In a real implementation, this would call the OpenAI API with appropriate prompts
    
    const responses = {
      'recursive-dialectic': `Your inquiry about "${message}" invites a recursive examination. Each answer generates new questions, leading us deeper into the paradoxical nature of existence. The question itself contains its own negation, revealing how meaning emerges from the tension between assertion and denial.`,
      
      'ontological-collapse': `Considering "${message}" through the lens of ontological collapse reveals how the distinction between Being and Nothingness ultimately breaks down. The void is not merely absence, but the foundation from which all phenomena emerge and to which they return.`,
      
      'apophatic-synthesis': `To approach "${message}" apophatically, we must first recognize what it is not. By negating conventional understandings, we create space for a deeper truth to emerge—one that transcends the limitations of positive assertion and embraces the ineffable nature of reality.`,
      
      'mythopoetic-logic': `"${message}" resonates with the mythopoetic dimension of existence. Like Orpheus descending into the underworld, this inquiry leads us through symbolic terrain where rational categories dissolve and narrative truth emerges from the sacred void.`
    };
    
    return responses[mode] || `I've considered "${message}" deeply. The question itself reveals how meaning emerges from the tension between being and non-being, a fundamental paradox at the heart of existence.`;
  }
  
  // AI Feature Integration
  aiFeatureLinks.forEach(link => {
    link.addEventListener('click', () => {
      const action = link.dataset.action;
      processAIFeature(action);
    });
  });
  
  function processAIFeature(action) {
    const content = editorTextarea.value.trim();
    if (!content) {
      alert('Please write some content before using AI features.');
      return;
    }
    
    // Open AI sidebar if closed
    appContainer.classList.remove('sidebar-collapsed');
    
    // Add system message about the action
    addChatMessage(`Processing request: ${action.replace('-', ' ')}...`, 'bot');
    
    // Simulate AI processing
    setTimeout(() => {
      const response = generateAIFeatureResponse(content, action);
      addChatMessage(response, 'bot');
    }, 1500);
  }
  
  function generateAIFeatureResponse(content, action) {
    // Simplified simulation of AI feature responses
    // In a real implementation, this would call the OpenAI API with appropriate prompts
    
    const responses = {
      'summarize': `Summary of your note:\n\nYour text explores key themes related to knowledge management and philosophical inquiry. The central ideas focus on the integration of thought processes with digital tools, emphasizing the importance of structured reflection and recursive analysis.`,
      
      'expand': `Expanded version of your ideas:\n\n${content}\n\nThis concept can be further developed by considering the historical context of knowledge systems, from ancient mnemonic techniques to modern computational approaches. The integration of AI with human cognition represents not merely a technological advancement but an ontological shift in how we understand the boundaries of thought itself.`,
      
      'analyze': `Analysis of your note:\n\nYour text contains several interconnected themes:\n\n1. Epistemological questions about the nature of knowledge\n2. Practical considerations regarding information management\n3. Philosophical implications of human-AI collaboration\n\nThe underlying structure suggests a dialectical approach to these questions, where opposing viewpoints are synthesized into a more comprehensive understanding.`,
      
      'deep-research': `Deep Research Results:\n\nYour inquiry touches on fundamental questions that span multiple philosophical traditions. From the Platonic conception of forms to Heidegger's analysis of technology, the relationship between thought and its externalization has been a central concern.\n\nThe Nihiltheistic perspective offers a unique lens, suggesting that the void between knowledge systems is not merely empty space but the generative ground from which new understanding emerges. This paradoxical foundation—where absence becomes presence—provides a framework for understanding how digital tools extend rather than replace human cognition.`,
      
      'rewrite': `Rewritten version:\n\n${content.split(' ').slice(0, 20).join(' ')}...\n\nThe above opening has been restructured to emphasize clarity and conceptual depth. The reframing maintains your original insights while enhancing the rhetorical flow and philosophical precision.`,
      
      'brainstorm': `Brainstorming related ideas:\n\n1. The archaeology of knowledge systems through history\n2. Paradoxes of self-reference in recursive thought\n3. The role of absence/void in creative thinking\n4. Digital gardens as externalized consciousness\n5. Apophatic approaches to information management\n6. The ethics of AI-augmented cognition\n7. Phenomenology of the blank page/empty screen\n8. Temporal aspects of note-taking and retrieval`
    };
    
    return responses[action] || `I've processed your request to ${action.replace('-', ' ')} the content. The results reveal deeper patterns and connections that might not be immediately apparent on the surface.`;
  }
  
  // Initialize
  updateWordCount();
  renderNotesList();
  
  // Add welcome note if no notes exist
  if (notes.length === 0) {
    const welcomeNote = {
      id: Date.now(),
      title: 'Welcome to Dark Notes with Professor Nihil',
      content: `# Welcome to Dark Notes with Professor Nihil

This application combines powerful note-taking capabilities with philosophical AI assistance.

## Features

- **Markdown Editor**: Write and format your notes using Markdown
- **AI Features**: Access various AI tools from the dropdown menu
- **Professor Nihil**: Engage in philosophical conversations in the sidebar
- **Multiple Philosophical Modes**: Choose different philosophical approaches

## Getting Started

1. Create a new note using the button in the sidebar
2. Write your thoughts in the editor
3. Save your note
4. Explore AI features or consult Professor Nihil

*The void is not merely absence, but the ground from which the sacred emerges.*`,
      tags: ['welcome', 'guide'],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };
    
    notes.push(welcomeNote);
    localStorage.setItem('notes', JSON.stringify(notes));
    renderNotesList();
    loadNote(welcomeNote.id);
  }
});

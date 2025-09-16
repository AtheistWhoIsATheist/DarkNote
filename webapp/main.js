// Simple chat logic for PHILOVOID webapp
const form = document.getElementById('message-form');
const input = document.getElementById('message-input');
const chat = document.getElementById('chat');

function addMessage(text, role) {
  const div = document.createElement('div');
  div.className = `message ${role}`;
  div.textContent = text;
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

form.addEventListener('submit', (e) => {
  e.preventDefault();
  const text = input.value.trim();
  if (!text) return;
  addMessage(text, 'user');
  input.value = '';

  // Placeholder assistant response
  setTimeout(() => {
    addMessage('Error: Could not reach the philosophical void. The connection to deeper understanding has been severed.', 'assistant');
  }, 500);
});

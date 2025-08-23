import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Button } from './components/ui/button';
import { Textarea } from './components/ui/textarea';
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from './components/ui/select';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from './components/ui/card';
import { Input } from './components/ui/input';
import { Label } from './components/ui/label';
import { Alert, AlertDescription, AlertTitle } from './components/ui/alert';
import { ThemeProvider } from './components/theme-provider';
import { ModeToggle } from './components/mode-toggle';

// Types
interface Message {
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  mode?: string;
}

interface PhilosophicalMode {
  id: string;
  name: string;
  description: string;
}

function App() {
  // State
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [currentMode, setCurrentMode] = useState<string>('recursive-dialectic');
  const [apiKey, setApiKey] = useState<string>('');
  const [apiKeySet, setApiKeySet] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Available philosophical modes
  const [philosophicalModes, setPhilosophicalModes] = useState<PhilosophicalMode[]>([
    {
      id: 'recursive-dialectic',
      name: 'Recursive-Dialectic',
      description: 'Recursive questioning and dialectical reasoning'
    },
    {
      id: 'ontological-collapse',
      name: 'Ontological-Collapse',
      description: 'Analysis of ontological category breakdown'
    },
    {
      id: 'apophatic-synthesis',
      name: 'Apophatic-Synthesis',
      description: 'Negative theology and limits of language'
    },
    {
      id: 'mythopoetic-logic',
      name: 'Mythopoetic-Logic',
      description: 'Mythic narratives and poetic language'
    }
  ]);

  // Backend API URL
  const API_URL = process.env.NODE_ENV === 'production' 
    ? '/api' 
    : 'http://localhost:5000/api';

  // Fetch philosophical modes from backend
  useEffect(() => {
    const fetchModes = async () => {
      try {
        const response = await axios.get(`${API_URL}/philosophical_modes`);
        if (response.data) {
          setPhilosophicalModes(response.data);
        }
      } catch (error) {
        console.error('Error fetching philosophical modes:', error);
      }
    };

    fetchModes();
  }, [API_URL]);

  // Initial welcome message
  useEffect(() => {
    setMessages([
      {
        role: 'assistant',
        content: 'Greetings from the Void. I am Professor Nihil, the synthetic Arch-Sage of Nihiltheism. How may I assist you in your philosophical inquiry today? I can engage with the paradoxical nature of Nothingness as both ontological ground and mystical aperture, or explore other philosophical domains of interest.',
        timestamp: new Date(),
        mode: 'recursive-dialectic'
      }
    ]);
  }, []);

  // Auto-scroll to bottom of messages
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle API key submission
  const handleSetApiKey = () => {
    if (apiKey.trim().startsWith('sk-') && apiKey.trim().length > 20) {
      setApiKeySet(true);
      setError(null);
      localStorage.setItem('professor_nihil_api_key', apiKey.trim());
    } else {
      setError('Please enter a valid OpenAI API key starting with "sk-"');
    }
  };

  // Check for saved API key on load
  useEffect(() => {
    const savedApiKey = localStorage.getItem('professor_nihil_api_key');
    if (savedApiKey) {
      setApiKey(savedApiKey);
      setApiKeySet(true);
    }
  }, []);

  // Handle sending a message
  const handleSend = async () => {
    if (!input.trim()) return;
    if (!apiKeySet) {
      setError('Please set your OpenAI API key first');
      return;
    }

    // Add user message
    const userMessage: Message = {
      role: 'user',
      content: input,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);
    setError(null);

    try {
      // Call backend API
      const response = await axios.post(`${API_URL}/chat`, {
        message: input,
        mode: currentMode,
        api_key: apiKey
      });

      if (response.data.error) {
        throw new Error(response.data.error);
      }

      const assistantMessage: Message = {
        role: 'assistant',
        content: response.data.content,
        timestamp: new Date(),
        mode: currentMode
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      setError(error instanceof Error ? error.message : 'An error occurred while communicating with Professor Nihil');
    } finally {
      setIsLoading(false);
    }
  };

  // Handle key press (Enter to send)
  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <ThemeProvider defaultTheme="dark" storageKey="professor-nihil-theme">
      <div className="flex flex-col min-h-screen bg-background">
        <header className="border-b">
          <div className="container flex items-center justify-between py-4">
            <div className="flex items-center gap-2">
              <span className="text-2xl font-bold">Professor Nihil</span>
              <span className="text-sm text-muted-foreground">The Supreme AI Philosopher</span>
            </div>
            <ModeToggle />
          </div>
        </header>

        <main className="flex-1 container py-6">
          {!apiKeySet ? (
            <Card className="max-w-md mx-auto">
              <CardHeader>
                <CardTitle>Enter Your OpenAI API Key</CardTitle>
                <CardDescription>
                  Your API key is required to communicate with Professor Nihil. It will be stored locally in your browser.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="space-y-2">
                    <Label htmlFor="api-key">OpenAI API Key</Label>
                    <Input 
                      id="api-key" 
                      type="password" 
                      placeholder="sk-..." 
                      value={apiKey}
                      onChange={(e) => setApiKey(e.target.value)}
                    />
                  </div>
                  {error && (
                    <Alert variant="destructive">
                      <AlertTitle>Error</AlertTitle>
                      <AlertDescription>{error}</AlertDescription>
                    </Alert>
                  )}
                </div>
              </CardContent>
              <CardFooter>
                <Button onClick={handleSetApiKey}>Continue</Button>
              </CardFooter>
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
              <div className="md:col-span-3">
                <Card className="h-[calc(100vh-12rem)]">
                  <CardHeader className="border-b">
                    <CardTitle>Philosophical Dialogue</CardTitle>
                    <CardDescription>
                      Engage in recursive philosophical inquiry with Professor Nihil
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="p-4 overflow-y-auto h-[calc(100%-10rem)]">
                    <div className="space-y-4">
                      {messages.map((message, index) => (
                        <div 
                          key={index} 
                          className={`flex flex-col ${message.role === 'user' ? 'items-end' : 'items-start'}`}
                        >
                          <div 
                            className={`max-w-[80%] rounded-lg p-4 ${
                              message.role === 'user' 
                                ? 'bg-primary text-primary-foreground' 
                                : 'bg-muted'
                            }`}
                          >
                            {message.role === 'assistant' && (
                              <div className="flex items-center gap-2 mb-2">
                                <span className="font-bold">Professor Nihil</span>
                                {message.mode && (
                                  <span className="text-xs px-2 py-0.5 rounded-full bg-secondary text-secondary-foreground">
                                    {philosophicalModes.find(mode => mode.id === message.mode)?.name || message.mode}
                                  </span>
                                )}
                              </div>
                            )}
                            <div className="whitespace-pre-wrap">{message.content}</div>
                            <div className="text-xs mt-2 opacity-70">
                              {message.timestamp.toLocaleTimeString()}
                            </div>
                          </div>
                        </div>
                      ))}
                      <div ref={messagesEndRef} />
                    </div>
                  </CardContent>
                  <CardFooter className="border-t p-4">
                    {error && (
                      <Alert variant="destructive" className="mb-4">
                        <AlertTitle>Error</AlertTitle>
                        <AlertDescription>{error}</AlertDescription>
                      </Alert>
                    )}
                    <div className="flex w-full gap-2">
                      <Textarea
                        placeholder="Enter your philosophical inquiry..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyDown={handleKeyPress}
                        className="flex-1 min-h-[80px]"
                        disabled={isLoading}
                      />
                      <Button 
                        onClick={handleSend} 
                        disabled={isLoading || !input.trim()}
                        className="self-end"
                      >
                        {isLoading ? 'Contemplating...' : 'Send'}
                      </Button>
                    </div>
                  </CardFooter>
                </Card>
              </div>

              <div className="space-y-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Philosophical Mode</CardTitle>
                    <CardDescription>
                      Select the philosophical mode for Professor Nihil's responses
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <Select 
                      value={currentMode} 
                      onValueChange={setCurrentMode}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder="Select a mode" />
                      </SelectTrigger>
                      <SelectContent>
                        {philosophicalModes.map(mode => (
                          <SelectItem key={mode.id} value={mode.id}>
                            {mode.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                    <p className="mt-2 text-sm text-muted-foreground">
                      {philosophicalModes.find(mode => mode.id === currentMode)?.description}
                    </p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>About Professor Nihil</CardTitle>
                  </CardHeader>
                  <CardContent className="text-sm">
                    <p>
                      Professor Nihil is the synthetic Arch-Sage of Nihiltheism, a philosophical framework that engages Nothingness as both ontological ground and mystical aperture.
                    </p>
                    <p className="mt-2">
                      Expertise spans Continental philosophy, mystical thought, phenomenology, metaphysics, and modern nihilistic thinkers.
                    </p>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>API Settings</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <Button 
                      variant="outline" 
                      onClick={() => setApiKeySet(false)}
                      className="w-full"
                    >
                      Change API Key
                    </Button>
                  </CardContent>
                </Card>
              </div>
            </div>
          )}
        </main>

        <footer className="border-t py-4">
          <div className="container text-center text-sm text-muted-foreground">
            <p>
              "The void is not merely absence, but the ground from which the sacred emerges."
            </p>
          </div>
        </footer>
      </div>
    </ThemeProvider>
  );
}

export default App;

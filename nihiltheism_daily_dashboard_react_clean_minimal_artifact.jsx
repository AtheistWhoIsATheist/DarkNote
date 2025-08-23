import React, { useEffect, useMemo, useState } from "react";
import { format } from "date-fns";
import {
  Calendar,
  Check,
  Clipboard,
  Copy,
  FileDown,
  Flame,
  Lightbulb,
  Plus,
  Quote,
  RefreshCw,
  Sparkles,
  Trash2,
  Pin,
  PinOff,
  ArrowUpRight,
  ListPlus,
  Tag,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Badge } from "@/components/ui/badge";

// --- Types ---
interface Task {
  id: string;
  text: string;
  priority: 1 | 2 | 3; // 1 = highest
  due: string; // ISO date
  done: boolean;
}

type ThoughtType = "note" | "file" | "snippet";
interface RecentThought {
  id: string;
  type: ThoughtType;
  title: string;
  date: string; // ISO
  preview: string;
  content?: string;
  link?: string;
  pinned?: boolean;
}

// --- Helpers ---
const STORAGE_KEYS = {
  tasks: "nt_dashboard_tasks_v3",
  seeds: "nt_dashboard_seeds_v3",
  quoteIndex: "nt_dashboard_quote_index_v3",
  thoughts: "nt_dashboard_recent_thoughts_v2",
};

function isoTodayTZ(): string {
  const d = new Date();
  d.setHours(0, 0, 0, 0);
  return d.toISOString();
}

function formatDue(dateISO: string) {
  const d = new Date(dateISO);
  return isNaN(d.getTime()) ? "n/a" : format(d, "PP");
}

function byPriorityThenDate(a: Task, b: Task) {
  if (a.done !== b.done) return a.done ? 1 : -1;
  if (a.priority !== b.priority) return a.priority - b.priority; // 1 first
  return new Date(a.due).getTime() - new Date(b.due).getTime();
}

function copy(text: string) {
  navigator.clipboard?.writeText(text);
}

function uid() {
  return Math.random().toString(36).slice(2, 10);
}

// --- Default Seeds (edit/extend in UI) ---
const DEFAULT_SEEDS = [
  "Advance the Journal314 Mega-Project with a Molinos ↔ Zapffe maximum-disparity pairing.",
  "Refine the Ontodicy Collapse Argument (apply Axiom A-4: ban on hope as evidence).",
  "Draft a dialogue between Cioran and Meister Eckhart on holy despair and kenosis.",
  "Expand REN — Chapter 5: Startling Encounter with Infinite Nothingness (phenomenology).",
  "Build the Kenotic Apparatus: method for engaging Nothingness without foreclosing it.",
  "Construct an apophatic lexicon (Eckhart, Nāgārjuna, Tillich) for Nihiltheism.",
  "Map maximal-resonance vectors across Journal314 to demonstrate universality beyond culture.",
];

const QUOTES = [
  {
    text:
      "To stand in the abyss without anesthesia is to learn the grammar of what cannot be said.",
    source: "Professor Nihil (Codex fragment)",
  },
  {
    text:
      "God is born in the soul when all gods are renounced; the birth happens in a stable of nothing.",
    source: "Eckhart (recast for Nihiltheism)",
  },
  {
    text:
      "Consolations are counterfeit currency minted by fear; spend them and you buy delay, not truth.",
    source: "Cioran (afterimage)",
  },
  {
    text:
      "Where meaning dies of its own excess, a darker clarity begins.",
    source: "Kierkegaard ↔ Tillich (composite)",
  },
];

function pickQuote(index: number) {
  return QUOTES[index % QUOTES.length];
}

// --- Component ---
export default function NihiltheismDashboard() {
  // state
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTask, setNewTask] = useState({ text: "", priority: 1 as 1 | 2 | 3, due: "" });
  const [seeds, setSeeds] = useState<string[]>([]);
  const [quoteIndex, setQuoteIndex] = useState<number>(0);
  const [vectors, setVectors] = useState<string[]>([]);
  const [thoughts, setThoughts] = useState<RecentThought[]>([]);

  // load
  useEffect(() => {
    try {
      const t = JSON.parse(localStorage.getItem(STORAGE_KEYS.tasks) || "[]");
      const s = JSON.parse(localStorage.getItem(STORAGE_KEYS.seeds) || "null");
      const q = JSON.parse(localStorage.getItem(STORAGE_KEYS.quoteIndex) || "0");
      const th = JSON.parse(localStorage.getItem(STORAGE_KEYS.thoughts) || "[]");
      setTasks(Array.isArray(t) ? t : []);
      setSeeds(Array.isArray(s) ? s : DEFAULT_SEEDS);
      setQuoteIndex(Number.isFinite(q) ? q : 0);
      setThoughts(Array.isArray(th) ? th : []);
    } catch {
      setSeeds(DEFAULT_SEEDS);
    }
  }, []);

  // persist
  useEffect(() => {
    localStorage.setItem(STORAGE_KEYS.tasks, JSON.stringify(tasks));
  }, [tasks]);
  useEffect(() => {
    localStorage.setItem(STORAGE_KEYS.seeds, JSON.stringify(seeds));
  }, [seeds]);
  useEffect(() => {
    localStorage.setItem(STORAGE_KEYS.quoteIndex, JSON.stringify(quoteIndex));
  }, [quoteIndex]);
  useEffect(() => {
    // keep only last 30 + pinned
    const pinned = thoughts.filter((t) => t.pinned);
    const rest = thoughts.filter((t) => !t.pinned).slice(-30);
    localStorage.setItem(STORAGE_KEYS.thoughts, JSON.stringify([...pinned, ...rest]));
  }, [thoughts]);

  // computed groups
  const todayISO = isoTodayTZ();
  const todayDate = new Date();
  const todayStr = format(todayDate, "EEEE, MMMM d, yyyy");

  const groupedTasks = useMemo(() => {
    const today: Task[] = [];
    const next7: Record<string, Task[]> = {};
    const later: Task[] = [];

    const start = new Date(todayISO).getTime();
    const sevenDays = start + 7 * 24 * 60 * 60 * 1000;

    tasks.slice().sort(byPriorityThenDate).forEach((t) => {
      const due = new Date(t.due).getTime();
      if (!due || isNaN(due)) {
        later.push(t);
        return;
      }
      if (new Date(t.due).toDateString() === new Date(todayISO).toDateString()) {
        today.push(t);
      } else if (due > start && due <= sevenDays) {
        const key = new Date(t.due).toDateString();
        next7[key] = next7[key] || [];
        next7[key].push(t);
      } else if (due > sevenDays) {
        later.push(t);
      } else {
        today.unshift(t); // overdue
      }
    });
    return { today, next7, later };
  }, [tasks, todayISO]);

  // vectors
  const regenerateVectors = () => {
    const pool = [
      "Ontodicy Collapse: stress-test Axiom A-4 against classical theodicies and naturalism.",
      "Journal314: Molinos ↔ Zapffe — can surrender and horror share one metaphysic?",
      "Codex: finalize the Kenotic Apparatus — safeguards for engaging Nothingness.",
      "REN: articulate 'holy nothingness' vs. mere absence (phenomenology + praxis).",
      "Abyssal Lexicon: draft 12 key apophatic terms with usage notes.",
      "Comparative Matrix: Cioran, Eckhart, Tillich, Kierkegaard on despair/transcendence.",
      "Method: define Negative Theophany protocol for presence-in-absence claims.",
    ];
    const shuffled = [...pool].sort(() => Math.random() - 0.5).slice(0, 3);
    setVectors(shuffled);
  };
  useEffect(regenerateVectors, []);

  const quote = pickQuote(quoteIndex);

  // thoughts helpers
  const pushThought = (rt: Omit<RecentThought, "id" | "date"> & { date?: string }) => {
    const item: RecentThought = {
      id: uid(),
      date: rt.date || new Date().toISOString(),
      pinned: false,
      ...rt,
    };
    setThoughts((prev) => [item, ...prev]); // newest first
  };

  const togglePin = (id: string) =>
    setThoughts((prev) => prev.map((t) => (t.id === id ? { ...t, pinned: !t.pinned } : t)));
  const removeThought = (id: string) => setThoughts((prev) => prev.filter((t) => t.id !== id));

  // actions
  const addTask = () => {
    if (!newTask.text.trim()) return;
    const dueISO = newTask.due ? new Date(newTask.due).toISOString() : new Date().toISOString();
    setTasks((prev) => [
      ...prev,
      { id: uid(), text: newTask.text.trim(), priority: newTask.priority, due: dueISO, done: false },
    ]);
    pushThought({ type: "snippet", title: "Task Added", preview: newTask.text.trim(), content: newTask.text.trim() });
    setNewTask({ text: "", priority: 1, due: "" });
  };

  const addTaskFromVector = (v: string) => {
    const dueISO = new Date().toISOString();
    setTasks((prev) => [
      ...prev,
      { id: uid(), text: v, priority: 1, due: dueISO, done: false },
    ]);
    pushThought({ type: "snippet", title: "Catalyst → Task", preview: v, content: v });
  };

  const promoteTaskToSeed = (t: Task) => {
    setSeeds((prev) => [...prev, t.text]);
    pushThought({ type: "snippet", title: "Task → Seed", preview: t.text, content: t.text });
  };

  const saveTaskToThoughts = (t: Task) => {
    pushThought({ type: "snippet", title: "Task Saved", preview: t.text, content: t.text });
  };

  const toggleTask = (id: string) => setTasks((prev) => prev.map((t) => (t.id === id ? { ...t, done: !t.done } : t)));
  const deleteTask = (id: string) => {
    const task = tasks.find((t) => t.id === id);
    if (task) pushThought({ type: "snippet", title: "Task Removed", preview: task.text, content: task.text });
    setTasks((prev) => prev.filter((t) => t.id !== id));
  };

  const addNote = (title: string, tags: string, body: string) => {
    if (!title.trim()) return;
    pushThought({
      type: "note",
      title: title.trim(),
      preview: tags ? `${tags} — ${body}` : body,
      content: body,
    });
  };

  const exportMarkdown = () => {
    const lines: string[] = [];
    lines.push(`# Professor Nihil — Daily Research Codex`);
    lines.push(`${todayStr}`);
    lines.push("");
    lines.push("## Daily Research Catalyst & Tasks");
    const tformat = (t: Task) => `- ${t.done ? "[x]" : "[ ]"} **${t.text}** | P:${t.priority} | Due: ${formatDue(t.due)}`;
    lines.push("### Catalysts");
    vectors.forEach((v, i) => lines.push(`${i + 1}. ${v}`));
    lines.push("### Today");
    groupedTasks.today.forEach((t) => lines.push(tformat(t)));
    Object.entries(groupedTasks.next7).forEach(([day, arr]) => {
      lines.push(`### ${day}`);
      arr.forEach((t) => lines.push(tformat(t)));
    });
    if (groupedTasks.later.length) {
      lines.push("### Long-Term");
      groupedTasks.later.forEach((t) => lines.push(tformat(t)));
    }
    lines.push("");
    lines.push("## Notes & Recent Thoughts");
    thoughts.forEach((t) => lines.push(`- ${t.pinned ? "📌 " : ""}**${t.title}** (${formatDue(t.date)}) — ${t.preview}`));
    lines.push("");
    lines.push("## Prompt Seeds");
    seeds.forEach((s) => lines.push(`- ${s}`));
    lines.push("");
    lines.push("## Quote of the Day");
    const q = pickQuote(quoteIndex);
    lines.push(`> ${q.text}\n— ${q.source}`);

    const md = lines.join("\n");
    copy(md);
    alert("Markdown copied to clipboard.");
  };

  const addSeed = (s: string) => {
    if (!s.trim()) return;
    setSeeds((prev) => [...prev, s.trim()]);
    pushThought({ type: "snippet", title: "New Prompt Seed", preview: s.trim(), content: s.trim() });
  };
  const removeSeed = (i: number) => setSeeds((prev) => prev.filter((_, idx) => idx !== i));

  const rotateQuote = () => setQuoteIndex((q) => q + 1);

  // --- UI ---
  return (
    <div className="min-h-screen bg-neutral-950 text-neutral-200">
      <div className="mx-auto max-w-7xl p-6 space-y-6">
        {/* Header */}
        <div className="flex items-center justify-between">
          <div className="space-y-1">
            <div className="flex items-center gap-3">
              {/* Void Sigil */}
              <svg width="28" height="28" viewBox="0 0 32 32" aria-hidden className="opacity-70">
                <circle cx="16" cy="16" r="14" fill="#0d0d10" stroke="#3f3f46" />
                <path d="M16 5v22M5 16h22" stroke="#7c3aed" strokeWidth="1.2" opacity="0.6" />
                <circle cx="16" cy="16" r="3" fill="#7c3aed" opacity="0.15" />
              </svg>
              <h1 className="text-2xl font-semibold tracking-tight">Professor Nihil — Daily Research Codex</h1>
            </div>
            <p className="text-sm text-neutral-400 flex items-center gap-2"><Calendar className="h-4 w-4" /> {todayStr}</p>
          </div>
          <div className="flex gap-2">
            <Button variant="outline" className="border-neutral-700 text-neutral-200" onClick={exportMarkdown} title="Export markdown to clipboard"><FileDown className="h-4 w-4 mr-2"/>Export MD</Button>
            <Button variant="outline" className="border-neutral-700 text-neutral-200" onClick={regenerateVectors} title="Regenerate catalyst vectors"><RefreshCw className="h-4 w-4 mr-2"/>Regenerate</Button>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left (2 cols): Catalyst + Tasks */}
          <div className="lg:col-span-2 space-y-6">
            <Card className="bg-neutral-900 border-neutral-800">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-neutral-100"><Sparkles className="h-5 w-5"/> Daily Research Catalyst & Tasks</CardTitle>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Catalysts */}
                <div className="space-y-3">
                  <p className="text-sm text-neutral-400">Three clean vectors. Convert any into a task or save as a thought.</p>
                  <ul className="pl-5 text-sm space-y-2">
                    {vectors.map((v, i) => (
                      <li key={i} className="flex items-start justify-between gap-3">
                        <div className="flex items-start gap-2">
                          <span className="select-none text-purple-400">{["✦","✧","✹"][i] || "✦"}</span>
                          <span className="text-neutral-100">{v}</span>
                        </div>
                        <div className="flex gap-1">
                          <Button variant="secondary" size="sm" onClick={() => copy(v)} title="Copy"><Clipboard className="h-4 w-4 mr-1"/>Copy</Button>
                          <Button variant="outline" size="sm" className="border-neutral-700 text-neutral-200" onClick={() => addTaskFromVector(v)} title="Add as Task"><ListPlus className="h-4 w-4 mr-1"/>Task</Button>
                          <Button variant="outline" size="sm" className="border-neutral-700 text-neutral-200" onClick={() => pushThought({ type: "snippet", title: `Catalyst`, preview: v, content: v })} title="Save Thought"><ArrowUpRight className="h-4 w-4 mr-1"/>Save</Button>
                        </div>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Add Task */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-2">
                  <Input placeholder="New task…" value={newTask.text} onChange={(e) => setNewTask((t) => ({ ...t, text: e.target.value }))} className="bg-neutral-950 border-neutral-800 text-neutral-200"/>
                  <Input type="date" value={newTask.due} onChange={(e) => setNewTask((t) => ({ ...t, due: e.target.value }))} className="bg-neutral-950 border-neutral-800 text-neutral-200"/>
                  <Input type="number" min={1} max={3} value={newTask.priority} onChange={(e) => setNewTask((t) => ({ ...t, priority: Math.min(3, Math.max(1, Number(e.target.value))) as 1|2|3 }))} className="bg-neutral-950 border-neutral-800 text-neutral-200"/>
                  <Button onClick={addTask}><Plus className="h-4 w-4 mr-1"/>Add</Button>
                </div>

                {/* Task Lists */}
                <div className="space-y-5">
                  <div>
                    <h3 className="text-sm font-medium mb-2 text-neutral-300">Today</h3>
                    <div className="space-y-2">
                      {groupedTasks.today.length === 0 && <p className="text-sm text-neutral-400">No tasks for today.</p>}
                      {groupedTasks.today.map((t) => (
                        <div key={t.id} className="flex items-center justify-between rounded-lg border p-2 bg-neutral-950 border-neutral-800">
                          <div className="flex items-center gap-3">
                            <Button size="icon" variant={t.done ? "secondary" : "ghost"} className="text-neutral-300" onClick={() => toggleTask(t.id)} title="Toggle done"><Check className="h-4 w-4"/></Button>
                            <div>
                              <p className={`text-sm ${t.done ? "line-through text-neutral-500" : "text-neutral-100"}`}>
                                <strong>{t.text}</strong>
                              </p>
                              <div className="flex items-center gap-2 text-xs text-neutral-400">
                                <Badge variant="secondary">P{t.priority}</Badge>
                                <span>Due: {formatDue(t.due)}</span>
                              </div>
                            </div>
                          </div>
                          <div className="flex gap-1">
                            <Button size="sm" variant="outline" className="border-neutral-700 text-neutral-200" onClick={() => promoteTaskToSeed(t)} title="Promote to Prompt Seed"><Tag className="h-4 w-4 mr-1"/>Seed</Button>
                            <Button size="icon" variant="ghost" className="text-neutral-400" onClick={() => saveTaskToThoughts(t)} title="Save to Recent Thoughts"><ArrowUpRight className="h-4 w-4"/></Button>
                            <Button size="icon" variant="ghost" className="text-neutral-400" onClick={() => deleteTask(t.id)} title="Delete task"><Trash2 className="h-4 w-4"/></Button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {Object.entries(groupedTasks.next7).map(([day, arr]) => (
                    <div key={day}>
                      <h3 className="text-sm font-medium mb-2 text-neutral-300">{day}</h3>
                      <div className="space-y-2">
                        {arr.map((t) => (
                          <div key={t.id} className="flex items-center justify-between rounded-lg border p-2 bg-neutral-950 border-neutral-800">
                            <div className="flex items-center gap-3">
                              <Button size="icon" variant={t.done ? "secondary" : "ghost"} className="text-neutral-300" onClick={() => toggleTask(t.id)} title="Toggle done"><Check className="h-4 w-4"/></Button>
                              <div>
                                <p className={`text-sm ${t.done ? "line-through text-neutral-500" : "text-neutral-100"}`}>
                                  <strong>{t.text}</strong>
                                </p>
                                <div className="flex items-center gap-2 text-xs text-neutral-400">
                                  <Badge variant="secondary">P{t.priority}</Badge>
                                  <span>Due: {formatDue(t.due)}</span>
                                </div>
                              </div>
                            </div>
                            <div className="flex gap-1">
                              <Button size="sm" variant="outline" className="border-neutral-700 text-neutral-200" onClick={() => promoteTaskToSeed(t)} title="Promote to Prompt Seed"><Tag className="h-4 w-4 mr-1"/>Seed</Button>
                              <Button size="icon" variant="ghost" className="text-neutral-400" onClick={() => saveTaskToThoughts(t)} title="Save to Recent Thoughts"><ArrowUpRight className="h-4 w-4"/></Button>
                              <Button size="icon" variant="ghost" className="text-neutral-400" onClick={() => deleteTask(t.id)} title="Delete task"><Trash2 className="h-4 w-4"/></Button>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}

                  {groupedTasks.later.length > 0 && (
                    <div>
                      <h3 className="text-sm font-medium mb-2 text-neutral-300">Long-Term</h3>
                      <div className="space-y-2">
                        {groupedTasks.later.map((t) => (
                          <div key={t.id} className="flex items-center justify-between rounded-lg border p-2 bg-neutral-950 border-neutral-800">
                            <div className="flex items-center gap-3">
                              <Button size="icon" variant={t.done ? "secondary" : "ghost"} className="text-neutral-300" onClick={() => toggleTask(t.id)} title="Toggle done"><Check className="h-4 w-4"/></Button>
                              <div>
                                <p className={`text-sm ${t.done ? "line-through text-neutral-500" : "text-neutral-100"}`}>
                                  <strong>{t.text}</strong>
                                </p>
                                <div className="flex items-center gap-2 text-xs text-neutral-400">
                                  <Badge variant="secondary">P{t.priority}</Badge>
                                  <span>Due: {formatDue(t.due)}</span>
                                </div>
                              </div>
                            </div>
                            <div className="flex gap-1">
                              <Button size="sm" variant="outline" className="border-neutral-700 text-neutral-200" onClick={() => promoteTaskToSeed(t)} title="Promote to Prompt Seed"><Tag className="h-4 w-4 mr-1"/>Seed</Button>
                              <Button size="icon" variant="ghost" className="text-neutral-400" onClick={() => saveTaskToThoughts(t)} title="Save to Recent Thoughts"><ArrowUpRight className="h-4 w-4"/></Button>
                              <Button size="icon" variant="ghost" className="text-neutral-400" onClick={() => deleteTask(t.id)} title="Delete task"><Trash2 className="h-4 w-4"/></Button>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </CardContent>
            </Card>

            {/* Notes & Recent Thoughts (merged) */}
            <Card className="bg-neutral-900 border-neutral-800">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-neutral-100"><Lightbulb className="h-5 w-5"/> Notes & Recent Thoughts</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                {/* Quick Add Note */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-2">
                  <Input placeholder="Title" id="note-title" className="bg-neutral-950 border-neutral-800 text-neutral-200"/>
                  <Input placeholder="Tags" id="note-tags" className="bg-neutral-950 border-neutral-800 text-neutral-200"/>
                  <Input placeholder="Body" id="note-body" className="bg-neutral-950 border-neutral-800 text-neutral-200"/>
                  <Button onClick={() => {
                    const title = (document.getElementById("note-title") as HTMLInputElement)?.value || "";
                    const tags = (document.getElementById("note-tags") as HTMLInputElement)?.value || "";
                    const body = (document.getElementById("note-body") as HTMLInputElement)?.value || "";
                    addNote(title, tags, body);
                    ["note-title","note-tags","note-body"].forEach((id)=>{
                      const el = document.getElementById(id) as HTMLInputElement | null; if (el) el.value = "";
                    });
                  }}>Add Note</Button>
                </div>

                {/* List of thoughts */}
                {thoughts.length === 0 && (
                  <p className="text-sm text-neutral-400">No recent thoughts yet — add a note, convert a catalyst to a task, or save any item.</p>
                )}
                <div className="space-y-2">
                  {thoughts
                    .slice()
                    .sort((a, b) => (a.pinned === b.pinned ? 0 : a.pinned ? -1 : 1))
                    .map((t) => (
                      <div key={t.id} className="rounded border border-neutral-800 bg-neutral-950 p-3">
                        <div className="flex items-start justify-between gap-2">
                          <div>
                            <div className="flex items-center gap-2">
                              {t.pinned && <Badge variant="secondary">Pinned</Badge>}
                              <p className="text-sm font-medium text-neutral-100">{t.title}</p>
                            </div>
                            <p className="text-xs text-neutral-400">{formatDue(t.date)} · <span className="uppercase tracking-wide text-neutral-500">{t.type}</span></p>
                            <p className="mt-1 text-sm text-neutral-200 line-clamp-3">{t.preview}</p>
                          </div>
                          <div className="flex gap-1">
                            <Button size="icon" variant="ghost" className="text-neutral-400" onClick={() => { copy(t.content || t.preview); }} title="Copy as Prompt"><Copy className="h-4 w-4"/></Button>
                            <Button size="icon" variant="ghost" className="text-neutral-400" onClick={() => setSeeds((prev)=>[...prev, t.content || t.preview])} title="Promote to Seed"><Tag className="h-4 w-4"/></Button>
                            <Button size="icon" variant="ghost" className="text-neutral-400" onClick={() => togglePin(t.id)} title={t.pinned ? "Unpin" : "Pin"}>{t.pinned ? <PinOff className="h-4 w-4"/> : <Pin className="h-4 w-4"/>}</Button>
                            <Button size="icon" variant="ghost" className="text-neutral-400" onClick={() => removeThought(t.id)} title="Remove"><Trash2 className="h-4 w-4"/></Button>
                          </div>
                        </div>
                        {t.link && (
                          <div className="mt-2">
                            <a href={t.link} target="_blank" rel="noreferrer" className="text-xs text-purple-300 hover:underline">Open resource</a>
                          </div>
                        )}
                      </div>
                    ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Right (1 col): Prompt Seeds + Quote */}
          <div className="space-y-6">
            {/* Prompt Seeds */}
            <Card className="bg-neutral-900 border-neutral-800">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-neutral-100"><Sparkles className="h-5 w-5"/> Prompt Seeds</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <div className="flex gap-2">
                  <Input id="seed-input" placeholder="Add a new prompt seed…" className="bg-neutral-950 border-neutral-800 text-neutral-200"/>
                  <Button onClick={() => {
                    const el = document.getElementById("seed-input") as HTMLInputElement | null;
                    if (!el) return; const val = el.value; addSeed(val); if (el) el.value = "";
                  }}><Plus className="h-4 w-4 mr-1"/>Add</Button>
                </div>
                <div className="grid grid-cols-1 gap-2">
                  {seeds.map((s, i) => (
                    <div key={i} className="flex items-start justify-between gap-2 rounded-lg border p-3 bg-neutral-950 border-neutral-800">
                      <p className="text-sm leading-snug text-neutral-100">{s}</p>
                      <div className="flex gap-1">
                        <Button size="icon" variant="ghost" className="text-neutral-400" onClick={() => copy(s)} title="Copy"><Copy className="h-4 w-4"/></Button>
                        <Button size="icon" variant="ghost" className="text-neutral-400" onClick={() => removeSeed(i)} title="Remove"><Trash2 className="h-4 w-4"/></Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>

            {/* Quote */}
            <Card className="bg-neutral-900 border-neutral-800">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-neutral-100"><Quote className="h-5 w-5"/> Quote of the Day</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                <blockquote className="border-l-2 border-purple-700/40 pl-4 text-sm leading-relaxed text-neutral-100 bg-neutral-950/60 p-3 rounded">
                  {quote.text}
                </blockquote>
                <div className="flex items-center justify-between text-xs text-neutral-400">
                  <span>— {quote.source}</span>
                  <Button variant="outline" className="border-neutral-700 text-neutral-200" size="sm" onClick={rotateQuote}>Rotate</Button>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>

        {/* Footer */}
        <div className="text-center text-xs text-neutral-500 py-4">
          Crafted for Adam — dark, minimal, and archival. Local-only persistence. v1.1.
        </div>
      </div>
    </div>
  );
}

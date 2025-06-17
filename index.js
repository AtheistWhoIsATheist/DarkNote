npm sintall
/cd C:\Users\adamm\OneDrive\.vscode\index.js* . && rm -rf "$APP-tmp"

echo "• Removing boilerplate src"
rm -rf src/*

echo "• Writing source files"
cat > src/db.js <<'EOF'
import Dexie from 'dexie';
export const db = new Dexie('QuickNoteDB');
db.version(1).stores({
  notes: '++id, title, content, tags, createdAt, updatedAt'
});
EOF

cat > src/contexts/NotesContext.js <<'EOF'
import React, { createContext, useReducer, useEffect } from 'react';
import { db } from '../db';

const initialState = { notes: [], searchTerm: '', filterTags: [] };
export const NotesContext = createContext();

function reducer(state, action) {
  switch (action.type) {
    case 'SET_NOTES':        return { ...state, notes: action.notes };
    case 'ADD_NOTE':         return { ...state, notes: [...state.notes, action.note] };
    case 'UPDATE_NOTE':      return { ...state, notes: state.notes.map(n => n.id === action.note.id ? { ...n, ...action.note } : n) };
    case 'DELETE_NOTE':      return { ...state, notes: state.notes.filter(n => n.id !== action.id) };
    case 'SET_SEARCH_TERM':  return { ...state, searchTerm: action.searchTerm };
    case 'SET_FILTER_TAGS':  return { ...state, filterTags: action.filterTags };
    default: throw new Error('Unknown action');
  }
}

export const NotesProvider = ({ children }) => {
  const [state, dispatch] = useReducer(reducer, initialState);

  useEffect(() => { db.notes.toArray().then(n => dispatch({ type: 'SET_NOTES', notes: n.sort((a,b)=>b.updatedAt-a.updatedAt) })); }, []);

  const addNote    = async d => { const t=Date.now(); const id=await db.notes.add({ ...d, createdAt:t, updatedAt:t }); dispatch({ type:'ADD_NOTE', note:{...d,id,createdAt:t,updatedAt:t} }); };
  const updateNote = async d => { const u=Date.now(); await db.notes.update(d.id,{ ...d,updatedAt:u }); dispatch({ type:'UPDATE_NOTE', note:{...d,updatedAt:u} }); };
  const deleteNote = async id=> { await db.notes.delete(id); dispatch({ type:'DELETE_NOTE', id }); };

  return <NotesContext.Provider value={{ ...state, addNote, updateNote, deleteNote,
    setSearchTerm:t=>dispatch({type:'SET_SEARCH_TERM',searchTerm:t}),
    setFilterTags:t=>dispatch({type:'SET_FILTER_TAGS',filterTags:t}) }}>{children}</NotesContext.Provider>;
};
EOF

cat > src/components/Header.js <<'EOF'
import React from 'react';
export default React.memo(() => <header className="header"><h1>QuickNote</h1></header>);
EOF

cat > src/components/SearchFilterControls.js <<'EOF'
import React, { useContext } from 'react';
import { NotesContext } from '../contexts/NotesContext';

export default React.memo(() => {
  const { notes, searchTerm, filterTags, setSearchTerm, setFilterTags } = useContext(NotesContext);
  const allTags = [...new Set(notes.flatMap(n => n.tags || []))];
  const toggle = t => setFilterTags(filterTags.includes(t) ? filterTags.filter(x=>x!==t) : [...filterTags,t]);
  return (
    <div className="controls">
      <input className="search-input" placeholder="Search…" value={searchTerm} onChange={e=>setSearchTerm(e.target.value)} />
      <div className="tag-filter">
        {allTags.map(t=>(
          <button key={t} onClick={()=>toggle(t)} className={`tag-button ${filterTags.includes(t)?'active':''}`}>{t}</button>
        ))}
      </div>
    </div>
  );
});
EOF

cat > src/components/InputArea.js <<'EOF'
import React, { useState, useContext } from 'react';
import { NotesContext } from '../contexts/NotesContext';

export default React.memo(() => {
  const { addNote } = useContext(NotesContext);
  const [title,setTitle]=useState(''); const [content,setContent]=useState(''); const [tags,setTags]=useState('');
  const save=()=>{ if(!title.trim()&&!content.trim())return; const t=tags.split(',').map(x=>x.trim()).filter(Boolean); addNote({title,content,tags:t}); setTitle('');setContent('');setTags(''); };
  return (
    <div className="input-area">
      <input className="title-input" placeholder="Title" value={title} onChange={e=>setTitle(e.target.value)} />
      <textarea className="content-input" placeholder="Your note…" value={content} onChange={e=>setContent(e.target.value)} />
      <input className="tags-input" placeholder="Tags comma-separated" value={tags} onChange={e=>setTags(e.target.value)} />
      <button className="button" onClick={save}>Add Note</button>
    </div>);
});
EOF

cat > src/components/NoteItem.js <<'EOF'
import React, { useState, useContext } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { NotesContext } from '../contexts/NotesContext';

export default React.memo(({ note }) => {
  const { notes, updateNote, deleteNote } = useContext(NotesContext);
  const [edit,setEdit]=useState(false); const [ttl,setTtl]=useState(note.title); const [cnt,setCnt]=useState(note.content); const [tg,setTg]=useState((note.tags||[]).join(', '));
  const links=note.title?notes.filter(n=>n.content?.includes(`[[${note.title}]]`)):[];
  const exportMd=()=>{const b=new Blob([`# ${note.title}\n\n${note.content}`],{type:'text/markdown'});const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=`${(note.title||'note').replace(/[^a-z0-9]/gi,'_')}.md`;a.click();URL.revokeObjectURL(a.href);};
  if(edit) return(
    <div className="note-item">
      <input className="title-input" value={ttl} onChange={e=>setTtl(e.target.value)} />
      <textarea className="content-input" value={cnt} onChange={e=>setCnt(e.target.value)} />
      <input className="tags-input" value={tg} onChange={e=>setTg(e.target.value)} />
      <div className="note-item-buttons">
        <button className="button" onClick={()=>{updateNote({id:note.id,title:ttl,content:cnt,tags:tg.split(',').map(x=>x.trim()).filter(Boolean)});setEdit(false);}}>Save</button>
        <button className="button" onClick={()=>setEdit(false)}>Cancel</button>
      </div>
    </div>);
  return (
    <div className="note-item">
      <h3>{note.title}</h3>
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{note.content}</ReactMarkdown>
      {note.tags?.length ? <div className="tags-list">{note.tags.map(t=><span key={t} className="tag-item">{t}</span>)}</div>:null}
      {links.length? <div className="backlinks"><strong>Backlinks:</strong><ul>{links.map(l=><li key={l.id}>{l.title}</li>)}</ul></div>:null}
      <div className="note-item-buttons">
        <button className="button" onClick={()=>setEdit(true)}>Edit</button>
        <button className="button" onClick={()=>deleteNote(note.id)}>Delete</button>
        <button className="button" onClick={exportMd}>Export</button>
      </div>
    </div>);
});
EOF

cat > src/components/NoteList.js <<'EOF'
import React, { useContext, useMemo } from 'react';
import { FixedSizeList as List } from 'react-window';
import { NotesContext } from '../contexts/NotesContext';
import NoteItem from './NoteItem';

export default React.memo(() => {
  const { notes, searchTerm, filterTags } = useContext(NotesContext);
  const filtered = useMemo(()=>notes.filter(n=>{
    const s=searchTerm.toLowerCase();
    const okS = !s || (n.title||'').toLowerCase().includes(s) || (n.content||'').toLowerCase().includes(s);
    const okT = !filterTags.length || (n.tags && filterTags.every(t=>n.tags.includes(t)));
    return okS && okT;
  }),[notes,searchTerm,filterTags]).sort((a,b)=>b.updatedAt-a.updatedAt);

  const h=Math.min(filtered.length*180,600);
  return (
    <List height={h} itemCount={filtered.length} itemSize={180} width="100%">
      {({index,style})=><div style={style}><NoteItem note={filtered[index]} /></div>}
    </List>);
});
EOF

cat > src/App.js <<'EOF'
import React from 'react';
import Header from './components/Header';
import SearchFilterControls from './components/SearchFilterControls';
import InputArea from './components/InputArea';
import NoteList from './components/NoteList';
import './App.css';

export default function App(){
  return (
    <div className="app-container">
      <Header/>
      <SearchFilterControls/>
      <InputArea/>
      <div className="note-list-container"><NoteList/></div>
    </div>);
}
EOF

cat > src/App.css <<'EOF'
body,html,#root{margin:0;height:100%;background:#121212;color:#fff;font-family:sans-serif;}
.app-container{max-width:414px;margin:0 auto;display:flex;flex-direction:column;height:100%;}
.header{padding:10px;background:#1e1e1e;border-bottom:1px solid #333;text-align:center;}
.controls{padding:10px;background:#1e1e1e;border-bottom:1px solid #333;}
.search-input{width:100%;padding:8px;margin-bottom:8px;background:#333;border:none;color:#fff;}
.tag-filter{display:flex;flex-wrap:wrap;}
.tag-button{margin:2px;padding:5px 8px;background:#333;color:#ccc;border:none;border-radius:4px;cursor:pointer;}
.tag-button.active{background:#555;color:#fff;}
.input-area{padding:10px;background:#1e1e1e;border-bottom:1px solid #333;display:flex;flex-direction:column;}
.title-input,.content-input,.tags-input{padding:8px;margin-bottom:8px;background:#333;border:none;color:#fff;}
.button{padding:8px 12px;background:#3a3a3a;border:none;color:#fff;cursor:pointer;margin-right:5px;margin-top:5px;}
.note-list-container{flex:1;overflow-y:auto;}
.note-item{padding:10px;border-bottom:1px solid #333;}
.note-item h3{margin:0 0 5px;}
.tags-list{margin-top:5px;}
.tag-item{display:inline-block;margin-right:5px;padding:2px 6px;background:#333;border-radius:4px;font-size:.85em;}
.backlinks{margin-top:10px;border-top:1px solid #444;padding-top:5px;}
.note-item-buttons{margin-top:10px;}
EOF

echo "• Installing extra dependencies"
npm install dexie react-markdown remark-gfm react-window

echo "• Launching development server"
npm start
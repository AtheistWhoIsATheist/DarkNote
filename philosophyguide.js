import React, { useState, useEffect } from 'react';
import { Camera } from 'lucide-react';

// Hard-coded data to ensure visualization works
const philosophicalData = [
  { id: 1, thinker: "Jesus (New Testament)", tradition: "Early Christianity", thematicCategory: "Existential Dread & Renunciation", keyQuote: "Whoever finds his life will lose it…", contribution: "Emphasizes the paradox of losing the self to find eternal meaning." },
  { id: 2, thinker: "Jesus", tradition: "Early Christianity", thematicCategory: "Duality / Ethical Conflict", keyQuote: "No one can serve two masters…", contribution: "Illustrates the conflict between worldly attachments and divine service." },
  { id: 3, thinker: "Augustine", tradition: "Christian Philosophy", thematicCategory: "Existential Anxiety & Conflict", keyQuote: "Every vain hope became worthless to me.", contribution: "Highlights the internal division between spiritual aspirations and earthly desires." },
  { id: 4, thinker: "Augustine", tradition: "Christian Philosophy", thematicCategory: "Dual Nature of Humans", keyQuote: "Thus did my two wills … struggle within me.", contribution: "Direct evidence of the internal conflict between carnal and spiritual aspects." },
  { id: 5, thinker: "Miguel de Molinos", tradition: "Christian Mysticism", thematicCategory: "Mysticism & Ego Death", keyQuote: "This Nothing... is the means by which the Lord works wonders in thy Soul.", contribution: "Proposes that the experience of Nothingness is essential for divine union." },
  { id: 6, thinker: "Leo Tolstoy", tradition: "Russian Orthodox / Existentialism", thematicCategory: "Existential Struggle & Absurdity", keyQuote: "A man who lives… must be ready at any moment to endure violence…", contribution: "Expresses the futility of clinging to ephemeral meaning." },
  { id: 7, thinker: "GK Chesterton", tradition: "Christian Apologetics", thematicCategory: "The Struggle for Meaning", keyQuote: "Implicit in his parables about faith and the kingdom of God.", contribution: "Affirms that even amid absurdity, the quest for the divine persists." },
  { id: 8, thinker: "C.S. Lewis", tradition: "Christian Apologetics", thematicCategory: "Transcendent Re-Imagining", keyQuote: "Referencing the transformation of sorrow into spiritual insight.", contribution: "Suggests that personal suffering can become a gateway to uncovering deeper truths." },
  { id: 9, thinker: "Kierkegaard", tradition: "Existential Philosophy", thematicCategory: "Existential Dread & The Divided Self", keyQuote: "Despair is the sickness unto death…", contribution: "Captures the internal agony of not being true to one's self." },
  { id: 10, thinker: "Kierkegaard", tradition: "Existential Philosophy", thematicCategory: "Dual Nature of Humans", keyQuote: "The self is a relation that relates itself to its own self.", contribution: "Points to the inherent contradiction and fragmentation within the self." },
  { id: 11, thinker: "Friedrich Nietzsche", tradition: "Existential Nihilism", thematicCategory: "Meaninglessness & Radical Nihilism", keyQuote: "God is dead. God remains dead. And we have killed him.", contribution: "Diagnoses the collapse of objective values and meaning." },
  { id: 12, thinker: "Friedrich Nietzsche", tradition: "Existential Nihilism", thematicCategory: "The Absurd & Overcoming Nihilism", keyQuote: "He who has a why to live can bear almost any how.", contribution: "Proposes that meaning is self-imposed and that the struggle itself is key to survival." },
  { id: 13, thinker: "Martin Luther", tradition: "Protestant Reformation", thematicCategory: "Divine Grace vs. Human Agency", keyQuote: "For the grace of God … overthrows free-will … and binds it to the divine will.", contribution: "Argues that human freedom is subordinate to divine purpose." },
  { id: 14, thinker: "Thomas Merton", tradition: "Christian Contemplative", thematicCategory: "Inner Conflict & Spiritual Isolation", keyQuote: "We are not at peace with others because we are not at peace with ourselves.", contribution: "Emphasizes that self-disintegration is necessary for spiritual progress." },
  { id: 15, thinker: "Meister Eckhart", tradition: "Christian Mysticism", thematicCategory: "Mysticism & Ego Dissolution", keyQuote: "To be full of things is to be empty of God. To be empty of things is to be full of God.", contribution: "Articulates the paradox of possession versus spiritual emptiness." }
];
  
// Simulated categories for visualization
const thematicCategories = [
  "Existential Dread & Renunciation",
  "Duality / Ethical Conflict",
  "Existential Anxiety & Conflict",
  "Dual Nature of Humans", 
  "Mysticism & Ego Death",
  "Existential Struggle & Absurdity",
  "The Struggle for Meaning",
  "Transcendent Re-Imagining",
  "Existential Dread & The Divided Self",
  "Meaninglessness & Radical Nihilism",
  "The Absurd & Overcoming Nihilism",
  "Divine Grace vs. Human Agency",
  "Inner Conflict & Spiritual Isolation",
  "Mysticism & Ego Dissolution"
];

// Simulated traditions for visualization
const traditions = [
  "Early Christianity",
  "Christian Philosophy",
  "Christian Mysticism",
  "Russian Orthodox / Existentialism",
  "Christian Apologetics",
  "Existential Philosophy",
  "Existential Nihilism",
  "Protestant Reformation",
  "Christian Contemplative"
];

const PhilosophicalGuide = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [actualData, setActualData] = useState([]);
  const [displayData, setDisplayData] = useState(philosophicalData);
  const [selectedThinker, setSelectedThinker] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedTradition, setSelectedTradition] = useState('All');
  const [errorMsg, setErrorMsg] = useState('');
  const [activeTab, setActiveTab] = useState('visual');

  useEffect(() => {
    // Try to load the actual data from the file
    const loadActualData = async () => {
      try {
        const fileContent = await window.fs.readFile('paste.txt', { encoding: 'utf8' });
        
        // First attempt to extract just the data we need
        let foundData = [];
        
        // Look for patterns like "| 1 | Jesus" or similar table entries
        const rowRegex = /\|\s*(\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|/g;
        let match;
        
        while ((match = rowRegex.exec(fileContent)) !== null) {
          // Skip header row or separator row
          if (match[1] === '#' || match[1].includes('-')) continue;
          
          foundData.push({
            id: parseInt(match[1].trim(), 10),
            thinker: match[2].replace(/\*\*/g, '').trim(),
            tradition: match[3].trim(),
            keyQuote: match[4].trim(),
            thematicCategory: match[5].trim(),
            contribution: match[6].trim(),
            logicalLink: match[7].trim()
          });
        }
        
        if (foundData.length > 0) {
          setActualData(foundData);
          setDisplayData(foundData);
        }
      } catch (error) {
        console.error("Error loading data:", error);
        setErrorMsg("Failed to parse the table data, using sample data instead");
      } finally {
        setIsLoading(false);
      }
    };
    
    loadActualData();
  }, []);
  
  // Filter the data based on search and filters
  useEffect(() => {
    const dataSource = actualData.length > 0 ? actualData : philosophicalData;
    
    const filtered = dataSource.filter(item => {
      const matchesSearch = searchTerm === '' || 
        item.thinker.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (item.keyQuote && item.keyQuote.toLowerCase().includes(searchTerm.toLowerCase()));
      
      const matchesCategory = selectedCategory === 'All' || item.thematicCategory === selectedCategory;
      const matchesTradition = selectedTradition === 'All' || item.tradition === selectedTradition;
      
      return matchesSearch && matchesCategory && matchesTradition;
    });
    
    setDisplayData(filtered);
  }, [searchTerm, selectedCategory, selectedTradition, actualData]);
  
  // Generate a color for a category
  const getCategoryColor = (category) => {
    const categoryIndex = thematicCategories.indexOf(category);
    const hue = ((categoryIndex * 137.5) % 360); // Golden ratio approximation for good distribution
    return `hsl(${hue}, 70%, 45%)`;
  };
  
  // Generate a complementary color for text on the category background
  const getTextColor = (category) => {
    const categoryIndex = thematicCategories.indexOf(category);
    const hue = ((categoryIndex * 137.5) % 360);
    // Darker categories need light text, lighter categories need dark text
    return hue > 60 && hue < 180 ? '#000' : '#fff';
  };
  
  const visibleCategories = [...new Set(displayData.map(item => item.thematicCategory))];
  const visibleTraditions = [...new Set(displayData.map(item => item.tradition))];
  
  return (
    <div className="flex flex-col h-full bg-gray-900 text-white">
      {/* Header */}
      <div className="p-4 bg-gray-800 border-b border-gray-700">
        <h1 className="text-2xl font-bold mb-2">Nihiltheism: Network of Philosophical Thought</h1>
        <p className="text-sm mb-4">Explore the connections between 53 philosophers and their contributions to existential, nihilistic, and theistic thought.</p>
        
        {errorMsg && <p className="text-yellow-400 text-sm mb-2">{errorMsg}</p>}
        
        {/* Search and filters */}
        <div className="flex flex-wrap gap-2 mb-4">
          <input
            type="text"
            placeholder="Search thinkers or quotes..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="p-2 bg-gray-700 rounded text-white outline-none flex-grow"
          />
          
          <select 
            value={selectedCategory}
            onChange={(e) => setSelectedCategory(e.target.value)}
            className="p-2 bg-gray-700 rounded text-white outline-none"
          >
            <option value="All">All Categories</option>
            {visibleCategories.map(cat => (
              <option key={cat} value={cat}>{cat}</option>
            ))}
          </select>
          
          <select 
            value={selectedTradition}
            onChange={(e) => setSelectedTradition(e.target.value)}
            className="p-2 bg-gray-700 rounded text-white outline-none"
          >
            <option value="All">All Traditions</option>
            {visibleTraditions.map(trad => (
              <option key={trad} value={trad}>{trad}</option>
            ))}
          </select>
        </div>
        
        {/* View tabs */}
        <div className="flex border-b border-gray-700">
          <button 
            className={`px-4 py-2 ${activeTab === 'visual' ? 'bg-gray-700 text-white' : 'text-gray-400'}`}
            onClick={() => setActiveTab('visual')}
          >
            Visual Grid
          </button>
          <button 
            className={`px-4 py-2 ${activeTab === 'table' ? 'bg-gray-700 text-white' : 'text-gray-400'}`}
            onClick={() => setActiveTab('table')}
          >
            Table View
          </button>
        </div>
      </div>
      
      {/* Loading state */}
      {isLoading && (
        <div className="flex-1 flex items-center justify-center">
          <p className="text-xl text-gray-400">Loading philosophical data...</p>
        </div>
      )}
      
      {/* Content */}
      {!isLoading && activeTab === 'visual' && (
        <div className="flex-1 overflow-auto p-4">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {displayData.map(item => (
              <div 
                key={`${item.id}-${item.thinker}`}
                className="bg-gray-800 rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow cursor-pointer"
                onClick={() => setSelectedThinker(selectedThinker === item ? null : item)}
              >
                <div 
                  className="p-3 text-center font-bold"
                  style={{ 
                    backgroundColor: getCategoryColor(item.thematicCategory),
                    color: getTextColor(item.thematicCategory)
                  }}
                >
                  {item.thematicCategory}
                </div>
                <div className="p-4">
                  <h3 className="text-xl font-bold mb-1">{item.thinker}</h3>
                  <p className="text-gray-400 text-sm mb-3">{item.tradition}</p>
                  
                  {selectedThinker === item ? (
                    <>
                      <p className="text-gray-300 italic mb-3">"{item.keyQuote}"</p>
                      <div className="bg-gray-700 p-3 rounded mb-3">
                        <h4 className="font-semibold mb-1">Contribution to Synthesis:</h4>
                        <p className="text-sm text-gray-300">{item.contribution}</p>
                      </div>
                      {item.logicalLink && (
                        <div className="bg-gray-700 p-3 rounded">
                          <h4 className="font-semibold mb-1">Logical Link:</h4>
                          <p className="text-sm text-gray-300">{item.logicalLink}</p>
                        </div>
                      )}
                    </>
                  ) : (
                    <p className="text-gray-300 italic line-clamp-2">"{item.keyQuote}"</p>
                  )}
                  
                  {selectedThinker !== item && (
                    <button 
                      className="mt-2 text-blue-400 text-sm flex items-center"
                      onClick={(e) => {
                        e.stopPropagation();
                        setSelectedThinker(item);
                      }}
                    >
                      View details <span className="ml-1">→</span>
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
          
          {displayData.length === 0 && (
            <div className="text-center py-16">
              <p className="text-xl text-gray-400">No matching philosophers found</p>
              <button 
                className="mt-4 px-4 py-2 bg-blue-600 rounded hover:bg-blue-700"
                onClick={() => {
                  setSearchTerm('');
                  setSelectedCategory('All');
                  setSelectedTradition('All');
                }}
              >
                Reset filters
              </button>
            </div>
          )}
        </div>
      )}
      
      {/* Table view */}
      {!isLoading && activeTab === 'table' && (
        <div className="flex-1 overflow-auto">
          <table className="min-w-full bg-gray-900 text-white">
            <thead className="bg-gray-800 sticky top-0">
              <tr>
                <th className="p-3 text-left">#</th>
                <th className="p-3 text-left">Thinker</th>
                <th className="p-3 text-left">Tradition</th>
                <th className="p-3 text-left">Thematic Category</th>
                <th className="p-3 text-left">Key Quote</th>
                <th className="p-3 text-left">Contribution</th>
              </tr>
            </thead>
            <tbody>
              {displayData.map((item, index) => (
                <tr 
                  key={`table-${item.id}-${item.thinker}`}
                  className={index % 2 === 0 ? 'bg-gray-800' : 'bg-gray-850'}
                >
                  <td className="p-3 align-top">{item.id}</td>
                  <td className="p-3 align-top font-medium">{item.thinker}</td>
                  <td className="p-3 align-top text-gray-300">{item.tradition}</td>
                  <td className="p-3 align-top">
                    <span 
                      className="px-2 py-1 rounded text-sm"
                      style={{ 
                        backgroundColor: getCategoryColor(item.thematicCategory),
                        color: getTextColor(item.thematicCategory)
                      }}
                    >
                      {item.thematicCategory}
                    </span>
                  </td>
                  <td className="p-3 align-top italic text-gray-300">"{item.keyQuote}"</td>
                  <td className="p-3 align-top text-gray-300">{item.contribution}</td>
                </tr>
              ))}
            </tbody>
          </table>
          
          {displayData.length === 0 && (
            <div className="text-center py-16">
              <p className="text-xl text-gray-400">No matching philosophers found</p>
              <button 
                className="mt-4 px-4 py-2 bg-blue-600 rounded hover:bg-blue-700"
                onClick={() => {
                  setSearchTerm('');
                  setSelectedCategory('All');
                  setSelectedTradition('All');
                }}
              >
                Reset filters
              </button>
            </div>
          )}
        </div>
      )}
      
      {/* Legend */}
      <div className="p-3 bg-gray-800 border-t border-gray-700 flex flex-wrap gap-2">
        <div className="text-sm text-gray-400 mr-2">Category Legend:</div>
        {visibleCategories.slice(0, 6).map(category => (
          <span 
            key={category}
            className="px-2 py-1 rounded text-xs"
            style={{ 
              backgroundColor: getCategoryColor(category),
              color: getTextColor(category)
            }}
          >
            {category}
          </span>
        ))}
        {visibleCategories.length > 6 && (
          <span className="text-gray-400 text-xs">+{visibleCategories.length - 6} more</span>
        )}
      </div>
    </div>
  );
};

export default PhilosophicalGuide;
import React, { useState, useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { Camera } from 'lucide-react';

// Sample data (fallback)
const philosophicalData = [ /* ... original entries ... */ ];

const NetworkGraph = ({ data }) => {
  const svgRef = useRef();
  useEffect(() => {
    if (!data.length) return;
    const width = 800, height = 600;
    const thinkers = [...new Set(data.map(d => d.thinker))];
    const nodes = thinkers.map(name => ({ id: name }));
    const links = [];
    const categories = [...new Set(data.map(d => d.thematicCategory))];
    categories.forEach(cat => {
      const group = data.filter(d => d.thematicCategory === cat).map(d => d.thinker);
      for (let i = 0; i < group.length; i++) {
        for (let j = i + 1; j < group.length; j++) {
          links.push({ source: group[i], target: group[j] });
        }
      }
    });
    const svg = d3.select(svgRef.current)
      .attr('viewBox', `0 0 ${width} ${height}`)
      .attr('width', '100%')
      .attr('height', '100%')
      .selectAll('*').remove(),
      svg = d3.select(svgRef.current);

    const simulation = d3.forceSimulation(nodes)
      .force('link', d3.forceLink(links).id(d => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-200))
      .force('center', d3.forceCenter(width / 2, height / 2));

    const link = svg.append('g')
      .selectAll('line')
      .data(links)
      .enter().append('line')
      .attr('stroke', '#999').attr('stroke-opacity', 0.6);

    const node = svg.append('g')
      .selectAll('circle')
      .data(nodes)
      .enter().append('circle')
      .attr('r', 8)
      .attr('fill', '#61dafb')
      .call(d3.drag()
        .on('start', (event, d) => {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          d.fx = d.x; d.fy = d.y;
        })
        .on('drag', (event, d) => { d.fx = event.x; d.fy = event.y; })
        .on('end', (event, d) => {
          if (!event.active) simulation.alphaTarget(0);
          d.fx = null; d.fy = null;
        })
      );

    const labels = svg.append('g')
      .selectAll('text')
      .data(nodes)
      .enter().append('text')
      .attr('dx', 12).attr('dy', '.35em')
      .text(d => d.id);

    simulation.on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);
      node
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);
      labels
        .attr('x', d => d.x)
        .attr('y', d => d.y);
    });
    return () => simulation.stop();
  }, [data]);

  return <svg ref={svgRef} />;
};

const PhilosophicalGuideExtended = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [actualData, setActualData] = useState([]);
  const [displayData, setDisplayData] = useState(philosophicalData);
  const [selectedThinker, setSelectedThinker] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [selectedTradition, setSelectedTradition] = useState('All');
  const [errorMsg, setErrorMsg] = useState('');
  const [activeTab, setActiveTab] = useState('visual');
  const [comparisonMode, setComparisonMode] = useState(false);
  const [comparedThinkers, setComparedThinkers] = useState([]);
  const [aiAnalysis, setAiAnalysis] = useState('');
  const [aiLoading, setAiLoading] = useState(false);

  // Load real data (if available)
  useEffect(() => {
    (async () => {
      try {
        const content = await window.fs.readFile('paste.txt', 'utf8');
        // parse logic...
      } catch {
        setErrorMsg('Using sample data');
      } finally {
        setIsLoading(false);
      }
    })();
  }, []);

  // Filters
  useEffect(() => {
    const source = actualData.length ? actualData : philosophicalData;
    const filtered = source.filter(item => {
      const bySearch = !searchTerm || item.thinker.toLowerCase().includes(searchTerm.toLowerCase());
      const byCat = selectedCategory === 'All' || item.thematicCategory === selectedCategory;
      const byTrad = selectedTradition === 'All' || item.tradition === selectedTradition;
      return bySearch && byCat && byTrad;
    });
    setDisplayData(filtered);
  }, [searchTerm, selectedCategory, selectedTradition, actualData]);

  const generateAIAnalysis = () => {
    if (comparedThinkers.length < 2) return setErrorMsg('Select at least two thinkers');
    setAiLoading(true);
    setTimeout(() => {
      setAiAnalysis(`## Comparative Analysis of ${comparedThinkers.join(' & ')}

This synthesis reveals shared tensions in ${displayData.find(d => d.thinker === comparedThinkers[0]).thematicCategory}...
`);
      setAiLoading(false);
    }, 1200);
  };

  const toggleCompare = name => {
    setComparedThinkers(curr => curr.includes(name)
      ? curr.filter(n => n !== name)
      : curr.length < 3 ? [...curr, name] : curr);
  };

  const categoryColor = cat => `hsl(${(thematicCategories.indexOf(cat) * 137.5) % 360},70%,45%)`;
  const textColor = cat => {
    const h = (thematicCategories.indexOf(cat) * 137.5) % 360;
    return h > 60 && h < 180 ? '#000' : '#fff';
  };

  return (
    <div className="flex flex-col h-full bg-gray-900 text-white">
      {/* Header & Filters... */}
      {/* Tabs: visual, table, timeline, network */}
      {/* Comparison panel and AI analysis */}
      {/* Conditional render for each tab, including NetworkGraph and timeline */}
    </div>
  );
};

export default PhilosophicalGuideExtended;
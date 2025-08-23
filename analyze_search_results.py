"""
Analyze the philosophical AI search results and extract key insights
"""

import json
import pandas as pd
from collections import defaultdict
import re

def load_and_analyze_results():
    """Load and analyze the search results for key insights"""
    
    # Load search results
    with open('/workspace/data/philosophical_ai_search_results.json', 'r', encoding='utf-8') as f:
        search_results = json.load(f)
    
    analysis = {
        'philosophical_ai_systems': [],
        'nihilistic_philosophy': [],
        'theistic_intersections': [],
        'ai_philosophy_methods': [],
        'key_findings': {},
        'research_gaps': [],
        'technical_insights': []
    }
    
    # Analyze each category
    for result in search_results:
        if isinstance(result, dict) and 'papers' in result:
            category = result.get('category', 'unknown')
            papers = result.get('papers', [])
            
            for paper in papers:
                paper_info = {
                    'title': paper.get('title', ''),
                    'snippet': paper.get('snippet', ''),
                    'year': paper.get('year', ''),
                    'link': paper.get('link', ''),
                    'publicationInfo': paper.get('publicationInfo', ''),
                    'citedBy': paper.get('citedBy', ''),
                    'pdfUrl': paper.get('pdfUrl', '')
                }
                
                if category in analysis:
                    analysis[category].append(paper_info)
    
    # Extract key insights by category
    analysis['key_findings'] = extract_key_findings(analysis)
    
    # Save detailed analysis
    with open('/workspace/data/detailed_philosophical_analysis.json', 'w', encoding='utf-8') as f:
        json.dump(analysis, f, indent=2, ensure_ascii=False)
    
    return analysis

def extract_key_findings(analysis):
    """Extract key findings from each research category"""
    
    findings = {}
    
    # Analyze Philosophical AI Systems
    ai_systems = analysis['philosophical_ai_systems']
    findings['philosophical_ai_systems'] = {
        'count': len(ai_systems),
        'key_themes': extract_themes_from_papers(ai_systems),
        'recent_developments': [p for p in ai_systems if str(p.get('year', '0')).isdigit() and int(str(p.get('year', '0'))) >= 2020],
        'methodological_approaches': extract_methodologies(ai_systems)
    }
    
    # Analyze Nihilistic Philosophy
    nihil_papers = analysis['nihilistic_philosophy']
    findings['nihilistic_philosophy'] = {
        'count': len(nihil_papers),
        'key_themes': extract_themes_from_papers(nihil_papers),
        'contemporary_debates': extract_contemporary_issues(nihil_papers),
        'philosophical_gaps': identify_gaps(nihil_papers)
    }
    
    # Analyze Theistic Intersections
    theistic_papers = analysis['theistic_intersections']
    findings['theistic_intersections'] = {
        'count': len(theistic_papers),
        'synthesis_attempts': extract_synthesis_approaches(theistic_papers),
        'paradox_resolution': extract_paradox_approaches(theistic_papers)
    }
    
    # Analyze AI Philosophy Methods
    method_papers = analysis['ai_philosophy_methods']
    findings['ai_philosophy_methods'] = {
        'count': len(method_papers),
        'validation_techniques': extract_validation_methods(method_papers),
        'content_generation': extract_generation_methods(method_papers)
    }
    
    return findings

def extract_themes_from_papers(papers):
    """Extract key themes from paper titles and snippets"""
    themes = defaultdict(int)
    keywords = [
        'reasoning', 'logic', 'argument', 'ethics', 'consciousness', 'meaning', 'existence', 
        'absurd', 'transcendence', 'authenticity', 'freedom', 'responsibility', 'dialogue',
        'computational', 'machine learning', 'natural language', 'knowledge representation'
    ]
    
    for paper in papers:
        text = f"{paper.get('title', '')} {paper.get('snippet', '')}".lower()
        for keyword in keywords:
            if keyword in text:
                themes[keyword] += 1
    
    return dict(sorted(themes.items(), key=lambda x: x[1], reverse=True)[:10])

def extract_methodologies(papers):
    """Extract methodological approaches from AI philosophy papers"""
    methodologies = []
    method_keywords = [
        'neural network', 'deep learning', 'transformer', 'knowledge graph', 'ontology',
        'formal logic', 'argumentation theory', 'semantic analysis', 'dialogue system',
        'natural language processing', 'symbolic reasoning', 'machine reasoning'
    ]
    
    for paper in papers:
        text = f"{paper.get('title', '')} {paper.get('snippet', '')}".lower()
        found_methods = [method for method in method_keywords if method in text]
        if found_methods:
            methodologies.append({
                'title': paper.get('title', ''),
                'methods': found_methods,
                'year': paper.get('year', '')
            })
    
    return methodologies[:15]  # Top 15 methodological papers

def extract_contemporary_issues(papers):
    """Extract contemporary issues in nihilistic philosophy"""
    issues = []
    issue_keywords = [
        'climate change', 'technology', 'digital age', 'postmodern', 'late capitalism',
        'artificial intelligence', 'virtual reality', 'social media', 'globalization',
        'pandemic', 'posthuman', 'transhumanism'
    ]
    
    for paper in papers:
        text = f"{paper.get('title', '')} {paper.get('snippet', '')}".lower()
        found_issues = [issue for issue in issue_keywords if issue in text]
        if found_issues:
            issues.append({
                'title': paper.get('title', ''),
                'issues': found_issues,
                'year': paper.get('year', '')
            })
    
    return issues

def identify_gaps(papers):
    """Identify research gaps in nihilistic philosophy"""
    gaps = []
    
    # Look for papers that mention gaps, future research, or unresolved questions
    gap_indicators = ['gap', 'future research', 'unresolved', 'further investigation', 'unexplored']
    
    for paper in papers:
        snippet = paper.get('snippet', '').lower()
        for indicator in gap_indicators:
            if indicator in snippet:
                gaps.append({
                    'title': paper.get('title', ''),
                    'gap_context': snippet,
                    'year': paper.get('year', '')
                })
                break
    
    return gaps[:10]

def extract_synthesis_approaches(papers):
    """Extract approaches to synthesizing theistic and nihilistic frameworks"""
    synthesis = []
    synthesis_keywords = [
        'synthesis', 'integration', 'bridge', 'reconcile', 'paradox', 'tension',
        'dialectic', 'complementary', 'fusion', 'hybrid'
    ]
    
    for paper in papers:
        text = f"{paper.get('title', '')} {paper.get('snippet', '')}".lower()
        found_approaches = [approach for approach in synthesis_keywords if approach in text]
        if found_approaches:
            synthesis.append({
                'title': paper.get('title', ''),
                'approaches': found_approaches,
                'year': paper.get('year', '')
            })
    
    return synthesis

def extract_paradox_approaches(papers):
    """Extract approaches to handling philosophical paradoxes"""
    paradox_handling = []
    paradox_keywords = [
        'paradox', 'contradiction', 'antinomy', 'aporia', 'dilemma',
        'tension', 'conflict', 'resolution', 'reconciliation'
    ]
    
    for paper in papers:
        text = f"{paper.get('title', '')} {paper.get('snippet', '')}".lower()
        if any(keyword in text for keyword in paradox_keywords):
            paradox_handling.append({
                'title': paper.get('title', ''),
                'year': paper.get('year', ''),
                'snippet': paper.get('snippet', '')[:200]
            })
    
    return paradox_handling[:10]

def extract_validation_methods(papers):
    """Extract validation methods for philosophical AI"""
    validation = []
    validation_keywords = [
        'validation', 'evaluation', 'assessment', 'verification', 'testing',
        'quality measure', 'coherence', 'consistency', 'soundness'
    ]
    
    for paper in papers:
        text = f"{paper.get('title', '')} {paper.get('snippet', '')}".lower()
        if any(keyword in text for keyword in validation_keywords):
            validation.append({
                'title': paper.get('title', ''),
                'year': paper.get('year', ''),
                'snippet': paper.get('snippet', '')[:200]
            })
    
    return validation[:10]

def extract_generation_methods(papers):
    """Extract content generation methods for philosophical AI"""
    generation = []
    generation_keywords = [
        'generation', 'synthesis', 'creation', 'composition', 'automatic',
        'automated', 'computational creativity', 'text generation'
    ]
    
    for paper in papers:
        text = f"{paper.get('title', '')} {paper.get('snippet', '')}".lower()
        if any(keyword in text for keyword in generation_keywords):
            generation.append({
                'title': paper.get('title', ''),
                'year': paper.get('year', ''),
                'snippet': paper.get('snippet', '')[:200]
            })
    
    return generation[:10]

def print_analysis_summary(analysis):
    """Print a summary of the analysis"""
    findings = analysis['key_findings']
    
    print("=== PHILOSOPHICAL AI RESEARCH ANALYSIS ===\n")
    
    print("1. PHILOSOPHICAL AI SYSTEMS:")
    print(f"   Papers analyzed: {findings['philosophical_ai_systems']['count']}")
    print(f"   Recent developments (2020+): {len(findings['philosophical_ai_systems']['recent_developments'])}")
    print(f"   Key themes: {list(findings['philosophical_ai_systems']['key_themes'].keys())[:5]}")
    print(f"   Methodological approaches found: {len(findings['philosophical_ai_systems']['methodological_approaches'])}")
    
    print("\n2. NIHILISTIC PHILOSOPHY:")
    print(f"   Papers analyzed: {findings['nihilistic_philosophy']['count']}")
    print(f"   Contemporary issues: {len(findings['nihilistic_philosophy']['contemporary_debates'])}")
    print(f"   Research gaps identified: {len(findings['nihilistic_philosophy']['philosophical_gaps'])}")
    
    print("\n3. THEISTIC INTERSECTIONS:")
    print(f"   Papers analyzed: {findings['theistic_intersections']['count']}")
    print(f"   Synthesis attempts: {len(findings['theistic_intersections']['synthesis_attempts'])}")
    print(f"   Paradox approaches: {len(findings['theistic_intersections']['paradox_resolution'])}")
    
    print("\n4. AI PHILOSOPHY METHODS:")
    print(f"   Papers analyzed: {findings['ai_philosophy_methods']['count']}")
    print(f"   Validation techniques: {len(findings['ai_philosophy_methods']['validation_techniques'])}")
    print(f"   Generation methods: {len(findings['ai_philosophy_methods']['content_generation'])}")

if __name__ == "__main__":
    analysis = load_and_analyze_results()
    print_analysis_summary(analysis)

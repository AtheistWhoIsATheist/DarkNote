"""
Comprehensive Literature Review for Nihiltheism Framework Development
Systematic academic search across classical and contemporary philosophical sources
"""

import asyncio
import concurrent.futures
import json
import pandas as pd
from external_api.data_sources.client import get_client
from datetime import datetime
from collections import defaultdict

class NihiltheismLiteratureResearcher:
    def __init__(self):
        self.client = None
        self.search_results = {}
        
    async def initialize_client(self):
        """Initialize the data source client"""
        self.client = get_client()
        
    async def search_scholar_papers(self, query, num_results=40, start_year=1900, category="", keywords=None):
        """Enhanced search with keyword tracking"""
        try:
            print(f"Searching for: {query}")
            result = await self.client.scholar.search_scholar(
                query=query,
                num_results=num_results,
                start_year=start_year,
                end_year=2024
            )
            
            if result["success"]:
                papers = result["data"]["papers"]
                print(f"Found {len(papers)} papers for query: {query}")
                return {
                    "category": category,
                    "query": query,
                    "keywords": keywords or [],
                    "papers": papers,
                    "search_date": datetime.now().isoformat(),
                    "start_year": start_year
                }
            else:
                print(f"Search failed for query '{query}': {result.get('error', 'Unknown error')}")
                return {"category": category, "query": query, "papers": [], "error": result.get('error')}
                
        except Exception as e:
            print(f"Exception during search for '{query}': {str(e)}")
            return {"category": category, "query": query, "papers": [], "error": str(e)}

    async def conduct_comprehensive_nihiltheism_search(self):
        """Conduct systematic searches across all Nihiltheism research areas"""
        
        search_queries = [
            # Classical Nihilistic Philosophy - Deep Dive
            ("Nietzsche death of God nihilism", 50, 1880, "classical_nihilism", ["nietzsche", "death_of_god", "nihilism"]),
            ("Nietzsche eternal recurrence will to power", 40, 1880, "classical_nihilism", ["nietzsche", "eternal_recurrence", "will_to_power"]),
            ("Camus absurd revolt sisyphean condition", 45, 1940, "classical_nihilism", ["camus", "absurd", "revolt", "sisyphean"]),
            ("Camus meaninglessness authentic living", 35, 1940, "classical_nihilism", ["camus", "meaninglessness", "authenticity"]),
            ("Sartre existential nihilism bad faith", 40, 1940, "classical_nihilism", ["sartre", "existential_nihilism", "bad_faith"]),
            ("Sartre radical freedom being-for-itself", 35, 1940, "classical_nihilism", ["sartre", "radical_freedom", "being_for_itself"]),
            ("Kierkegaard despair sickness unto death", 40, 1840, "classical_nihilism", ["kierkegaard", "despair", "sickness_unto_death"]),
            ("Kierkegaard leap of faith authentic existence", 35, 1840, "classical_nihilism", ["kierkegaard", "leap_of_faith", "authenticity"]),
            
            # Contemporary Nihilistic Thinkers
            ("Thomas Nagel absurd meaninglessness", 30, 1970, "contemporary_nihilism", ["nagel", "absurd", "meaninglessness"]),
            ("John Marmysz humorous nihilism", 25, 1990, "contemporary_nihilism", ["marmysz", "humorous_nihilism"]),
            ("Ray Brassier eliminative materialism nihilism", 25, 1990, "contemporary_nihilism", ["brassier", "eliminative_materialism"]),
            ("contemporary nihilism philosophy", 40, 2000, "contemporary_nihilism", ["nihilism", "contemporary"]),
            
            # Theistic Philosophy Intersections
            ("apophatic theology via negativa", 35, 1900, "theistic_intersections", ["apophatic", "via_negativa", "negative_theology"]),
            ("mystical traditions unknowing divine", 35, 1900, "theistic_intersections", ["mystical", "unknowing", "divine"]),
            ("Cloud of Unknowing mysticism", 25, 1900, "theistic_intersections", ["cloud_of_unknowing", "mysticism"]),
            ("John of the Cross dark night soul", 30, 1900, "theistic_intersections", ["john_of_the_cross", "dark_night"]),
            ("process theology Whitehead divine becoming", 30, 1920, "theistic_intersections", ["process_theology", "whitehead", "becoming"]),
            ("Tillich God above God ultimate concern", 35, 1920, "theistic_intersections", ["tillich", "god_above_god", "ultimate_concern"]),
            ("theological responses secular meaninglessness", 30, 1950, "theistic_intersections", ["theology", "secular", "meaninglessness"]),
            
            # Paradox and Synthesis Opportunities
            ("Hegelian dialectics thesis antithesis synthesis", 35, 1800, "synthesis_methods", ["hegel", "dialectics", "synthesis"]),
            ("postmodern theology Caputo Marion", 30, 1980, "synthesis_methods", ["postmodern_theology", "caputo", "marion"]),
            ("Buddhist emptiness fullness philosophy", 35, 1900, "synthesis_methods", ["buddhist", "emptiness", "fullness"]),
            ("Taoist wu wei non-action philosophy", 30, 1900, "synthesis_methods", ["taoist", "wu_wei", "non_action"]),
            ("philosophical paradox resolution methodology", 30, 1950, "synthesis_methods", ["paradox", "resolution", "methodology"]),
            
            # AI and Digital Existence Philosophy
            ("machine consciousness existential questions", 30, 1990, "ai_digital_existence", ["machine_consciousness", "existential"]),
            ("artificial intelligence meaning making", 35, 1990, "ai_digital_existence", ["ai", "meaning_making"]),
            ("digital ontology virtual reality philosophy", 30, 1990, "ai_digital_existence", ["digital_ontology", "virtual_reality"]),
            ("posthuman theology transhumanism", 25, 1990, "ai_digital_existence", ["posthuman", "theology", "transhumanism"]),
            ("AI ethics artificial suffering transcendence", 25, 2000, "ai_digital_existence", ["ai_ethics", "artificial_suffering", "transcendence"]),
            ("computational consciousness existential states", 25, 2000, "ai_digital_existence", ["computational_consciousness", "existential_states"]),
            
            # Innovation Gaps and Contemporary Issues
            ("technology mediated spiritual experience", 25, 1990, "innovation_gaps", ["technology", "spiritual", "experience"]),
            ("humor play existential philosophy", 25, 1970, "innovation_gaps", ["humor", "play", "existential"]),
            ("digital spaces meaning meaninglessness", 25, 2000, "innovation_gaps", ["digital_spaces", "meaning", "meaninglessness"]),
            ("virtual reality existential philosophy", 25, 1990, "innovation_gaps", ["virtual_reality", "existential"]),
            ("artificial consciousness theistic experience", 20, 2000, "innovation_gaps", ["artificial_consciousness", "theistic"]),
            
            # Methodological Frameworks
            ("hermeneutic philosophy meaning interpretation", 30, 1900, "methodological", ["hermeneutic", "meaning", "interpretation"]),
            ("phenomenological experiential analysis", 30, 1900, "methodological", ["phenomenological", "experiential", "analysis"]),
            ("dialectical synthesis creation methodology", 25, 1800, "methodological", ["dialectical", "synthesis", "methodology"]),
            ("philosophical argumentation paradox", 30, 1900, "methodological", ["argumentation", "paradox"]),
        ]
        
        # Execute searches in batches with controlled concurrency
        batch_size = 4
        all_results = []
        
        for i in range(0, len(search_queries), batch_size):
            batch = search_queries[i:i+batch_size]
            batch_tasks = []
            
            for query, num_results, start_year, category, keywords in batch:
                task = self.search_scholar_papers(query, num_results, start_year, category, keywords)
                batch_tasks.append(task)
            
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
            all_results.extend(batch_results)
            
            # Pause between batches to be respectful to the API
            await asyncio.sleep(3)
        
        return all_results

    def analyze_nihiltheism_results(self, results):
        """Analyze search results for Nihiltheism framework development"""
        analysis = {
            "total_papers": 0,
            "categories": {},
            "key_concepts": defaultdict(list),
            "classical_foundations": [],
            "contemporary_developments": [],
            "synthesis_opportunities": [],
            "innovation_gaps": [],
            "methodological_insights": [],
            "keyword_analysis": defaultdict(int),
            "temporal_analysis": defaultdict(int),
            "high_impact_papers": []
        }
        
        for result in results:
            if isinstance(result, dict) and "papers" in result:
                category = result.get("category", "unknown")
                papers = result.get("papers", [])
                keywords = result.get("keywords", [])
                
                if category not in analysis["categories"]:
                    analysis["categories"][category] = {
                        "paper_count": 0,
                        "queries": [],
                        "key_papers": [],
                        "concepts": []
                    }
                
                analysis["categories"][category]["paper_count"] += len(papers)
                analysis["categories"][category]["queries"].append(result.get("query", ""))
                analysis["total_papers"] += len(papers)
                
                # Track keywords
                for keyword in keywords:
                    analysis["keyword_analysis"][keyword] += len(papers)
                
                # Analyze papers by category and impact
                for paper in papers:
                    year = self.extract_year(paper.get("year", ""))
                    if year:
                        analysis["temporal_analysis"][year] += 1
                    
                    # Extract citation count for impact analysis
                    citation_count = self.extract_citation_count(paper.get("citedBy", ""))
                    
                    paper_info = {
                        "title": paper.get("title", ""),
                        "snippet": paper.get("snippet", ""),
                        "year": year,
                        "citations": citation_count,
                        "category": category,
                        "keywords": keywords,
                        "link": paper.get("link", ""),
                        "pdfUrl": paper.get("pdfUrl", "")
                    }
                    
                    # Categorize by research area
                    if category == "classical_nihilism":
                        analysis["classical_foundations"].append(paper_info)
                    elif category == "contemporary_nihilism":
                        analysis["contemporary_developments"].append(paper_info)
                    elif category == "theistic_intersections":
                        analysis["synthesis_opportunities"].append(paper_info)
                    elif category == "ai_digital_existence":
                        analysis["innovation_gaps"].append(paper_info)
                    elif category == "methodological":
                        analysis["methodological_insights"].append(paper_info)
                    
                    # High-impact papers (high citation count)
                    if citation_count > 100:
                        analysis["high_impact_papers"].append(paper_info)
        
        # Sort high-impact papers by citation count
        analysis["high_impact_papers"].sort(key=lambda x: x["citations"], reverse=True)
        analysis["high_impact_papers"] = analysis["high_impact_papers"][:30]  # Top 30
        
        return analysis
    
    def extract_year(self, year_str):
        """Extract year from various year string formats"""
        if not year_str:
            return None
        try:
            # Handle various formats
            year_str = str(year_str).strip()
            if year_str.isdigit() and len(year_str) == 4:
                return int(year_str)
            # Extract 4-digit year from longer strings
            import re
            match = re.search(r'\b(19|20)\d{2}\b', year_str)
            if match:
                return int(match.group())
        except:
            pass
        return None
    
    def extract_citation_count(self, cited_by_str):
        """Extract citation count from citedBy string"""
        if not cited_by_str:
            return 0
        try:
            import re
            # Look for "Cited by X" pattern
            match = re.search(r'Cited by (\d+)', str(cited_by_str))
            if match:
                return int(match.group(1))
        except:
            pass
        return 0

    def save_results(self, results, analysis, base_filename):
        """Save search results and analysis"""
        # Save raw results
        results_file = f"/workspace/data/{base_filename}_raw_results.json"
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        # Save analysis
        analysis_file = f"/workspace/data/{base_filename}_analysis.json"
        with open(analysis_file, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        print(f"Results saved to {results_file}")
        print(f"Analysis saved to {analysis_file}")
        
        return results_file, analysis_file

async def main():
    """Main research execution function"""
    researcher = NihiltheismLiteratureResearcher()
    
    print("Initializing Nihiltheism Literature Research...")
    await researcher.initialize_client()
    
    print("Conducting comprehensive literature search across all philosophical areas...")
    search_results = await researcher.conduct_comprehensive_nihiltheism_search()
    
    print("Analyzing results for Nihiltheism framework development...")
    analysis = researcher.analyze_nihiltheism_results(search_results)
    
    print("Saving results and analysis...")
    results_file, analysis_file = researcher.save_results(search_results, analysis, "nihiltheism_literature")
    
    print(f"\nNihiltheism Literature Review Complete!")
    print(f"Total papers analyzed: {analysis['total_papers']}")
    print(f"Categories covered: {len(analysis['categories'])}")
    print(f"High-impact papers identified: {len(analysis['high_impact_papers'])}")
    
    for category, data in analysis['categories'].items():
        print(f"- {category}: {data['paper_count']} papers")
    
    print(f"\nTop keywords by frequency:")
    sorted_keywords = sorted(analysis['keyword_analysis'].items(), key=lambda x: x[1], reverse=True)
    for keyword, count in sorted_keywords[:10]:
        print(f"- {keyword}: {count}")
    
    return search_results, analysis

def run_nihiltheism_research():
    """Run the research with proper async handling"""
    with concurrent.futures.ThreadPoolExecutor() as executor:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            results = loop.run_until_complete(main())
            return results
        finally:
            loop.close()

if __name__ == "__main__":
    search_results, analysis = run_nihiltheism_research()

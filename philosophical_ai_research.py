"""
Comprehensive research script for Philosophical AI Frameworks and Nihilistic Discourse Analysis
"""

import asyncio
import concurrent.futures
import json
import pandas as pd
from external_api.data_sources.client import get_client
from datetime import datetime

class PhilosophicalAIResearcher:
    def __init__(self):
        self.client = None
        self.search_results = {}
        
    async def initialize_client(self):
        """Initialize the data source client"""
        self.client = get_client()
        
    async def search_scholar_papers(self, query, num_results=50, start_year=2015, category=""):
        """Search for academic papers with enhanced error handling"""
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
                    "papers": papers,
                    "search_date": datetime.now().isoformat()
                }
            else:
                print(f"Search failed for query '{query}': {result.get('error', 'Unknown error')}")
                return {"category": category, "query": query, "papers": [], "error": result.get('error')}
                
        except Exception as e:
            print(f"Exception during search for '{query}': {str(e)}")
            return {"category": category, "query": query, "papers": [], "error": str(e)}

    async def conduct_comprehensive_search(self):
        """Conduct searches across all research areas"""
        
        # Define search queries for different research areas
        search_queries = [
            # Existing Philosophical AI Systems
            ("AI philosophical reasoning systems", 30, "philosophical_ai_systems"),
            ("automated philosophical argument generation", 25, "philosophical_ai_systems"),
            ("computational philosophy artificial intelligence", 25, "philosophical_ai_systems"),
            ("machine learning philosophical discourse", 20, "philosophical_ai_systems"),
            ("AI ethics philosophy reasoning", 20, "philosophical_ai_systems"),
            
            # Nihilistic Philosophy Analysis
            ("nihilism philosophy contemporary debates", 30, "nihilistic_philosophy"),
            ("Nietzsche nihilism existential meaninglessness", 25, "nihilistic_philosophy"),
            ("Camus absurdism nihilistic thought", 20, "nihilistic_philosophy"),
            ("Sartre existentialism nihilism", 20, "nihilistic_philosophy"),
            ("modern nihilism philosophical gaps", 15, "nihilistic_philosophy"),
            
            # Theistic Philosophy Intersections
            ("theism nihilism philosophical synthesis", 20, "theistic_intersections"),
            ("meaning meaninglessness transcendence philosophy", 20, "theistic_intersections"),
            ("religious existentialism nihilistic critique", 15, "theistic_intersections"),
            ("theology nihilism contemporary philosophy", 15, "theistic_intersections"),
            
            # AI-Assisted Philosophical Inquiry
            ("AI philosophical research methodology", 25, "ai_philosophy_methods"),
            ("computational philosophy validation techniques", 20, "ai_philosophy_methods"),
            ("artificial intelligence philosophical content generation", 20, "ai_philosophy_methods"),
            ("machine learning philosophical argument coherence", 15, "ai_philosophy_methods"),
            ("digital humanities philosophy AI", 15, "ai_philosophy_methods"),
        ]
        
        # Execute searches concurrently
        search_tasks = []
        for query, num_results, category in search_queries:
            task = self.search_scholar_papers(query, num_results, 2015, category)
            search_tasks.append(task)
        
        # Run searches concurrently with reasonable batch size
        batch_size = 5
        all_results = []
        
        for i in range(0, len(search_tasks), batch_size):
            batch = search_tasks[i:i+batch_size]
            batch_results = await asyncio.gather(*batch, return_exceptions=True)
            all_results.extend(batch_results)
            
            # Small delay between batches to be respectful to the API
            await asyncio.sleep(2)
        
        return all_results

    def save_search_results(self, results, filename):
        """Save search results to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"Search results saved to {filename}")
        except Exception as e:
            print(f"Error saving results: {str(e)}")

    def analyze_search_results(self, results):
        """Analyze and categorize search results"""
        analysis = {
            "total_papers": 0,
            "categories": {},
            "key_papers": [],
            "search_summary": {}
        }
        
        for result in results:
            if isinstance(result, dict) and "papers" in result:
                category = result.get("category", "unknown")
                papers = result.get("papers", [])
                
                if category not in analysis["categories"]:
                    analysis["categories"][category] = {
                        "paper_count": 0,
                        "queries": [],
                        "top_papers": []
                    }
                
                analysis["categories"][category]["paper_count"] += len(papers)
                analysis["categories"][category]["queries"].append(result.get("query", ""))
                analysis["total_papers"] += len(papers)
                
                # Extract high-impact papers (high citation count)
                for paper in papers:
                    try:
                        cited_by = paper.get("citedBy", "0")
                        # Extract number from citation string like "Cited by 123"
                        if "Cited by" in cited_by:
                            citation_count = int(cited_by.split("Cited by")[1].strip())
                        else:
                            citation_count = 0
                            
                        if citation_count > 50:  # High-impact threshold
                            analysis["key_papers"].append({
                                "title": paper.get("title", ""),
                                "citations": citation_count,
                                "category": category,
                                "link": paper.get("link", ""),
                                "year": paper.get("year", ""),
                                "snippet": paper.get("snippet", "")[:200]
                            })
                    except:
                        continue
        
        # Sort key papers by citation count
        analysis["key_papers"].sort(key=lambda x: x["citations"], reverse=True)
        analysis["key_papers"] = analysis["key_papers"][:20]  # Top 20
        
        return analysis

async def main():
    """Main research execution function"""
    researcher = PhilosophicalAIResearcher()
    
    print("Initializing Philosophical AI Research...")
    await researcher.initialize_client()
    
    print("Conducting comprehensive literature search...")
    search_results = await researcher.conduct_comprehensive_search()
    
    print("Saving and analyzing results...")
    researcher.save_search_results(search_results, "/workspace/data/philosophical_ai_search_results.json")
    
    analysis = researcher.analyze_search_results(search_results)
    researcher.save_search_results(analysis, "/workspace/data/philosophical_ai_analysis.json")
    
    print(f"\nSearch Complete!")
    print(f"Total papers found: {analysis['total_papers']}")
    print(f"Categories analyzed: {len(analysis['categories'])}")
    print(f"High-impact papers identified: {len(analysis['key_papers'])}")
    
    for category, data in analysis['categories'].items():
        print(f"- {category}: {data['paper_count']} papers")
    
    return search_results, analysis

def run_research():
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
    # Create data directory if it doesn't exist
    import os
    os.makedirs("/workspace/data", exist_ok=True)
    
    search_results, analysis = run_research()

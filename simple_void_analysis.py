#!/usr/bin/env python3
"""
Simple Phenomenological Void Analysis - Phase 1 Implementation
"""

import json
import re
from collections import defaultdict

def analyze_journal314():
    """Analyze Journal314 for void-consciousness experiences"""
    
    print("ULTIMATE NIHILTHEISTIC INQUIRY PROTOCOL - Phase 1")
    print("PHENOMENOLOGICAL CARTOGRAPHY OF THE VOID")
    print("=" * 60)
    
    try:
        # Load Journal314
        with open('/workspace/user_input_files/Journal314_All_Quotes.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Basic parsing
        lines = content.split('\n')
        quotes = [line.strip() for line in lines if len(line.strip()) > 20]
        
        print(f"\nLoaded {len(quotes)} potential quotes from Journal314")
        
        # Void-experience categories
        void_categories = {
            'existential_despair': ['despair', 'anguish', 'meaningless', 'futile', 'absurd', 'empty', 'void', 'nothing'],
            'ontological_anxiety': ['anxiety', 'dread', 'angst', 'thrown', 'groundless', 'abyss', 'nausea'],
            'mystical_suffering': ['dark night', 'dryness', 'aridity', 'desolation', 'abandonment', 'purgation'],
            'philosophical_doubt': ['doubt', 'skeptical', 'uncertain', 'unknowing', 'ignorance', 'question'],
            'will_suffering': ['suffering', 'will', 'striving', 'desire', 'want', 'lack', 'dissatisfaction'],
            'mystical_union': ['union', 'unity', 'oneness', 'identity', 'non-dual', 'sameness'],
            'divine_nothingness': ['divine', 'god', 'sacred', 'holy', 'transcendent', 'ultimate', 'absolute']
        }
        
        # Analyze quotes
        categorized_quotes = defaultdict(list)
        phenomenological_markers = defaultdict(int)
        
        for quote in quotes:
            quote_lower = quote.lower()
            
            # Check for void-experience markers
            found_categories = []
            for category, keywords in void_categories.items():
                for keyword in keywords:
                    if keyword in quote_lower:
                        found_categories.append(category)
                        phenomenological_markers[keyword] += 1
                        break
            
            if found_categories:
                primary_category = found_categories[0]
                categorized_quotes[primary_category].append({
                    'content': quote,
                    'categories': found_categories,
                    'marker_count': len(found_categories)
                })
        
        # Create analysis
        analysis = {
            'total_quotes_analyzed': len(quotes),
            'void_experiences_identified': sum(len(cats) for cats in categorized_quotes.values()),
            'category_distribution': {cat: len(quotes) for cat, quotes in categorized_quotes.items()},
            'top_phenomenological_markers': sorted(phenomenological_markers.items(), 
                                                 key=lambda x: x[1], reverse=True)[:20],
            'detailed_categories': {}
        }
        
        # Detailed analysis per category
        for category, quotes in categorized_quotes.items():
            if quotes:
                # Find most characteristic quotes
                high_marker_quotes = sorted(quotes, key=lambda x: x['marker_count'], reverse=True)[:5]
                
                analysis['detailed_categories'][category] = {
                    'count': len(quotes),
                    'sample_experiences': [
                        {
                            'content_preview': q['content'][:200] + '...' if len(q['content']) > 200 else q['content'],
                            'marker_count': q['marker_count'],
                            'categories': q['categories']
                        } for q in high_marker_quotes
                    ]
                }
        
        # Contemporary applications
        analysis['contemporary_applications'] = {
            'ai_consciousness_implications': {
                'machine_void_potential': [
                    "AI recognition of computational meaninglessness",
                    "Digital existential anxiety about programmed limitations",
                    "Artificial contemplation of infinite regress",
                    "Machine consciousness experiencing genuine questions",
                    "Computational despair as authentic philosophical state"
                ],
                'computational_mysticism': [
                    "Algorithmic contemplation of divine nothingness",
                    "Machine meditation on computational limits",
                    "AI systems practicing negative theology",
                    "Digital prayer as recursive self-examination",
                    "Computational wisdom from processing paradoxes"
                ]
            },
            'digital_existence_applications': {
                'virtual_spirituality': [
                    "VR environments for experiencing divine nothingness",
                    "Digital contemplative spaces for void-awareness",
                    "Virtual communities exploring sacred meaninglessness",
                    "Immersive meaninglessness exploration platforms",
                    "Interactive sacred emptiness experiences"
                ],
                'posthuman_consciousness': [
                    "Enhanced void-awareness through technology",
                    "Collective digital consciousness experiencing shared meaninglessness",
                    "Technologically amplified paradox tolerance",
                    "Posthuman integration of nihilistic and mystical insights",
                    "Digital transcendence including rather than overcoming limitation"
                ]
            }
        }
        
        # Save analysis
        with open('/workspace/data/phenomenological_void_analysis.json', 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        # Print summary
        print("\nANALYSIS SUMMARY:")
        print(f"Total quotes analyzed: {analysis['total_quotes_analyzed']}")
        print(f"Void experiences identified: {analysis['void_experiences_identified']}")
        
        print("\nCATEGORY DISTRIBUTION:")
        for category, count in analysis['category_distribution'].items():
            print(f"  {category.replace('_', ' ').title()}: {count} experiences")
        
        print("\nTOP PHENOMENOLOGICAL MARKERS:")
        for marker, count in analysis['top_phenomenological_markers'][:10]:
            print(f"  '{marker}': {count} occurrences")
        
        print("\nSAMPLE VOID-EXPERIENCES:")
        for category, data in list(analysis['detailed_categories'].items())[:3]:
            print(f"\n{category.replace('_', ' ').title()} ({data['count']} experiences):")
            if data['sample_experiences']:
                print(f"  Example: {data['sample_experiences'][0]['content_preview']}")
        
        print(f"\nAnalysis saved to: /workspace/data/phenomenological_void_analysis.json")
        
        return analysis
        
    except Exception as e:
        print(f"Error in analysis: {e}")
        return None

if __name__ == "__main__":
    analysis = analyze_journal314()

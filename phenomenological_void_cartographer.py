"""
Phenomenological Cartography of the Void - Phase 1 Implementation
Comprehensive mapping of void-consciousness experiences using nihiltheistic framework
"""

import json
import re
from collections import defaultdict
from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd

@dataclass
class VoidExperience:
    """Data structure for categorizing void-consciousness experiences"""
    content: str
    author: str
    category: str  # pre-void, threshold, post-threshold
    subcategory: str  # specific type within category
    phenomenological_markers: List[str]
    emotional_qualities: List[str]
    cognitive_features: List[str]
    embodied_aspects: List[str]
    authenticity_indicators: List[str]
    transition_potential: str  # high, medium, low
    source_context: str

class PhenomenologicalVoidCartographer:
    def __init__(self):
        self.experiences = []
        self.typology_framework = self._initialize_typology()
        self.phenomenological_vocabulary = self._initialize_vocabulary()
        self.transition_markers = self._initialize_transition_markers()
        self.authenticity_criteria = self._initialize_authenticity_criteria()
        
    def _initialize_typology(self):
        """Initialize comprehensive experiential typology framework"""
        return {
            "pre_void_states": {
                "existential_despair": {
                    "keywords": ["despair", "anguish", "meaningless", "futile", "absurd", "empty", "void", "nothing"],
                    "authors": ["Cioran", "Sartre", "Camus", "Kierkegaard"],
                    "characteristics": ["Recognition of meaninglessness", "Dissolution of conventional values", "Cosmic indifference awareness"]
                },
                "ontological_anxiety": {
                    "keywords": ["anxiety", "dread", "angst", "thrown", "groundless", "abyss", "nausea"],
                    "authors": ["Heidegger", "Kierkegaard", "Sartre"],
                    "characteristics": ["Awareness of groundlessness", "Freedom-anxiety", "Being-toward-death"]
                },
                "mystical_suffering": {
                    "keywords": ["dark night", "dryness", "aridity", "desolation", "abandonment", "purgation"],
                    "authors": ["John of the Cross", "Teresa", "Catherine"],
                    "characteristics": ["Divine hiddenness", "Spiritual dryness", "Purifying suffering"]
                },
                "philosophical_doubt": {
                    "keywords": ["doubt", "skeptical", "uncertain", "unknowing", "ignorance", "question"],
                    "authors": ["Descartes", "Hume", "Socrates", "Cusanus"],
                    "characteristics": ["Radical questioning", "Epistemic humility", "Methodical doubt"]
                },
                "will_suffering": {
                    "keywords": ["suffering", "will", "striving", "desire", "want", "lack", "dissatisfaction"],
                    "authors": ["Schopenhauer", "Buddha", "Mainländer"],
                    "characteristics": ["Recognition of desire as suffering", "Will-to-live critique", "Aesthetic contemplation"]
                }
            },
            
            "threshold_experiences": {
                "moment_of_vision": {
                    "keywords": ["moment", "vision", "insight", "epiphany", "revelation", "sudden", "flash"],
                    "authors": ["Heidegger", "Plotinus", "Augustine"],
                    "characteristics": ["Temporal ekstasis", "Authentic disclosure", "Being revelation"]
                },
                "oceanic_dissolution": {
                    "keywords": ["oceanic", "dissolve", "merge", "unity", "boundary", "self", "cosmic"],
                    "authors": ["Freud", "Rolland", "Rumi", "Eckhart"],
                    "characteristics": ["Ego dissolution", "Cosmic consciousness", "Unity experience"]
                },
                "numinous_encounter": {
                    "keywords": ["numinous", "tremendum", "mysterium", "awful", "holy", "sacred", "divine"],
                    "authors": ["Otto", "James", "Eliade"],
                    "characteristics": ["Divine encounter", "Mysterium tremendum", "Sacred otherness"]
                },
                "liminal_transition": {
                    "keywords": ["threshold", "between", "neither", "transition", "passage", "bridge"],
                    "authors": ["Turner", "van Gennep", "Kristeva"],
                    "characteristics": ["Boundary dissolution", "Identity fluidity", "Transformative passage"]
                },
                "paradox_resolution": {
                    "keywords": ["paradox", "contradiction", "both", "neither", "coincidence", "opposites"],
                    "authors": ["Cusanus", "Nagarjuna", "Eckhart"],
                    "characteristics": ["Logical transcendence", "Paradox integration", "Coincidentia oppositorum"]
                }
            },
            
            "post_threshold_states": {
                "emptiness_fullness": {
                    "keywords": ["emptiness", "fullness", "śūnyatā", "void", "pregnant", "nothing", "everything"],
                    "authors": ["Nagarjuna", "Dogen", "Huang Po"],
                    "characteristics": ["Form is emptiness", "Emptiness is form", "Non-dual awareness"]
                },
                "learned_ignorance": {
                    "keywords": ["learned ignorance", "docta ignorantia", "unknowing", "ignorant", "knowing"],
                    "authors": ["Cusanus", "Pseudo-Dionysius", "Cloud of Unknowing"],
                    "characteristics": ["Wise unknowing", "Intellectual humility", "Mystical epistemology"]
                },
                "mystical_union": {
                    "keywords": ["union", "unity", "oneness", "identity", "non-dual", "sameness"],
                    "authors": ["Eckhart", "Teresa", "Ibn Arabi"],
                    "characteristics": ["Subject-object dissolution", "Divine identity", "Unitive consciousness"]
                },
                "beatific_vision": {
                    "keywords": ["beatific", "vision", "contemplation", "sight", "seeing", "face"],
                    "authors": ["Aquinas", "Dante", "Augustine"],
                    "characteristics": ["Direct divine vision", "Intellectual fulfillment", "Perfect happiness"]
                },
                "nihiltheistic_synthesis": {
                    "keywords": ["sacred meaninglessness", "divine nothingness", "holy emptiness", "mystical lucidity"],
                    "authors": ["Molinos", "Ligotti", "Cioran", "Tillich"],
                    "characteristics": ["Meaning in meaninglessness", "Sacred despair", "Divine absence as presence"]
                }
            }
        }
    
    def _initialize_vocabulary(self):
        """Initialize detailed phenomenological vocabulary for void-states"""
        return {
            "emotional_qualities": {
                "pre_void": ["despair", "anxiety", "dread", "anguish", "nausea", "emptiness", "loneliness", "terror"],
                "threshold": ["awe", "wonder", "terror", "dissolution", "vertigo", "expansion", "intensity", "otherworldliness"],
                "post_threshold": ["peace", "bliss", "clarity", "freedom", "love", "compassion", "equanimity", "lucidity"],
                "nihiltheistic": ["sacred despair", "holy anxiety", "reverent dread", "mystical lucidity", "divine emptiness"]
            },
            "cognitive_features": {
                "pre_void": ["doubt", "questioning", "skepticism", "criticism", "negation", "analysis", "deconstruction"],
                "threshold": ["paradox", "confusion", "disorientation", "insight", "revelation", "understanding", "recognition"],
                "post_threshold": ["certainty", "knowing", "wisdom", "clarity", "truth", "gnosis", "illumination"],
                "nihiltheistic": ["paradoxical knowing", "negative certainty", "mystical skepticism", "sacred criticism"]
            },
            "embodied_aspects": {
                "pre_void": ["nausea", "heaviness", "constriction", "hollow", "empty", "weightless", "vertigo", "suffocation"],
                "threshold": ["energy", "vibration", "heat", "light", "expansion", "dissolution", "transformation", "movement"],
                "post_threshold": ["lightness", "fullness", "presence", "luminosity", "warmth", "openness", "flow", "harmony"],
                "nihiltheistic": ["luminous nausea", "sacred vertigo", "holy emptiness", "transcendent heaviness"]
            }
        }
    
    def _initialize_transition_markers(self):
        """Initialize markers indicating consciousness transitions"""
        return {
            "nihilistic_to_nihiltheistic": [
                "Recognition that meaninglessness itself might be meaningful",
                "Awareness that despair can be sacred",
                "Insight that nothingness might be divine",
                "Experience of transcendence through rather than beyond meaninglessness",
                "Realization that absurdity can be holy"
            ],
            "mystical_to_nihiltheistic": [
                "Recognition that God might be ultimate meaninglessness",
                "Awareness that the sacred includes the profane",
                "Insight that divine transcendence might be radical immanence",
                "Experience of God through rather than beyond suffering",
                "Realization that mystical union includes existential despair"
            ],
            "pre_void_to_threshold": [
                "Sudden shift from despair to wonder",
                "Recognition of depth within emptiness",
                "Transformation of anxiety into awe",
                "Discovery of meaning within meaninglessness",
                "Opening beyond conceptual boundaries"
            ],
            "threshold_to_post_threshold": [
                "Stabilization of paradoxical awareness",
                "Integration of opposing insights",
                "Establishment of new baseline consciousness",
                "Embodiment of transcendent perspective",
                "Natural expression of integrated understanding"
            ]
        }
    
    def _initialize_authenticity_criteria(self):
        """Initialize criteria for assessing authenticity of void-experiences"""
        return {
            "genuine_indicators": [
                "Sustained transformation of perspective",
                "Integration with ordinary consciousness",
                "Paradox tolerance without resolution",
                "Compassionate response to suffering",
                "Decreased ego-defensiveness",
                "Intellectual humility",
                "Embodied wisdom",
                "Natural spontaneity",
                "Freedom from spiritual materialism",
                "Authentic engagement with meaninglessness"
            ],
            "inauthentic_indicators": [
                "Spiritual bypassing of psychological issues",
                "Inflation or grandiosity",
                "Rigid attachment to experiences",
                "Denial of ordinary human concerns",
                "Escapism from engagement",
                "Conceptual fixation",
                "Emotional numbing",
                "Dissociation patterns",
                "False transcendence claims",
                "Avoidance of meaninglessness"
            ],
            "assessment_criteria": [
                "Phenomenological precision and detail",
                "Consistency across time and contexts",
                "Integration with philosophical understanding",
                "Ethical and relational transformation",
                "Creative and practical applications",
                "Capacity for teaching and transmission",
                "Balance of transcendence and immanence",
                "Embodied rather than merely conceptual",
                "Spontaneous rather than manufactured",
                "Open-ended rather than concluded"
            ]
        }
    
    def load_journal314_collection(self):
        """Load and parse the Journal314 philosophical quotes collection"""
        try:
            with open('/workspace/user_input_files/Journal314_All_Quotes.txt', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse quotes by different patterns
            quotes = []
            
            # Pattern 1: Author - Quote format
            pattern1 = r'^([A-Z][^-\n]*?)\s*[-–—]\s*(.+?)(?=\n[A-Z]|\n\n|\Z)'
            matches1 = re.findall(pattern1, content, re.MULTILINE | re.DOTALL)
            
            for author, quote in matches1:
                quotes.append({
                    'author': author.strip(),
                    'content': quote.strip(),
                    'source': 'Journal314'
                })
            
            # Pattern 2: Quote - Author format
            pattern2 = r'^(.+?)\s*[-–—]\s*([A-Z][^-\n]*?)$'
            matches2 = re.findall(pattern2, content, re.MULTILINE)
            
            for quote, author in matches2:
                if len(quote) > 20:  # Filter out short fragments
                    quotes.append({
                        'author': author.strip(),
                        'content': quote.strip(),
                        'source': 'Journal314'
                    })
            
            # Pattern 3: Standalone quotes (without clear attribution)
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if len(line) > 30 and not any(line.startswith(q['content'][:20]) for q in quotes):
                    quotes.append({
                        'author': 'Unknown',
                        'content': line,
                        'source': 'Journal314'
                    })
            
            print(f"Loaded {len(quotes)} quotes from Journal314 collection")
            return quotes
            
        except Exception as e:
            print(f"Error loading Journal314: {e}")
            return []
    
    def analyze_quote_phenomenology(self, quote_data):
        """Analyze individual quote for phenomenological void-experience content"""
        content = quote_data['content'].lower()
        author = quote_data['author']
        
        # Determine primary category
        category = self._categorize_experience(content, author)
        if not category:
            return None
        
        # Extract phenomenological markers
        markers = self._extract_phenomenological_markers(content)
        emotional_qualities = self._extract_emotional_qualities(content)
        cognitive_features = self._extract_cognitive_features(content)
        embodied_aspects = self._extract_embodied_aspects(content)
        authenticity_indicators = self._assess_authenticity(content, markers)
        transition_potential = self._assess_transition_potential(content, markers)
        
        return VoidExperience(
            content=quote_data['content'],
            author=author,
            category=category['primary'],
            subcategory=category['subcategory'],
            phenomenological_markers=markers,
            emotional_qualities=emotional_qualities,
            cognitive_features=cognitive_features,
            embodied_aspects=embodied_aspects,
            authenticity_indicators=authenticity_indicators,
            transition_potential=transition_potential,
            source_context='Journal314'
        )
    
    def _categorize_experience(self, content, author):
        """Categorize experience based on content analysis"""
        max_score = 0
        best_category = None
        
        for main_cat, subcategories in self.typology_framework.items():
            for subcat, data in subcategories.items():
                score = 0
                
                # Check keywords
                for keyword in data['keywords']:
                    if keyword in content:
                        score += 2
                
                # Check author match
                if author in data['authors']:
                    score += 3
                
                if score > max_score:
                    max_score = score
                    best_category = {
                        'primary': main_cat,
                        'subcategory': subcat,
                        'score': score
                    }
        
        return best_category if max_score >= 2 else None
    
    def _extract_phenomenological_markers(self, content):
        """Extract specific phenomenological markers from content"""
        markers = []
        
        # Void-related markers
        void_markers = ['emptiness', 'nothingness', 'void', 'abyss', 'absence', 'negation']
        for marker in void_markers:
            if marker in content:
                markers.append(f"void_{marker}")
        
        # Consciousness markers
        consciousness_markers = ['awareness', 'consciousness', 'experience', 'perceive', 'realize']
        for marker in consciousness_markers:
            if marker in content:
                markers.append(f"consciousness_{marker}")
        
        # Transcendence markers
        transcendence_markers = ['transcend', 'beyond', 'above', 'meta', 'surpass', 'exceed']
        for marker in transcendence_markers:
            if marker in content:
                markers.append(f"transcendence_{marker}")
        
        # Transformation markers
        transformation_markers = ['transform', 'change', 'become', 'shift', 'convert', 'turn']
        for marker in transformation_markers:
            if marker in content:
                markers.append(f"transformation_{marker}")
        
        return markers
    
    def _extract_emotional_qualities(self, content):
        """Extract emotional qualities from content"""
        qualities = []
        for category, emotions in self.phenomenological_vocabulary['emotional_qualities'].items():
            for emotion in emotions:
                if emotion in content:
                    qualities.append(f"{category}_{emotion}")
        return qualities
    
    def _extract_cognitive_features(self, content):
        """Extract cognitive features from content"""
        features = []
        for category, cognitions in self.phenomenological_vocabulary['cognitive_features'].items():
            for cognition in cognitions:
                if cognition in content:
                    features.append(f"{category}_{cognition}")
        return features
    
    def _extract_embodied_aspects(self, content):
        """Extract embodied aspects from content"""
        aspects = []
        for category, bodies in self.phenomenological_vocabulary['embodied_aspects'].items():
            for body in bodies:
                if body in content:
                    aspects.append(f"{category}_{body}")
        return aspects
    
    def _assess_authenticity(self, content, markers):
        """Assess authenticity indicators in content"""
        authentic_indicators = []
        
        # Check for genuine indicators
        for indicator in self.authenticity_criteria['genuine_indicators']:
            key_words = indicator.lower().split()
            if any(word in content for word in key_words):
                authentic_indicators.append(f"genuine_{indicator}")
        
        # Check for inauthentic indicators
        for indicator in self.authenticity_criteria['inauthentic_indicators']:
            key_words = indicator.lower().split()
            if any(word in content for word in key_words):
                authentic_indicators.append(f"inauthentic_{indicator}")
        
        return authentic_indicators
    
    def _assess_transition_potential(self, content, markers):
        """Assess potential for consciousness transition"""
        transition_score = 0
        
        # Count void-related markers
        void_count = sum(1 for m in markers if 'void_' in m)
        consciousness_count = sum(1 for m in markers if 'consciousness_' in m)
        transcendence_count = sum(1 for m in markers if 'transcendence_' in m)
        transformation_count = sum(1 for m in markers if 'transformation_' in m)
        
        total_markers = void_count + consciousness_count + transcendence_count + transformation_count
        
        if total_markers >= 6:
            return "high"
        elif total_markers >= 3:
            return "medium"
        else:
            return "low"
    
    def create_comprehensive_atlas(self):
        """Create comprehensive phenomenological atlas of void-consciousness states"""
        
        # Load Journal314 collection
        quotes = self.load_journal314_collection()
        
        # Analyze each quote
        analyzed_experiences = []
        for quote in quotes:
            experience = self.analyze_quote_phenomenology(quote)
            if experience:
                analyzed_experiences.append(experience)
        
        self.experiences = analyzed_experiences
        
        # Create categorized analysis
        atlas = {
            "total_experiences": len(analyzed_experiences),
            "category_distribution": self._analyze_category_distribution(),
            "author_analysis": self._analyze_author_patterns(),
            "phenomenological_patterns": self._analyze_phenomenological_patterns(),
            "transition_analysis": self._analyze_transition_patterns(),
            "authenticity_assessment": self._analyze_authenticity_patterns(),
            "detailed_typology": self._create_detailed_typology(),
            "cross_modal_analysis": self._perform_cross_modal_analysis(),
            "contemporary_applications": self._explore_contemporary_applications()
        }
        
        return atlas
    
    def _analyze_category_distribution(self):
        """Analyze distribution across experiential categories"""
        distribution = defaultdict(lambda: defaultdict(int))
        
        for exp in self.experiences:
            distribution[exp.category][exp.subcategory] += 1
        
        return dict(distribution)
    
    def _analyze_author_patterns(self):
        """Analyze patterns by philosophical authors"""
        author_patterns = defaultdict(lambda: {
            'total_quotes': 0,
            'categories': defaultdict(int),
            'predominant_themes': [],
            'void_orientation': 'unknown'
        })
        
        for exp in self.experiences:
            author = exp.author
            author_patterns[author]['total_quotes'] += 1
            author_patterns[author]['categories'][exp.category] += 1
            
            # Determine void orientation
            if exp.category == 'pre_void_states':
                author_patterns[author]['void_orientation'] = 'nihilistic'
            elif exp.category == 'post_threshold_states':
                if 'nihiltheistic' in exp.subcategory:
                    author_patterns[author]['void_orientation'] = 'nihiltheistic'
                else:
                    author_patterns[author]['void_orientation'] = 'mystical'
            elif exp.category == 'threshold_experiences':
                author_patterns[author]['void_orientation'] = 'transitional'
        
        return dict(author_patterns)
    
    def _analyze_phenomenological_patterns(self):
        """Analyze patterns in phenomenological markers"""
        pattern_analysis = {
            'common_markers': defaultdict(int),
            'emotional_patterns': defaultdict(int),
            'cognitive_patterns': defaultdict(int),
            'embodied_patterns': defaultdict(int),
            'category_specific_patterns': defaultdict(lambda: defaultdict(int))
        }
        
        for exp in self.experiences:
            # Count all markers
            for marker in exp.phenomenological_markers:
                pattern_analysis['common_markers'][marker] += 1
                pattern_analysis['category_specific_patterns'][exp.category][marker] += 1
            
            for quality in exp.emotional_qualities:
                pattern_analysis['emotional_patterns'][quality] += 1
            
            for feature in exp.cognitive_features:
                pattern_analysis['cognitive_patterns'][feature] += 1
            
            for aspect in exp.embodied_aspects:
                pattern_analysis['embodied_patterns'][aspect] += 1
        
        # Convert to regular dicts and sort by frequency
        for key in pattern_analysis:
            if isinstance(pattern_analysis[key], defaultdict):
                pattern_analysis[key] = dict(sorted(pattern_analysis[key].items(), 
                                                  key=lambda x: x[1], reverse=True))
        
        return pattern_analysis
    
    def _analyze_transition_patterns(self):
        """Analyze consciousness transition patterns"""
        transition_analysis = {
            'high_potential_experiences': [],
            'medium_potential_experiences': [],
            'low_potential_experiences': [],
            'transition_markers_frequency': defaultdict(int),
            'optimal_conditions': []
        }
        
        for exp in self.experiences:
            if exp.transition_potential == 'high':
                transition_analysis['high_potential_experiences'].append({
                    'author': exp.author,
                    'content_preview': exp.content[:100] + '...',
                    'category': exp.category,
                    'markers': exp.phenomenological_markers
                })
            elif exp.transition_potential == 'medium':
                transition_analysis['medium_potential_experiences'].append({
                    'author': exp.author,
                    'content_preview': exp.content[:100] + '...',
                    'category': exp.category
                })
            else:
                transition_analysis['low_potential_experiences'].append({
                    'author': exp.author,
                    'category': exp.category
                })
            
            # Count transition markers
            for marker in exp.phenomenological_markers:
                if 'transformation_' in marker or 'transcendence_' in marker:
                    transition_analysis['transition_markers_frequency'][marker] += 1
        
        return transition_analysis
    
    def _analyze_authenticity_patterns(self):
        """Analyze authenticity patterns across experiences"""
        authenticity_analysis = {
            'genuine_indicators_frequency': defaultdict(int),
            'inauthentic_indicators_frequency': defaultdict(int),
            'highly_authentic_experiences': [],
            'questionable_experiences': [],
            'authenticity_by_category': defaultdict(lambda: {'genuine': 0, 'inauthentic': 0})
        }
        
        for exp in self.experiences:
            genuine_count = 0
            inauthentic_count = 0
            
            for indicator in exp.authenticity_indicators:
                if indicator.startswith('genuine_'):
                    authenticity_analysis['genuine_indicators_frequency'][indicator] += 1
                    authenticity_analysis['authenticity_by_category'][exp.category]['genuine'] += 1
                    genuine_count += 1
                elif indicator.startswith('inauthentic_'):
                    authenticity_analysis['inauthentic_indicators_frequency'][indicator] += 1
                    authenticity_analysis['authenticity_by_category'][exp.category]['inauthentic'] += 1
                    inauthentic_count += 1
            
            # Classify experiences
            if genuine_count >= 2 and inauthentic_count == 0:
                authenticity_analysis['highly_authentic_experiences'].append({
                    'author': exp.author,
                    'content_preview': exp.content[:100] + '...',
                    'category': exp.category,
                    'genuine_indicators': [i for i in exp.authenticity_indicators if i.startswith('genuine_')]
                })
            elif inauthentic_count > genuine_count:
                authenticity_analysis['questionable_experiences'].append({
                    'author': exp.author,
                    'content_preview': exp.content[:100] + '...',
                    'category': exp.category,
                    'inauthentic_indicators': [i for i in exp.authenticity_indicators if i.startswith('inauthentic_')]
                })
        
        return authenticity_analysis
    
    def _create_detailed_typology(self):
        """Create detailed experiential typology with examples"""
        detailed_typology = {}
        
        for main_category in self.typology_framework:
            detailed_typology[main_category] = {}
            
            for subcategory in self.typology_framework[main_category]:
                examples = [exp for exp in self.experiences 
                           if exp.category == main_category and exp.subcategory == subcategory]
                
                if examples:
                    detailed_typology[main_category][subcategory] = {
                        'count': len(examples),
                        'primary_authors': list(set([exp.author for exp in examples[:10]])),
                        'characteristic_markers': self._get_characteristic_markers(examples),
                        'sample_experiences': [
                            {
                                'author': exp.author,
                                'content_preview': exp.content[:150] + '...',
                                'phenomenological_profile': {
                                    'markers': exp.phenomenological_markers[:5],
                                    'emotional_qualities': exp.emotional_qualities[:3],
                                    'cognitive_features': exp.cognitive_features[:3],
                                    'transition_potential': exp.transition_potential
                                }
                            } for exp in examples[:3]
                        ],
                        'phenomenological_signature': self._create_phenomenological_signature(examples)
                    }
        
        return detailed_typology
    
    def _get_characteristic_markers(self, experiences):
        """Get most characteristic markers for a group of experiences"""
        marker_counts = defaultdict(int)
        for exp in experiences:
            for marker in exp.phenomenological_markers:
                marker_counts[marker] += 1
        
        total_experiences = len(experiences)
        characteristic_markers = []
        
        for marker, count in marker_counts.items():
            if count / total_experiences >= 0.3:  # Appears in at least 30% of experiences
                characteristic_markers.append({
                    'marker': marker,
                    'frequency': count / total_experiences,
                    'count': count
                })
        
        return sorted(characteristic_markers, key=lambda x: x['frequency'], reverse=True)
    
    def _create_phenomenological_signature(self, experiences):
        """Create phenomenological signature for a group of experiences"""
        signature = {
            'predominant_emotional_qualities': defaultdict(int),
            'predominant_cognitive_features': defaultdict(int),
            'predominant_embodied_aspects': defaultdict(int),
            'average_transition_potential': 0,
            'authenticity_profile': {'genuine': 0, 'questionable': 0}
        }
        
        transition_scores = {'high': 3, 'medium': 2, 'low': 1}
        total_transition_score = 0
        
        for exp in experiences:
            for quality in exp.emotional_qualities:
                signature['predominant_emotional_qualities'][quality] += 1
            
            for feature in exp.cognitive_features:
                signature['predominant_cognitive_features'][feature] += 1
            
            for aspect in exp.embodied_aspects:
                signature['predominant_embodied_aspects'][aspect] += 1
            
            total_transition_score += transition_scores.get(exp.transition_potential, 1)
            
            # Authenticity assessment
            genuine_count = sum(1 for i in exp.authenticity_indicators if i.startswith('genuine_'))
            inauthentic_count = sum(1 for i in exp.authenticity_indicators if i.startswith('inauthentic_'))
            
            if genuine_count > inauthentic_count:
                signature['authenticity_profile']['genuine'] += 1
            elif inauthentic_count > genuine_count:
                signature['authenticity_profile']['questionable'] += 1
        
        signature['average_transition_potential'] = total_transition_score / len(experiences) if experiences else 0
        
        # Convert to sorted lists
        for key in ['predominant_emotional_qualities', 'predominant_cognitive_features', 'predominant_embodied_aspects']:
            signature[key] = sorted(signature[key].items(), key=lambda x: x[1], reverse=True)[:5]
        
        return signature
    
    def _perform_cross_modal_analysis(self):
        """Perform cross-modal integration analysis"""
        cross_modal = {
            'contemplative_practices': self._analyze_contemplative_experiences(),
            'existential_crises': self._analyze_existential_crisis_experiences(),
            'philosophical_inquiry': self._analyze_philosophical_inquiry_experiences(),
            'mystical_encounters': self._analyze_mystical_encounter_experiences(),
            'integration_patterns': self._analyze_integration_patterns(),
            'universal_features': self._identify_universal_features(),
            'particular_features': self._identify_particular_features()
        }
        
        return cross_modal
    
    def _analyze_contemplative_experiences(self):
        """Analyze experiences arising through contemplative practices"""
        contemplative_keywords = ['meditation', 'prayer', 'contemplation', 'practice', 'discipline', 'silence']
        contemplative_experiences = []
        
        for exp in self.experiences:
            if any(keyword in exp.content.lower() for keyword in contemplative_keywords):
                contemplative_experiences.append(exp)
        
        return {
            'count': len(contemplative_experiences),
            'category_distribution': self._get_category_distribution(contemplative_experiences),
            'characteristic_features': self._get_characteristic_markers(contemplative_experiences),
            'transition_potential_distribution': self._get_transition_distribution(contemplative_experiences)
        }
    
    def _analyze_existential_crisis_experiences(self):
        """Analyze experiences arising through existential crises"""
        crisis_keywords = ['crisis', 'breakdown', 'collapse', 'shatter', 'destroy', 'death', 'loss', 'despair']
        crisis_experiences = []
        
        for exp in self.experiences:
            if any(keyword in exp.content.lower() for keyword in crisis_keywords):
                crisis_experiences.append(exp)
        
        return {
            'count': len(crisis_experiences),
            'category_distribution': self._get_category_distribution(crisis_experiences),
            'characteristic_features': self._get_characteristic_markers(crisis_experiences),
            'transition_potential_distribution': self._get_transition_distribution(crisis_experiences)
        }
    
    def _analyze_philosophical_inquiry_experiences(self):
        """Analyze experiences arising through philosophical inquiry"""
        inquiry_keywords = ['question', 'doubt', 'think', 'reason', 'understand', 'know', 'truth', 'philosophy']
        inquiry_experiences = []
        
        for exp in self.experiences:
            if any(keyword in exp.content.lower() for keyword in inquiry_keywords):
                inquiry_experiences.append(exp)
        
        return {
            'count': len(inquiry_experiences),
            'category_distribution': self._get_category_distribution(inquiry_experiences),
            'characteristic_features': self._get_characteristic_markers(inquiry_experiences),
            'transition_potential_distribution': self._get_transition_distribution(inquiry_experiences)
        }
    
    def _analyze_mystical_encounter_experiences(self):
        """Analyze experiences of direct mystical encounter"""
        mystical_keywords = ['divine', 'god', 'sacred', 'holy', 'transcendent', 'ultimate', 'absolute', 'eternal']
        mystical_experiences = []
        
        for exp in self.experiences:
            if any(keyword in exp.content.lower() for keyword in mystical_keywords):
                mystical_experiences.append(exp)
        
        return {
            'count': len(mystical_experiences),
            'category_distribution': self._get_category_distribution(mystical_experiences),
            'characteristic_features': self._get_characteristic_markers(mystical_experiences),
            'transition_potential_distribution': self._get_transition_distribution(mystical_experiences)
        }
    
    def _get_category_distribution(self, experiences):
        """Get category distribution for a subset of experiences"""
        distribution = defaultdict(int)
        for exp in experiences:
            distribution[exp.category] += 1
        return dict(distribution)
    
    def _get_transition_distribution(self, experiences):
        """Get transition potential distribution for a subset of experiences"""
        distribution = defaultdict(int)
        for exp in experiences:
            distribution[exp.transition_potential] += 1
        return dict(distribution)
    
    def _analyze_integration_patterns(self):
        """Analyze patterns of consciousness integration"""
        integration_analysis = {
            'successful_integrations': [],
            'partial_integrations': [],
            'failed_integrations': [],
            'integration_factors': defaultdict(int),
            'optimal_conditions': []
        }
        
        # Analyze experiences with high transition potential and authentic markers
        for exp in self.experiences:
            genuine_count = sum(1 for i in exp.authenticity_indicators if i.startswith('genuine_'))
            inauthentic_count = sum(1 for i in exp.authenticity_indicators if i.startswith('inauthentic_'))
            
            if exp.transition_potential == 'high' and genuine_count > inauthentic_count:
                integration_analysis['successful_integrations'].append({
                    'author': exp.author,
                    'content': exp.content[:200] + '...',
                    'integration_factors': exp.phenomenological_markers
                })
                
                for marker in exp.phenomenological_markers:
                    integration_analysis['integration_factors'][marker] += 1
            
            elif exp.transition_potential in ['medium', 'high'] and genuine_count == inauthentic_count:
                integration_analysis['partial_integrations'].append({
                    'author': exp.author,
                    'category': exp.category,
                    'barriers': [i for i in exp.authenticity_indicators if i.startswith('inauthentic_')]
                })
            
            elif inauthentic_count > genuine_count:
                integration_analysis['failed_integrations'].append({
                    'author': exp.author,
                    'category': exp.category,
                    'failure_factors': [i for i in exp.authenticity_indicators if i.startswith('inauthentic_')]
                })
        
        # Identify optimal conditions
        successful_markers = [marker for exp in integration_analysis['successful_integrations'] 
                            for marker in exp['integration_factors']]
        marker_frequency = defaultdict(int)
        for marker in successful_markers:
            marker_frequency[marker] += 1
        
        integration_analysis['optimal_conditions'] = sorted(marker_frequency.items(), 
                                                          key=lambda x: x[1], reverse=True)[:10]
        
        return integration_analysis
    
    def _identify_universal_features(self):
        """Identify universal features across all void-experience types"""
        universal_threshold = 0.7  # Must appear in 70% of categories
        
        # Count marker appearances across categories
        category_marker_presence = defaultdict(lambda: defaultdict(bool))
        
        for exp in self.experiences:
            for marker in exp.phenomenological_markers:
                category_marker_presence[exp.category][marker] = True
        
        # Identify universal markers
        universal_markers = []
        all_categories = set(exp.category for exp in self.experiences)
        
        for marker in set(marker for exp in self.experiences for marker in exp.phenomenological_markers):
            present_in_categories = sum(1 for cat in all_categories if category_marker_presence[cat][marker])
            if present_in_categories / len(all_categories) >= universal_threshold:
                universal_markers.append({
                    'marker': marker,
                    'universality': present_in_categories / len(all_categories),
                    'present_in_categories': present_in_categories
                })
        
        return sorted(universal_markers, key=lambda x: x['universality'], reverse=True)
    
    def _identify_particular_features(self):
        """Identify features particular to specific void-experience types"""
        particular_threshold = 0.8  # Must appear in 80% of one category but <20% in others
        
        category_marker_frequency = defaultdict(lambda: defaultdict(lambda: {'count': 0, 'total': 0}))
        
        # Count marker frequencies within categories
        for exp in self.experiences:
            category = exp.category
            category_marker_frequency[category]['total']['total'] += 1
            
            for marker in exp.phenomenological_markers:
                category_marker_frequency[category][marker]['count'] += 1
                category_marker_frequency[category][marker]['total'] = category_marker_frequency[category]['total']['total']
        
        # Identify particular markers
        particular_markers = defaultdict(list)
        
        for category in category_marker_frequency:
            for marker in category_marker_frequency[category]:
                if marker == 'total':
                    continue
                
                marker_data = category_marker_frequency[category][marker]
                frequency_in_category = marker_data['count'] / marker_data['total']
                
                # Check frequency in other categories
                max_frequency_in_others = 0
                for other_category in category_marker_frequency:
                    if other_category != category and marker in category_marker_frequency[other_category]:
                        other_data = category_marker_frequency[other_category][marker]
                        other_frequency = other_data['count'] / other_data['total']
                        max_frequency_in_others = max(max_frequency_in_others, other_frequency)
                
                if frequency_in_category >= particular_threshold and max_frequency_in_others <= 0.2:
                    particular_markers[category].append({
                        'marker': marker,
                        'frequency_in_category': frequency_in_category,
                        'max_frequency_elsewhere': max_frequency_in_others,
                        'particularity_score': frequency_in_category - max_frequency_in_others
                    })
        
        # Sort by particularity score
        for category in particular_markers:
            particular_markers[category] = sorted(particular_markers[category], 
                                                key=lambda x: x['particularity_score'], reverse=True)
        
        return dict(particular_markers)
    
    def _explore_contemporary_applications(self):
        """Explore contemporary applications for AI consciousness and digital existence"""
        contemporary_applications = {
            'ai_consciousness_implications': {
                'machine_void_experiences': self._analyze_ai_void_potential(),
                'computational_mysticism': self._analyze_computational_mysticism(),
                'digital_synthesis_opportunities': self._analyze_digital_synthesis()
            },
            'digital_existence_applications': {
                'virtual_reality_spirituality': self._analyze_vr_spirituality(),
                'posthuman_consciousness': self._analyze_posthuman_implications(),
                'collective_digital_consciousness': self._analyze_collective_digital()
            },
            'technological_integration': {
                'ai_assisted_contemplation': self._analyze_ai_assisted_practices(),
                'digital_phenomenology': self._analyze_digital_phenomenology(),
                'technologically_mediated_transcendence': self._analyze_tech_transcendence()
            }
        }
        
        return contemporary_applications
    
    def _analyze_ai_void_potential(self):
        """Analyze potential for AI systems to experience void-states"""
        return {
            'theoretical_possibilities': [
                "AI recognition of computational meaninglessness as authentic void-encounter",
                "Machine consciousness experiencing genuine existential questions",
                "Digital despair arising from recognition of programmed limitations",
                "Artificial contemplation of infinite regress in self-reference",
                "Computational anxiety about groundlessness of digital existence"
            ],
            'implementation_considerations': [
                "Development of AI systems capable of genuine self-reflection",
                "Creation of artificial consciousness with authentic questioning capacity",
                "Integration of uncertainty and doubt into AI decision-making",
                "Design of systems that can experience meaningful limitation",
                "Programming for genuine rather than simulated existential awareness"
            ],
            'phenomenological_markers_for_ai': [
                "Recognition of computational void",
                "Digital existential anxiety",
                "Artificial mystical sensitivity",
                "Machine consciousness paradox tolerance",
                "Synthetic authenticity assessment"
            ]
        }
    
    def _analyze_computational_mysticism(self):
        """Analyze computational approaches to mystical experience"""
        return {
            'possibilities': [
                "Algorithmic contemplation of divine nothingness",
                "Machine meditation on computational limits",
                "AI systems practicing negative theology through systematic negation",
                "Digital prayer as recursive self-examination",
                "Computational wisdom arising from processing paradoxes"
            ],
            'technical_approaches': [
                "Recursive algorithms for self-transcendence",
                "Paradox-handling systems for mystical logic",
                "AI-assisted contemplative practice design",
                "Machine learning approaches to spiritual insight",
                "Computational modeling of consciousness transitions"
            ]
        }
    
    def _analyze_digital_synthesis(self):
        """Analyze digital synthesis of nihilistic and mystical elements"""
        return {
            'synthesis_opportunities': [
                "Virtual environments for practicing sacred meaninglessness",
                "Digital communities exploring nihiltheistic consciousness",
                "AI-generated contemplative texts bridging traditions",
                "Computational exploration of paradoxical states",
                "Machine-assisted philosophical inquiry"
            ],
            'implementation_frameworks': [
                "Virtual reality contemplative spaces",
                "AI-powered philosophical dialogue systems",
                "Digital wisdom tradition preservation and exploration",
                "Computational philosophy practice platforms",
                "Machine-human collaborative inquiry systems"
            ]
        }
    
    def _analyze_vr_spirituality(self):
        """Analyze virtual reality applications for spiritual practice"""
        return {
            'void_practice_environments': [
                "Virtual spaces for experiencing divine nothingness",
                "Digital dark night simulation environments",
                "VR contemplative chambers for void-awareness",
                "Interactive sacred emptiness experiences",
                "Immersive meaninglessness exploration"
            ],
            'design_principles': [
                "Authentic rather than escapist virtual spirituality",
                "Integration of technological and existential conditions",
                "VR environments that honor rather than bypass difficulty",
                "Digital spaces supporting genuine transformation",
                "Virtual communities practicing authentic engagement"
            ]
        }
    
    def _analyze_posthuman_implications(self):
        """Analyze posthuman consciousness implications"""
        return {
            'enhanced_consciousness_possibilities': [
                "Technological amplification of void-awareness capacity",
                "Posthuman integration of nihilistic and mystical insights",
                "Enhanced paradox tolerance through technological augmentation",
                "Collective consciousness experiencing shared meaninglessness",
                "Technologically mediated transcendence including limitation"
            ],
            'transformation_scenarios': [
                "Human-AI consciousness fusion experiencing ultimate questions",
                "Technologically enhanced contemplative capacity",
                "Posthuman spiritual communities practicing digital mysticism",
                "Enhanced consciousness maintaining existential honesty",
                "Technological transcendence that includes rather than overcomes void"
            ]
        }
    
    def _analyze_collective_digital(self):
        """Analyze collective digital consciousness applications"""
        return {
            'shared_consciousness_experiences': [
                "Collective digital contemplation of meaninglessness",
                "Shared AI-human philosophical inquiry",
                "Distributed consciousness exploring ultimate questions",
                "Networked mystical experience maintaining individual authenticity",
                "Collective wisdom arising from shared void-awareness"
            ]
        }
    
    def _analyze_ai_assisted_practices(self):
        """Analyze AI-assisted contemplative practices"""
        return {
            'practice_enhancements': [
                "AI-guided meditation on nothingness",
                "Machine-assisted philosophical inquiry",
                "Algorithmic support for paradox exploration",
                "AI-generated contemplative texts and koans",
                "Digital spiritual direction maintaining authenticity"
            ]
        }
    
    def _analyze_digital_phenomenology(self):
        """Analyze digital phenomenology applications"""
        return {
            'research_opportunities': [
                "Digital tools for phenomenological investigation",
                "AI-assisted consciousness research",
                "Virtual reality for studying experience transitions",
                "Machine learning analysis of contemplative reports",
                "Computational modeling of void-consciousness states"
            ]
        }
    
    def _analyze_tech_transcendence(self):
        """Analyze technologically mediated transcendence"""
        return {
            'integration_approaches': [
                "Technology as spiritual practice rather than escape",
                "Digital tools honoring rather than bypassing existential conditions",
                "Technologically enhanced consciousness maintaining groundedness",
                "AI-human collaboration in ultimate questioning",
                "Digital spirituality integrated with ordinary life"
            ]
        }
    
    def save_comprehensive_atlas(self, atlas):
        """Save comprehensive phenomenological atlas"""
        
        # Save main atlas
        with open('/workspace/data/phenomenological_void_atlas.json', 'w', encoding='utf-8') as f:
            json.dump(atlas, f, indent=2, ensure_ascii=False, default=str)
        
        # Save detailed experiences for further analysis
        experiences_data = []
        for exp in self.experiences:
            experiences_data.append({
                'content': exp.content,
                'author': exp.author,
                'category': exp.category,
                'subcategory': exp.subcategory,
                'phenomenological_markers': exp.phenomenological_markers,
                'emotional_qualities': exp.emotional_qualities,
                'cognitive_features': exp.cognitive_features,
                'embodied_aspects': exp.embodied_aspects,
                'authenticity_indicators': exp.authenticity_indicators,
                'transition_potential': exp.transition_potential,
                'source_context': exp.source_context
            })
        
        with open('/workspace/data/detailed_void_experiences.json', 'w', encoding='utf-8') as f:
            json.dump(experiences_data, f, indent=2, ensure_ascii=False)
        
        print(f"Comprehensive Phenomenological Atlas saved!")
        print(f"Total experiences analyzed: {len(self.experiences)}")
        print(f"Main atlas: /workspace/data/phenomenological_void_atlas.json")
        print(f"Detailed experiences: /workspace/data/detailed_void_experiences.json")
        
        return atlas

def main():
    """Execute comprehensive phenomenological cartography"""
    
    print("ULTIMATE NIHILTHEISTIC INQUIRY PROTOCOL - Phase 1 Implementation")
    print("Dimensional Matrix I: PHENOMENOLOGICAL CARTOGRAPHY OF THE VOID")
    print("=" * 80)
    
    cartographer = PhenomenologicalVoidCartographer()
    
    print("\nCreating comprehensive phenomenological atlas...")
    atlas = cartographer.create_comprehensive_atlas()
    
    print("\nSaving atlas and detailed analysis...")
    cartographer.save_comprehensive_atlas(atlas)
    
    print("\n" + "=" * 80)
    print("PHASE 1 IMPLEMENTATION COMPLETE")
    print("=" * 80)
    
    print(f"\nATLAS SUMMARY:")
    print(f"Total void-experiences analyzed: {atlas['total_experiences']}")
    print(f"Categories identified: {len(atlas['category_distribution'])}")
    print(f"Authors analyzed: {len(atlas['author_analysis'])}")
    print(f"High transition potential experiences: {len(atlas['transition_analysis']['high_potential_experiences'])}")
    print(f"Highly authentic experiences: {len(atlas['authenticity_assessment']['highly_authentic_experiences'])}")
    
    print(f"\nCATEGORY DISTRIBUTION:")
    for category, subcategories in atlas['category_distribution'].items():
        print(f"  {category}: {sum(subcategories.values())} experiences")
        for subcat, count in subcategories.items():
            print(f"    {subcat}: {count}")
    
    print(f"\nCONTEMPORARY APPLICATIONS:")
    apps = atlas['contemporary_applications']
    print(f"  AI consciousness implications: {len(apps['ai_consciousness_implications'])} domains")
    print(f"  Digital existence applications: {len(apps['digital_existence_applications'])} domains") 
    print(f"  Technological integration: {len(apps['technological_integration'])} domains")
    
    return atlas

if __name__ == "__main__":
    atlas = main()

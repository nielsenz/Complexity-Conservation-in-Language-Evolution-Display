import stanza
from collections import defaultdict
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import matplotlib.pyplot as plt
import seaborn as sns
import json 
import scipy.stats as stats
import traceback

class EnhancedComplexityTracker:
    def __init__(self):
        self.latin_nlp = stanza.Pipeline('la')
        self.spanish_nlp = stanza.Pipeline('es')
        self.corpus_dir = Path("corpus")

    def load_corpus(self) -> Dict[str, str]:
        """Load all texts from the corpus directory"""
        corpus = {}
    
    # Load Classical Latin
        latin_dir = self.corpus_dir / "classical_latin"
        for text_file in latin_dir.glob("*.txt"):
            with open(text_file, 'r', encoding='utf-8') as f:
                corpus[f"latin_{text_file.stem}"] = f.read()
    
    # Load Medieval Latin
        medieval_dir = self.corpus_dir / "medieval_latin"
        for text_file in medieval_dir.glob("*.txt"):
            with open(text_file, 'r', encoding='utf-8') as f:
                corpus[f"medieval_{text_file.stem}"] = f.read()
    
    # Load Early Spanish
        spanish_dir = self.corpus_dir / "early_spanish"
        for text_file in spanish_dir.glob("*.txt"):
            with open(text_file, 'r', encoding='utf-8') as f:
                corpus[f"spanish_{text_file.stem}"] = f.read()
    
        return corpus


    def analyze_analytical_constructions(self, text: str, language: str) -> Dict:
        """Track multi-word expressions that replace single morphological markers"""
        nlp = self.latin_nlp if language == 'la' else self.spanish_nlp
        doc = nlp(text)
        
        analytical_forms = {
            'future_tense': {
                'synthetic': 0,    # amabit
                'analytic': 0,     # va a amar
                'components': defaultdict(int)
            },
            'perfect_tense': {
                'synthetic': 0,    # amavit
                'analytic': 0,     # ha amado
                'components': defaultdict(int)
            },
            'passive_voice': {
                'synthetic': 0,    # amatur
                'analytic': 0,     # es amado
                'components': defaultdict(int)
            },
            'conditional': {
                'synthetic': 0,    # amaret
                'analytic': 0,     # amaría
                'components': defaultdict(int)
            }
        }
        
        for sent in doc.sentences:
            for word in sent.words:
                # Check for synthetic forms in Latin
                if language == 'la' and word.upos == 'VERB':
                    if 'Tense=Fut' in (word.feats or ''):
                        analytical_forms['future_tense']['synthetic'] += 1
                    elif 'Tense=Perf' in (word.feats or ''):
                        analytical_forms['perfect_tense']['synthetic'] += 1
                    elif 'Voice=Pass' in (word.feats or ''):
                        analytical_forms['passive_voice']['synthetic'] += 1
                
                # Check for analytical forms in Spanish
                if language == 'es':
                    if word.upos == 'AUX':
                        next_verb = self._find_next_verb(sent, word)
                        if next_verb:
                            construction = self._identify_analytical_construction(word, next_verb)
                            if construction:
                                analytical_forms[construction]['analytic'] += 1
                                analytical_forms[construction]['components'][word.text.lower()] += 1
                                analytical_forms[construction]['components'][next_verb.text.lower()] += 1
        
        return analytical_forms

    def _classify_preposition(self, prep_word, sentence) -> str:
        """
        Classify preposition usage type
        """
        try:
            # For Spanish
            if prep_word.text.lower() == 'de':
                # Check if it's replacing genitive
                for word in sentence.words:
                    if word.head == prep_word.id and word.deprel == 'nmod':
                        return 'case_replacement'
            elif prep_word.text.lower() in ['en', 'sobre', 'bajo']:
                return 'semantic'  # Spatial prepositions
            elif prep_word.text.lower() in ['a', 'para', 'por']:
                # Check for grammaticalized uses
                if any(w.deprel == 'iobj' and w.head == prep_word.id for w in sentence.words):
                    return 'case_replacement'
                return 'semantic'
            
            # For Latin (mostly semantic since it has case system)
            if prep_word.text.lower() in ['in', 'ad', 'ex', 'ab', 'cum']:
                return 'semantic'
                
            return 'other'  # Default case
        except Exception as e:
            print(f"Error in _classify_preposition: {e}")
            return 'other'
        
    def _classify_article(self, det_word, sentence, language: str) -> str:
        """
        Classify article usage type - only applies to Spanish as Latin has no articles
        """
        # Latin has no articles - all DET tags should be ignored for article analysis
        if language == 'la':
            return 'not_article'
        
        # Spanish articles only
        if language == 'es':
            if det_word.text.lower() in ['el', 'la', 'los', 'las']:
                # Check if it's marking case role
                if any(w.deprel in ['nsubj', 'obj'] and w.head == det_word.head for w in sentence.words):
                    return 'case_marking'
                return 'definiteness'
            elif det_word.text.lower() in ['un', 'una', 'unos', 'unas']:
                return 'definiteness'
    
        return 'other'


    def _find_next_verb(self, sentence, aux_word) -> Optional[stanza.models.common.doc.Word]:
        """Find the main verb that follows an auxiliary"""
        for word in sentence.words[aux_word.id:]:  # Start from auxiliary position
            if word.upos == 'VERB':
                return word
        return None

    def _identify_analytical_construction(self, aux_word, main_verb) -> Optional[str]:
        """Identify the type of analytical construction"""
        aux_text = aux_word.text.lower()
        verb_feats = main_verb.feats or ''
        
        if aux_text in ['ir', 'voy', 'vas', 'va'] and 'a' in [w.text.lower() for w in aux_word.sent.words]:
            return 'future_tense'
        elif aux_text in ['he', 'has', 'ha', 'hemos'] and 'VerbForm=Part' in verb_feats:
            return 'perfect_tense'
        elif aux_text in ['ser', 'es', 'son'] and 'VerbForm=Part' in verb_feats:
            return 'passive_voice'
        return None

    def analyze_function_words(self, text: str, language: str) -> Dict:
        """Detailed function word analysis"""
        nlp = self.latin_nlp if language == 'la' else self.spanish_nlp
        doc = nlp(text)
        
        metrics = {
            'prepositions': {
                'case_replacement': defaultdict(int),
                'semantic': defaultdict(int),
                'grammaticalized': defaultdict(int),
                'other': defaultdict(int)  # Add default 'other' category
            },
            'articles': {
                'definiteness': defaultdict(int),
                'case_marking': defaultdict(int),
                'other': defaultdict(int)  # Add default 'other' category
            },
            'conjunctions': {
                'coordination': defaultdict(int),
                'subordination': defaultdict(int)
            },
            'total_by_type': defaultdict(int),
            'word_count': 0  # Add total word count for proper normalization
        }
        
        try:
            for sent in doc.sentences:
                for word in sent.words:
                    # Count all words for normalization
                    metrics['word_count'] += 1
                    
                    if word.upos == 'ADP':  # Prepositions
                        prep_type = self._classify_preposition(word, sent)
                        metrics['prepositions'][prep_type][word.text.lower()] += 1
                        metrics['total_by_type']['prepositions'] += 1
                    
                    elif word.upos == 'DET':  # Articles
                        art_type = self._classify_article(word, sent, language)
                        # Only count actual articles, not Latin determiners
                        if art_type != 'not_article':
                            metrics['articles'][art_type][word.text.lower()] += 1
                            metrics['total_by_type']['articles'] += 1
                    
                    elif word.upos == 'CCONJ' or word.upos == 'SCONJ':
                        conj_type = 'coordination' if word.upos == 'CCONJ' else 'subordination'
                        metrics['conjunctions'][conj_type][word.text.lower()] += 1
                        metrics['total_by_type']['conjunctions'] += 1
        except Exception as e:
            print(f"Error in analyze_function_words: {e}")
            
        return metrics  
    def analyze_dependency_complexity(self, text: str, language: str) -> Dict:
        """More sophisticated dependency analysis"""
        nlp = self.latin_nlp if language == 'la' else self.spanish_nlp
        doc = nlp(text)
        
        metrics = {
            'path_lengths': [],
            'embedding_depth': [],
            'dependency_types': {
                'argument_structure': defaultdict(int),
                'modification': defaultdict(int),
                'coordination': defaultdict(int)
            },
            'dependency_distances': defaultdict(int),
            'average_depth': 0.0,
            'max_depth': 0
        }
        
        for sent in doc.sentences:
            # Track path lengths and distances
            for word in sent.words:
                if word.head != 0:  # Not root
                    distance = abs(word.id - word.head)
                    metrics['dependency_distances'][distance] += 1
                    
                    # Classify dependency types
                    if word.deprel in ['nsubj', 'obj', 'iobj', 'ccomp']:
                        metrics['dependency_types']['argument_structure'][word.deprel] += 1
                    elif word.deprel in ['amod', 'advmod', 'nmod']:
                        metrics['dependency_types']['modification'][word.deprel] += 1
                    elif word.deprel in ['conj', 'cc']:
                        metrics['dependency_types']['coordination'][word.deprel] += 1
            
            # Calculate embedding depth
            depth = self._calculate_dependency_depth(sent)
            metrics['embedding_depth'].append(depth)
            metrics['max_depth'] = max(metrics['max_depth'], depth)
        
        if metrics['embedding_depth']:
            metrics['average_depth'] = sum(metrics['embedding_depth']) / len(metrics['embedding_depth'])
        
        return metrics

    def _calculate_dependency_depth(self, sentence) -> int:
        """Calculate maximum dependency depth in a sentence"""
        depths = defaultdict(int)
        max_depth = 0
        
        for word in sentence.words:
            current = word
            depth = 0
            while current.head != 0:
                depth += 1
                current = sentence.words[current.head - 1]
            depths[word.id] = depth
            max_depth = max(max_depth, depth)
        
        return max_depth

    def track_clause_transformations(self, text: str, language: str) -> Dict:
        """Track how Latin constructions transform in Spanish"""
        nlp = self.latin_nlp if language == 'la' else self.spanish_nlp
        doc = nlp(text)
        
        transformations = {
            'ablative_absolute': {
                'temporal_clause': 0,
                'causal_clause': 0,
                'gerund': 0,
                'other': defaultdict(int)
            },
            'participial_constructions': {
                'relative_clause': 0,
                'finite_verb': 0,
                'other': defaultdict(int)
            },
            'subordination_strategies': {
                'que_clauses': 0,
                'gerund_clauses': 0,
                'infinitive_clauses': 0,
                'relative_clauses': 0
            }
        }
        
        for sent in doc.sentences:
            if language == 'la':
                self._analyze_latin_constructions(sent, transformations)
            else:
                self._analyze_spanish_constructions(sent, transformations)
        
        return transformations

    def _analyze_latin_constructions(self, sentence, metrics: Dict):
        """Analyze Latin-specific constructions"""
        for word in sentence.words:
            # Check for ablative absolute
            if ('Case=Abl' in (word.feats or '') and 
                'VerbForm=Part' in (word.feats or '')):
                metrics['ablative_absolute']['other']['found'] += 1
            
            # Check for participial constructions
            elif 'VerbForm=Part' in (word.feats or ''):
                metrics['participial_constructions']['other']['found'] += 1

    def _analyze_spanish_constructions(self, sentence, metrics: Dict):
        """Analyze Spanish-specific constructions"""
        for word in sentence.words:
            # Track different types of subordination
            if word.text.lower() == 'que' and word.upos == 'SCONJ':
                metrics['subordination_strategies']['que_clauses'] += 1
            elif 'VerbForm=Ger' in (word.feats or ''):
                metrics['subordination_strategies']['gerund_clauses'] += 1
            elif 'VerbForm=Inf' in (word.feats or ''):
                metrics['subordination_strategies']['infinitive_clauses'] += 1
            elif word.deprel == 'acl:relcl':
                metrics['subordination_strategies']['relative_clauses'] += 1

    def integrated_analysis(self, text: str, language: str) -> Dict:
        """
        Perform comprehensive analysis combining all metrics
        """
        results = {
            'analytical_constructions': self.analyze_analytical_constructions(text, language),
            'function_words': self.analyze_function_words(text, language),
            'dependency_complexity': self.analyze_dependency_complexity(text, language),
            'clause_transformations': self.track_clause_transformations(text, language)
        }
        
        # Add normalized metrics
        word_count = len(text.split())
        results['normalized_metrics'] = self._calculate_normalized_metrics(results, word_count)
        
        return results

    def _calculate_normalized_metrics(self, results: Dict, word_count: int) -> Dict:
        """
        Calculate normalized versions of key metrics
        """
        normalized = {
            'analytical_density': {},
            'function_word_density': {},
            'complexity_scores': {}
        }
        
        # Normalize analytical constructions
        for construction_type, counts in results['analytical_constructions'].items():
            if isinstance(counts, dict) and 'analytic' in counts:
                normalized['analytical_density'][construction_type] = counts['analytic'] / word_count
        
        # Normalize function words
        for category, counts in results['function_words']['total_by_type'].items():
            normalized['function_word_density'][category] = counts / word_count
        
        # Calculate complexity scores
        normalized['complexity_scores'] = {
            'dependency_depth': sum(results['dependency_complexity']['embedding_depth']) / len(results['dependency_complexity']['embedding_depth']) if results['dependency_complexity']['embedding_depth'] else 0,
            'clause_complexity': len(results['clause_transformations']['subordination_strategies']) / word_count
        }
        
        return normalized

    def generate_enhanced_report(self, results: Dict):
        """
        Generate a detailed report including all new metrics
        """
        report = []
        report.append("Enhanced Complexity Analysis Report")
        report.append("=" * 50)
        
        for text_name, analysis in results.items():
            report.append(f"\nAnalysis for {text_name}")
            report.append("-" * 30)
            
            # Analytical Constructions
            report.append("\nAnalytical Constructions:")
            for const_type, counts in analysis['analytical_constructions'].items():
                if isinstance(counts, dict) and 'synthetic' in counts:
                    report.append(f"  {const_type}:")
                    report.append(f"    Synthetic: {counts['synthetic']}")
                    report.append(f"    Analytic: {counts['analytic']}")
            
            # Function Words
            report.append("\nFunction Word Analysis:")
            for category, subcounts in analysis['function_words'].items():
                if category != 'total_by_type':
                    report.append(f"  {category}:")
                    for subcat, counts in subcounts.items():
                        if isinstance(counts, dict):
                            report.append(f"    {subcat}: {sum(counts.values())}")
                        else:
                            report.append(f"    {subcat}: {counts}")
            
            # Dependency Complexity
            report.append("\nDependency Complexity:")
            dep_complex = analysis['dependency_complexity']
            report.append(f"  Average Depth: {dep_complex['average_depth']:.2f}")
            report.append(f"  Maximum Depth: {dep_complex['max_depth']}")
            report.append(f"  Argument Structures: {sum(dep_complex['dependency_types']['argument_structure'].values())}")
            
            # Clause Transformations
            report.append("\nClause Transformations:")
            clause_trans = analysis['clause_transformations']
            if 'subordination_strategies' in clause_trans:
                report.append("  Subordination Strategies:")
                for strategy, count in clause_trans['subordination_strategies'].items():
                    report.append(f"    {strategy}: {count}")
            
            # Normalized Metrics
            report.append("\nNormalized Metrics:")
            norm = analysis['normalized_metrics']
            report.append("  Analytical Density:")
            for const_type, density in norm['analytical_density'].items():
                report.append(f"    {const_type}: {density:.4f}")
            report.append("  Complexity Scores:")
            for score_type, value in norm['complexity_scores'].items():
                report.append(f"    {score_type}: {value:.4f}")
            
            report.append("\n" + "=" * 50)
        
        return "\n".join(report)

    def analyze_full_corpus(self):
        """
        Analyze entire corpus with enhanced metrics
        """
        corpus = self.load_corpus()
        results = {}
        
        print("Starting enhanced corpus analysis...")
        
        for text_name, text_content in corpus.items():
            print(f"Analyzing {text_name}...")
            language = 'la' if 'latin' in text_name else 'es'
            
            try:
                results[text_name] = self.integrated_analysis(text_content, language)
            except Exception as e:
                print(f"Error analyzing {text_name}: {e}")
                continue
        
        return results

class StatisticalAnalysis:
    def __init__(self, results):
        self.results = results
        self.period_data = self._organize_by_period()

    def _organize_by_period(self):
        period_data = {
            'Classical': [],
            'Medieval': [],
            'Spanish': []
        }
        
        for text_name, data in self.results.items():
            if text_name.startswith('latin_'):
                period_data['Classical'].append(data)
            elif text_name.startswith('medieval_'):
                period_data['Medieval'].append(data)
            elif text_name.startswith('spanish_'):
                period_data['Spanish'].append(data)
        return period_data

    def analyze_dependency_evolution(self):
        """Analyze dependency complexity evolution"""
        depths = {
            period: [text['dependency_complexity']['average_depth'] 
                    for text in texts]
            for period, texts in self.period_data.items()
        }
        
        # Parametric test (ANOVA)
        f_stat, anova_p = stats.f_oneway(*depths.values())
        
        # Non-parametric test (Kruskal-Wallis)
        h_stat, kw_p = stats.kruskal(*depths.values())
        
        # Mann-Whitney tests
        mw_tests = {}
        for p1, p2 in [('Classical', 'Medieval'), ('Medieval', 'Spanish'), ('Classical', 'Spanish')]:
            stat, p_val = stats.mannwhitneyu(depths[p1], depths[p2], alternative='two-sided')
            mw_tests[f'{p1}_vs_{p2}'] = {'statistic': stat, 'p_value': p_val}
        
        # Effect sizes
        effect_sizes = {
            'Classical_vs_Medieval': self.cohens_d(depths['Classical'], depths['Medieval']),
            'Medieval_vs_Spanish': self.cohens_d(depths['Medieval'], depths['Spanish']),
            'Classical_vs_Spanish': self.cohens_d(depths['Classical'], depths['Spanish'])
        }
        
        # Period stats with confidence intervals
        period_stats = {
            period: {
                'mean': np.mean(values),
                'std': np.std(values),
                'n': len(values),
                'ci': self.bootstrap_ci(values)
            }
            for period, values in depths.items()
        }
        
        return {
            'name': 'Dependency Evolution Analysis',
            'parametric': {'f_stat': f_stat, 'p_value': anova_p},
            'non_parametric': {
                'kruskal_wallis': {'h_stat': h_stat, 'p_value': kw_p},
                'mann_whitney': mw_tests
            },
            'effect_sizes': effect_sizes,
            'period_stats': period_stats,
            'raw_data': depths
        }

    def analyze_article_development(self):
        """Analyze article system development with robust error handling"""
        def get_article_rates(texts):
            rates = []
            for text in texts:
                try:
                    # Debug print to help identify structure
                    print(f"Text structure: {text.keys()}")
                    
                    # Get articles with error handling
                    articles_dict = text['function_words']['articles']
                    print(f"Articles dict: {articles_dict}")
                    
                    # Sum all article types safely
                    total_articles = (
                        sum(articles_dict['definiteness'].values() if isinstance(articles_dict['definiteness'], dict) else articles_dict['definiteness']) +
                        sum(articles_dict['case_marking'].values() if isinstance(articles_dict['case_marking'], dict) else articles_dict['case_marking']) +
                        sum(articles_dict['other'].values() if isinstance(articles_dict['other'], dict) else articles_dict['other'])
                    )
                    
                    # Get text length from word count (proper normalization)
                    text_length = None
                    if 'function_words' in text and 'word_count' in text['function_words']:
                        text_length = text['function_words']['word_count']
                    
                    # Ensure we have a valid text length
                    if text_length and text_length > 0:
                        print(f"Total articles: {total_articles}, Text length (words): {text_length}")
                        # Calculate articles per 1000 words (standard linguistic normalization)
                        article_rate = (total_articles / text_length) * 1000
                        rates.append(article_rate)
                    else:
                        print(f"Warning: Invalid text length for text. Articles: {total_articles}")
                        
                except (KeyError, TypeError, AttributeError) as e:
                    print(f"Error processing text: {e}")
                    print(f"Text structure was: {text.keys() if isinstance(text, dict) else 'Not a dict'}")
                    continue
            return rates

        try:
            # Get rates for each period
            article_rates = {
                period: get_article_rates(texts)
                for period, texts in self.period_data.items()
            }
            
            print(f"Article rates by period: {article_rates}")
            
            # Only proceed if we have valid data
            valid_periods = {k: v for k, v in article_rates.items() if len(v) > 0}
            if not valid_periods:
                print("No valid periods found with article data")
                print("Period data available:", self.period_data.keys())
                print("Article rates found:", article_rates)
                return {
                    'name': 'Article Development Analysis',
                    'error': 'No valid data found',
                    'raw_data': article_rates
                }
            
            if len(valid_periods) >= 2:
                # Run statistical tests
                f_stat, anova_p = stats.f_oneway(*valid_periods.values())
                h_stat, kw_p = stats.kruskal(*valid_periods.values())
                
                # Calculate pairwise tests and effect sizes
                mw_tests = {}
                effect_sizes = {}
                for p1, p2 in [('Classical', 'Medieval'), ('Medieval', 'Spanish'), ('Classical', 'Spanish')]:
                    if p1 in valid_periods and p2 in valid_periods:
                        stat, p_val = stats.mannwhitneyu(valid_periods[p1], valid_periods[p2], 
                                                    alternative='two-sided')
                        mw_tests[f'{p1}_vs_{p2}'] = {'statistic': stat, 'p_value': p_val}
                        effect_sizes[f'{p1}_vs_{p2}'] = self.cohens_d(valid_periods[p1], 
                                                                    valid_periods[p2])
                
                # Calculate period statistics
                period_stats = {
                    period: {
                        'mean': np.mean(rates),
                        'std': np.std(rates),
                        'n': len(rates),
                        'ci': self.bootstrap_ci(rates)
                    }
                    for period, rates in valid_periods.items()
                }
                
                return {
                    'name': 'Article Development Analysis',
                    'parametric': {'f_stat': f_stat, 'p_value': anova_p},
                    'non_parametric': {
                        'kruskal_wallis': {'h_stat': h_stat, 'p_value': kw_p},
                        'mann_whitney': mw_tests
                    },
                    'effect_sizes': effect_sizes,
                    'period_stats': period_stats,
                    'raw_data': article_rates
                }
            else:
                return {
                    'name': 'Article Development Analysis',
                    'error': 'Insufficient data for analysis',
                    'raw_data': article_rates,
                    'valid_periods': len(valid_periods)
                }
                
        except Exception as e:
            print(f"Error in article analysis: {str(e)}")
            return {
                'name': 'Article Development Analysis',
                'error': str(e),
                'traceback': traceback.format_exc()
            }
        
    def format_analytical_shift(self, result):
        """Format analytical shift results with complete detail"""
        output = []
        output.append("\nAnalytical Construction Analysis")
        output.append("-" * 40)
        
        # Construction counts by period
        output.append("\nConstruction Counts by Period:")
        for period, (syn, ana) in result['construction_counts'].items():
            output.append(f"  {period}:")
            output.append(f"    Synthetic: {syn:,}")
            output.append(f"    Analytic: {ana:,}")
            total = syn + ana
            if total > 0:
                output.append(f"    Synthetic Ratio: {syn/total:.4f}")
                output.append(f"    Analytic Ratio: {ana/total:.4f}")
        
        # Total counts
        if 'total_counts' in result:
            output.append("\nTotal Counts:")
            output.append(f"  Total Synthetic: {result['total_counts']['synthetic']:,}")
            output.append(f"  Total Analytic: {result['total_counts']['analytic']:,}")
        
        # Statistical test results
        if 'fishers_exact' in result:
            output.append("\nStatistical Tests:")
            output.append("Fisher's Exact Test:")
            output.append(f"  Odds Ratio: {result['fishers_exact']['oddsratio']:.4f}")
            output.append(f"  p-value: {result['fishers_exact']['p_value']:.4g}")
        
        # Effect size if available
        if 'effect_size' in result:
            output.append("\nEffect Size:")
            output.append(f"  Cramer's V: {result['effect_size']['cramers_v']:.4f}")
        
        # Proportional change
        if 'proportions' in result:
            output.append("\nProportional Change:")
            for period, stats in result['proportions'].items():
                output.append(f"  {period}:")
                output.append(f"    Synthetic: {stats['synthetic_ratio']:.4f}")
                output.append(f"    Analytic: {stats['analytic_ratio']:.4f}")
        
        # Any error messages
        if 'error' in result:
            output.append(f"\nNote: {result['error']}")
        
        return "\n".join(output)
        
    def analyze_analytical_shift(self):
        """Analyze the shift from synthetic to analytical constructions with robust debug"""
        print("Starting analytical shift analysis...")
        
        try:
            # Get counts for each period
            construction_counts = {}
            total_synthetic = 0
            total_analytic = 0
            
            for period, texts in self.period_data.items():
                synthetic = 0
                analytic = 0
                
                for text in texts:
                    constructions = text.get('analytical_constructions', {})
                    for const_type in ['passive_voice', 'perfect_tense', 'future_tense']:
                        const_data = constructions.get(const_type, {})
                        synthetic += const_data.get('synthetic', 0)
                        analytic += const_data.get('analytic', 0)
                
                print(f"DEBUG: {period} total - synthetic: {synthetic}, analytic: {analytic}")
                construction_counts[period] = (synthetic, analytic)
                total_synthetic += synthetic
                total_analytic += analytic

            print(f"DEBUG: Total counts - synthetic: {total_synthetic}, analytic: {total_analytic}")
            print(f"DEBUG: Construction counts: {construction_counts}")

            # Create contingency table
            contingency = np.array([[syn, ana] for period, (syn, ana) in construction_counts.items()])
            print(f"DEBUG: Contingency table shape: {contingency.shape}")
            print(f"DEBUG: Contingency table:\n{contingency}")

            result = {
                'name': 'Analytical Construction Shift',
                'construction_counts': construction_counts,
                'total_counts': {
                    'synthetic': total_synthetic,
                    'analytic': total_analytic
                }
            }

            # Check if we have data for Fisher's exact test
            if contingency.sum() > 0:
                try:
                    print("DEBUG: Attempting Fisher's exact test...")
                    oddsratio, p_value = stats.fisher_exact(contingency)
                    result['fishers_exact'] = {
                        'oddsratio': float(oddsratio),
                        'p_value': float(p_value)
                    }
                    print(f"DEBUG: Fisher's test results - OR: {oddsratio:.4f}, p: {p_value:.4f}")
                except Exception as e:
                    print(f"DEBUG: Fisher's test failed: {str(e)}")
                    result['error'] = f'Statistical test failed: {str(e)}'
            else:
                result['error'] = 'No data for statistical testing'

            # Add proportions
            proportions = {}
            for period, (syn, ana) in construction_counts.items():
                total = syn + ana
                if total > 0:
                    proportions[period] = {
                        'synthetic_ratio': syn/total,
                        'analytic_ratio': ana/total,
                        'total_constructions': total
                    }
                else:
                    proportions[period] = {
                        'synthetic_ratio': 0,
                        'analytic_ratio': 0,
                        'total_constructions': 0
                    }
            result['proportions'] = proportions

            print("DEBUG: Analysis complete.")
            return result
                    
        except Exception as e:
            print(f"DEBUG: Fatal error in analysis: {str(e)}")
            print(f"DEBUG: Error traceback: {traceback.format_exc()}")
            return {
                'name': 'Analytical Construction Shift',
                'error': str(e),
                'construction_counts': construction_counts if 'construction_counts' in locals() else None
            }
                
    def cohens_d(self, group1, group2):
        """Calculate Cohen's d effect size"""
        n1, n2 = len(group1), len(group2)
        var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
        pooled_se = np.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
        return (np.mean(group1) - np.mean(group2)) / pooled_se

    def bootstrap_ci(self, data, n_bootstrap=1000):
        """Calculate 95% confidence intervals"""
        bootstrap_samples = []
        for _ in range(n_bootstrap):
            sample = np.random.choice(data, size=len(data), replace=True)
            bootstrap_samples.append(np.mean(sample))
        return np.percentile(bootstrap_samples, [2.5, 97.5])

    def format_results(self, result):
        """Format a single analysis result with robust error handling"""
        output = []
        output.append(f"\n{result.get('name', 'Analysis Results')}")
        output.append("-" * 40)
        
        # Always show construction counts if available
        if 'construction_counts' in result:
            output.append("\nConstruction Counts:")
            for period, (syn, ana) in result['construction_counts'].items():
                output.append(f"  {period}:")
                output.append(f"    Synthetic: {syn:,}")
                output.append(f"    Analytic: {ana:,}")
        
        if 'total_counts' in result:
            totals = result['total_counts']
            output.append("\nTotal Counts:")
            output.append(f"  Synthetic: {totals['synthetic']:,}")
            output.append(f"  Analytic: {totals['analytic']:,}")
        
        # Show proportions
        if 'proportions' in result:
            output.append("\nProportions:")
            for period, stats in result['proportions'].items():
                output.append(f"  {period}:")
                output.append(f"    Synthetic Ratio: {stats['synthetic_ratio']:.4f}")
                output.append(f"    Analytic Ratio: {stats['analytic_ratio']:.4f}")
                output.append(f"    Total Constructions: {stats['total_constructions']:,}")

        # Show statistical test results
        if 'fishers_exact' in result:
            output.append("\nFisher's Exact Test:")
            fisher = result['fishers_exact']
            output.append(f"  Odds ratio: {fisher['oddsratio']:.4f}")
            output.append(f"  p-value: {fisher['p_value']:.4g}")

        # Show any errors
        if 'error' in result:
            output.append(f"\nAnalysis Note: {result['error']}")
            
        return "\n".join(output)

    def run_all_analyses(self):
        """Run all analyses and format results properly"""
        formatted_output = ["Enhanced Statistical Analysis Results", "=" * 50]
        
        # Run analyses
        dependency_results = self.analyze_dependency_evolution()
        analytical_results = self.analyze_analytical_shift()
        article_results = self.analyze_article_development()

        # Format dependency evolution
        formatted_output.extend(["\ndependency_evolution:", self.format_results(dependency_results)])
        formatted_output.append("=" * 50)

        # Format analytical shift - Special handling
        formatted_output.append("\nanalytical_shift:")
        analytical_output = []
        analytical_output.append("\nConstruction Counts by Period:")
        for period, (syn, ana) in analytical_results['construction_counts'].items():
            analytical_output.append(f"  {period}:")
            analytical_output.append(f"    Synthetic: {syn:,}")
            analytical_output.append(f"    Analytic: {ana:,}")
            total = syn + ana
            if total > 0:
                analytical_output.append(f"    Synthetic Ratio: {syn/total:.4f}")
                analytical_output.append(f"    Analytic Ratio: {ana/total:.4f}")

        analytical_output.append("\nStatistical Tests:")
        if 'fishers_exact' in analytical_results:
            analytical_output.append("Fisher's Exact Test:")
            fisher = analytical_results['fishers_exact']
            analytical_output.append(f"  Odds Ratio: {fisher['oddsratio']:.4f}")
            analytical_output.append(f"  p-value: {fisher['p_value']:.4g}")

        if 'proportions' in analytical_results:
            analytical_output.append("\nProportional Changes:")
            for period, stats in analytical_results['proportions'].items():
                analytical_output.append(f"  {period}:")
                analytical_output.append(f"    Synthetic: {stats['synthetic_ratio']:.4f}")
                analytical_output.append(f"    Analytic: {stats['analytic_ratio']:.4f}")

        formatted_output.append("\n".join(analytical_output))
        formatted_output.append("=" * 50)

        # Format article development
        formatted_output.extend(["\narticle_development:", self.format_results(article_results)])
        formatted_output.append("=" * 50)

        formatted_output = "\n".join(formatted_output)

        return {
            'raw_results': {
                'dependency_evolution': dependency_results,
                'analytical_shift': analytical_results,
                'article_development': article_results
            },
            'formatted_output': formatted_output
        }
    
if __name__ == "__main__":
    # Initialize and run corpus analysis
    tracker = EnhancedComplexityTracker()
    print("Starting enhanced analysis of complete corpus...")
    results = tracker.analyze_full_corpus()

        # Debug print - check what's in results
    for text_name, text_data in results.items():
        print(f"\nAnalyzing {text_name}:")
        if 'analytical_constructions' in text_data:
            print(f"Analytical constructions found: {text_data['analytical_constructions']}")
        else:
            print("No analytical constructions found")
    
    # Run statistical analyses
    stats_analyzer = StatisticalAnalysis(results)
    analysis_results = stats_analyzer.run_all_analyses()
    
    # Print descriptive results
    print(tracker.generate_enhanced_report(results))
    
    # Print statistical results
    print("\nEnhanced Statistical Analysis Results:")
    print("=" * 50)
    
    # Access raw results
    raw_results = analysis_results['raw_results']
    
    for analysis_name, result in raw_results.items():
        print(f"\n{analysis_name}:")
        
        # Print parametric test results
        print("  Test Statistics:")
        if 'parametric' in result:
            print(f"    ANOVA:")
            print(f"      F-statistic: {result['parametric']['f_stat']:.4f}")
            print(f"      p-value: {result['parametric']['p_value']:.4f}")
        
        # Print non-parametric test results
        if 'non_parametric' in result:
            print("\n    Non-parametric Tests:")
            kw = result['non_parametric']['kruskal_wallis']
            print(f"      Kruskal-Wallis H: {kw['h_stat']:.4f}")
            print(f"      p-value: {kw['p_value']:.4f}")
            
            print("\n    Mann-Whitney Tests:")
            for pair, stats in result['non_parametric']['mann_whitney'].items():
                print(f"      {pair}:")
                print(f"        Statistic: {stats['statistic']:.4f}")
                print(f"        p-value: {stats['p_value']:.4f}")
        
        # Print effect sizes
        if 'effect_sizes' in result:
            print("\n  Effect Sizes:")
            for comparison, effect in result['effect_sizes'].items():
                print(f"    {comparison}: {effect:.4f}")
        
        # Print period statistics
        if 'period_stats' in result:
            print("\n  Period Statistics:")
            for period, stats in result['period_stats'].items():
                print(f"\n    {period}:")
                for stat_name, value in stats.items():
                    if stat_name != 'ci':
                        print(f"      {stat_name}: {value:.4f}")
                    else:
                        print(f"      95% CI: [{value[0]:.4f}, {value[1]:.4f}]")
        
        # Print line for readability
        print("\n" + "=" * 50)
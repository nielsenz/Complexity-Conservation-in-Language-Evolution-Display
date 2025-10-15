#!/usr/bin/env python3
"""
Create figures for Latin-Spanish complexity conservation paper.

This script generates the two main figures:
1. Article development across historical periods
2. Analytical vs synthetic construction shift
"""

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Set style for academic publication
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def create_article_development_figure():
    """Create Figure 1: Article Development Across Periods"""
    
    # Data from corrected analysis
    periods = ['Classical\nLatin', 'Medieval\nLatin', 'Early\nSpanish']
    means = [0.000, 0.000, 107.018]
    errors = [0.000, 0.000, 22.970]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Create bars with different colors for each period
    colors = ['#8B4513', '#A0522D', '#CD853F']  # Brown tones
    bars = ax.bar(periods, means, yerr=errors, capsize=10, 
                  color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
    
    # Customize the plot
    ax.set_ylabel('Articles per 1000 words', fontsize=14, fontweight='bold')
    ax.set_title('Development of Article System from Latin to Spanish', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_ylim(0, 140)
    ax.grid(axis='y', alpha=0.3)
    
    # Add significance annotation
    ax.text(2, 120, '***', fontsize=20, ha='center', fontweight='bold')
    ax.text(2, 115, 'p = 0.0007', fontsize=12, ha='center', style='italic')
    
    # Add confidence interval text
    ax.text(2, 95, '95% CI: [85.8, 122.4]', fontsize=10, ha='center')
    
    # Improve x-axis labels
    ax.set_xlabel('Historical Period', fontsize=14, fontweight='bold')
    ax.tick_params(axis='both', which='major', labelsize=12)
    
    # Add value labels on bars
    for i, (mean, error) in enumerate(zip(means, errors)):
        if mean > 0:
            ax.text(i, mean + error + 5, f'{mean:.1f}', 
                   ha='center', va='bottom', fontsize=11, fontweight='bold')
        else:
            ax.text(i, 5, '0', ha='center', va='bottom', 
                   fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    
    # Save as PDF for publication
    plt.savefig('/Users/znielsen/projects/python/linguistics/computation-complexity/display/latin-spanish-complexity/results/figures/figure1_articles.pdf', 
                dpi=300, bbox_inches='tight')
    plt.savefig('/Users/znielsen/projects/python/linguistics/computation-complexity/display/latin-spanish-complexity/results/figures/figure1_articles.png', 
                dpi=300, bbox_inches='tight')
    
    print("Figure 1 saved: Article Development Across Periods")
    plt.show()

def create_construction_shift_figure():
    """Create Figure 2: Analytical vs Synthetic Constructions"""
    
    # Data from analysis
    periods = ['Classical Latin', 'Early Spanish']
    synthetic_counts = [6182, 0]
    analytical_counts = [0, 22]
    
    # Create figure with side-by-side bars
    fig, ax = plt.subplots(figsize=(12, 8))
    
    x = np.arange(len(periods))
    width = 0.35
    
    # Create bars
    bars1 = ax.bar(x - width/2, synthetic_counts, width, 
                   label='Synthetic Constructions', 
                   color='#4472C4', alpha=0.8, edgecolor='black')
    bars2 = ax.bar(x + width/2, analytical_counts, width,
                   label='Analytical Constructions', 
                   color='#E76F51', alpha=0.8, edgecolor='black')
    
    # Customize the plot
    ax.set_ylabel('Number of Constructions', fontsize=14, fontweight='bold')
    ax.set_xlabel('Historical Period', fontsize=14, fontweight='bold')
    ax.set_title('Shift from Synthetic to Analytical Constructions', 
                 fontsize=16, fontweight='bold', pad=20)
    ax.set_xticks(x)
    ax.set_xticklabels(periods)
    ax.legend(loc='upper right', fontsize=12)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.text(bar.get_x() + bar.get_width()/2., height + 50,
                       f'{int(height)}', ha='center', va='bottom', 
                       fontsize=11, fontweight='bold')
    
    # Add significance annotation
    ax.text(0.5, 6500, "Fisher's Exact Test", ha='center', 
            fontsize=12, style='italic')
    ax.text(0.5, 6200, 'p = 0.0001', ha='center', 
            fontsize=12, fontweight='bold')
    ax.text(0.5, 5900, 'Complete Structural Transition', ha='center', 
            fontsize=11)
    
    # Set y-axis to accommodate both scales
    ax.set_ylim(0, 6800)
    
    plt.tight_layout()
    
    # Save as PDF for publication
    plt.savefig('/Users/znielsen/projects/python/linguistics/computation-complexity/display/latin-spanish-complexity/results/figures/figure2_constructions.pdf', 
                dpi=300, bbox_inches='tight')
    plt.savefig('/Users/znielsen/projects/python/linguistics/computation-complexity/display/latin-spanish-complexity/results/figures/figure2_constructions.png', 
                dpi=300, bbox_inches='tight')
    
    print("Figure 2 saved: Analytical vs Synthetic Constructions")
    plt.show()

def create_summary_stats_table():
    """Create a summary table of key statistical results"""
    
    import pandas as pd
    
    # Key results from the analysis
    results_data = {
        'Measure': [
            'Article Development',
            'Article Development', 
            'Article Development',
            'Construction Shift',
            'Dependency Complexity'
        ],
        'Period': [
            'Classical Latin',
            'Medieval Latin',
            'Early Spanish', 
            'Classical → Spanish',
            'All Periods'
        ],
        'Value': [
            '0.000 ± 0.000',
            '0.000 ± 0.000',
            '107.018 ± 22.970',
            '6,182 → 22',
            'Non-significant'
        ],
        'Statistical_Test': [
            'Kruskal-Wallis H = 14.619',
            'Kruskal-Wallis H = 14.619',
            'Kruskal-Wallis H = 14.619',
            "Fisher's Exact Test",
            'Kruskal-Wallis H = 4.343'
        ],
        'P_Value': [
            '0.0007',
            '0.0007',
            '0.0007',
            '0.0001',
            '0.1140'
        ],
        'Significance': [
            '***',
            '***', 
            '***',
            '***',
            'ns'
        ]
    }
    
    df = pd.DataFrame(results_data)
    
    # Save as CSV
    df.to_csv('/Users/znielsen/projects/python/linguistics/computation-complexity/display/latin-spanish-complexity/results/tables/statistical_summary.csv', 
              index=False)
    
    print("Statistical summary table saved")
    return df

if __name__ == "__main__":
    print("Creating figures for Latin-Spanish complexity conservation paper...")
    print("=" * 60)
    
    # Create both figures
    create_article_development_figure()
    print()
    create_construction_shift_figure()
    print()
    
    # Create summary table
    summary_df = create_summary_stats_table()
    print()
    print("Summary of key results:")
    print(summary_df)
    
    print("\nAll figures and tables created successfully!")
    print("Files saved in /results/figures/ and /results/tables/")
#!/usr/bin/env python3
"""
Generate sample datasets for testing.
Based on sample_generator.py.
"""
import pandas as pd
import numpy as np
import random
from pathlib import Path

class DataPreparer:
    """Generate sample datasets with controlled patterns."""
    
    @staticmethod
    def generate_hookworm_data(n: int = 100) -> pd.DataFrame:
        """Generate hookworm infection dataset."""
        np.random.seed(42)
        random.seed(42)
        
        # Risk factors
        is_rural = np.random.choice([0, 1], n, p=[0.6, 0.4])
        shoe_pattern = np.random.choice(['Always', 'Sometimes', 'Never'], n, p=[0.3, 0.4, 0.3])
        edu_levels = np.random.choice(['Illiterate', 'Primary', 'Secondary', 'Higher'], n, p=[0.3, 0.3, 0.25, 0.15])
        water_sources = np.random.choice(['Tap', 'Spring', 'River', 'Well'], n, p=[0.3, 0.3, 0.3, 0.1])
        
        # Infection probability
        hookworm = np.zeros(n)
        for i in range(n):
            risk = 0
            if is_rural[i]: risk += 1
            if shoe_pattern[i] == 'Never': risk += 1
            if edu_levels[i] == 'Illiterate': risk += 1
            if water_sources[i] in ['Spring', 'River']: risk += 1
            
            prob = 0.1 + risk * 0.15
            prob = min(prob, 0.8)
            hookworm[i] = 1 if np.random.random() < prob else 0
        
        # Hemoglobin
        hb = np.zeros(n)
        for i in range(n):
            if hookworm[i] == 1:
                hb[i] = np.random.uniform(9.0, 11.5)
            else:
                hb[i] = np.random.uniform(11.5, 14.5)
        
        df = pd.DataFrame({
            'patient_id': [f'P{i:05d}' for i in range(100, 100 + n)],
            'age': np.random.randint(18, 45, n),
            'education': edu_levels,
            'residence': ['Rural' if x else 'Urban' for x in is_rural],
            'water_source': water_sources,
            'shoe_wearing': shoe_pattern,
            'hemoglobin': np.round(hb, 1),
            'hookworm': hookworm.astype(int)
        })
        
        df['anemia'] = (df['hemoglobin'] < 11).astype(int)
        return df
    
    @staticmethod
    def save_dataset(df: pd.DataFrame, path: str) -> None:
        """Save dataset to file."""
        path = Path(path)
        if path.suffix == '.csv':
            df.to_csv(path, index=False)
        else:
            df.to_excel(path.with_suffix('.xlsx'), index=False)

def main():
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    output = sys.argv[2] if len(sys.argv) > 2 else 'sample_data.csv'
    
    df = DataPreparer.generate_hookworm_data(n)
    DataPreparer.save_dataset(df, output)
    print(f"Generated {n} rows saved to {output}")
    print(f"Hookworm prevalence: {df['hookworm'].mean()*100:.1f}%")

if __name__ == "__main__":
    main()

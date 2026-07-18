import json
import sys
sys.path.insert(0, '/ai-inventor/.claude/skills/aii-semscholar-bib/scripts')
from aii_semscholar_bib__fetch import core_semscholar_bib_fetch

# Prepare references with available DOIs/ArXiv IDs
references = [
    {"doi": "10.48550/arXiv.1706.03762", "author": "Guo", "year": 2017},  # On calibration of modern neural networks
    {"title": "Semantic uncertainty: Linguistic invariances for uncertainty estimation in natural language generation", "author": "Kuhn", "year": 2023},
    {"title": "Exploratory annealed decoding for verifiable reinforcement learning", "author": "Yang", "year": 2024},
    {"doi": "10.48550/arXiv.1909.13557", "author": "Kull", "year": 2019},  # Dirichlet calibration
    {"title": "Parameterized temperature scaling for boosting the expressive power of convolutional neural network architectures", "author": "Tomani", "year": 2021},
    {"title": "Sample-dependent adaptive temperature scaling for improved calibration", "author": "Joy", "year": 2023},
    {"arxiv": "2409.19817", "author": "Xie", "year": 2024},  # Calibrating language models with adaptive temperature scaling
    {"arxiv": "2305.14975", "author": "Tian", "year": 2023},  # Just ask for calibration
    {"doi": "10.1002/j.1538-7305.1948.tb01338.x", "author": "Shannon", "year": 1948},  # A mathematical theory of communication
    {"doi": "10.48550/arXiv.1506.02142", "author": "Gal", "year": 2016},  # Dropout as Bayesian approximation
    {"title": "Information theory and statistical mechanics", "author": "Jaynes", "year": 1957},
    {"doi": "10.1126/science.220.4598.671", "author": "Kirkpatrick", "year": 1983},  # Optimization by simulated annealing
    {"doi": "10.1175/1520-0493(1950)078<0001:VOFETI>2.0.CO;2", "author": "Brier", "year": 1950},  # Verification of forecasts
    {"doi": "10.48550/arXiv.1705.03551", "author": "Joshi", "year": 2017},  # TriviaQA
    {"arxiv": "1804.07461", "author": "Wang", "year": 2018},  # GLUE
    {"arxiv": "2109.07914", "author": "Lin", "year": 2021},  # TruthfulQA
]

# Try to fetch BibTeX entries
result = core_semscholar_bib_fetch(references)
print(json.dumps(result, indent=2))

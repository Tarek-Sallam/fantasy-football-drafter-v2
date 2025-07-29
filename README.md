# Fantasy Football RL Drafter

A reinforcement learning-based fantasy football draft assistant

## Project Structure

```
fantasy_drafter/
│
├── data/                    # Data storage
│   ├── raw/                 # Unprocessed scraped/downloaded files
│   ├── processed/           # Cleaned and feature-rich datasets
│   └── adp/                 # ADP-specific datasets
│
├── data_pipeline/           # Data gathering and preprocessing
│   ├── __init__.py
│
├── envs/                    # Custom OpenAI Gym-style environments
│   ├── __init__.py
│
├── agents/                  # RL agent implementations
│   ├── __init__.py
│
├── models/                  # Neural network models
│   ├── __init__.py

├── configs/                 # Configuration files
│
├── training/                # Training scripts & evaluation
│   ├── __init__.py
│
└── deployment/             # Live drafting tools
    ├── __init__.py
```
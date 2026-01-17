# Chess Games Analysis Project

A comprehensive data analysis project exploring 6.25 million chess games from lichess.org played in July 2016. This project includes detailed statistical analysis, visualizations, and an interactive Streamlit dashboard.

## 📋 Project Overview

This project analyzes chess game data to uncover patterns in:
- Game outcomes and results distribution
- Player ELO ratings and their impact on game results
- Popular chess openings and their effectiveness
- Time control preferences and effects
- Temporal patterns in gameplay
- Rating changes and game termination reasons

## 🎯 Objectives

- Explore game patterns and player behavior
- Analyze opening preferences and outcomes
- Examine rating distributions and changes
- Investigate time control effects
- Study game termination patterns

## 📁 Project Structure

```
chess_project/
├── chess_games.csv          # Dataset (6.25M games)
├── chess_analysis.ipynb     # Jupyter notebook with 12 analytical questions
├── streamlit_dashboard.py   # Interactive Streamlit dashboard
├── utils.py                 # Utility functions for data processing
├── pyproject.toml          # Project dependencies
├── README.md               # This file
├── about_dataset.md        # Dataset documentation
└── instructions.md         # Project requirements
```

## 🔧 Setup

### Prerequisites

- Python 3.13 or higher
- pip or poetry for dependency management

### Installation

1. Clone or navigate to the project directory:
```bash
cd chess_project
```

2. Install dependencies:
```bash
pip install -e .
```

Or if using poetry:
```bash
poetry install
```

## 📊 Usage

### Jupyter Notebook Analysis

1. Start Jupyter Notebook:
```bash
jupyter notebook
```

2. Open `chess_analysis.ipynb` and run all cells.

The notebook contains 12 analytical questions, each with its own visualization:
1. Distribution of game results (White wins, Black wins, Draws)
2. ELO rating distributions
3. ELO difference impact on game outcomes
4. Most popular chess openings
5. Opening categories and their outcomes
6. Time control distribution
7. Time control effects on outcomes
8. Game termination reasons
9. Games played by hour of day
10. Games played by day of week
11. Draw rate by average ELO
12. Rating changes by game outcome

**Note**: The notebook loads a sample of 500,000 games by default for faster processing. To analyze the full dataset, modify the `sample_size` parameter in the data loading cell to `None`.

### Streamlit Dashboard

1. Run the Streamlit dashboard:
```bash
streamlit run streamlit_dashboard.py
```

2. The dashboard will open in your browser at `http://localhost:8501`

The dashboard includes:
- **Key Metrics**: Overview statistics
- **Game Results**: Results distribution and termination reasons
- **ELO Analysis**: Rating distributions, ELO difference effects, and draw rates
- **Openings**: Popular openings and opening categories
- **Time Controls**: Time control distribution and outcomes
- **Temporal Patterns**: Hourly and weekly game patterns

**Interactive Features**:
- Adjustable sample size slider
- Time control filter
- ELO range filter
- Interactive Plotly visualizations

## 📈 Key Findings

1. **Game Results**: White has a slight advantage in online chess games
2. **ELO Impact**: Higher rated players win more often, especially with larger rating gaps
3. **Openings**: Certain openings like Sicilian Defense dominate online play
4. **Time Controls**: Blitz and bullet games are most popular online
5. **Temporal Patterns**: Clear peak playing times throughout the day and week
6. **Draw Rate**: Higher rated players draw more frequently

## 🛠️ Technologies Used

- **Python 3.13**
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computations
- **Matplotlib**: Static visualizations
- **Seaborn**: Statistical visualizations
- **Plotly**: Interactive visualizations
- **Streamlit**: Interactive dashboard framework
- **Jupyter**: Notebook environment

## 📝 Dataset Information

The dataset contains 6.25 million chess games from lichess.org played in July 2016.

**Columns**:
- `Event`: Game type
- `White`: White player's ID
- `Black`: Black player's ID
- `Result`: Game result (1-0, 0-1, 1/2-1/2)
- `UTCDate`: UTC date
- `UTCTime`: UTC time
- `WhiteElo`: White player's ELO rating
- `BlackElo`: Black player's ELO rating
- `WhiteRatingDiff`: White's rating change after game
- `BlackRatingDiff`: Black's rating change after game
- `ECO`: Opening ECO code
- `Opening`: Opening name
- `TimeControl`: Time control in seconds
- `Termination`: Reason for game end
- `AN`: Moves in algebraic notation

For more details, see `about_dataset.md`.

## 🚀 Performance Notes

- The full dataset is very large (>200MB), so the notebook uses sampling by default
- For faster processing, adjust the `sample_size` parameter
- The Streamlit dashboard includes caching for better performance
- Consider using chunked processing for the full dataset

## 📚 Deliverables

✅ **Jupyter Notebook** (`chess_analysis.ipynb`)
- 12 analytical questions
- 12+ visualizations
- Comprehensive data analysis

✅ **Streamlit Dashboard** (`streamlit_dashboard.py`)
- Interactive visualizations
- Filtering capabilities
- Real-time data exploration

## 👤 Author

Chess Games Analysis Project

## 📄 License

This project is for educational purposes.

## 🙏 Acknowledgments

- Dataset: lichess.org
- Data source: Kaggle Chess Games Dataset

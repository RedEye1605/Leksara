
# [Project_Name]

## Description
**[Project_Name]** is a Python toolkit designed to streamline the preprocessing and cleaning of raw text data for Data Scientists and Machine Learning Engineers. It focuses on handling messy and noisy text data from various domains such as e-commerce, social media, and medical documents. The tool helps clean text by removing punctuation, stopwords, contractions, and other irrelevant content, allowing for efficient data analysis and machine learning model preparation.

## Key Features
- **Basic Cleaning Pipeline**: A straightforward pipeline to clean raw text data by handling common tasks like punctuation removal, casing normalization, and stopword filtering.
- **Advanced Customization**: Users can create custom cleaning pipelines tailored to specific datasets, including support for regex pattern matching, stemming, and custom dictionaries.
- **Preset Options**: Includes predefined cleaning presets for various domains like e-commerce, allowing for one-click cleaning.
- **Slang and Informal Text Handling**: Users can define their own custom dictionaries for slang terms and informal language, especially useful for Indonesian text.

## Usage Examples

### Basic Usage: Basic Cleaning Pipeline
This example demonstrates how to clean e-commerce product reviews using a pre-built preset.

```python
from [Project_Name] import [Project_Name]

df['cleaned_review'] = [Project_Name](df['review_text'], preset='ecommerce_review')
print(df[['review_id', 'cleaned_review']])
```

**Input Data (df):**

| review_id | review_text                            |
|-----------|----------------------------------------|
| 1         | `<p>brgnya ORI & pengiriman cepat. Mantulll 👍</p>` |
| 2         | `Kualitasnya krg bgs, ga sesuai ekspektasi...` |

**Output Data:**

| review_id | cleaned_review                 |
|-----------|---------------------------------|
| 1         | `barang nya original pengiriman cepat mantap` |
| 2         | `kualitasnya kurang bagus tidak sesuai ekspektasi` |

### Advanced Usage: Custom Cleaning Pipeline
Customize the pipeline to mask phone numbers and normalize whitespace in chat logs.

```python
from [Project_Name] import [Project_Name]
from [Project_Name].functions import to_lowercase, normalize_whitespace
from [Project_Name].patterns import MASK_PHONE_NUMBER

custom_pipeline = {
    'patterns': [MASK_PHONE_NUMBER],
    'functions': [to_lowercase, normalize_whitespace]
}

df['safe_message'] = [Project_Name](df['chat_message'], pipeline=custom_pipeline)
print(df[['chat_id', 'safe_message']])
```

**Input Data (df):**

| chat_id | chat_message                           |
|---------|----------------------------------------|
| 101     | `Hi kak, pesanan saya INV/123 blm sampai. No HP saya 081234567890` |
| 102     | `Tolong dibantu ya sis, thanks`        |

**Output Data:**

| chat_id | safe_message                           |
|---------|----------------------------------------|
| 101     | `hi kak, pesanan saya inv/123 blm sampai. no hp saya [PHONE_NUMBER]` |
| 102     | `tolong dibantu ya sis, thanks`        |

## Goals & Objectives
- Provide an intuitive and adaptable cleaning tool for Indonesian text, focusing on domains like e-commerce.
- Enable Data Scientists and ML Engineers to clean and preprocess text with minimal effort.
- Allow for deep customization through configuration options and the use of custom dictionaries.

## Success Metrics
- **On-time Delivery**: Targeted release by October 15, 2025.
- **Processing Speed**: Clean a 10,000-row Pandas Series in under 5 seconds.
- **Cleaning Accuracy**: Achieve over 95% accuracy for core cleaning functions.

## Folder Structure
Below is the recommended folder structure for organizing the project:
```
[Project_Name]/
├── data/                     
│   ├── raw/                  # Raw data files (e.g., CSV, TXT, etc.)
│   ├── processed/            # Processed data files
│   └── external/             # External data sources (optional)
├── docs/                     
│   └── index.md              # Main documentation file
├── project_name/             
│   ├── __init__.py           # Initialization file
│   ├── clean.py              # Core cleaning functions
│   ├── utils.py              # Utility functions
│   ├── presets.py            # Preset configuration
│   └── functions/            
│       ├── __init__.py
│       ├── to_lowercase.py
│       └── normalize_whitespace.py
├── tests/                    
│   ├── __init__.py
│   ├── test_clean.py         # Tests for cleaning functions
│   ├── test_utils.py         # Tests for utility functions
│   └── test_presets.py       # Tests for presets
├── setup.py                  # Setup script for the package
├── requirements.txt          # Dependencies for the project
├── .gitignore                # Git ignore file
└── README.md                 # Project readme
```

## Milestones

| Sprint | Dates                | Goal                                           |
|--------|----------------------|------------------------------------------------|
| 1      | Aug 18 – Aug 22      | Project Kickoff, Discovery, Set up repository |
| 2      | Aug 22 – Aug 29      | Build Core Cleaning Engine                    |
| 3      | Aug 29 – Sep 5       | Develop Configurable Features                 |
| 4      | Sep 5 – Sep 12       | Implement Advanced Customization              |
| 5      | Sep 12 – Sep 19      | Refine API                                    |
| 6      | Sep 19 – Sep 26      | Optimize System                               |
| 7      | Sep 26 – Oct 3       | Finalize Documentation                        |
| 8      | Oct 3 – Oct 10       | Prepare for Launch                            |

## Requirements
- Python 3.x
- Pandas

### Install
```bash
pip install [Project_Name]
```

## Contributors
- **Vivian & Zahra** – Document Owners
- **Salsa** – UI/UX Designer
- **Aufi, Althaf, Rhendy, Adit** – Data Science Team
- **Alya, Vivin** – Data Analyst Team

For more details on the features and usage, refer to the official documentation linked above.

## Links
- [UI Design](https://www.figma.com/proto/ATkL3Omdc2ZdT7ppldx2Br/Laplace-Project?node-id=41-19&t=OIOqDyu4cKp3Q90P-1)
- [Product Design and Mockups](https://www.figma.com/proto/ATkL3Omdc2ZdT7ppldx2Br/Laplace-Project?node-id=41-19&t=OIOqDyu4cKp3Q90P-1)

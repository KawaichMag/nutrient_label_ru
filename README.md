# Nutrient Label Generator (RU)

A Python tool for generating nutrition facts labels in Russian (Cyrillic) format. This tool creates standardized nutrition labels that comply with Russian food labeling requirements.

## Features

- Generates nutrition facts labels in Russian language
- Supports Cyrillic characters using DejaVu Sans font
- Creates standardized label format with proper spacing and layout
- Includes all required nutritional information fields
- Outputs labels in PDF format

## Requirements

- Python 3.x
- reportlab==3.6.8

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/nutrient_label_ru.git
cd nutrient_label_ru
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

The main script (`src/main.py`) provides a function to generate nutrition facts labels. Here's an example of how to use it:

```python
from src.main import create_nutrition_facts

create_nutrition_facts(
    serving_size="100 г",
    calories=250,
    total_fat=12,
    saturated_fat=3,
    trans_fat=0,
    cholesterol=30,
    sodium=470,
    total_carb=31,
    dietary_fiber=3,
    total_sugars=2,
    added_sugars=0,
    protein=5,
    vitamin_d=2,
    calcium=260,
    iron=4.5,
    potassium=240
)
```

## Project Structure

```
nutrient_label_ru/
├── src/
│   ├── main.py          # Main script for label generation
│   └── label.pdf        # Example output
├── fonts/               # Font files directory
├── requirements.txt     # Project dependencies
└── README.md           # This file
```

## License

This project is licensed under the terms specified in the LICENSE file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Uses DejaVu Sans font for Cyrillic character support
- Built with ReportLab library for PDF generation 
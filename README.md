# Grammar Autocorrect

## Overview
Grammar Autocorrect is a web-based application that automatically corrects grammar and spelling errors in text. It utilizes NLP techniques powered by `spaCy`, `language-tool-python`, and `autocorrect` to improve text accuracy.

## Features
- Fixes common contractions (e.g., "dont" -> "don't")
- Corrects spelling mistakes
- Enhances grammar using `language-tool-python`
- Provides an interactive web interface built with Flask and Bootstrap

## Installation

### Prerequisites
Ensure you have Python installed (version 3.7 or later).

### Clone the Repository
```sh
git clone https://github.com/serkankahveci/Grammar-autocorrect.git
cd Grammar-autocorrect
```

### Install Dependencies
```sh
pip install -r requirements.txt
```

### Download spaCy Model
```sh
python -m spacy download en_core_web_sm
```

## Usage

### Run the Application
```sh
python app.py
```
The web app will be accessible at `http://127.0.0.1:5000/`.

### API Endpoint
The application provides an endpoint for grammar correction:
- **POST /process**
  - **Request:** `{ "text": "Your input text here." }`
  - **Response:** `{ "corrected_text": "Corrected text output." }`

## License
This project is licensed under the MIT License.

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests.

## Contact
For any questions or suggestions, please reach out via GitHub Issues.


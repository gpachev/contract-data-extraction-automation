# Contract Data Extraction Automation (MVP)

## Setup Instructions

1. **Create a Python virtual environment (Python 3.12):**
   ```sh
   python -m venv .venv
   ```
2. **Activate the virtual environment:**
   - On Windows:
     ```sh
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```sh
     source .venv/bin/activate
     ```
3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
4. **Configure environment variables:**
   - Create a `.env` file in the project root with the following keys:
     ```env
     CONTRACTS_INPUT_PATH=path/to/contracts/folder
     GEMINI_API_KEY=your-gemini-api-key
     ```
   - `.env` is for environment variables only. `.venv` is your Python virtual environment folder.

## Running the Script

- The main script is located in `apps/ocr/main.py`.
- Run the script after setup to process contracts and generate outputs.

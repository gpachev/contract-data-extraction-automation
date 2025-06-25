# Feature: Contract Data Extraction Automation (MVP)

## Architecture Diagram

```
User / Analyst
     |
     v
Main Python Script
     |
     v
+-------------------+
| .env Loader       |
+-------------------+
     |
     v
+-------------------+
| File System       |
| Traversal         |
+-------------------+
     |
     v
+-------------------+
| Contract Files    |
| (.pdf, .docx,     |
|  .png, .jpeg)     |
+-------------------+
     |
     +-------------------+
     |                   |
     v                   v
+-------------------+  +-------------------+
| DOCX Text         |  | Gemini API Client |
| Extractor         |  +-------------------+
+-------------------+         |
     |                          v
     +---------------------->Google Gemini API
                                |
                                v
                         +-------------------+
                         | Data Parser       |
                         +-------------------+
                                |
                                v
                         +-------------------+
                         | Data Aggregator   |
                         +-------------------+
                                |
                 +--------------+--------------+
                 |                             |
                 v                             v
         +---------------+             +---------------+
         | CSV Writer    |             | Logger        |
         +---------------+             +---------------+
                 |                             |
                 v                             v
         CSV Output File                 Log File

Main Python Script also shows progress in the console.
```

## Micro System Design

**Main Modules & Responsibilities:**

- `config_loader.py`: Loads configuration from `.env` (input path, Gemini API key).
- `file_discovery.py`: Recursively discovers all supported contract files in the input directory.
- `docx_extractor.py`: Extracts text from DOCX files for LLM input.
- `gemini_client.py`: Handles communication with Google Gemini API (text and multimodal input).
- `data_parser.py`: Parses Gemini's JSON response and normalizes data.
- `aggregator.py`: Aggregates parsed data, adds file path, and prepares for CSV output.
- `csv_writer.py`: Writes aggregated results to a CSV file with the correct format and naming.
- `logger.py`: Logs processing status, errors, and progress to a timestamped log file.
- `main.py`: Orchestrates the workflow, manages progress reporting, and error handling.

**Data Flow:**
1. Load configuration from `.env` using `config_loader.py`.
2. Discover all contract files using `file_discovery.py`.
3. For each file:
    - If DOCX, extract text using `docx_extractor.py`.
    - For all formats, send content to Gemini using `gemini_client.py`.
    - Parse Gemini's response with `data_parser.py`.
    - Aggregate results and add file path using `aggregator.py`.
    - Log status and errors using `logger.py`.
4. After all files are processed, write results to CSV using `csv_writer.py`.
5. Log file and CSV output are available for user review.

---

### Main Components & Data Flow

- **User / Analyst**: Initiates the script.
- **Main Python Script**: Orchestrates the workflow.
- **.env Loader**: Loads configuration (input path, API key).
- **File System Traversal**: Recursively finds all supported contract files.
- **DOCX Text Extractor**: Extracts text from DOCX files for LLM input.
- **Gemini API Client**: Handles communication with Google Gemini (text or multimodal input).
- **Google Gemini API**: Performs OCR and data extraction (external dependency).
- **Data Parser**: Parses Gemini's JSON response.
- **Data Aggregator**: Collects and structures extracted data, adds file path.
- **CSV Writer**: Outputs results to a CSV file.
- **Logger**: Logs processing status and errors.
- **Console Progress**: Displays real-time progress to the user.

#### Dependencies
- **External**: Google Gemini API (via google-genai)
- **Python Libraries**: python-dotenv, python-docx, pandas
- **Local Files**: .env, contract files, log files, CSV output

---

## User Stories

### User Story 1: Bulk Contract Data Extraction
**As** an operations analyst
**I want** to automatically extract key data points from all contract files in a folder (including subfolders)
**So that** I can quickly analyze and report on contract terms without manual review.

### User Story 2: Multiformat Support
**As** a user
**I want** the script to process PDF, DOCX, PNG, and JPEG contract files
**So that** I can handle both digital and scanned contracts in one workflow.

### User Story 3: Accurate Data Structuring
**As** a data consumer
**I want** the extracted contract data to be output in a single, well-structured CSV file
**So that** I can easily import and analyze the results in other tools.

### User Story 4: Logging and Error Reporting
**As** a user
**I want** detailed logs of processing status and errors for each file
**So that** I can audit the process and troubleshoot issues efficiently.

---

## Use Cases

### Use Case 1: Extract Data from Contracts in Folder
- **Primary Actor:** Operations Analyst
- **Precondition:** Contracts are stored in a local folder (with possible subfolders); .env file is configured with input path and Gemini API key.
- **Main Flow:**
    1. User runs the script.
    2. Script loads input folder path and API key from .env.
    3. Script recursively finds all supported contract files.
    4. For each file:
        - If DOCX: extract text, then send to Gemini.
        - If PDF/PNG/JPEG: send file directly to Gemini for OCR and extraction.
        - Parse Gemini's JSON response for required data points.
        - Add file path as URL of Original Contract.
    5. Write all results to a single CSV file with specified columns and naming convention.
    6. Log processing status for each file.
- **Postcondition:** CSV and log files are created; user can review results and errors.

### Use Case 2: Handle Missing or Partial Data
- **Primary Actor:** Script
- **Precondition:** Some contracts may lack certain data points.
- **Main Flow:**
    1. If Gemini omits a key (other than IsNonCompeteClause), leave the corresponding CSV cell blank.
    2. If IsNonCompeteClause is missing, default to false.
    3. Continue processing even if some files or fields fail.
- **Postcondition:** CSV reflects missing data as blanks; log records any extraction issues.

### Use Case 3: Logging and Progress Reporting
- **Primary Actor:** Script
- **Precondition:** Script is running on a set of contract files.
- **Main Flow:**
    1. For each file, log success or failure with high-level reason and file path.
    2. Display running count of processed files in the console.
- **Postcondition:** Timestamped log file is created; user can track progress and review errors.

---

## Acceptance Criteria

1. The script reads the input folder path and Gemini API key from a .env file.
2. The script processes all .pdf, .docx, .png, and .jpeg files in the input folder and subfolders.
3. For .docx files, the script extracts text before sending to Gemini; for other formats, files are sent directly to Gemini.
4. The script uses Google Gemini (via google-genai) for data extraction, following the specified prompt and JSON schema.
5. The script extracts the following data points for each contract:
    - Own Company Name
    - Subcontractor Name
    - Subcontractor Location
    - Date of Contract (YYYY-MM-DD)
    - End Date of Contract (YYYY-MM-DD, blank if missing)
    - Is Non-compete Clause (boolean, defaults to false if missing)
    - Non-compete Text (blank if missing)
    - Penalty Amount (blank if missing)
    - URL of Original Contract (absolute file path)
6. The output CSV file is named as YYYY-MM-DD-HHMMSS-contract_intelligence.csv and contains the specified columns in the correct order.
7. If a data point is missing from Gemini's output, the corresponding CSV cell is left blank (except Is Non-compete Clause, which defaults to false).
8. The script creates a timestamped log file for each run, logging success or failure (with high-level reason) for each file.
9. The script displays a running count of processed files in the console.
10. The script continues processing remaining files even if some files or fields fail. 
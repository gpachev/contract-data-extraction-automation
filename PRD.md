## Software Specification: Contract Data Extraction Automation (MVP)

**Document Version:** 1.0
**Date:** June 24, 2025
**Prepared for:** [Your Company Name]
**Prepared by:** Gemini (AI Assistant)

---

### 1. Introduction

This document outlines the requirements and specifications for an MVP (Minimum Viable Product) Python script designed to automate the extraction of key data points from company contracts. The primary goal is to process various document formats, including scanned contracts, and output the extracted information into a structured table file, leveraging Google Gemini's capabilities.

### 2. Overall Description

The script will operate on a local file system, traversing a specified input folder (including subfolders) to identify contract documents. It will utilize Google Gemini for advanced OCR and intelligent data extraction from these documents. The extracted data will then be compiled into a single CSV file.

### 3. Functional Requirements

#### 3.1. Input Handling

* **Source:** Contracts will be located in a local file system folder, which may contain subfolders.
* **Input Path Configuration:** The path to the root input folder will be read from a `.env` file using the key `CONTRACTS_INPUT_PATH`.
* **Supported File Formats:** The script must process the following file extensions:
    * `.pdf` (PDF documents, including scanned PDFs)
    * `.docx` (Microsoft Word documents)
    * `.png` (Image files)
    * `.jpeg` (Image files)
* **DOCX Pre-processing:** For `.docx` files, the script will perform direct text extraction (e.g., using `python-docx`) before sending the content to Gemini.
* **Other Formats:** `.pdf`, `.png`, and `.jpeg` files will be provided directly to Google Gemini's multimodal input for OCR and extraction.

#### 3.2. Data Extraction

* **Extraction Engine:** Google Gemini (specifically using the `google-genai` Python library).
* **API Key Management:** The Google Gemini API key will be stored as an environment variable (e.g., `GEMINI_API_KEY`) within the `.env` file and loaded by `python-dotenv`.
* **Data Points to Extract:** For each contract, the script will extract the following information:
    1.  **Own Company Name** (string)
    2.  **Subcontractor Name** (string)
    3.  **Subcontractor Location** (string)
    4.  **Date of Contract** (string, formatted as `YYYY-MM-DD`)
    5.  **End Date of Contract** (string, formatted as `YYYY-MM-DD`)
    6.  **Is Non-compete Clause** (boolean: `true` if found, `false` if not found)
    7.  **Non-compete Text** (string: the entire clause; if bilingual, both versions separated by `\n\n`)
    8.  **Penalty Amount** (string: e.g., `USD 10 000`, with currency code and space as thousands separator)
    9.  **URL of Original Contract** (string: absolute file path to the original contract file) - *Note: This field is added by the script, not extracted by Gemini.*
* **Missing Data Handling (Gemini Output):** If a data point (other than `IsNonCompeteClause`, which defaults to `false`) cannot be found by Gemini, its corresponding key will be **omitted** from the JSON output.
* **Non-compete Clause Identification:** The script will rely on Gemini's LLM capabilities to identify the beginning and end of the entire non-compete clause.
* **Accuracy:** Slight variations in formatting for extracted numerical data (e.g., "10,000" vs. "10000") are acceptable as long as the value is correct.

#### 3.3. Output Generation

* **Output Format:** Single CSV file.
* **File Naming Convention:** `YYYY-MM-DD-contract_intelligence.csv` (based on the script's execution date).
* **CSV Column Headers & Order:** The CSV file will have the exact header names and order as follows:
    1.  Own Company Name
    2.  Subcontractor Name
    3.  Subcontractor Location
    4.  Date of Contract
    5.  End Date of Contract
    6.  Is Non-compete Clause
    7.  Non-compete Text
    8.  Penalty Amount
    9.  URL of Original Contract
* **Missing Data Handling (CSV):** If a data point is missing from Gemini's JSON output (i.e., the key was omitted), the corresponding cell in the CSV will be left **blank**.

#### 3.4. Logging and Progress Reporting

* **Log File:** A timestamped log file will be created for each run: `YYYY-MM-DD-HH:MM:SS-company-intelligence.log`.
* **Log Content (MVP):** Each line in the log file will indicate the processing status and the full file path.
    * **Successful Processing:** `Success - /path/to/contract/file.pdf`
    * **Failed Processing:** `Failed - [High-Level Reason] - /path/to/contract/file.pdf`
        * **High-Level Reasons:**
            * `File Access Error`
            * `Unsupported Format`
            * `DOCX Conversion Error`
            * `Gemini API Error`
            * `Gemini Response Error`
            * `Data Extraction Issue`
            * `CSV Write Error`
            * `Unknown Error`
* **Console Output:** A running count of currently processed files will be displayed on the console.

### 4. Non-Functional Requirements (MVP Scope)

* **Performance:** No specific performance targets or resource constraints are defined for the MVP. The focus is on functionality.
* **Scalability:** Not a primary concern for MVP; re-processing all files each run is acceptable.
* **Resume Capability:** No resume capability for interrupted runs in the MVP. The script will re-process all files from scratch each time.
* **Error Handling:** The script will handle errors gracefully (as defined in logging) and continue processing subsequent files/fields.
* **Security:** API key will be managed via `.env` file, which is a standard secure practice for local environments.

### 5. Technical Stack

* **Programming Language:** Python 3.12
* **External Python Libraries:**
    * `python-dotenv` (for loading `.env` variables)
    * `google-genai` (for Google Gemini API interaction)
    * `python-docx` (for `.docx` text extraction)
    * `pandas` (for CSV file handling and data structuring)

### 6. Google Gemini Prompt Specification

The script will use the following structure for prompting Google Gemini. It's assumed the API call will configure `response_mime_type="application/json"` and provide a `response_schema`.

**JSON Schema for Gemini Output (Conceptual, for API `response_schema`):**

```json
{
  "type": "object",
  "properties": {
    "OwnCompanyName": { "type": "string" },
    "SubcontractorName": { "type": "string" },
    "SubcontractorLocation": { "type": "string" },
    "DateOfContract": { "type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}<span class="math-inline">" \},
"EndDateOfContract"\: \{ "type"\: "string", "pattern"\: "^\\\\d\{4\}\-\\\\d\{2\}\-\\\\d\{2\}</span>" },
    "IsNonCompeteClause": { "type": "boolean" },
    "NonCompeteText": { "type": "string" },
    "PenaltyAmount": { "type": "string", "pattern": "^[A-Z]{3} (\\d{1,3}( \\d{3})*|\\d+)$" }
  },
  "required": ["OwnCompanyName", "SubcontractorName", "SubcontractorLocation", "DateOfContract", "IsNonCompeteClause"],
  "additionalProperties": false
}
User Prompt (to be sent with each contract's content):

"You are an expert contract analyst. Your task is to meticulously extract specific data points from the provided legal contract. Your response MUST be a JSON object that strictly adheres to the provided schema.

**Extract the following information:**

1.  **Own Company Name:** The full legal name of your company as a party to this contract.
2.  **Subcontractor Name:** The full legal name of the other party (the subcontractor).
3.  **Subcontractor Location:** The primary geographic location (e.g., City, State/Province, Country) of the subcontractor.
4.  **Date of Contract:** The effective or start date of the contract. Format this strictly as `YYYY-MM-DD`.
5.  **End Date of Contract:** The explicit end or termination date of the contract. Format this strictly as `YYYY-MM-DD`. If no explicit end date is stated, omit this field from the JSON.
6.  **Is Non-compete Clause:** Determine if any form of non-compete clause is present in the contract. Set to `true` if found, `false` otherwise.
7.  **Non-compete Text:** If a non-compete clause is found (i.e., `IsNonCompeteClause` is `true`), extract the *entire and complete* text of that clause. If the clause is presented in multiple languages (e.g., English and French), include both language versions, clearly separated by `\n\n`. Use your best judgment to identify the full boundaries of the clause.
8.  **Penalty Amount:** Identify any specific monetary penalty amounts associated with breaches, early termination, or non-compliance. Extract the currency code (e.g., USD, EUR) and the numerical amount. Format this as a string like `CURRENCY AMOUNT` using a space as a thousands separator (e.g., `USD 10 000`, `EUR 5 500`). If no specific penalty amount is found, omit this field from the JSON.

**Important Guidelines:**
* If a field (other than `IsNonCompeteClause`) is explicitly requested but not found in the contract, *do not include that key* in the final JSON output.
* Adhere strictly to the specified date and penalty amount formats.
* Your output must be *only* the JSON object. Do not include any conversational text or explanations outside the JSON.

**Contract Content for Analysis:**
[**INSERT CONTRACT CONTENT HERE** - this will be the text for DOCX files, or the direct PDF/image for other formats via multimodal input]
"
7. Future Considerations (Beyond MVP)
The following enhancements are planned for future versions of the script:

Google Drive Integration: Migrating the input source from a local folder to a Google Drive folder.
Extended Data Extraction: Adding more columns to the result table to provide additional intelligence from the contracts.
Resume Capability: Implementing the ability to resume processing from where an interrupted run left off.
More Detailed Logging: Providing more granular details within the log file beyond high-level failure reasons.
# Address Parser and Extractor

Address Parser and Extractor is a Python tool designed to extract and parse addresses from websites efficiently. This application allows users to input a list of company websites and extracts addresses from their content. With advanced parsing techniques and address similarity removal, users can obtain clean and structured address data for further analysis or processing.

## Modules and Dependencies
The application relies on several modules and dependencies to streamline the address extraction and parsing process:
* Pandas: Used for data manipulation and reading input files.
* Requests: Enables sending HTTP requests to company websites for content retrieval.
* BeautifulSoup: Facilitates parsing HTML content to extract text data.
* pyap: Provides address parsing capabilities, supporting various countries.
* JSON: Allows serialization of address data for storage and export.
* Threading: Utilized for concurrent processing of multiple website requests.
* Difflib: Enables comparison of address similarity for removal of duplicates.

## Installation Guide

### 1. Pandas
```bash
pip install pandas
```

### 2. Requests
```bash
pip install requests
```

### 3. BeautifulSoup
```bash
pip install beautifulsoup4
```

### 4. pyap
```bash
pip install pyap
```

### 5. JSON (Included in Python Standard Library)
JSON module is included in the Python Standard Library and does not require separate installation.

### 6. Threading (Included in Python Standard Library)
Threading module is included in the Python Standard Library and does not require separate installation.

### 7. Difflib (Included in Python Standard Library)
Difflib module is included in the Python Standard Library and does not require separate installation.

## Usage
* Users can utilize Address Parser and Extractor to extract and parse addresses from company websites efficiently. Here's how to use the tool:
* Input File: Provide a file containing a list of company websites in a suitable format (e.g., Parquet).
* Extraction Process: The application sends requests to each website, extracts text content, and parses addresses using advanced algorithms.
* Address Parsing: Extracted addresses are parsed to obtain structured data, including country, region, city, postcode, and road details.
* Similar Address Removal: Address similarity is evaluated and similar addresses are removed, ensuring a clean and unique address dataset.
* Export: Parsed addresses are exported to a CSV file for further analysis or integration with other systems.

## Efficiency
* Address Parser and Extractor emphasizes efficiency in various aspects:
* Concurrent Processing: Utilizing threading, the application processes multiple website requests concurrently, reducing processing time.
* Error Handling: Robust error handling ensures graceful handling of exceptions during website processing, maintaining application stability.
* Address Parsing: Advanced parsing techniques enable accurate extraction of address components, enhancing data quality.
* Duplicate Removal: By evaluating address similarity, the application eliminates duplicate addresses, producing a clean and concise dataset.

By combining advanced parsing algorithms with efficient processing techniques, Address Parser and Extractor empowers users to extract and parse addresses from company websites effectively, facilitating various applications such as data analysis, geocoding, and address validation.

# Document Intelligence Pipeline

This project implements a document processing pipeline using Azure Document Intelligence and Azure OpenAI services. It extracts content from PDF documents, categorizes the content into sections, and generates a structured document based on an example format.

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/cdreetz/fullstack-serverless-azure.git
   ```

2. Navigate to the project directory:
   ```
   cd fullstack-serverless-azure/document-intel
   ```

3. Create and activate a virtual environment:
   ```
   python3 -m venv env
   source env/bin/activate
   ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

5. Create a `.env` file in the project root and add your Azure credentials:
   ```
   AZURE_API_KEY=your_document_intelligence_api_key
   AZURE_ENDPOINT=your_document_intelligence_endpoint
   AZURE_OPENAI_API_KEY=your_azure_openai_api_key
   OPENAI_ENDPOINT=your_azure_openai_endpoint
   ```
   Refer to `.env.example` for the required format.

## Usage

Run the pipeline:
```
python pipeline2.py
```



## Project Structure

The main script `pipeline2.py` contains several key classes that form the document processing pipeline:

1. `Document`: A simple class to represent a document with sections.

2. `DocumentProcessor`: This class is responsible for processing the input PDF document. It performs the following tasks:
   - Extracts text from the PDF using Azure Document Intelligence.
   - Categorizes the extracted text into sections using Azure OpenAI.
   - Generates structured content for each section based on an example document.

3. `DocumentEvaluator`: This class evaluates the quality of the generated document by comparing it to an example document. It provides:
   - Individual scores for each section.
   - An overall score for the entire document.

The main function demonstrates how to use these classes together to process a document, generate structured content, and evaluate the results.



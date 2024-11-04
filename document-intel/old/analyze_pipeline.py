from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

endpoint = os.getenv("AZURE_ENDPOINT")
key = os.getenv("AZURE_API_KEY")
openai_key = os.getenv("OPENAI_API_KEY")
openai_endpoint = os.getenv("OPENAI_ENDPOINT")


SECTION_PROMPTS = {
    "administrative": """
    Analyze the following administrative provisions and create a clear summary that:
    - Identifies key administrative requirements
    - Highlights any deadlines or important dates
    - Outlines specific procedures or processes
    Content to analyze: {content}
    """,
    # Add other section types...
}


class DocumentProcessor:
    def __init__(self, endpoint, key, openai_key, openai_endpoint):
        self.doc_client = DocumentIntelligenceClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )
        self.openai_client = AzureOpenAI(
            api_key=openai_key,
            api_base=openai_endpoint
        )
        
    def process_document(self, document_path):
        # Use Document Intelligence to extract content
        with open(document_path, "rb") as f:
            poller = self.doc_client.begin_analyze_document(
                "prebuilt-layout", f
            )
        result = poller.result()
        return self._structure_content(result)
        
    def _structure_content(self, analysis_result):
        # Extract and structure content maintaining hierarchy
        structured_content = []
        for page in analysis_result.pages:
            for paragraph in page.paragraphs:
                structured_content.append({
                    'text': paragraph.content,
                    'page': page.page_number,
                    'confidence': paragraph.confidence
                })
        return structured_content
        
    def classify_sections(self, content):
        # Use Azure OpenAI to classify content sections
        sections = {}
        for block in content:
            classification = self._get_section_classification(block['text'])
            if classification not in sections:
                sections[classification] = []
            sections[classification].append(block)
        return sections
        
    def generate_summary(self, section_content, section_type):
        # Generate summary using Azure OpenAI
        prompt = self._get_section_prompt(section_type, section_content)
        response = self.openai_client.chat.completions.create(
            model="gpt-4",  # or your deployed model name
            messages=[
                {"role": "system", "content": "You are a document summarization assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
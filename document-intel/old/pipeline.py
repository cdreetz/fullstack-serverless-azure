from typing import List, Dict
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

class DocumentProcessor:
    def __init__(self, 
                 doc_intelligence_key: str, 
                 doc_intelligence_endpoint: str,
                 openai_key: str, 
                 openai_endpoint: str):
        # Initialize Azure Document Intelligence
        self.doc_client = DocumentIntelligenceClient(
            endpoint=doc_intelligence_endpoint,
            credential=AzureKeyCredential(doc_intelligence_key)
        )
        
        # Initialize Azure OpenAI
        self.openai_client = AzureOpenAI(
            api_key=openai_key,
            api_base=openai_endpoint
        )
    
    def process_documents(self, document_paths: List[str]) -> Dict[str, str]:
        """Main pipeline to process documents and generate summaries"""
        
        # 1. Extract content from all documents
        all_content = []
        for path in document_paths:
            content = self.extract_content(path)
            all_content.extend(content)
            
        # 2. Classify and group content by section
        sections = self.classify_sections(all_content)
        
        # 3. Generate summaries for each section
        summaries = {}
        for section_type, content in sections.items():
            if content:  # Only process sections with content
                prompt = self._get_section_prompt(section_type, content)
                summary = self.generate_summary(prompt)
                summaries[section_type] = summary
                
        return summaries

    def extract_content(self, document_path: str) -> List[dict]:
        """Extract text from document using Azure Document Intelligence"""
        with open(document_path, "rb") as doc:
            poller = self.doc_client.begin_analyze_document(
                "prebuilt-layout", doc
            )
        result = poller.result()
        
        # Extract paragraphs with their confidence scores
        content = []
        for page in result.pages:
            for paragraph in page.paragraphs:
                content.append({
                    'text': paragraph.content,
                    'confidence': paragraph.confidence
                })
        return content

    def _get_section_classification(self, text: str) -> str:
        """Classify text into a section category using Azure OpenAI"""
        prompt = f"""Classify the following text into one of these categories:
        - Water (floods, ports)
        - Fire (wildfires, fire stations)
        - Administrative (employees, establishments, admin support, etc.)
        - Other (anything else)

        Text to classify:
        {text[:500]}...

        Return only the category name, nothing else."""
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a document classification assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
            max_tokens=10
        )
        
        return response.choices[0].message.content.strip().lower()

    def classify_sections(self, content_blocks: List[dict]) -> Dict[str, List[str]]:
        """Group content blocks into sections by type"""
        sections = {
            "water": [],
            "fire": [],
            "administrative": [],
            "other": []
        }
        
        for block in content_blocks:
            if block['confidence'] >= 0.8:  # Only process high-confidence blocks
                section_type = self._get_section_classification(block['text'])
                sections[section_type].append(block['text'])
                
        return sections

    def _get_section_prompt(self, section_type: str, content: List[str]) -> str:
        """Generate appropriate prompt for each section type"""
        prompts = {
            "water": """
            Create a clear summary of these water provisions that:
            - Identifies key water related items
            - Highlights any budgetary requirements
            - Outlines specific procedures
            Use bullet points for clarity.
            """,
            
            "fire": """
            Create a clear summary of these fire provisions that:
            - Identifies key fire related items
            - Highlights any budgetary requirements
            - Outlines specific procedures
            Use bullet points for clarity.
            """,
            
            "administrative": """
            Create a clear summary of these administrative provisions that:
            - Identifies key administrative related items
            - Highlights any budgetary requirements
            - Outlines specific procedures
            Use bullet points for clarity.
            """,
            
            "other": """
            Create a clear summary of this content that:
            - Highlights key points
            - Maintains important details
            - Preserves any specific requirements
            """
        }
        
        # Join all content blocks together
        full_content = "\n\n".join(content)
        
        return f"""{prompts[section_type]}

        Content to summarize:
        {full_content}
        """

    def generate_summary(self, prompt: str) -> str:
        """Generate summary using Azure OpenAI"""
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a document summarization assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content.strip()

def print_summaries(summaries: Dict[str, str]):
    """Print summaries in a readable format"""
    print("\n" + "="*80 + "\n")
    
    for section_type, summary in summaries.items():
        if summary:  # Only print sections that have content
            print(f"SECTION: {section_type.upper()}")
            print("-" * 40)
            print(summary)
            print("\n" + "="*80 + "\n")

# Example usage
if __name__ == "__main__":
    # Initialize processor with your Azure keys and endpoints
    processor = DocumentProcessor(
        doc_intelligence_key=os.getenv("AZURE_API_KEY"),
        doc_intelligence_endpoint=os.getenv("AZURE_ENDPOINT"),
        openai_key=os.getenv("OPENAI_API_KEY"),
        openai_endpoint=os.getenv("OPENAI_ENDPOINT")
    )
    
    # Process documents
    summaries = processor.process_documents([
        "./documents/AdminProvisions.pdf",
    ])
    
    # Print results
    print_summaries(summaries)
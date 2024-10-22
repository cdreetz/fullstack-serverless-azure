import os
import base64
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest

load_dotenv()

endpoint = os.getenv("AZURE_ENDPOINT")
key = os.getenv("AZURE_API_KEY")

url = "https://github.com/cdreetz/fullstack-serverless-azure/blob/master/document-intel/BILLS-118hr82ih.pdf"
file_path = "./BILLS-118hr82ih.pdf"

def analyze_document(file_path, endpoint, key):
    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, 
        credential=AzureKeyCredential(key)
    )

    # Open and read the file
    with open(file_path, "rb") as f:
        file_content = f.read()
        file_content_base64 = base64.b64encode(file_content).decode("utf-8")

    analyze_request = {
        "base64Source": file_content_base64
    }
    poller = document_intelligence_client.begin_analyze_document(
        "prebuilt-layout",
        analyze_request=analyze_request,
    )

    result = poller.result()
    return result

# Example usage:
result = analyze_document(file_path, endpoint, key)
print(result)

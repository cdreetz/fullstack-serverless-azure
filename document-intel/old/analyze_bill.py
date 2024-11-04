import os
import base64
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeResult
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
import matplotlib.pyplot as plt
import matplotlib.patches as patches

load_dotenv()

endpoint = os.getenv("AZURE_ENDPOINT")
key = os.getenv("AZURE_API_KEY")

file_path = "./documents/AdminProvisions.pdf"

def analyze_document(file_path, endpoint, key):
    document_intelligence_client = DocumentIntelligenceClient(
        endpoint=endpoint, 
        credential=AzureKeyCredential(key)
    )

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

def print_all_content(result):
    print("Extracted Content:")
    print(result.content)

def display_document_with_bounding_boxes(result):
    for page in result.pages:
        fig, ax = plt.subplots()
        ax.set_ylim(page.height, 0)
        ax.set_xlim(0, page.width)

        for word in page.words:
            bbox = word.polygon
            rect = patches.Rectangle((bbox[0], bbox[1]), bbox[2] - bbox[0], bbox[3] - bbox[1], 
                                     fill=False, edgecolor='red', linewidth=2)
            ax.add_patch(rect)
            ax.text(bbox[0], bbox[1], word.content, fontsize=8, color='blue')

        plt.title(f"Page {page.page_number}")
        plt.show()

def extract_tables(result):
    print("Extracted Tables:")
    for table_idx, table in enumerate(result.tables):
        print(f"Table {table_idx + 1}:")
        for row in range(table.row_count):
            for col in range(table.column_count):
                cell = next((cell for cell in table.cells if cell.row_index == row and cell.column_index == col), None)
                if cell:
                    print(f"[{row}][{col}]: {cell.content}")
            print()
        print("---")

def extract_key_value_pairs(result):
    print("Key-Value Pairs:")
    for kv_pair in result.key_value_pairs:
        if kv_pair.key and kv_pair.value:
            print(f"{kv_pair.key.content}: {kv_pair.value.content}")

# Example usage:
result = analyze_document(file_path, endpoint, key)
print_all_content(result)
display_document_with_bounding_boxes(result)
extract_tables(result)
extract_key_value_pairs(result)

import React, { useState } from "react";
import { ScrollArea } from "../components/ui/scroll-area";
import { Input } from "../components/ui/input";
import {
  Card,
  CardHeader,
  CardContent,
  CardTitle,
} from "../components/ui/card";
import { Button } from "../components/ui/button";
import { Loader2 } from "lucide-react";

interface Document {
  name: string;
  type: string;
  file: File;
}

const DocumentUpload: React.FC<{
  onFileUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;
}> = ({ onFileUpload }) => (
  <div>
    <h3 className="text-lg font-semibold mb-2">Upload Documents</h3>
    <Input type="file" multiple onChange={onFileUpload} />
  </div>
);

const DocumentList: React.FC<{
  documents: Document[];
  onDocumentTypeChange: (index: number, type: string) => void;
}> = ({ documents, onDocumentTypeChange }) => (
  <div>
    <h3 className="text-lg font-semibold mb-2">Uploaded Documents</h3>
    <ScrollArea className="h-40 border rounded p-2">
      {documents.map((doc, index) => (
        <div key={index} className="flex items-center justify-between mb-2">
          <span>{doc.name}</span>
          <select
            value={doc.type}
            onChange={(e) => onDocumentTypeChange(index, e.target.value)}
            className="border rounded p-1"
          >
            <option value="Unknown">Unknown</option>
            <option value="Report">Report</option>
            <option value="Presentation">Presentation</option>
            <option value="Spreadsheet">Spreadsheet</option>
          </select>
        </div>
      ))}
    </ScrollArea>
  </div>
);

const SummaryTypeSelector: React.FC<{
  summaryType: string;
  onSummaryTypeChange: (type: string) => void;
}> = ({ summaryType, onSummaryTypeChange }) => (
  <div>
    <h3 className="text-lg font-semibold mb-2">Summary Type</h3>
    <select
      value={summaryType}
      onChange={(e) => onSummaryTypeChange(e.target.value)}
      className="w-full border rounded p-2"
    >
      <option value="">Select a summary type</option>
      <option value="Executive">Executive</option>
      <option value="Technical">Technical</option>
      <option value="Financial">Financial</option>
    </select>
  </div>
);

const SummaryDisplay: React.FC<{ summary: string }> = ({ summary }) => (
  <div>
    <h3 className="text-lg font-semibold mb-2">Generated Summary</h3>
    <ScrollArea className="h-40 border rounded p-2">
      <p>{summary}</p>
    </ScrollArea>
  </div>
);

const Summary: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [summaryType, setSummaryType] = useState<string>("");
  const [summary, setSummary] = useState<string>("");
  const [status, setStatus] = useState<'idle' | 'uploading' | 'processing' | 'complete' | 'error'>('idle');
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (files) {
      const newDocuments = Array.from(files).map((file) => ({
        name: file.name,
        type: "Unknown",
        file: file,
      }));
      setDocuments([...documents, ...newDocuments]);
    }
  };

  const handleDocumentTypeChange = (index: number, type: string) => {
    const updatedDocuments = [...documents];
    updatedDocuments[index].type = type;
    setDocuments(updatedDocuments);
  };

  const generateSummary = async () => {
    if (documents.length === 0 || !summaryType) {
      setStatus('error');
      setSummary('Please upload documents and select a summary type');
      return;
    }

    setStatus('uploading');
    const formData = new FormData();
    documents.forEach((doc, index) => {
      formData.append(`file`, doc.file);
      formData.append(`type`, doc.type);
    });
    formData.append("summary_type", summaryType);

    try {
      setStatus('processing');
      const response = await fetch('http://localhost:8000/generate_summary', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to generate summary');
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      setDownloadUrl(url);

      setSummary('Your summary is ready to download');
      setStatus('complete');
    } catch (error) {
      console.error('Error generating summary:', error);
      setStatus('error');
      setSummary('Error generating summary. Please try again.');
    }
  };

  const downloadSummary = () => {
    if (downloadUrl) {
      const link = document.createElement('a');
      link.href = downloadUrl;
      link.download = 'summary.pdf';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }
  };

  return (
    <Card className="w-full max-w-4xl mx-auto mt-8">
      <CardHeader>
        <CardTitle>Executive Summary Generator</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <DocumentUpload onFileUpload={handleFileUpload} />
          <DocumentList
            documents={documents}
            onDocumentTypeChange={handleDocumentTypeChange}
          />
          <SummaryTypeSelector
            summaryType={summaryType}
            onSummaryTypeChange={setSummaryType}
          />
          <Button
            onClick={generateSummary}
          >
            {status === 'idle' && 'Generate Summary'}
            {status === 'uploading' && (
              <>
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
                Uploading...
              </>
            )}
            {status === 'processing' && (
              <>
                <Loader2 className="h-4 w-4 animate-spin mr-2" />
                Processing...
              </>
            )}
            {status === 'complete' && 'Download Summary'}
            {status === 'error' && 'Error generating summary'}
          </Button>
          {status === 'complete' && summary && (
            <>
              <SummaryDisplay summary={summary} />
              <Button onClick={downloadSummary}>Download Summary</Button>
            </>
          )}
          {status === 'error' && (
            <div className="text-red-500">
              Error generating summary. Please try again.
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
};

export default Summary;

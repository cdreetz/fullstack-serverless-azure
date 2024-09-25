import React, { useState } from "react";
import { Card, CardHeader, CardContent, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import Editor from 'react-simple-code-editor';
import Prism from 'prismjs';
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-python';
import 'prismjs/themes/prism.css';

const CodeEditor: React.FC = () => {
  const [code, setCode] = useState("# Enter your Python code here");

  const sendCodeToAI = () => {
    // Implement the logic to send code to AI
    console.log("Sending code to AI:", code);
  };

  return (
    <Card className='flex flex-col h-full'>
      <CardHeader>
        <CardTitle>Your Code</CardTitle>
      </CardHeader>
      <CardContent className='flex-grow flex flex-col'>
        <div className="flex-grow border rounded overflow-hidden mb-4">
          <Editor
            value={code}
            onValueChange={setCode}
            highlight={code => Prism.highlight(code, Prism.languages.python, 'python')}
            padding={10}
            style={{
              fontFamily: '"Fira code", "Fira Mono", monospace',
              fontSize: 14,
              height: '100%',
            }}
          />
        </div>
        <div className="flex space-x-2">
          <Button onClick={() => setCode(code)} variant="outline">Save Code</Button>
          <Button onClick={sendCodeToAI} variant="outline">Send Code to AI</Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default CodeEditor;

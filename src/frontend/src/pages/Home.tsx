import React, { useState, KeyboardEvent } from "react";
import { ScrollArea } from "../components/ui/scroll-area";
import { Input } from "../components/ui/input";
import { Card, CardHeader, CardContent, CardTitle } from "../components/ui/card";
import { Button } from "../components/ui/button";
import Editor from 'react-simple-code-editor';
import { highlight, languages } from 'prismjs';
import 'prismjs/components/prism-clike';
import 'prismjs/components/prism-javascript';
import 'prismjs/components/prism-python';
import 'prismjs/themes/prism.css';
//import CodeEditor from "../components/CodeEditor";

interface Message {
  role: "assistant" | "user";
  content: string;
}

const exampleMessages: Message[] = [
  { role: "assistant", content: "Hello! How can I help you today?" },
  { role: "user", content: "I have a question about React." },
  { role: "assistant", content: "Sure, I'd be happy to help with your React question. What would you like to know?" },
];

function Chat() {
  const [messages, setMessages] = useState<Message[]>(exampleMessages);
  const [inputValue, setInputValue] = useState("");

  const handleKeyPress = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter" && inputValue.trim() !== "") {
      const newMessage: Message = {
        role: "user",
        content: inputValue.trim(),
      };
      setMessages((prevMessages) => [...prevMessages, newMessage]);
      setInputValue("");
    }
  };

  return (
    <Card className="flex flex-col h-full">
      <CardHeader className="flex-shrink-0">
        <CardTitle>Chat</CardTitle>
      </CardHeader>
      <CardContent className="flex-grow flex flex-col overflow-hidden">
        <ScrollArea className="flex-grow mb-4 border rounded">
          <div className="p-2">
            {messages.map((message, index) => (
              <div key={index} className={`mb-2 p-2 rounded w-3/4 ${
                message.role === 'assistant' 
                  ? 'bg-blue-100 border border-blue-200 self-start' 
                  : 'bg-gray-100 border border-gray-200 self-end ml-auto'
              }`}>
                {message.content}
              </div>
            ))}
          </div>
        </ScrollArea>
        <Input
          className="flex-shrink-0 mt-auto p-2 border border-gray-300 rounded"
          placeholder="Type your message..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyPress={handleKeyPress}
        />
      </CardContent>
    </Card>
  )
}

function CodeEditor() {
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
            highlight={code => highlight(code, languages.python, 'python')}
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
}

const Home: React.FC = () => {
  return (
    <div className="flex justify-center p-4 h-[calc(100vh-4rem)] w-full">
      <div className="w-1/2 h-full pr-2">
        <Chat />
      </div>
      <div className="w-1/2 h-full pl-2">
        <CodeEditor />
      </div>
    </div>
  );
};

export default Home;

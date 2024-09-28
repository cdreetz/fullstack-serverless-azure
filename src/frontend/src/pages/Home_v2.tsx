import React, { useState, KeyboardEvent } from "react";
import { ScrollArea } from "../components/ui/scroll-area";
import { Input } from "../components/ui/input";
import {
  Card,
  CardHeader,
  CardContent,
  CardTitle,
} from "../components/ui/card";
import { Button } from "../components/ui/button";
import Editor from "react-simple-code-editor";
import { highlight, languages } from "prismjs";
import "prismjs/components/prism-clike";
import "prismjs/components/prism-javascript";
import "prismjs/components/prism-python";
import "prismjs/themes/prism.css";
//import CodeEditor from "../components/CodeEditor";

interface Message {
  role: "assistant" | "user";
  content: string;
}

const examplePrompts: string[] = [
  "Write some code for me",
  "How to optimize React performance?",
  "Can you explain this code to me?",
  "Convert this code from one language to another",
];

function Chat() {
  const [messages, setMessages] = useState<Message[]>([]);
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

  const handlePromptClick = (prompt: string) => {
    const userMessage: Message = {
      role: "user",
      content: prompt,
    };

    let assistantMessage: Message;
    switch (prompt) {
      case "Write some code for me":
        assistantMessage = {
          role: "assistant",
          content:
            "Certainly! I'd be happy to help you write some code. Could you tell me more about what you'd like to create? What programming language are you using, and what should the code do?",
        };
        break;
      case "How to optimize React performance?":
        assistantMessage = {
          role: "assistant",
          content:
            "Great question! I'd be glad to discuss React performance optimization. To get started, could you tell me about any specific performance issues you're experiencing, or are you looking for general optimization tips?",
        };
        break;
      case "Can you explain this code to me?":
        assistantMessage = {
          role: "assistant",
          content:
            "Of course! I'd be happy to explain code for you. You can either paste the code you want explained in the chat here, or write it in the code editor on the right. Once you've done that, I'll do my best to break it down and explain how it works.",
        };
        break;
      case "Convert this code from one language to another":
        assistantMessage = {
          role: "assistant",
          content:
            "Certainly! I can help you convert code between programming languages. To get started, could you tell me what language the original code is in, and what language you'd like to convert it to? Then, you can either paste the code here or write it in the code editor on the right.",
        };
        break;
      default:
        assistantMessage = {
          role: "assistant",
          content: "Hello! How can I assist you with your request?",
        };
    }

    setMessages([userMessage, assistantMessage]);
  };

  return (
    <Card className="flex flex-col h-full">
      <CardHeader className="flex-shrink-0">
        <CardTitle>Chat</CardTitle>
      </CardHeader>
      <CardContent className="flex-grow flex flex-col overflow-hidden">
        {messages.length === 0 ? (
          <div className="flex-grow flex flex-col border rounded mb-2">
            <div className="flex justify-center items-center py-10">
              <h1 className="text-xl">What would you like help with?</h1>
            </div>
            <div className="grid grid-cols-2 gap-4 m-4">
              {examplePrompts.map((prompt, index) => (
                <Button
                  key={index}
                  onClick={() => handlePromptClick(prompt)}
                  variant="outline"
                  className="h-24 text-center p-2 overflow-hidden whitespace-normal break-words"
                >
                  <div className="line-clamp-3">{prompt}</div>
                </Button>
              ))}
            </div>
          </div>
        ) : (
          <ScrollArea className="flex-grow mb-2 border rounded h-full">
            <div className="p-2">
              {messages.map((message, index) => (
                <div
                  key={index}
                  className={`mb-2 p-2 rounded w-3/4 ${
                    message.role === "assistant"
                      ? "bg-blue-100 border border-blue-200 self-start"
                      : "bg-gray-100 border border-gray-200 self-end ml-auto text-right"
                  }`}
                >
                  {message.content}
                </div>
              ))}
            </div>
          </ScrollArea>
        )}
        <div className="flex flex-row gap-2 w-full">
          <Input
            className="flex-shrink-0 mt-auto p-2 border border-gray-300 rounded w-4/5"
            placeholder="Type your message..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
          />
          <Button
            // onClick={() => handleClearClick()}
            variant="destructive"
            className="flex-grow mt-auto"
          >
            Clear
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

function CodeEditor() {
  const [code, setCode] = useState("# Enter your Python code here");

  const sendCodeToAI = () => {
    // Implement the logic to send code to AI
    console.log("Sending code to AI:", code);
  };

  return (
    <Card className="flex flex-col h-full">
      <CardHeader>
        <CardTitle>Your Code</CardTitle>
      </CardHeader>
      <CardContent className="flex-grow flex flex-col">
        <div className="flex-grow border rounded overflow-hidden mb-2 h-full">
          <Editor
            value={code}
            onValueChange={setCode}
            highlight={(code) => highlight(code, languages.python, "python")}
            padding={10}
            style={{
              fontFamily: '"Fira code", "Fira Mono", monospace',
              fontSize: 14,
              height: "100%",
            }}
          />
        </div>
        <div className="flex space-x-2">
          <Button onClick={() => setCode(code)} variant="outline">
            Save Code
          </Button>
        </div>
      </CardContent>
    </Card>
  );
}

const Home2: React.FC = () => {
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

export default Home2;

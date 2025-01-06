"use client";
import { useState, useRef, useEffect } from 'react';
import Chat from './Chat';
import MessageInput from './MessageInput';
import { FaBars } from 'react-icons/fa';  // Import for hamburger icon

export type Message = {
  messageId: string;
  chatId: string;
  createdAt: Date;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  content: { user_query?: string } | any;
  role: 'user' | 'assistant' | 'loading';
};

interface ChatWindowProps {
  messages: Message[];
  loading: boolean;
  error: string | null;
  onSendMessage: (message: string) => Promise<string | null>;
  pendingMessageId?: string | null;
}

const ChatWindow = ({
  messages,
  loading,
  error,
  onSendMessage,
  pendingMessageId,
}: ChatWindowProps) => {
  const [localMessages, setLocalMessages] = useState<Message[]>(messages);
  const [userQueries, setUserQueries] = useState<string[]>([]);
  const [menuOpen, setMenuOpen] = useState(false);  // Menu toggle state
  const messageRefs = useRef<{ [key: string]: HTMLDivElement | null }>({});

  useEffect(() => {
    setLocalMessages(messages);

    // Extract user queries from messages
    const queries = messages
      .filter((msg) => msg.role === 'user' && (msg.content as { user_query: string }).user_query)
      .map((msg) => (msg.content as { user_query: string }).user_query || '');
    setUserQueries(queries);
  }, [messages]);

    // Function to add a user query dynamically
    const addUserQuery = (query: string) => {
      setUserQueries((prev) => [...prev, query]);
    };

  const handleSendMessage = async (message: string) => {
    if (!message.trim()) return;

    const tempMessageId = `temp-${Date.now()}`;

    const tempUserMessage: Message = {
      messageId: tempMessageId,
      chatId: '',
      createdAt: new Date(),
      content: { user_query: message },
      role: 'user',
    };

    const loadingMessage: Message = {
      messageId: `loading-${tempMessageId}`,
      chatId: '',
      createdAt: new Date(),
      content: '',
      role: 'loading',
    };

    setLocalMessages((prev) => [...prev, tempUserMessage, loadingMessage]);

    try {
      const response = await onSendMessage(message);

      // Remove loading indicator
      setLocalMessages((prev) =>
        prev.filter((msg) => msg.messageId !== loadingMessage.messageId)
      );

      if (response) {
        const newAssistantMessage: Message = {
          messageId: `response-${Date.now()}`,
          chatId: '',
          createdAt: new Date(),
          content: response,
          role: 'assistant',
        };
        setLocalMessages((prev) => [...prev, newAssistantMessage]);
      }
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  // Scroll to the selected message
  const scrollToMessage = (index: number) => {
    const targetElement = messageRefs.current[`message-${index}`];
    if (targetElement) {
      targetElement.scrollIntoView({ behavior: 'smooth' });
    }
    setMenuOpen(false);  // Close menu after selection
  };

  
  return (
    <div className="flex flex-col h-screen bg-black text-white relative">
      {error && <div className="text-center p-4 bg-red-500">{error}</div>}

      {/* Chat Window */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        <Chat
          messages={localMessages}
          loading={loading}
          messageRefs={messageRefs}
          pendingMessageId={pendingMessageId}
        />
      </div>

      {/* Message Input */}
      <div className="w-full">
        <MessageInput sendMessage={handleSendMessage} loading={loading} addUserQuery={addUserQuery} />
      </div>

      {/* Floating Hamburger Menu */}
      <div className="fixed right-6 top-6 z-50">
        <button
          onClick={() => setMenuOpen(!menuOpen)}
          className="p-3 bg-[#333333] rounded-full shadow-md hover:bg-[#555] transition-all focus:outline-none"
        >
          <FaBars size={20} />
        </button>
      </div>

      {/* Collapsible User Query Menu */}
      {menuOpen && (
        <div className="fixed right-6 top-16 w-72 bg-[#1e1e1e] text-white rounded-lg shadow-xl p-4 z-50 animate-slideIn">
          <h3 className="text-lg font-semibold mb-3">User Queries</h3>
          <ul className="space-y-2 max-h-60 overflow-y-auto">
            {userQueries.length > 0 ? (
              userQueries.map((query, idx) => (
                <li
                  key={idx}
                  onClick={() => scrollToMessage(idx)}
                  className="cursor-pointer hover:text-blue-400 transition"
                >
                  {query}
                </li>
              ))
            ) : (
              <p className="text-gray-400">No queries yet</p>
            )}
          </ul>
        </div>
      )}
    </div>
  );
};
export default ChatWindow;


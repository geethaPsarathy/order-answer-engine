import { useState, useRef, useLayoutEffect } from 'react';
import TextareaAutosize from 'react-textarea-autosize';
import { FaArrowUp } from 'react-icons/fa';

const DRAFT_KEY = 'chat_draft';

const MessageInput = ({
  sendMessage,
  loading,
  addUserQuery
}: {
  sendMessage: (message: string) => void;
  loading: boolean;
  addUserQuery: (query: string) => void;
}) => {
  const [message, setMessage] = useState<string>('');
  const debounceTimeout = useRef<NodeJS.Timeout | null>(null);

  useLayoutEffect(() => {
    const savedDraft = localStorage.getItem(DRAFT_KEY);
    if (savedDraft) {
      setMessage(savedDraft);
    }
  }, []);

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    setMessage(value);

    if (debounceTimeout.current) {
      clearTimeout(debounceTimeout.current);
    }
    debounceTimeout.current = setTimeout(() => {
      localStorage.setItem(DRAFT_KEY, value);
    }, 500);
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!message.trim() || loading) return;
    sendMessage(message);
    addUserQuery(message);  // Add query to the list upon submission
    setMessage('');
    localStorage.removeItem(DRAFT_KEY);
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="flex items-center w-full max-w-2xl mx-auto bg-gray-700 border border-gray-600 rounded-lg p-2 shadow-lg"
    >
      <TextareaAutosize
        value={message}
        onChange={handleInputChange}
        placeholder="Type a message..."
        minRows={1}
        maxRows={5}
        className="flex-grow bg-transparent text-white px-4 py-2 resize-none outline-none placeholder-gray-400"
      />
      <button
        type="submit"
        disabled={!message.trim() || loading}
        className={`ml-3 p-3 rounded-full ${
          message.trim() ? 'bg-blue-500 hover:bg-blue-600' : 'bg-gray-500 cursor-not-allowed'
        } transition-all`}
      >
        <FaArrowUp size={18} className="text-white" />
      </button>
    </form>
  );
};

export default MessageInput;

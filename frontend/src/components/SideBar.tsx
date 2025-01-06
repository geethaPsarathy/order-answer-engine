'use client';

import { useState } from 'react';
import Link from 'next/link';
import useLibrary from '@/hooks/useLibrary';

// Placeholder drafts
const drafts = [{ id: 1, title: 'Work in progress' }];

const Sidebar = () => {
  const url = `${process.env.NEXT_PUBLIC_API_URL}/library`;  // API URL
  const [isOpen, setIsOpen] = useState(true);
  const library = useLibrary(url);  // Use the hook

  const toggleSidebar = () => {
    setIsOpen(!isOpen);
  };

  return (
    <div
      className={`fixed inset-y-0 left-0 z-40 flex flex-col shadow-lg transition-all duration-300 ${
        isOpen ? 'w-64' : 'w-20'
      } bg-light-secondary dark:bg-dark-secondary`}
    >
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-6">
        {isOpen && (
          <h1 className="text-lg font-semibold text-gray-800 dark:text-white">
            Blend
          </h1>
        )}
        <button
          onClick={toggleSidebar}
          aria-label="Toggle Sidebar"
          className="text-gray-800 dark:text-white p-2 rounded-full hover:bg-gray-200 dark:hover:bg-gray-700"
        >
          ☰
        </button>
      </div>

      {/* Navigation Links */}
      <nav className="flex flex-col space-y-6 px-4">
        <Link
          href="/"
          className={`p-3 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 ${
            isOpen ? '' : 'justify-center'
          }`}
        >
          {isOpen && <span className="text-gray-800 dark:text-white">Home</span>}
        </Link>

        {/* Drafts Section */}
        <div>
          <h2
            className={`text-sm font-medium text-gray-500 dark:text-gray-400 ${
              isOpen ? 'block' : 'hidden'
            }`}
          >
            Drafts
          </h2>
          <div className="space-y-2 mt-2">
            {drafts.length > 0 ? (
              drafts.map((draft) => (
                <div
                  key={draft.id}
                  className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer"
                >
                  {isOpen && (
                    <span className="text-xs text-gray-700 dark:text-gray-300">
                      {draft.title}
                    </span>
                  )}
                </div>
              ))
            ) : (
              <p
                className={`text-xs text-gray-500 dark:text-gray-400 ${
                  isOpen ? 'block' : 'hidden'
                }`}
              >
                No drafts available
              </p>
            )}
          </div>
        </div>

        {/* Library Section */}
        <div>
          <h2
            className={`text-sm font-medium text-gray-500 dark:text-gray-400 ${
              isOpen ? 'block' : 'hidden'
            }`}
          >
            Library
          </h2>
          <div className="space-y-2 mt-2">
            {library.length > 0 ? (
              library.map((item) => (
                <Link href={`/chat/${item.chatId}`} key={item.chatId}>
                  <div className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800 cursor-pointer">
                    {isOpen && (
                      <span className="text-xs text-gray-700 dark:text-gray-300">
                        {item.title}
                      </span>
                    )}
                  </div>
                </Link>
              ))
            ) : (
              <p
                className={`text-xs text-gray-500 dark:text-gray-400 ${
                  isOpen ? 'block' : 'hidden'
                }`}
              >
                No library items yet
              </p>
            )}
          </div>
        </div>
      </nav>
    </div>
  );
};

export default Sidebar;



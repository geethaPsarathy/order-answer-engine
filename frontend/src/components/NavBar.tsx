'use client';

import { FaEdit, FaShare } from 'react-icons/fa';
import Link from 'next/link';
import { Message } from './ChatWindow';
import { useEffect, useState } from 'react';

const Navbar = ({
  messages,
}: {
  messages: Message[];
  chatId: string;
}) => {
  const [title, setTitle] = useState<string>('');

  useEffect(() => {
    if (messages.length > 0) {
      const newTitle = `${messages[0].content.substring(0, 20).trim()}...`;
      setTitle(newTitle);
    }
  }, [messages]);

  return (
    <>
      <Link href="/">
        <FaEdit size={17} />
      </Link>
      <p className="hidden lg:flex">{title}</p>
      <div className="flex flex-row items-center space-x-4">
        <FaShare size={17} className="cursor-pointer" />
      </div>
    </>
  );
};

export default Navbar;

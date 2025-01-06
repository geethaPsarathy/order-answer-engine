import { useState, useEffect } from 'react';
import dotenv from 'dotenv';

dotenv.config(); 

type LibraryItem = {
  _id: string;
  title: string;
  createdAt: string;
  chatId: string;
};



const useLibrary = (url: string | URL | Request) => {
  const [library, setLibrary] = useState<LibraryItem[]>([]);

  useEffect(() => {
    const fetchLibrary = async () => {
      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error('Failed to fetch library items');
        }
        const data: LibraryItem[] = await response.json();

        // Sort by createdAt (descending) and get latest 3
        const sortedLibrary = data
          .sort(
            (a, b) =>
              new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime()
          )
          .slice(0, 3);

        setLibrary(sortedLibrary);
      } catch (error) {
        console.error('Error fetching library:', error);
      }
    };
    fetchLibrary();
  }, []);

  return library;
};

export default useLibrary;

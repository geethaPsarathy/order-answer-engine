import { useState, useEffect } from 'react';

type LibraryItem = {
  _id: string;
  title: string;
  createdAt: string;
  chatId: string;
};

const useLibrary = () => {
  const [library, setLibrary] = useState<LibraryItem[]>([]);

  useEffect(() => {
    const fetchLibrary = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/library');
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

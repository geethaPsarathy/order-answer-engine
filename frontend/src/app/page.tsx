import HomePage from '@/components/HomePage';
import { Metadata } from 'next';
import { Suspense } from 'react';

export const metadata: Metadata = {
  title: 'Menu Decoder - Enhance Your Dining Experience',
  description: 'Chat with Me !.',
};

const Home = () => {
  return (
    <div>
      <Suspense>
        <HomePage />
      </Suspense>
    </div>
  );
};

export default Home;

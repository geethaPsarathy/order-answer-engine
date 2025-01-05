"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { v4 as uuidv4 } from 'uuid';
import MessageInput from "@/components/MessageInput";
import { FaArrowLeft } from "react-icons/fa";

type Restaurant = {
  name: string;
  menu: string[];
  location: string;
  emoji: string;
  menuEmoji: string[];
};

const mockRestaurants: Restaurant[] = [
  {
    name: "In-N-Out Burger",
    menu: ["Ham Burger", "Double Double Burger"],
    menuEmoji: ["🍔", "🍔"],
    location: "Los Angeles",
    emoji: "🍟",
  },
  {
    name: "Shake Shack",
    menu: ["Shack Burger", "Cheese Fries"],
    menuEmoji: ["🍔", "🍟"],
    location: "New York",
    emoji: "🥤",
  },
];

const HomePage = () => {
  const [selectedRestaurant, setSelectedRestaurant] = useState<Restaurant | null>(null);
  const [selectedMenu, setSelectedMenu] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [pendingMessage, setPendingMessage] = useState<string | null>(null);
  const router = useRouter();

  // const startNewChat = async (message: string) => {
  //   if (!message.trim() || !selectedMenu || !selectedRestaurant) return;

  //   setLoading(true);
  //   setPendingMessage(message);
  //   const chatId = uuidv4();

  //   try {
  //     console.log(message)
  //     const createChatResponse = await fetch('http://127.0.0.1:8000/chat/new', {
  //       method: 'POST',
  //       body: JSON.stringify({ chatId , title: message.trim()}),
  //       headers: {
  //         'Content-Type': 'application/json',
  //       },
  //     });

  //     if (!createChatResponse.ok) {
  //       throw new Error('Failed to create chat');
  //     }

  //     router.push(`/chat/${chatId}`);

  //     setTimeout(async () => {
  //       const queryParam = `dish_name=${selectedMenu}&restaurant_name=${selectedRestaurant.name}&location=${selectedRestaurant.location}&user_query=${message}&limit=10`;

  //       const sendMessageResponse = await fetch(
  //         `http://127.0.0.1:8000/chat/${chatId}/send-message?${queryParam}`,
  //         {
  //           method: 'POST',
  //         }
  //       );

  //       if (!sendMessageResponse.ok) {
  //         throw new Error('Failed to send message');
  //       }
  //     }, 1500);
  //   } catch (error) {
  //     console.error('Error starting chat or sending message:', error);
  //     alert('Failed to start chat. Please try again.');
  //   } finally {
  //     setLoading(false);
  //     setPendingMessage(null);
  //   }
  // };

  const startNewChat = async (message: string) => {
    if (!message.trim() || !selectedMenu || !selectedRestaurant) return;
    setLoading(true);
    setPendingMessage(message);
  
    const chatId = uuidv4();
    try {
      // Create new chat
      const createChatResponse = await fetch('http://127.0.0.1:8000/chat/new', {
        method: 'POST',
        body: JSON.stringify({ chatId, title: message.trim() }),
        headers: { 'Content-Type': 'application/json' },
      });
      if (!createChatResponse.ok) throw new Error('Failed to create chat');
  
      // Send initial message
      const queryParam = `dish_name=${selectedMenu}&restaurant_name=${selectedRestaurant.name}&location=${selectedRestaurant.location}&user_query=${message}&limit=10`;
      const sendMessageResponse = await fetch(
        `http://127.0.0.1:8000/chat/${chatId}/send-message?${queryParam}`,
        { method: 'POST' }
      );
      if (!sendMessageResponse.ok) throw new Error('Failed to send message');
  
      // Navigate only after both requests succeed
      router.push(`/chat/${chatId}`);
    } catch (error) {
      console.error('Error starting chat or sending message:', error);
      alert('Failed to start chat. Please try again.');
    } finally {
      setLoading(false);
      setPendingMessage(null);
    }
  };
  
  const handleBack = () => {
    if (selectedMenu) {
      setSelectedMenu(null);
    } else if (selectedRestaurant) {
      setSelectedRestaurant(null);
    }
  };

  return (
    <div className="flex flex-col items-center justify-center h-screen space-y-10 bg-black text-white">
      {selectedRestaurant && !selectedMenu ? (
        <div className="flex flex-col items-center">
          <button
            onClick={handleBack}
            className="absolute top-8 left-8 bg-gray-800 p-3 rounded-full"
          >
            <FaArrowLeft size={18} />
          </button>
          <h2 className="text-3xl font-bold mb-6">{selectedRestaurant.name} Menu</h2>
          <div className="grid grid-cols-1 gap-4">
            {selectedRestaurant.menu.map((item, idx) => (
              <button
                key={idx}
                onClick={() => setSelectedMenu(item)}
                className="bg-gray-700 hover:bg-gray-600 text-white px-6 py-3 rounded-lg shadow-md transition-all"
              >
                {selectedRestaurant.menuEmoji[idx]} {item}
              </button>
            ))}
          </div>
        </div>
      ) : selectedMenu ? (
        <div className="flex flex-col items-center justify-center h-screen space-y-6">
          <button
            onClick={handleBack}
            className="absolute top-8 left-8 bg-gray-800 p-3 rounded-full"
          >
            <FaArrowLeft size={18} />
          </button>
          <h2 className="text-3xl font-bold">Query about {selectedMenu}?</h2>
          <MessageInput sendMessage={startNewChat} loading={loading} addUserQuery={() => {}} />
          {pendingMessage && (
            <p className="mt-6 text-blue-300">
              Sending: <span className="font-semibold">{pendingMessage}</span>
            </p>
          )}
        </div>
      ) : (
        <div className="flex flex-col items-center">
          <h1 className="text-4xl font-bold">Pick a Restaurant</h1>
          <div className="grid grid-cols-2 gap-8 mt-6">
            {mockRestaurants.map((restaurant) => (
              <div
                key={restaurant.name}
                onClick={() => setSelectedRestaurant(restaurant)}
                className="p-6 w-80 bg-gray-800 hover:bg-gray-700 rounded-xl shadow-lg cursor-pointer"
              >
                <div className="text-6xl mb-4">{restaurant.emoji}</div>
                <h3 className="text-2xl">{restaurant.name}</h3>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default HomePage;

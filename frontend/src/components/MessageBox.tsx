// import ReactMarkdown from "react-markdown";
// import { Message } from "./ChatWindow";

// type MessageBoxProps = {
//   message: Message;
// };

// type Content = {
//   message?: string;  // Adjusted for assistant follow-up responses
//   user_query?: string;
//   summarized_reviews?: string[];
//   insights?: string[];
//   customizations?: string[];
//   ingredients?: string[];
//   flavors?: string[];
//   beverages?: string[];
//   desserts?: string[];
// };

// const MessageBox = ({ message }: MessageBoxProps) => {
//   const content = message.content as Content | string;  // Type assertion
//   const isUser = message.role === 'user';

//   // Safely render message content
//   const renderContent = () => {
//     // Handle assistant response where the message is nested
//     if (typeof content === 'object' && content !== null) {
//       if (isUser) {
//         return <p className="text-sm">{content.user_query || 'User Query'}</p>;
//       }

//       // Extract and render assistant message
//       if (content.message) {
//         return (
//           <div className="prose max-w-full">
//             <ReactMarkdown>{content.message}</ReactMarkdown>
//           </div>
//         );
//       }

//       // Render fallback for other structured responses
//       return (
//         <div>
//           {content.insights?.length ? (
//             content.insights.map((review: string, idx: number) => (
//               <div key={idx} className="mt-2">
//                 <ReactMarkdown>{review}</ReactMarkdown>
//               </div>
//             ))
//           ) : (
//             <p>No insights available.</p>
//           )}
          
//           {renderSection("Customizations", content.customizations)}
//           {renderSection("Ingredients", content.ingredients)}
//           {renderSection("Flavors", content.flavors)}
//           {renderSection("Beverages", content.beverages)}
//           {renderSection("Desserts", content.desserts)}
//         </div>
//       );
//     }

//     // Render plain text message directly if no object
//     return <p className="text-sm">{content}</p>;
//   };

//   // Helper to render list sections dynamically
//   const renderSection = (title: string, items?: string[]) => {
//     if (items && items.length > 0) {
//       return (
//         <div className="mt-4">
//           <strong>{title}:</strong>
//           <ul className="list-disc pl-5">
//             {items.map((item, idx) => (
//               <li key={idx}>{item}</li>
//             ))}
//           </ul>
//         </div>
//       );
//     }
//     return null;
//   };

//   return (
//     <div
//       className={`p-4 rounded-lg max-w-[75%] ${
//         isUser ? 'bg-transparent text-white' : 'bg-gray-100 text-gray-900'
//       }`}
//     >
//       {renderContent()}
//     </div>
//   );
// };
"use client"
import React, { useState, useEffect } from "react";
import { Message } from "./ChatWindow";

interface MessageBoxProps {
  message: Message;
  isFollowUp?: boolean;
}

const MessageBox = ({ message, isFollowUp = false }: MessageBoxProps) => {
  const [displayedSections, setDisplayedSections] = useState<string[]>([]);
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const [contentObject, setContentObject] = useState<Record<string, any> | null>(null);
  const isUser = message.role === "user";

  useEffect(() => {
    const content = message.content;

    if (typeof content === "string") {
      setDisplayedSections([content]);  // Directly show plain user text queries
    } else if (typeof content === "object" && content !== null) {
      setContentObject(content);
      const keys = Object.keys(content);

      if (isFollowUp) {
        // Animate for follow-up assistant messages
        let index = 0;
        const interval = setInterval(() => {
          setDisplayedSections((prev) => [...prev, keys[index]]);
          index++;
          if (index >= keys.length) {
            clearInterval(interval);
          }
        }, 500);
        return () => clearInterval(interval);
      } else {
        // Show entire object immediately for history
        setDisplayedSections(keys);
      }
    }
  }, [message, isFollowUp]);

  const renderContent = () => {
    if (contentObject) {
      return (
        <div className="space-y-4">
          {displayedSections.includes("user_query") && (
            <p className="text-lg font-semibold">
              {contentObject.user_query}
            </p>
          )}
          {displayedSections.includes("dish_name") && (
            <h2 className="text-xl font-bold">{contentObject.dish_name}</h2>
          )}
          {displayedSections.includes("restaurant_name") && (
            <p>
              <strong>Restaurant:</strong> {contentObject.restaurant_name}
            </p>
          )}
          {displayedSections.includes("summarized_reviews") && contentObject.summarized_reviews && (
            <div>
              <h3 className="font-medium">🔍 Reviews:</h3>
              <p>{contentObject.summarized_reviews[0]}</p>
            </div>
          )}
          {displayedSections.includes("customizations") && contentObject.customizations && (
            <div>
              <h3 className="font-medium">✨ Customizations:</h3>
              <ul>
                {contentObject.customizations.map((item: string, idx: number) => (
                  <li key={idx}>{item}</li>
                ))}
              </ul>
            </div>
          )}
          {displayedSections.includes("ingredients") && contentObject.ingredients && (
            <div>
              <h3 className="font-medium">🍔 Ingredients:</h3>
              <ul>
                {contentObject.ingredients.map((item: string, idx: number) => (
                  <li key={idx}>{item}</li>
                ))}
              </ul>
            </div>
          )}
          {displayedSections.includes("beverages") && contentObject.beverages && (
            <div>
              <h3 className="font-medium">🍹 Beverages:</h3>
              <ul>
                {contentObject.beverages.map((item: string, idx: number) => (
                  <li key={idx}>{item}</li>
                ))}
              </ul>
            </div>
          )}
          {displayedSections.includes("message") && (
            <p>{contentObject.message}</p>
          )}
        </div>
      );
    }
    return <p className="text-sm">{displayedSections[0]}</p>;
  };

  return (
    <div
      className={`max-w-[75%] ${
        isUser
          ? "ml-auto bg-[#282828] text-white px-6 py-4 rounded-2xl shadow-md"
          : "bg-[#1e1e1e] text-gray-200 px-6 py-4 rounded-2xl shadow-md"
      }`}
    >
      {renderContent()}
    </div>
  );
}

export default MessageBox;




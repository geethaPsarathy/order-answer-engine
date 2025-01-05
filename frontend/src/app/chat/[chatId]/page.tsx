"use client";

// import { useParams } from "next/navigation";
// import { useState, useEffect } from "react";
// import axios from "axios";
// import ChatWindow from "@/components/ChatWindow";
// import { Message } from "@/components/ChatWindow";

// export default function Page() {
//   const { chatId } = useParams();
//   const [messages, setMessages] = useState<Message[]>([]);
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState<string | null>(null);
//   const [pendingMessage, setPendingMessage] = useState<string | null>(null);

//   useEffect(() => {
//     const loadChatHistory = async () => {
//       if (!chatId) {
//         setError("Invalid chat ID.");
//         setLoading(false);
//         return;
//       }
  
//       try {
//         const response = await axios.get(`http://127.0.0.1:8000/chat/${chatId}`);
//         console.log("API Response:", response.data);  // Debugging
  
//         if (response.data && Array.isArray(response.data.messages)) {
//           // Set messages immediately without pending state
//           setMessages(response.data.messages);
//           setPendingMessage(null);
//         } else {
//           setMessages([]);
//         }
//       } catch (err) {
//         console.error("Failed to load chat history:", err);
//         setError("Failed to load chat history. Please try again.");
//       } finally {
//         setLoading(false);
//       }
//     };
  
//     loadChatHistory();
//   }, [chatId]);
//   // const sendFollowUpMessage = async (message: string): Promise<string | null> => {
//   //   if (!message.trim()) return null;  // Return null if no message
  
//   //   const tempMessage: Message = {
//   //     messageId: `temp-${Date.now()}`,
//   //     chatId: chatId as string,
//   //     createdAt: new Date(),
//   //     content: message,
//   //     role: "user",
//   //   };
//   //   setMessages((prev) => [...prev, tempMessage]);
  
//   //   const loadingMessage: Message = {
//   //     messageId: `loading-${Date.now()}`,
//   //     chatId: chatId as string,
//   //     createdAt: new Date(),
//   //     content: "Assistant is typing...",
//   //     role: "loading",
//   //   };
//   //   setMessages((prev) => [...prev, loadingMessage]);
//   //   setPendingMessage(tempMessage.messageId);

//   //     //   try {
//   // //     console.log("Sending follow-up message:", message);  // Debugging
//   // //     const queryParam = `user_query=${message}`;
//   // //     const response = await axios.post(
//   // //       `http://127.0.0.1:8000/chat/${chatId}/followup-message?${queryParam}`
//   // //     );
//   // //     console.log("Sending follow-up response:", response);  // Debugging

//   // //     setMessages((prev) =>
//   // //       prev.filter((msg) => msg.messageId !== loadingMessage.messageId)
//   // //     );

//   // //     if (response.data && response.data.messages) {
//   // //       const assistantMessage = response.data.messages;
      
//   // //       // Extract the last message only
//   // //       const lastMessage = assistantMessage[assistantMessage.length - 1];
      
//   // //       // Append the last message to the state (avoid duplicates)
//   // //       setMessages((prev) => {
//   // //         const messageExists = prev.some((msg) => msg.messageId === lastMessage.messageId);
//   // //         return messageExists ? prev : [...prev, lastMessage];
//   // //       });
      
//   // //       console.log("Assistant response:", lastMessage);  // Debugging
        
//   // //       return lastMessage.content.message;
//   // //     }
  
//   //   try {
//   //     const response = await axios.post(
//   //       `http://127.0.0.1:8000/chat/${chatId}/followup`,
//   //       { user_query: message }
//   //     );
  
//   //     setMessages((prev) =>
//   //       prev.filter((msg) => msg.messageId !== loadingMessage.messageId)
//   //     );
  
//   //     if (response.data && response.data.messages) {
//   //       const assistantMessage = response.data.messages.pop();
//   //       setMessages((prev) => [...prev, assistantMessage]);
//   //       setPendingMessage(null);
  
//   //       // Return the assistant's response message
//   //       return assistantMessage.content.message || null;
//   //     }
//   //   } catch (error) {
//   //     console.error("Error sending follow-up message:", error);
//   //   }
  
//   //   // If something fails, return null to satisfy the type
//   //   return null;
//   // };
  
  

//   const sendFollowUpMessage = async (message: string) => {
//     if (!message.trim()) return null;

//     const tempMessage: Message = {
//       messageId: `temp-${Date.now()}`,
//       chatId: chatId as string,
//       createdAt: new Date(),
//       content: message,
//       role: 'user',
//     };
//     setMessages((prev) => [...prev, tempMessage]);

//     const loadingMessage: Message = {
//       messageId: `loading-${Date.now()}`,
//       chatId: chatId as string,
//       createdAt: new Date(),
//       content: 'Assistant is typing...',
//       role: 'loading',
//     };
//     setMessages((prev) => [...prev, loadingMessage]);
//     setPendingMessage(message);

//     try {
//       console.log("Sending follow-up message:", message);  // Debugging
//       const queryParam = `user_query=${message}`;
//       const response = await axios.post(
//         `http://127.0.0.1:8000/chat/${chatId}/followup-message?${queryParam}`
//       );
//       console.log("Sending follow-up response:", response);  // Debugging

//       setMessages((prev) =>
//         prev.filter((msg) => msg.messageId !== loadingMessage.messageId)
//       );

//       if (response.data && response.data.messages) {
//         const assistantMessage = response.data.messages;
      
//         // Extract the last message only
//         const lastMessage = assistantMessage[assistantMessage.length - 1];
      
//         // Append the last message to the state (avoid duplicates)
//         setMessages((prev) => {
//           const messageExists = prev.some((msg) => msg.messageId === lastMessage.messageId);
//           return messageExists ? prev : [...prev, lastMessage];
//         });
      
//         console.log("Assistant response:", lastMessage);  // Debugging
        
//         return lastMessage.content.message;
//       }
      
//     } catch (error) {
//       console.error("Error sending follow-up message:", error);
//       // setError("Failed to send message. Please try again.");
//     } finally {
//       setPendingMessage(null);
//     }
//   };

//   if (loading) {
//     return (
//       <div className="flex items-center justify-center h-screen">
//         <p className="text-gray-400">Loading chat history...</p>
//       </div>
//     );
//   }

//   if (error) {
//     return (
//       <div className="text-center p-4 bg-red-500 text-white">
//         {error}
//       </div>
//     );
//   }

//   return (
//     <div>
//       <ChatWindow
//         messages={messages}
//         loading={loading}
//         error={error}
//         onSendMessage={sendFollowUpMessage}
//       />
//       {pendingMessage && (
//         <div className="fixed bottom-4 left-4 bg-blue-600 text-white p-3 rounded-md shadow-md">
//           Sending: {pendingMessage}
//         </div>
//       )}
//     </div>
//   );
// }


import { useParams } from "next/navigation";
import { useState, useEffect } from "react";
import axios from "axios";
import ChatWindow from "@/components/ChatWindow";
import { Message } from "@/components/ChatWindow";

export default function Page() {
  const { chatId } = useParams();
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [pendingMessageId, setPendingMessageId] = useState<string | null>(null);

  useEffect(() => {
    const loadChatHistory = async () => {
      if (!chatId) {
        setError("Invalid chat ID.");
        setLoading(false);
        return;
      }

      try {
        const response = await axios.get(`http://127.0.0.1:8000/chat/${chatId}`);
        console.log("API Response:", response.data);

        if (response.data && Array.isArray(response.data.messages)) {
          setMessages(response.data.messages);  // Load all messages immediately
          console.log("PAGE -- pendingMessageId:", pendingMessageId);  // Debugging
          // setPendingMessageId(null);  // Clear pending message
           // Delay clearing the pending state
          setTimeout(() => {
            setPendingMessageId(null);
          }, 500);
        } else {
          setMessages([]);
        }
      } catch (err) {
        console.error("Failed to load chat history:", err);
        setError("Failed to load chat history. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    loadChatHistory();
  }, [chatId, pendingMessageId]);

  const sendFollowUpMessage = async (message: string): Promise<string | null> => {
    if (!message.trim()) return null;

    console.log("sendFollowUpMessage -- message:", message);  // Debugging

    const tempMessage: Message = {
      messageId: `temp-${Date.now()}`,
      chatId: chatId as string,
      createdAt: new Date(),
      content: message,
      role: "user",
    };
    setMessages((prev) => [...prev, tempMessage]);

    console.log("sendFollowUpMessage -- message:", messages);  // Debugging

    const loadingMessage: Message = {
      messageId: `loading-${Date.now()}`,
      chatId: chatId as string,
      createdAt: new Date(),
      content: "Generating response...",
      role: "loading",
    };
    setMessages((prev) => [...prev, loadingMessage]);
    setPendingMessageId(tempMessage.messageId);

    console.log("sendFollowUpMessage -- messageId:", messages);  // Debugging


    try {
      console.log("Sending follow-up message:", message);  // Debugging
            const queryParam = `user_query=${message}`;
            const response = await axios.post(
              `http://127.0.0.1:8000/chat/${chatId}/followup-message?${queryParam}`
            );

      setMessages((prev) =>
        prev.filter((msg) => msg.messageId !== loadingMessage.messageId)
      );


      // if (response.data && response.data.messages) {
      //   const assistantMessage = response.data.messages.pop();
      //   setMessages((prev) => [...prev, assistantMessage]);
      //   setPendingMessageId(null);
      //   return assistantMessage.content.message || null;
      // }


      if (response.data && response.data.messages) {
                const assistantMessage = response.data.messages;
              
                // Extract the last message only
                const lastMessage = assistantMessage[assistantMessage.length - 1];
              
                // Append the last message to the state (avoid duplicates)
                setMessages((prev) => {

                  const messageExists = prev.some((msg) => msg.messageId === lastMessage.messageId);
                  return messageExists ? prev : [...prev, lastMessage];
                });
              
                
                return lastMessage.content.message;
              }
    } 
    catch (error) {
      console.error("Error sending follow-up message:", error);
    }
    return null;
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <p className="text-gray-400">Loading chat history...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center p-4 bg-red-500 text-white">
        {error}
      </div>
    );
  }

  return (
    <div>
      <ChatWindow
        messages={messages}
        loading={loading}
        error={error}
        onSendMessage={sendFollowUpMessage}
        pendingMessageId={pendingMessageId}
      />
    </div>
  );
}

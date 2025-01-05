// import { Fragment } from 'react';
// import MessageBox from './MessageBox';
// import ShimmerEffect from './ShimmerEffect';
// import { Message } from './ChatWindow';

// const Chat = ({
//   messages,
//   loading,
//   messageRefs,
// }: {
//   messages: Message[];
//   loading: boolean;
//   messageRefs?: React.MutableRefObject<{ [key: string]: HTMLDivElement | null }>;
// }) => {
//   return (
//     <div className="flex flex-col space-y-6 pt-4 pb-44 lg:pb-32 sm:px-4 md:px-8">
//       {messages.map((msg, index) => (
//         <Fragment key={msg.messageId}>
//           <div ref={(el) => { 
//             if (messageRefs) {
//               messageRefs.current[`message-${index}`] = el;
//             }
//           }}>
//             <MessageBox message={msg} />
//           </div>
//         </Fragment>
//       ))}

//       {loading && (
//         <div className="space-y-4">
//           {Array.from({ length: 2 }).map((_, i) => (
//             <ShimmerEffect key={i} />
//           ))}
//         </div>
//       )}
//     </div>
//   );
// };

import { Fragment } from "react";
import MessageBox from "./MessageBox";
import ShimmerEffect from "./ShimmerEffect";
import { Message } from "./ChatWindow";

interface ChatProps {
  messages: Message[];
  loading: boolean;
  pendingMessageId?: string | null;
  messageRefs?: React.MutableRefObject<{ [key: string]: HTMLDivElement | null }>;
}

const Chat = ({ messages, loading, pendingMessageId, messageRefs }: ChatProps) => {
  console.log('Chat.tsx: messages:', messages ,loading, pendingMessageId);
  return (
    <div className="flex flex-col space-y-6 pt-4 pb-44 lg:pb-32 sm:px-4 md:px-8">
      {messages.map((msg, index) => (
        <Fragment key={msg.messageId}>
          <div
            ref={(el) => {
              if (messageRefs) {
                messageRefs.current[`message-${index}`] = el;
              }
            }}
          >
            {
              msg.messageId === pendingMessageId ? (
                <MessageBox message={msg} isFollowUp ={ msg.role === 'assistant' && !!pendingMessageId}
                />
              ) : (
                <MessageBox message={msg} />
              )
            }
            {/* <MessageBox
              message={msg}
              isFollowUp={msg.messageId === pendingMessageId}
            /> */}
          </div>
        </Fragment>
      ))}

      {loading && (
        <div className="space-y-4">
          {Array.from({ length: 2 }).map((_, i) => (
            <ShimmerEffect key={i} />
          ))}
        </div>
      )}
    </div>
  );
};

export default Chat;


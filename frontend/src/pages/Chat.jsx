import Navbar from "../components/layout/Navbar";
import ChatContainer from "../components/chat/ChatContainer";

export default function Chat() {
  return (
    <>
      <Navbar />

      <div className="bg-slate-50 py-10 min-h-screen">
        <ChatContainer />
      </div>
    </>
  );
}
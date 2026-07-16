
import React, { useState, useRef, useEffect } from 'react';
import { Send, Mic, MicOff, Video, VideoOff, Users, ArrowLeft, Plus } from 'lucide-react';
import { useApp } from '../contexts/AppContext';
import AddToQueueModal from './AddToQueueModal';

const WatchParty = () => {
  const { 
    roomName, 
    roomUsers, 
    movieQueue, 
    chatMessages, 
    addChatMessage, 
    emojiReactions,
    addEmojiReaction,
    removeFromQueue,
    setCurrentPage,
    setIsInRoom
  } = useApp();
  
  const [chatInput, setChatInput] = useState('');
  const [isMuted, setIsMuted] = useState(true);
  const [isVideoOff, setIsVideoOff] = useState(false); // Start with video on
  const [showAddToQueue, setShowAddToQueue] = useState(false);
  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);

  const currentMovie = movieQueue[0];
  const emojis = ['😂', '❤️', '😮', '👏', '🔥', '💯', '😍', '🤔'];

  // Auto-start webcam when component mounts
  useEffect(() => {
    startVideo();
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  const startVideo = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      streamRef.current = stream;
      setIsVideoOff(false);
    } catch (error) {
      console.error('Error accessing webcam:', error);
      setIsVideoOff(true);
    }
  };

  const stopVideo = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setIsVideoOff(true);
  };

  const handleSendMessage = () => {
    if (chatInput.trim()) {
      addChatMessage(chatInput);
      setChatInput('');
    }
  };

  const handleEmojiClick = (emoji: string, event: React.MouseEvent) => {
    const rect = event.currentTarget.getBoundingClientRect();
    const x = rect.left + rect.width / 2;
    const y = rect.top;
    addEmojiReaction(emoji, x, y);
  };

  const handleLeaveRoom = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
    }
    setIsInRoom(false);
    setCurrentPage('home');
  };

  const handleVideoToggle = () => {
    if (isVideoOff) {
      startVideo();
    } else {
      stopVideo();
    }
  };

  return (
    <div className="min-h-screen bg-fire-darker flex">
      {/* Main Content Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-fire-dark/90 backdrop-blur-md p-4 flex items-center justify-between border-b border-fire-gray/30">
          <div className="flex items-center space-x-4">
            <button
              onClick={handleLeaveRoom}
              className="p-2 hover:bg-fire-gray/50 text-white rounded-lg transition-colors duration-200"
            >
              <ArrowLeft size={20} />
            </button>
            <h1 className="text-xl font-bold text-white">{roomName}</h1>
            <div className="flex items-center space-x-2 text-fire-orange">
              <Users size={16} />
              <span className="text-sm">{roomUsers.filter(u => u.isOnline).length} online</span>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            {roomUsers.slice(0, 4).map((user) => (
              <div 
                key={user.id}
                className={`relative w-8 h-8 rounded-full bg-fire-gray flex items-center justify-center text-sm ${
                  user.isOnline ? 'ring-2 ring-fire-orange' : 'opacity-50'
                }`}
              >
                {user.avatar}
                {user.isOnline && (
                  <div className="absolute -bottom-1 -right-1 w-3 h-3 bg-green-500 rounded-full border-2 border-fire-dark" />
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Video Area */}
        <div className="flex-1 flex items-center justify-center p-8 relative">
          {/* My Video Feed - Top Left Corner */}
          {!isVideoOff && (
            <div className="absolute top-4 left-4 w-48 h-36 bg-black rounded-lg overflow-hidden z-10 border-2 border-fire-orange">
              <video
                ref={videoRef}
                autoPlay
                muted
                playsInline
                className="w-full h-full object-cover scale-x-[-1]"
              />
              <div className="absolute bottom-2 left-2 bg-black/70 text-white text-xs px-2 py-1 rounded">
                You
              </div>
            </div>
          )}

          {currentMovie ? (
            <div className="relative max-w-4xl w-full">
              <div className="aspect-video bg-black rounded-xl overflow-hidden shadow-2xl">
                <img 
                  src={currentMovie.image} 
                  alt={currentMovie.title}
                  className="w-full h-full object-cover"
                />
                <div className="absolute inset-0 bg-black/40 flex items-center justify-center">
                  <div className="text-center text-white">
                    <div className="w-20 h-20 bg-fire-orange/20 rounded-full flex items-center justify-center mb-4 mx-auto">
                      <div className="w-8 h-8 bg-fire-orange rounded-full flex items-center justify-center">
                        ▶
                      </div>
                    </div>
                    <h3 className="text-2xl font-bold mb-2">{currentMovie.title}</h3>
                    <p className="text-gray-300">Ready to watch together</p>
                  </div>
                </div>
              </div>
              
              {/* Floating emoji reactions */}
              {emojiReactions.map((reaction) => (
                <div
                  key={reaction.id}
                  className="fixed text-4xl animate-float-up pointer-events-none z-50"
                  style={{
                    left: reaction.x,
                    top: reaction.y,
                  }}
                >
                  {reaction.emoji}
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center text-gray-400">
              <p className="text-xl mb-4">No movie in queue</p>
              <button 
                onClick={() => setShowAddToQueue(true)}
                className="px-6 py-3 bg-fire-orange text-white rounded-lg hover:bg-fire-blue transition-colors duration-200"
              >
                Browse Movies
              </button>
            </div>
          )}
        </div>

        {/* Controls */}
        <div className="bg-fire-dark/90 backdrop-blur-md p-4 flex items-center justify-between border-t border-fire-gray/30">
          <div className="flex items-center space-x-4">
            <button
              onClick={() => setIsMuted(!isMuted)}
              className={`p-3 rounded-full transition-colors duration-200 ${
                isMuted ? 'bg-red-600 text-white' : 'bg-fire-gray text-white hover:bg-fire-orange'
              }`}
            >
              {isMuted ? <MicOff size={20} /> : <Mic size={20} />}
            </button>
            
            <button
              onClick={handleVideoToggle}
              className={`p-3 rounded-full transition-colors duration-200 ${
                isVideoOff ? 'bg-red-600 text-white' : 'bg-fire-gray text-white hover:bg-fire-orange'
              }`}
            >
              {isVideoOff ? <VideoOff size={20} /> : <Video size={20} />}
            </button>
          </div>

          {/* Emoji reactions */}
          <div className="flex items-center space-x-2">
            {emojis.map((emoji, index) => (
              <button
                key={index}
                onClick={(e) => handleEmojiClick(emoji, e)}
                className="p-2 hover:bg-fire-orange/20 rounded-lg transition-colors duration-200 text-xl"
              >
                {emoji}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* Sidebar */}
      <div className="w-80 bg-fire-dark border-l border-fire-gray/30 flex flex-col">
        {/* Friend Videos Section */}
        <div className="p-4 border-b border-fire-gray/30">
          <h3 className="text-white font-bold mb-3">Friends in Room</h3>
          <div className="grid grid-cols-2 gap-2">
            {roomUsers.filter(u => u.isOnline).slice(0, 4).map((user) => (
              <div key={user.id} className="relative aspect-video bg-fire-gray/30 rounded-lg overflow-hidden">
                <div className="absolute inset-0 flex items-center justify-center text-2xl">
                  {user.avatar}
                </div>
                <div className="absolute bottom-1 left-1 right-1">
                  <div className="bg-black/70 px-2 py-1 rounded text-white text-xs flex items-center justify-between">
                    <span className="truncate">{user.name}</span>
                    <div className="flex space-x-1">
                      <div className={`w-2 h-2 rounded-full ${isMuted ? 'bg-red-500' : 'bg-green-500'}`} />
                      <div className={`w-2 h-2 rounded-full ${isVideoOff ? 'bg-red-500' : 'bg-green-500'}`} />
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Queue Section */}
        <div className="p-4 border-b border-fire-gray/30">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-white font-bold">Queue ({movieQueue.length})</h3>
            <button
              onClick={() => setShowAddToQueue(true)}
              className="p-1 bg-fire-orange hover:bg-fire-blue text-white rounded transition-colors duration-200"
            >
              <Plus size={16} />
            </button>
          </div>
          <div className="space-y-2 max-h-40 overflow-y-auto">
            {movieQueue.map((movie, index) => (
              <div key={movie.id} className="flex items-center space-x-3 p-2 bg-fire-gray/30 rounded-lg">
                <img 
                  src={movie.image} 
                  alt={movie.title}
                  className="w-12 h-16 object-cover rounded"
                />
                <div className="flex-1 min-w-0">
                  <p className="text-white text-sm font-medium truncate">{movie.title}</p>
                  <p className="text-gray-400 text-xs">{movie.duration}</p>
                  {index === 0 && (
                    <span className="text-fire-orange text-xs font-bold">NOW PLAYING</span>
                  )}
                </div>
                {index > 0 && (
                  <button
                    onClick={() => removeFromQueue(movie.id)}
                    className="text-gray-400 hover:text-red-400 transition-colors duration-200"
                  >
                    ×
                  </button>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* Chat Section */}
        <div className="flex-1 flex flex-col">
          <div className="p-4 border-b border-fire-gray/30">
            <h3 className="text-white font-bold">Group Chat</h3>
          </div>
          
          <div className="flex-1 overflow-y-auto p-4 space-y-3">
            {chatMessages.map((message) => (
              <div key={message.id} className="animate-slide-in">
                <div className="flex items-start space-x-2">
                  <div className="w-8 h-8 rounded-full bg-fire-gray flex items-center justify-center text-sm">
                    {message.avatar}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className="text-white text-sm font-medium">{message.user}</span>
                      <span className="text-gray-500 text-xs">
                        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                      </span>
                    </div>
                    <p className="text-gray-300 text-sm">{message.message}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="p-4 border-t border-fire-gray/30">
            <div className="flex items-center space-x-2">
              <input
                type="text"
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Type a message..."
                className="flex-1 px-3 py-2 bg-fire-gray text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-fire-orange placeholder-gray-400"
              />
              <button
                onClick={handleSendMessage}
                className="p-2 bg-fire-orange hover:bg-fire-blue text-white rounded-lg transition-colors duration-200"
              >
                <Send size={16} />
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Add to Queue Modal */}
      <AddToQueueModal 
        isOpen={showAddToQueue}
        onClose={() => setShowAddToQueue(false)}
      />
    </div>
  );
};

export default WatchParty;

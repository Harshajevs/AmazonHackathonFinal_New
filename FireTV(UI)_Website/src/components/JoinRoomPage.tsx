
import React, { useState } from 'react';
import { useApp } from '../contexts/AppContext';
import { ArrowLeft } from 'lucide-react';

const JoinRoomPage = () => {
  const { setIsInRoom, setCurrentPage, setRoomName } = useApp();
  const [roomId, setRoomId] = useState('');
  const [password, setPassword] = useState('');

  const handleJoinRoom = () => {
    if (!roomId) return;
    
    setRoomName(`Room ${roomId}`);
    setIsInRoom(true);
    setCurrentPage('room');
  };

  const handleBack = () => {
    setCurrentPage('home');
  };

  return (
    <div className="min-h-screen bg-fire-darker p-8">
      <div className="max-w-2xl mx-auto">
        <button
          onClick={handleBack}
          className="flex items-center space-x-2 text-gray-300 hover:text-white mb-8 transition-colors duration-200"
        >
          <ArrowLeft size={20} />
          <span>Back to Home</span>
        </button>
        
        <h1 className="text-4xl font-bold text-white mb-8">Join a Room</h1>
        
        <div className="bg-fire-gray/20 rounded-xl p-8">
          <div className="space-y-6">
            <div>
              <label className="block text-white font-medium mb-2">Room ID</label>
              <input
                type="text"
                value={roomId}
                onChange={(e) => setRoomId(e.target.value)}
                placeholder="Enter room ID"
                className="w-full px-4 py-3 bg-fire-gray text-white rounded-lg border border-fire-gray/50 focus:border-fire-orange focus:outline-none"
              />
            </div>
            
            <div>
              <label className="block text-white font-medium mb-2">Password (if required)</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter password"
                className="w-full px-4 py-3 bg-fire-gray text-white rounded-lg border border-fire-gray/50 focus:border-fire-orange focus:outline-none"
              />
            </div>
            
            <div className="flex space-x-4">
              <button
                onClick={handleBack}
                className="flex-1 px-6 py-3 bg-gray-600 hover:bg-gray-700 text-white font-bold rounded-lg transition-colors duration-200"
              >
                Back
              </button>
              <button
                onClick={handleJoinRoom}
                disabled={!roomId}
                className="flex-1 px-6 py-3 bg-fire-orange hover:bg-fire-blue disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-bold rounded-lg transition-colors duration-200"
              >
                Join
              </button>
            </div>
          </div>
          
          <div className="mt-8 p-4 bg-fire-dark/50 rounded-lg">
            <h3 className="text-white font-medium mb-2">How to join a room:</h3>
            <ul className="text-gray-300 text-sm space-y-1">
              <li>• Get the Room ID from your friend</li>
              <li>• Enter the password if the room is protected</li>
              <li>• Click "Join" to start watching together</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default JoinRoomPage;

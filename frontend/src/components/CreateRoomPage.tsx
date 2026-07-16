
import React, { useState } from 'react';
import { useApp } from '../contexts/AppContext';
import { predefinedMovies, movieData } from '../data/movieData';
import { Users, UserPlus, Plus } from 'lucide-react';

const CreateRoomPage = () => {
  const { setIsInRoom, setCurrentPage, setRoomName, roomUsers, setSelectedRoomMovie, addFriendToRoom } = useApp();
  const [selectedMovie, setSelectedMovie] = useState('');
  const [roomNameInput, setRoomNameInput] = useState('');
  const [roomPassword, setRoomPassword] = useState('');
  const [showAddFriend, setShowAddFriend] = useState(false);
  const [friendName, setFriendName] = useState('');

  const selectedMovieData = movieData.find(m => m.title === selectedMovie);

  const handleCreateRoom = () => {
    if (!roomNameInput || !selectedMovie) return;
    
    setRoomName(roomNameInput);
    setSelectedRoomMovie(selectedMovieData || null);
    setIsInRoom(true);
    setCurrentPage('room');
  };

  const handleAddFriend = () => {
    if (friendName.trim()) {
      addFriendToRoom(friendName);
      setFriendName('');
      setShowAddFriend(false);
    }
  };

  return (
    <div className="min-h-screen bg-fire-darker p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-8">Create a Room</h1>
        
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Room Settings */}
          <div className="bg-fire-gray/20 rounded-xl p-8">
            <h2 className="text-2xl font-bold text-white mb-6">Room Settings</h2>
            
            <div className="space-y-4">
              <div>
                <label className="block text-white font-medium mb-2">Room Name</label>
                <input
                  type="text"
                  value={roomNameInput}
                  onChange={(e) => setRoomNameInput(e.target.value)}
                  placeholder="Enter room name"
                  className="w-full px-4 py-3 bg-fire-gray text-white rounded-lg border border-fire-gray/50 focus:border-fire-orange focus:outline-none"
                />
              </div>
              
              <div>
                <label className="block text-white font-medium mb-2">Room Password (Optional)</label>
                <input
                  type="password"
                  value={roomPassword}
                  onChange={(e) => setRoomPassword(e.target.value)}
                  placeholder="Enter password"
                  className="w-full px-4 py-3 bg-fire-gray text-white rounded-lg border border-fire-gray/50 focus:border-fire-orange focus:outline-none"
                />
              </div>
              
              <div>
                <label className="block text-white font-medium mb-2">Select Movie</label>
                <select
                  value={selectedMovie}
                  onChange={(e) => setSelectedMovie(e.target.value)}
                  className="w-full px-4 py-3 bg-fire-gray text-white rounded-lg border border-fire-gray/50 focus:border-fire-orange focus:outline-none"
                >
                  <option value="">Choose a movie</option>
                  {predefinedMovies.map((movie) => (
                    <option key={movie} value={movie}>{movie}</option>
                  ))}
                </select>
              </div>

              {/* Friends Management */}
              <div>
                <div className="flex items-center justify-between mb-3">
                  <label className="block text-white font-medium">Friends in Room</label>
                  <button
                    onClick={() => setShowAddFriend(true)}
                    className="flex items-center space-x-2 px-3 py-1 bg-fire-orange/20 text-fire-orange rounded-lg hover:bg-fire-orange/30 transition-colors duration-200"
                  >
                    <UserPlus size={16} />
                    <span>Add Friend</span>
                  </button>
                </div>
                <div className="flex flex-wrap gap-2">
                  {roomUsers.filter(u => u.isOnline).map((user) => (
                    <div key={user.id} className="flex items-center space-x-2 px-3 py-2 bg-fire-gray rounded-lg">
                      <span className="text-lg">{user.avatar}</span>
                      <span className="text-white text-sm">{user.name}</span>
                    </div>
                  ))}
                </div>
              </div>
            </div>
            
            <button
              onClick={handleCreateRoom}
              disabled={!roomNameInput || !selectedMovie}
              className="w-full mt-6 px-6 py-3 bg-fire-orange hover:bg-fire-blue disabled:bg-gray-600 disabled:cursor-not-allowed text-white font-bold rounded-lg transition-colors duration-200"
            >
              Create Room
            </button>
          </div>
          
          {/* Movie Preview */}
          <div className="bg-fire-gray/20 rounded-xl p-8">
            <h2 className="text-2xl font-bold text-white mb-6">Selected Movie</h2>
            
            {selectedMovieData ? (
              <div className="text-center">
                <div className="relative mb-6">
                  <img 
                    src={selectedMovieData.image} 
                    alt={selectedMovieData.title}
                    className="w-full max-w-sm mx-auto rounded-xl shadow-2xl"
                  />
                  <div className="absolute inset-0 bg-black/40 rounded-xl flex items-center justify-center">
                    <div className="w-20 h-20 bg-fire-orange/20 rounded-full flex items-center justify-center">
                      <div className="w-8 h-8 bg-fire-orange rounded-full flex items-center justify-center">
                        ▶
                      </div>
                    </div>
                  </div>
                </div>
                
                <h3 className="text-2xl font-bold text-white mb-2">{selectedMovieData.title}</h3>
                <p className="text-gray-300 mb-4">{selectedMovieData.description}</p>
                
                <div className="flex items-center justify-center space-x-4 mb-4">
                  <span className="px-3 py-1 bg-fire-orange/20 text-fire-orange rounded-full text-sm">
                    {selectedMovieData.year}
                  </span>
                  <span className="px-3 py-1 bg-fire-orange/20 text-fire-orange rounded-full text-sm">
                    ⭐ {selectedMovieData.rating}
                  </span>
                  <span className="px-3 py-1 bg-fire-orange/20 text-fire-orange rounded-full text-sm">
                    {selectedMovieData.duration}
                  </span>
                </div>
                
                <div className="flex flex-wrap justify-center gap-2">
                  {selectedMovieData.genre.map((genre, index) => (
                    <span key={index} className="px-2 py-1 bg-fire-gray text-white text-xs rounded-full">
                      {genre}
                    </span>
                  ))}
                </div>
              </div>
            ) : (
              <div className="text-center text-gray-400 py-12">
                <div className="w-32 h-48 bg-fire-gray rounded-xl mx-auto mb-4 flex items-center justify-center">
                  <Plus size={32} className="text-gray-600" />
                </div>
                <p>Select a movie to see preview</p>
              </div>
            )}
          </div>
        </div>

        {/* Add Friend Modal */}
        {showAddFriend && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={() => setShowAddFriend(false)}>
            <div className="bg-fire-dark p-6 rounded-xl max-w-md w-full mx-4" onClick={(e) => e.stopPropagation()}>
              <h3 className="text-white text-lg font-bold mb-4">Add Friend to Room</h3>
              <input
                type="text"
                value={friendName}
                onChange={(e) => setFriendName(e.target.value)}
                placeholder="Enter friend's name"
                className="w-full px-4 py-2 bg-fire-gray text-white rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-fire-orange"
                autoFocus
              />
              <div className="flex space-x-4">
                <button
                  onClick={handleAddFriend}
                  disabled={!friendName.trim()}
                  className="flex-1 px-4 py-2 bg-fire-orange hover:bg-fire-blue disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg transition-colors duration-200"
                >
                  Add Friend
                </button>
                <button
                  onClick={() => setShowAddFriend(false)}
                  className="flex-1 px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors duration-200"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default CreateRoomPage;

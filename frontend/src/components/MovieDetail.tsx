
import React, { useEffect } from 'react';
import { Play, Plus, Users, ArrowLeft } from 'lucide-react';
import { useApp } from '../contexts/AppContext';

const MovieDetail = () => {
  const { selectedMovie, setCurrentPage, addToQueue, setIsInRoom, setRoomName } = useApp();

  const platformThemes = {
    'Netflix': 'bg-black',
    'Prime Video': 'bg-blue-900',
    'Hotstar': 'bg-gradient-to-br from-pink-600 to-purple-600',
    'Aha': 'bg-orange-600'
  };

  useEffect(() => {
    if (selectedMovie) {
      document.body.style.background = '';
      document.body.className = platformThemes[selectedMovie.platform];
    }
    
    return () => {
      document.body.style.background = '';
      document.body.className = '';
    };
  }, [selectedMovie]);

  if (!selectedMovie) return null;

  const handleCreateRoom = () => {
    setRoomName(`${selectedMovie.title} Party`);
    setIsInRoom(true);
    setCurrentPage('room');
    addToQueue(selectedMovie);
  };

  const handleBack = () => {
    setCurrentPage('home');
  };

  return (
    <div className={`min-h-screen ${platformThemes[selectedMovie.platform]} transition-all duration-500`}>
      <div className="relative h-screen flex items-center">
        <img 
          src={selectedMovie.image} 
          alt={selectedMovie.title}
          className="absolute inset-0 w-full h-full object-cover opacity-30"
        />
        <div className="absolute inset-0 bg-gradient-to-r from-black/90 via-black/60 to-black/30" />
        
        <button
          onClick={handleBack}
          className="absolute top-8 left-8 z-20 p-3 bg-black/50 hover:bg-black/70 text-white rounded-full transition-all duration-300"
        >
          <ArrowLeft size={24} />
        </button>

        <div className="relative z-10 max-w-6xl mx-auto px-8 grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <div className="order-2 lg:order-1">
            <h1 className="text-5xl md:text-7xl font-bold text-white mb-6 leading-tight">
              {selectedMovie.title}
            </h1>
            
            <div className="flex items-center space-x-6 mb-6">
              <span className="text-fire-orange font-bold text-xl">⭐ {selectedMovie.rating}</span>
              <span className="text-white">{selectedMovie.year}</span>
              <span className="text-white">{selectedMovie.duration}</span>
              <span className="px-3 py-1 bg-white/20 text-white rounded-full text-sm font-medium">
                {selectedMovie.platform}
              </span>
            </div>

            <div className="flex flex-wrap gap-2 mb-6">
              {selectedMovie.genre.map((genre, index) => (
                <span 
                  key={index}
                  className="px-4 py-2 bg-fire-orange/20 text-fire-orange rounded-full text-sm font-medium"
                >
                  {genre}
                </span>
              ))}
            </div>

            <p className="text-xl text-gray-200 mb-8 leading-relaxed">
              {selectedMovie.description}
            </p>

            <div className="flex flex-col sm:flex-row gap-4">
              <button className="px-8 py-4 bg-fire-orange hover:bg-fire-blue text-white font-bold rounded-xl flex items-center justify-center space-x-3 transition-all duration-300 hover:scale-105 shadow-lg">
                <Play size={20} />
                <span>Play Movie</span>
              </button>
              
              <button 
                onClick={() => addToQueue(selectedMovie)}
                className="px-8 py-4 bg-white/20 hover:bg-white/30 text-white font-bold rounded-xl flex items-center justify-center space-x-3 backdrop-blur-sm transition-all duration-300"
              >
                <Plus size={20} />
                <span>Add to Queue</span>
              </button>
              
              <button 
                onClick={handleCreateRoom}
                className="px-8 py-4 bg-fire-purple hover:bg-fire-purple/80 text-white font-bold rounded-xl flex items-center justify-center space-x-3 transition-all duration-300 hover:scale-105 shadow-lg"
              >
                <Users size={20} />
                <span>Create Room</span>
              </button>
            </div>
          </div>

          <div className="order-1 lg:order-2">
            <div className="relative">
              <img 
                src={selectedMovie.image} 
                alt={selectedMovie.title}
                className="w-full max-w-md mx-auto rounded-2xl shadow-2xl"
              />
              <div className="absolute inset-0 rounded-2xl ring-2 ring-fire-orange/30" />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MovieDetail;

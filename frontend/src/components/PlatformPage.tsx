
import React, { useState } from 'react';
import { ArrowLeft, Play, Plus, Search } from 'lucide-react';
import { useApp } from '../contexts/AppContext';
import MovieCard from './MovieCard';
import { movieData } from '../data/movieData';

const PlatformPage = () => {
  const { selectedPlatform, setCurrentPage } = useApp();
  const [showExitModal, setShowExitModal] = useState(false);

  // Filter movies by platform
  const platformMovies = movieData.filter(movie => movie.platform === selectedPlatform);

  const handleBackClick = () => {
    setShowExitModal(true);
  };

  const handleConfirmExit = () => {
    setShowExitModal(false);
    setCurrentPage('home');
  };

  const handleCancelExit = () => {
    setShowExitModal(false);
  };

  return (
    <div className="min-h-screen bg-fire-darker relative">
      {/* Header with Back button */}
      <div className="relative">
        <button
          onClick={handleBackClick}
          className="absolute top-4 left-4 z-20 flex items-center space-x-2 px-4 py-2 bg-black/70 hover:bg-black/90 text-white rounded-lg transition-colors duration-200"
        >
          <ArrowLeft size={20} />
          <span>Back</span>
        </button>
        
        {/* Platform Header */}
        <div className="relative h-64 overflow-hidden">
          <div 
            className="absolute inset-0 bg-cover bg-center"
            style={{
              backgroundImage: selectedPlatform ? `url(/images/${selectedPlatform.toLowerCase().replace(' ', '-')}.jpg)` : 'none'
            }}
          />
          <div className="absolute inset-0 bg-gradient-to-t from-fire-darker via-black/50 to-transparent" />
          <div className="relative z-10 flex items-center justify-center h-full">
            <h1 className="text-5xl font-bold text-white">{selectedPlatform}</h1>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="p-8">
        <div className="max-w-7xl mx-auto">
          {/* Featured Section */}
          {platformMovies.length > 0 && (
            <div className="mb-12">
              <h2 className="text-2xl font-bold text-white mb-6">Featured on {selectedPlatform}</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-6">
                {platformMovies.slice(0, 12).map((movie) => (
                  <MovieCard key={movie.id} movie={movie} />
                ))}
              </div>
            </div>
          )}

          {/* All Content */}
          {platformMovies.length > 12 && (
            <div className="mb-12">
              <h2 className="text-2xl font-bold text-white mb-6">All Content</h2>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-6">
                {platformMovies.slice(12).map((movie) => (
                  <MovieCard key={movie.id} movie={movie} />
                ))}
              </div>
            </div>
          )}

          {/* Empty State */}
          {platformMovies.length === 0 && (
            <div className="text-center text-gray-400 mt-12">
              <h2 className="text-2xl font-bold mb-2">No content available</h2>
              <p>Content for {selectedPlatform} will be available soon!</p>
            </div>
          )}
        </div>
      </div>

      {/* Exit Confirmation Modal */}
      {showExitModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
          <div className="bg-fire-dark p-8 rounded-xl max-w-md mx-4" onClick={(e) => e.stopPropagation()}>
            <div className="text-center">
              <h3 className="text-white text-xl font-bold mb-4">Confirm Exit</h3>
              <p className="text-gray-300 mb-6">
                Are you sure you want to exit {selectedPlatform} and return to Home?
              </p>
              <div className="flex space-x-4">
                <button
                  onClick={handleConfirmExit}
                  className="flex-1 px-4 py-2 bg-fire-orange text-white rounded-lg hover:bg-fire-orange/80 transition-colors"
                >
                  Yes, Exit to Home
                </button>
                <button
                  onClick={handleCancelExit}
                  className="flex-1 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default PlatformPage;

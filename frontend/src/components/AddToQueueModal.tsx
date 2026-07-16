
import React, { useState } from 'react';
import { X, Plus } from 'lucide-react';
import { useApp } from '../contexts/AppContext';
import { movieCategories } from '../data/movieData';
import { Movie } from '../types/Movie';
import MovieRow from './MovieRow';

interface AddToQueueModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const AddToQueueModal = ({ isOpen, onClose }: AddToQueueModalProps) => {
  const { addToQueue } = useApp();
  const [selectedCategory, setSelectedCategory] = useState('Trending');

  const allMovies = Object.values(movieCategories).flat();
  const categories = Object.keys(movieCategories);

  // Room recommendations - a curated selection of movies
  const roomRecommendations = allMovies.slice(10, 20);

  const handleAddToQueue = (movie: Movie) => {
    addToQueue(movie);
    onClose();
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={onClose}>
      <div className="bg-fire-dark rounded-xl max-w-6xl w-full mx-4 max-h-[90vh] overflow-hidden" onClick={(e) => e.stopPropagation()}>
        <div className="p-6 border-b border-fire-gray/30 flex items-center justify-between">
          <h2 className="text-white text-xl font-bold">Add Movie to Queue</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-fire-gray/50 text-white rounded-lg transition-colors duration-200"
          >
            <X size={20} />
          </button>
        </div>
        
        <div className="p-6 overflow-y-auto max-h-[calc(90vh-120px)]">
          {/* Room Recommendations Section */}
          <div className="mb-8">
            <h3 className="text-xl font-bold text-white mb-4">Room Recommendations</h3>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
              {roomRecommendations.map((movie) => (
                <div key={movie.id} className="relative group">
                  <img
                    src={movie.image}
                    alt={movie.title}
                    className="w-full h-48 object-cover rounded-lg"
                  />
                  <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-lg flex items-center justify-center">
                    <button
                      onClick={() => handleAddToQueue(movie)}
                      className="p-2 bg-fire-orange hover:bg-fire-blue text-white rounded-full transition-colors duration-200"
                    >
                      <Plus size={20} />
                    </button>
                  </div>
                  <div className="absolute bottom-2 left-2 right-2">
                    <p className="text-white text-sm font-medium truncate bg-black/70 px-2 py-1 rounded">
                      {movie.title}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Category Selection */}
          <div className="flex space-x-4 mb-6 overflow-x-auto">
            {categories.map((category) => (
              <button
                key={category}
                onClick={() => setSelectedCategory(category)}
                className={`px-4 py-2 rounded-lg whitespace-nowrap transition-colors duration-200 ${
                  selectedCategory === category
                    ? 'bg-fire-orange text-white'
                    : 'bg-fire-gray text-gray-300 hover:bg-fire-gray/70'
                }`}
              >
                {category}
              </button>
            ))}
          </div>

          {/* Category Movies */}
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
            {movieCategories[selectedCategory]?.map((movie) => (
              <div key={movie.id} className="relative group">
                <img
                  src={movie.image}
                  alt={movie.title}
                  className="w-full h-48 object-cover rounded-lg"
                />
                <div className="absolute inset-0 bg-black/50 opacity-0 group-hover:opacity-100 transition-opacity duration-300 rounded-lg flex items-center justify-center">
                  <button
                    onClick={() => handleAddToQueue(movie)}
                    className="p-2 bg-fire-orange hover:bg-fire-blue text-white rounded-full transition-colors duration-200"
                  >
                    <Plus size={20} />
                  </button>
                </div>
                <div className="absolute bottom-2 left-2 right-2">
                  <p className="text-white text-sm font-medium truncate bg-black/70 px-2 py-1 rounded">
                    {movie.title}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default AddToQueueModal;

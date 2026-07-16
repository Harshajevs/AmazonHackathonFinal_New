
import React, { useState, useMemo } from 'react';
import { Search, Mic } from 'lucide-react';
import { useApp } from '../contexts/AppContext';
import { movieData, predefinedMovies } from '../data/movieData';
import MovieCard from './MovieCard';

const SearchPage = () => {
  const { searchQuery, setSearchQuery } = useApp();
  const [inputValue, setInputValue] = useState(searchQuery);

  const filteredMovies = useMemo(() => {
    if (!inputValue.trim()) return [];
    
    return movieData.filter(movie => 
      movie.title.toLowerCase().includes(inputValue.toLowerCase()) ||
      movie.genre.some(genre => genre.toLowerCase().includes(inputValue.toLowerCase())) ||
      movie.description.toLowerCase().includes(inputValue.toLowerCase())
    );
  }, [inputValue]);

  const handleSearch = (value: string) => {
    setInputValue(value);
    setSearchQuery(value);
  };

  const handleVoiceSearch = () => {
    console.log('Voice search activated');
    // Here you would typically integrate with Web Speech API
    // For now, just a placeholder function
  };

  return (
    <div className="min-h-screen bg-fire-darker p-8">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-white mb-6">Search</h1>
          
          <div className="relative max-w-2xl flex items-center">
            <div className="relative flex-1">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                value={inputValue}
                onChange={(e) => handleSearch(e.target.value)}
                placeholder="Search for movies, shows, and more..."
                className="w-full pl-12 pr-4 py-3 bg-fire-gray text-white rounded-xl border border-fire-gray/50 focus:border-fire-orange focus:outline-none"
              />
            </div>
            <button
              onClick={handleVoiceSearch}
              className="ml-3 w-12 h-12 bg-fire-gray hover:bg-fire-orange border border-fire-gray/50 rounded-xl flex items-center justify-center transition-colors duration-200"
            >
              <Mic size={20} className="text-white" />
            </button>
          </div>
        </div>

        {inputValue.trim() === '' ? (
          <div className="text-center text-gray-400 mt-12">
            <Search size={64} className="mx-auto mb-4 opacity-50" />
            <h2 className="text-2xl font-bold mb-2">Search for content</h2>
            <p>Start typing to find movies, TV shows, and more</p>
          </div>
        ) : filteredMovies.length === 0 ? (
          <div className="text-center text-gray-400 mt-12">
            <h2 className="text-2xl font-bold mb-2">No results found</h2>
            <p>Try searching for something else</p>
          </div>
        ) : (
          <div>
            <h2 className="text-2xl font-bold text-white mb-6">
              Search Results ({filteredMovies.length})
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-6">
              {filteredMovies.map((movie) => (
                <MovieCard key={movie.id} movie={movie} size="medium" />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default SearchPage;

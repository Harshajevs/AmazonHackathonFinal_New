
import React from 'react';
import { useApp } from '../contexts/AppContext';
import { movieData, allCategories } from '../data/movieData';
import MovieCard from './MovieCard';

const CategoriesPage = () => {
  const { selectedCategory, setSelectedCategory } = useApp();

  const filteredMovies = selectedCategory === 'All' 
    ? movieData 
    : movieData.filter(movie => movie.genre.includes(selectedCategory));

  return (
    <div className="min-h-screen bg-fire-darker p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-8">Categories</h1>
        
        {/* Category Filter */}
        <div className="flex flex-wrap gap-4 mb-8">
          {allCategories.map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-6 py-3 rounded-full font-medium transition-all duration-300 ${
                selectedCategory === category
                  ? 'bg-fire-orange text-white'
                  : 'bg-fire-gray text-gray-300 hover:bg-fire-gray/70 hover:text-white'
              }`}
            >
              {category}
            </button>
          ))}
        </div>

        {/* Movies Grid */}
        <div>
          <h2 className="text-2xl font-bold text-white mb-6">
            {selectedCategory === 'All' ? 'All Movies' : selectedCategory} ({filteredMovies.length})
          </h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-6">
            {filteredMovies.map((movie) => (
              <MovieCard key={movie.id} movie={movie} size="medium" />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CategoriesPage;

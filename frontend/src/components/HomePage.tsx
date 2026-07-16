
import React from 'react';
import MovieRow from './MovieRow';
import HeroSlider from './HeroSlider';
import AppsRow from './AppsRow';
import { movieCategories } from '../data/movieData';

const HomePage = () => {
  // Rename categories for display
  const categoryMapping: { [key: string]: string } = {
    'Trending': 'Recently Watched',
    'Popular Movies': 'Personal Recommendations',
    'New Releases': 'Trending',
    'Action Movies': "Friend's Recommendations",
    'Comedy Movies': 'Newly Released'
  };

  return (
    <div className="min-h-screen bg-fire-darker">
      {/* Hero Slider */}
      <HeroSlider />

      {/* Apps Row */}
      <AppsRow />

      {/* Movie Rows */}
      <div className="space-y-12 pb-20">
        {Object.entries(movieCategories).map(([originalTitle, movies]) => {
          const displayTitle = categoryMapping[originalTitle] || originalTitle;
          return (
            <MovieRow key={originalTitle} title={displayTitle} movies={movies} />
          );
        })}
      </div>
    </div>
  );
};

export default HomePage;

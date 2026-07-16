import React from 'react';
import MovieRow from './MovieRow';
import HeroSlider from './HeroSlider';
import AppsRow from './AppsRow';
import { useHomeRows } from '../api/hooks';

const HomePage = () => {
  const { rows, isLive, isLoading } = useHomeRows();

  return (
    <div className="min-h-screen bg-fire-darker">
      {/* Hero Slider */}
      <HeroSlider />

      {/* Apps Row */}
      <AppsRow />

      {/* Movie Rows */}
      <div className="space-y-12 pb-20">
        {isLoading ? (
          <div className="px-8 space-y-4">
            <div className="h-6 w-64 bg-fire-gray/40 rounded animate-pulse" />
            <div className="flex space-x-4">
              {Array.from({ length: 6 }).map((_, i) => (
                <div key={i} className="w-40 h-56 bg-fire-gray/30 rounded-lg animate-pulse" />
              ))}
            </div>
          </div>
        ) : (
          rows.map((row) => <MovieRow key={row.key} title={row.title} movies={row.movies} />)
        )}
        {!isLive && !isLoading && (
          <p className="px-8 text-xs text-gray-500">
            Showing the built-in demo catalog — start the backend for live AI recommendations.
          </p>
        )}
      </div>
    </div>
  );
};

export default HomePage;

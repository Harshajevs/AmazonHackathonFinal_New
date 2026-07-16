
import React from 'react';
import { Clock, ArrowLeft } from 'lucide-react';
import { useApp } from '../contexts/AppContext';
import { movieData } from '../data/movieData';
import MovieCard from './MovieCard';

interface RecentApp {
  id: string;
  name: string;
  icon: string;
  color: string;
  lastUsed: string;
  imageName: string;
}

const recentApps: RecentApp[] = [
  { id: 'netflix', name: 'Netflix', icon: '🎬', color: 'bg-red-600', lastUsed: '2 hours ago', imageName: 'netflix' },
  { id: 'prime', name: 'Prime Video', icon: '📺', color: 'bg-blue-600', lastUsed: '5 hours ago', imageName: 'prime-video' },
  { id: 'youtube', name: 'YouTube', icon: '📹', color: 'bg-red-500', lastUsed: '1 day ago', imageName: 'youtube' },
  { id: 'hotstar', name: 'Hotstar', icon: '⭐', color: 'bg-purple-600', lastUsed: '2 days ago', imageName: 'hotstar' },
  { id: 'aha', name: 'Aha', icon: '🎭', color: 'bg-orange-600', lastUsed: '3 days ago', imageName: 'aha' }
];

const recentMovies = movieData.slice(0, 12).map((movie, index) => ({
  ...movie,
  watchedAt: index === 0 ? '30 minutes ago' : 
            index === 1 ? '2 hours ago' : 
            index === 2 ? 'Yesterday' : 
            index < 6 ? '2 days ago' : 
            '1 week ago',
  progress: index === 0 ? 85 : index === 1 ? 100 : index === 2 ? 45 : Math.floor(Math.random() * 100)
}));

const HistoryPage = () => {
  const { setCurrentPage, setSelectedPlatform, setSelectedMovie } = useApp();

  const handleAppClick = (app: RecentApp) => {
    setSelectedPlatform(app.name);
    setCurrentPage('platform');
  };

  return (
    <div className="min-h-screen bg-fire-darker p-8 overflow-hidden">
      <div className="max-w-7xl mx-auto h-full">
        <h1 className="text-4xl font-bold text-white mb-8">History</h1>
        
        {/* Recent Apps */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6">Recent Apps</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-6">
            {recentApps.map((app) => (
              <div
                key={app.id}
                className="cursor-pointer group"
                onClick={() => handleAppClick(app)}
              >
                <div
                  className="w-full h-32 rounded-xl overflow-hidden relative transition-all duration-300 group-hover:scale-105 group-hover:shadow-2xl"
                  style={{
                    backgroundImage: `url(/images/${app.imageName}.png)`,
                    backgroundSize: 'cover',
                    backgroundPosition: 'center',
                    backgroundColor: app.color
                  }}
                >
                  <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
                  <div className="absolute bottom-2 left-2 bg-black/70 text-white text-xs px-2 py-1 rounded flex items-center space-x-1">
                    <Clock size={12} />
                    <span>{app.lastUsed}</span>
                  </div>
                </div>
                <p className="text-white text-sm mt-2 font-medium">{app.name}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Movies */}
        <div className="pb-8">
          <h2 className="text-2xl font-bold text-white mb-6">Recent Movies</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-6 gap-6">
            {recentMovies.map((movie) => (
              <div key={movie.id} className="relative">
                <MovieCard movie={movie} size="small" />
                <div className="absolute top-2 left-2 bg-black/70 text-white text-xs px-2 py-1 rounded font-bold">
                  {movie.platform}
                </div>
                <div className="absolute bottom-2 left-2 bg-black/70 text-white text-xs px-2 py-1 rounded flex items-center space-x-1">
                  <Clock size={12} />
                  <span>{movie.watchedAt}</span>
                </div>
                {movie.progress > 0 && movie.progress < 100 && (
                  <div className="absolute bottom-8 left-2 right-2">
                    <div className="w-full bg-gray-600 rounded-full h-1 mb-1">
                      <div 
                        className="bg-fire-orange h-1 rounded-full transition-all duration-300"
                        style={{ width: `${movie.progress}%` }}
                      ></div>
                    </div>
                    <p className="text-white text-xs">{movie.progress}% watched</p>
                  </div>
                )}
                {movie.progress === 100 && (
                  <div className="absolute top-2 right-2 bg-green-500 text-white text-xs px-2 py-1 rounded">
                    ✓ Watched
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default HistoryPage;

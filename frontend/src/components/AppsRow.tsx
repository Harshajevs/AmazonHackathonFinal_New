
import React, { useRef, useState } from 'react';
import { ChevronLeft, ChevronRight } from 'lucide-react';
import { useApp } from '../contexts/AppContext';
import AppSplashScreen from './AppSplashScreen';

interface App {
  id: string;
  name: string;
  color: string;
  imageName: string;
  platform?: string;
}

const apps: App[] = [
  { id: 'prime', name: 'Prime Video', color: 'bg-blue-600', imageName: 'prime-video', platform: 'Prime Video' },
  { id: 'hotstar', name: 'Hotstar', color: 'bg-purple-600', imageName: 'hotstar', platform: 'Hotstar' },
  { id: 'aha', name: 'Aha', color: 'bg-orange-600', imageName: 'aha', platform: 'Aha' },
  { id: 'netflix', name: 'Netflix', color: 'bg-red-600', imageName: 'netflix', platform: 'Netflix' },
  { id: 'youtube', name: 'YouTube', color: 'bg-red-500', imageName: 'youtube' },
  { id: 'spotify', name: 'Spotify', color: 'bg-green-500', imageName: 'spotify' },
  { id: 'zee5', name: 'Zee5', color: 'bg-purple-700', imageName: 'zee5', platform: 'Zee5' },
  { id: 'sonyliv', name: 'SonyLIV', color: 'bg-blue-800', imageName: 'sonyliv', platform: 'SonyLIV' },
  { id: 'voot', name: 'Voot', color: 'bg-orange-500', imageName: 'voot', platform: 'Voot' },
  { id: 'appletv', name: 'Apple TV', color: 'bg-gray-800', imageName: 'appletv', platform: 'Apple TV' },
  { id: 'mxplayer', name: 'MX Player', color: 'bg-blue-500', imageName: 'mxplayer', platform: 'MX Player' },
  { id: 'jiocinema', name: 'JioCinema', color: 'bg-purple-800', imageName: 'jiocinema', platform: 'JioCinema' },
  { id: 'erosnow', name: 'Eros Now', color: 'bg-red-700', imageName: 'erosnow', platform: 'Eros Now' },
  { id: 'altbalaji', name: 'ALTBalaji', color: 'bg-yellow-600', imageName: 'altbalaji', platform: 'ALTBalaji' },
  { id: 'discovery', name: 'Discovery+', color: 'bg-blue-400', imageName: 'discovery', platform: 'Discovery+' }
];

const AppsRow = () => {
  const scrollRef = useRef<HTMLDivElement>(null);
  const { setCurrentPage, setSelectedPlatform } = useApp();
  const [showSplash, setShowSplash] = useState(false);
  const [selectedApp, setSelectedApp] = useState<App | null>(null);

  const scroll = (direction: 'left' | 'right') => {
    if (scrollRef.current) {
      const scrollAmount = 400;
      scrollRef.current.scrollBy({
        left: direction === 'left' ? -scrollAmount : scrollAmount,
        behavior: 'smooth'
      });
    }
  };

  const handleAppClick = (app: App) => {
    setSelectedApp(app);
    setShowSplash(true);
  };

  const handleSplashComplete = () => {
    setShowSplash(false);
    if (selectedApp && selectedApp.platform) {
      setSelectedPlatform(selectedApp.platform);
      setCurrentPage('platform');
    }
    setSelectedApp(null);
  };

  return (
    <div className="mb-8">
      <h2 className="text-2xl font-bold text-white mb-4 px-8">Apps</h2>
      <div className="relative group">
        <button
          onClick={() => scroll('left')}
          className="absolute left-2 top-1/2 -translate-y-1/2 z-10 w-12 h-12 bg-black/50 hover:bg-black/70 text-white rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300"
        >
          <ChevronLeft size={24} />
        </button>
        
        <div
          ref={scrollRef}
          className="flex space-x-6 overflow-x-auto scrollbar-hide px-8 pb-4"
          style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
        >
          {apps.map((app) => (
            <div
              key={app.id}
              className="flex-shrink-0 cursor-pointer group"
              onClick={() => handleAppClick(app)}
            >
              <div
                className="w-72 h-40 rounded-xl overflow-hidden relative transition-all duration-300 group-hover:scale-105 group-hover:shadow-2xl"
                style={{
                  backgroundImage: `url(/images/${app.imageName}.png)`,
                  backgroundSize: 'cover',
                  backgroundPosition: 'center',
                  backgroundColor: app.color
                }}
              >
                {/* Hover overlay */}
                <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
              </div>
              <p className="text-white text-lg text-center mt-3 font-medium truncate max-w-72">
                {app.name}
              </p>
            </div>
          ))}
        </div>

        <button
          onClick={() => scroll('right')}
          className="absolute right-2 top-1/2 -translate-y-1/2 z-10 w-12 h-12 bg-black/50 hover:bg-black/70 text-white rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 transition-all duration-300"
        >
          <ChevronRight size={24} />
        </button>
      </div>

      {/* App Splash Screen */}
      {showSplash && selectedApp && (
        <AppSplashScreen
          appImage={selectedApp.imageName}
          onComplete={handleSplashComplete}
        />
      )}
    </div>
  );
};

export default AppsRow;

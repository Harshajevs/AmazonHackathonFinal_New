
import React, { useState } from 'react';
import { useApp } from '../contexts/AppContext';
import AppSplashScreen from './AppSplashScreen';

interface App {
  id: string;
  name: string;
  color: string;
  imageName: string;
  platform?: string;
}

const allApps: App[] = [
  { id: 'hotstar', name: 'Hotstar', color: 'bg-purple-600', imageName: 'hotstar', platform: 'Hotstar' },
  { id: 'aha', name: 'Aha', color: 'bg-orange-600', imageName: 'aha', platform: 'Aha' },
  { id: 'netflix', name: 'Netflix', color: 'bg-red-600', imageName: 'netflix', platform: 'Netflix' },
  { id: 'youtube', name: 'YouTube', color: 'bg-red-500', imageName: 'youtube' },
  { id: 'spotify', name: 'Spotify', color: 'bg-green-500', imageName: 'spotify' },
  { id: 'zee5', name: 'Zee5', color: 'bg-purple-700', imageName: 'zee5', platform: 'Zee5' },
  { id: 'sonyliv', name: 'SonyLIV', color: 'bg-blue-800', imageName: 'sonyliv', platform: 'SonyLIV' },
  { id: 'prime', name: 'Prime Video', color: 'bg-blue-600', imageName: 'prime-video', platform: 'Prime Video' },
  { id: 'voot', name: 'Voot', color: 'bg-orange-500', imageName: 'voot', platform: 'Voot' },
  { id: 'appletv', name: 'Apple TV', color: 'bg-gray-800', imageName: 'appletv', platform: 'Apple TV' },
  { id: 'mxplayer', name: 'MX Player', color: 'bg-blue-500', imageName: 'mxplayer', platform: 'MX Player' },
  { id: 'jiocinema', name: 'JioCinema', color: 'bg-purple-800', imageName: 'jiocinema', platform: 'JioCinema' },
  { id: 'erosnow', name: 'Eros Now', color: 'bg-red-700', imageName: 'erosnow', platform: 'Eros Now' },
  { id: 'altbalaji', name: 'ALTBalaji', color: 'bg-yellow-600', imageName: 'altbalaji', platform: 'ALTBalaji' },
  { id: 'discovery', name: 'Discovery+', color: 'bg-blue-400', imageName: 'discovery', platform: 'Discovery+' }
];

const AppsPage = () => {
  const { setCurrentPage, setSelectedPlatform } = useApp();
  const [showSplash, setShowSplash] = useState(false);
  const [selectedApp, setSelectedApp] = useState<App | null>(null);

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
    <div className="min-h-screen bg-fire-darker p-8">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-8">Apps</h1>
        
        <div className="grid grid-cols-4 gap-8">
          {allApps.map((app) => (
            <div
              key={app.id}
              className="cursor-pointer group"
              onClick={() => handleAppClick(app)}
            >
              <div
                className="w-full h-40 rounded-xl overflow-hidden relative transition-all duration-300 group-hover:scale-105 group-hover:shadow-2xl"
                style={{
                  backgroundImage: `url(/images/${app.imageName}.png)`,
                  backgroundSize: 'cover',
                  backgroundPosition: 'center',
                  backgroundColor: app.color
                }}
              >
                <div className="absolute inset-0 bg-black/20 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
              </div>
              <p className="text-white text-center mt-3 font-medium group-hover:text-fire-orange transition-colors">
                {app.name}
              </p>
            </div>
          ))}
        </div>
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

export default AppsPage;

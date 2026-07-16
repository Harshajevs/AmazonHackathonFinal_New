
import React, { useState } from 'react';
import { Home, Search, Grid3X3, Settings, Menu, Smartphone } from 'lucide-react';
import { useApp } from '../contexts/AppContext';
import ProfileMenu from './ProfileMenu';

const Navigation = () => {
  const { currentPage, setCurrentPage, isInRoom, setIsInRoom } = useApp();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);

  const navItems = [
    { id: 'home', label: 'Home', icon: Home },
    { id: 'search', label: 'Search', icon: Search },
    { id: 'categories', label: 'Categories', icon: Grid3X3 },
    { id: 'apps', label: 'Apps', icon: Smartphone },
    { id: 'settings', label: 'Settings', icon: Settings }
  ];

  const dropdownItems = [
    { id: 'apps', label: 'Apps' },
    { id: 'games', label: 'Games' },
    { id: 'create-room', label: 'Create a Room' },
    { id: 'join-room', label: 'Join a Room' },
    { id: 'mylist', label: 'Playlists' },
    { id: 'subscriptions', label: 'Subscriptions' },
    { id: 'history', label: 'History' },
    { id: 'friends', label: 'Friends' },
    { id: 'dashboard', label: 'Dashboard' },
    { id: 'settings', label: 'Settings' }
  ];

  const handleNavClick = (pageId: string) => {
    if (isInRoom && pageId !== 'home') {
      setIsInRoom(false);
    }
    setCurrentPage(pageId);
    setIsDropdownOpen(false);
  };

  const handleDropdownItemClick = (itemId: string) => {
    handleNavClick(itemId);
  };

  return (
    <>
      {/* Dropdown Overlay */}
      {isDropdownOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={() => setIsDropdownOpen(false)}
        />
      )}

      <nav className="flex items-center justify-between px-8 py-4 bg-fire-dark/90 backdrop-blur-md border-b border-fire-gray/30 relative z-50">
        <div className="flex items-center space-x-8">
          <div className="flex items-center space-x-4">
            {/* Single Hamburger Menu */}
            <div className="relative">
              <button
                onClick={() => setIsDropdownOpen(!isDropdownOpen)}
                className="flex items-center space-x-1 text-gray-300 hover:text-white transition-colors duration-200"
              >
                <Menu size={20} />
              </button>

              {/* Dropdown Menu */}
              {isDropdownOpen && (
                <div className="absolute top-12 left-0 w-64 bg-black rounded-lg shadow-lg border border-fire-gray/30 z-50">
                  <div className="py-2">
                    {dropdownItems.map((item) => (
                      <button
                        key={item.id}
                        onClick={() => handleDropdownItemClick(item.id)}
                        className="w-full px-4 py-3 text-left text-white hover:bg-fire-orange/20 hover:text-fire-orange transition-colors duration-200"
                      >
                        {item.label}
                      </button>
                    ))}
                  </div>
                </div>
              )}
            </div>

            <div className="text-2xl font-bold text-gradient">
              Fire TV
            </div>
          </div>
          
          <div className="hidden md:flex items-center space-x-6">
            {navItems.map((item) => {
              const Icon = item.icon;
              return (
                <button
                  key={item.id}
                  onClick={() => handleNavClick(item.id)}
                  className={`nav-glow flex items-center space-x-2 px-4 py-2 rounded-lg transition-all duration-300 hover:bg-fire-gray/50 ${
                    currentPage === item.id ? 'active text-fire-orange' : 'text-gray-300 hover:text-white'
                  }`}
                >
                  <Icon size={20} />
                  <span className="hidden lg:block">{item.label}</span>
                </button>
              );
            })}
          </div>
        </div>

        <div className="flex items-center space-x-4">
          {isInRoom && (
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2 text-fire-orange">
                <div className="w-2 h-2 bg-fire-orange rounded-full animate-pulse"></div>
                <span className="text-sm font-medium">Live Session</span>
              </div>
              <button
                onClick={() => setIsInRoom(false)}
                className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors duration-200"
              >
                Leave Room
              </button>
            </div>
          )}
          <ProfileMenu />
        </div>
      </nav>
    </>
  );
};

export default Navigation;

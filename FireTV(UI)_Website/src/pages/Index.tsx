
import React from 'react';
import { AppProvider, useApp } from '../contexts/AppContext';
import Navigation from '../components/Navigation';
import HomePage from '../components/HomePage';
import MovieDetail from '../components/MovieDetail';
import WatchParty from '../components/WatchParty';
import SearchPage from '../components/SearchPage';
import CategoriesPage from '../components/CategoriesPage';
import MyListPage from '../components/MyListPage';
import CreateRoomPage from '../components/CreateRoomPage';
import JoinRoomPage from '../components/JoinRoomPage';
import SettingsPage from '../components/SettingsPage';
import AppsPage from '../components/AppsPage';
import GamesPage from '../components/GamesPage';
import SubscriptionsPage from '../components/SubscriptionsPage';
import PlaylistsPage from '../components/PlaylistsPage';
import HistoryPage from '../components/HistoryPage';
import DashboardPage from '../components/DashboardPage';
import PlatformPage from '../components/PlatformPage';
import FriendsPage from '../components/FriendsPage';

const AppContent = () => {
  const { currentPage, isInRoom } = useApp();

  const renderPage = () => {
    if (isInRoom || currentPage === 'room') {
      return <WatchParty />;
    }

    switch (currentPage) {
      case 'home':
        return <HomePage />;
      case 'detail':
        return <MovieDetail />;
      case 'search':
        return <SearchPage />;
      case 'categories':
        return <CategoriesPage />;
      case 'mylist':
        return <MyListPage />;
      case 'create-room':
        return <CreateRoomPage />;
      case 'join-room':
        return <JoinRoomPage />;
      case 'settings':
        return <SettingsPage />;
      case 'apps':
        return <AppsPage />;
      case 'games':
        return <GamesPage />;
      case 'subscriptions':
        return <SubscriptionsPage />;
      case 'playlists':
        return <PlaylistsPage />;
      case 'history':
        return <HistoryPage />;
      case 'friends':
        return <FriendsPage />;
      case 'dashboard':
        return <DashboardPage />;
      case 'platform':
        return <PlatformPage />;
      default:
        return <HomePage />;
    }
  };

  return (
    <div className="min-h-screen bg-fire-darker">
      {(!isInRoom && currentPage !== 'room') && <Navigation />}
      {renderPage()}
    </div>
  );
};

const Index = () => {
  return (
    <AppProvider>
      <AppContent />
    </AppProvider>
  );
};

export default Index;

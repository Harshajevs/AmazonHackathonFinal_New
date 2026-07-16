import React, { useState } from 'react';
import { UserPlus, Users, Search, MoreHorizontal, Check, X, Play, Plus, Calendar } from 'lucide-react';
import { Movie } from '../types/Movie';
import { useApp } from '../contexts/AppContext';
import MovieCard from './MovieCard';

interface Friend {
  id: string;
  name: string;
  avatar: string;
  status: 'online' | 'offline' | 'watching';
  mutualFriends: number;
  currentlyWatching?: string;
}

interface FriendRequest {
  id: string;
  name: string;
  avatar: string;
  mutualFriends: number;
  requestType: 'incoming' | 'suggestion';
}

interface MovieSuggestion {
  id: string;
  movie: Movie;
  suggestedBy: string;
  suggestedByAvatar: string;
  message?: string;
  timestamp: Date;
}

const FriendsPage = () => {
  const [activeTab, setActiveTab] = useState<'friends' | 'requests' | 'suggestions' | 'movies'>('friends');
  const [searchTerm, setSearchTerm] = useState('');
  const { setSelectedMovie, setCurrentPage, addToQueue, addToPlaylist, createPlaylist, playlists } = useApp();

  const friends: Friend[] = [
    { id: '1', name: 'Manasa', avatar: '👩‍🦰', status: 'online', mutualFriends: 12, currentlyWatching: 'Stranger Things' },
    { id: '2', name: 'Rohith', avatar: '👨‍💼', status: 'watching', mutualFriends: 8, currentlyWatching: 'The Crown' },
    { id: '3', name: 'Maruthi', avatar: '👩‍🎨', status: 'offline', mutualFriends: 15 },
    { id: '4', name: 'Harsha', avatar: '👨‍🚀', status: 'online', mutualFriends: 6 },
    { id: '5', name: 'Suhasini', avatar: '👩‍💻', status: 'watching', mutualFriends: 20, currentlyWatching: 'Breaking Bad' }
  ];

  const friendRequests: FriendRequest[] = [
    { id: '6', name: 'Varshith', avatar: '👨‍🔬', mutualFriends: 3, requestType: 'incoming' },
    { id: '7', name: 'Akash', avatar: '👩‍🏫', mutualFriends: 7, requestType: 'incoming' }
  ];

  const friendSuggestions: FriendRequest[] = [
    { id: '8', name: 'Goutham', avatar: '👨‍🎓', mutualFriends: 5, requestType: 'suggestion' },
    { id: '9', name: 'Viswateja', avatar: '👩‍⚕️', mutualFriends: 9, requestType: 'suggestion' },
    { id: '10', name: 'Prathvik', avatar: '👨‍🎨', mutualFriends: 4, requestType: 'suggestion' }
  ];

  const movieSuggestions: MovieSuggestion[] = [
    {
      id: '1',
      movie: {
        id: 'suggestion1',
        title: 'Stranger Things',
        description: 'A sci-fi horror series',
        genre: ['Sci-Fi', 'Horror'],
        duration: '50min',
        rating: '8.7',
        year: 2016,
        image: '/images/image1.png',
        platform: 'Netflix'
      },
      suggestedBy: 'Manasa',
      suggestedByAvatar: '👩‍🦰',
      message: 'You have to watch this!',
      timestamp: new Date('2024-06-20')
    },
    {
      id: '2',
      movie: {
        id: 'suggestion2',
        title: 'The Crown',
        description: 'British royal family drama',
        genre: ['Drama', 'Biography'],
        duration: '60min',
        rating: '8.6',
        year: 2016,
        image: '/images/image2.png',
        platform: 'Netflix'
      },
      suggestedBy: 'Rohith',
      suggestedByAvatar: '👨‍💼',
      message: 'Perfect historical drama!',
      timestamp: new Date('2024-06-19')
    },
    {
      id: '3',
      movie: {
        id: 'suggestion3',
        title: 'The Family Man',
        description: 'Indian spy thriller series',
        genre: ['Thriller', 'Action'],
        duration: '45min',
        rating: '8.9',
        year: 2019,
        image: '/images/image3.png',
        platform: 'Prime Video'
      },
      suggestedBy: 'Harsha',
      suggestedByAvatar: '👨‍🚀',
      timestamp: new Date('2024-06-18')
    }
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'online': return 'bg-green-500';
      case 'watching': return 'bg-fire-orange';
      case 'offline': return 'bg-gray-500';
      default: return 'bg-gray-500';
    }
  };

  const filteredFriends = friends.filter(friend =>
    friend.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const handlePlayMovie = (movie: Movie) => {
    setSelectedMovie(movie);
    setCurrentPage('detail');
  };

  const handleCreateRoom = (movie: Movie) => {
    setSelectedMovie(movie);
    setCurrentPage('create-room');
  };

  return (
    <div className="min-h-screen bg-fire-darker text-white p-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gradient mb-4">Friends</h1>
          <div className="flex items-center space-x-6">
            <button
              onClick={() => setActiveTab('friends')}
              className={`px-6 py-3 rounded-lg font-medium transition-all ${
                activeTab === 'friends' ? 'bg-fire-orange text-white' : 'bg-fire-gray text-gray-300 hover:bg-fire-gray/70'
              }`}
            >
              <Users className="inline mr-2" size={20} />
              My Friends ({friends.length})
            </button>
            <button
              onClick={() => setActiveTab('requests')}
              className={`px-6 py-3 rounded-lg font-medium transition-all ${
                activeTab === 'requests' ? 'bg-fire-orange text-white' : 'bg-fire-gray text-gray-300 hover:bg-fire-gray/70'
              }`}
            >
              <UserPlus className="inline mr-2" size={20} />
              Requests ({friendRequests.length})
            </button>
            <button
              onClick={() => setActiveTab('suggestions')}
              className={`px-6 py-3 rounded-lg font-medium transition-all ${
                activeTab === 'suggestions' ? 'bg-fire-orange text-white' : 'bg-fire-gray text-gray-300 hover:bg-fire-gray/70'
              }`}
            >
              Suggestions ({friendSuggestions.length})
            </button>
            <button
              onClick={() => setActiveTab('movies')}
              className={`px-6 py-3 rounded-lg font-medium transition-all ${
                activeTab === 'movies' ? 'bg-fire-orange text-white' : 'bg-fire-gray text-gray-300 hover:bg-fire-gray/70'
              }`}
            >
              Movie Suggestions ({movieSuggestions.length})
            </button>
          </div>
        </div>

        {/* Search Bar (only for friends tab) */}
        {activeTab === 'friends' && (
          <div className="mb-6">
            <div className="relative max-w-md">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
              <input
                type="text"
                placeholder="Search friends..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-3 bg-fire-gray border border-fire-gray/50 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-fire-orange"
              />
            </div>
          </div>
        )}

        {/* Content */}
        {activeTab === 'friends' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredFriends.map((friend) => (
              <div key={friend.id} className="bg-fire-dark rounded-xl p-6 hover:bg-fire-gray/50 transition-all duration-300">
                <div className="flex items-center justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <div className="relative">
                      <div className="w-12 h-12 bg-fire-gray rounded-full flex items-center justify-center text-2xl">
                        {friend.avatar}
                      </div>
                      <div className={`absolute -bottom-1 -right-1 w-4 h-4 ${getStatusColor(friend.status)} rounded-full border-2 border-fire-dark`}></div>
                    </div>
                    <div>
                      <h3 className="font-semibold text-lg">{friend.name}</h3>
                      <p className="text-gray-400 text-sm">{friend.mutualFriends} mutual friends</p>
                    </div>
                  </div>
                  <button className="p-2 hover:bg-fire-gray/50 rounded-lg transition-colors">
                    <MoreHorizontal size={20} className="text-gray-400" />
                  </button>
                </div>
                
                {friend.currentlyWatching && (
                  <div className="bg-fire-orange/20 rounded-lg p-3 mb-4">
                    <p className="text-fire-orange text-sm font-medium">Currently watching</p>
                    <p className="text-white">{friend.currentlyWatching}</p>
                  </div>
                )}
                
                <div className="flex space-x-2">
                  <button className="flex-1 px-4 py-2 bg-fire-orange text-white rounded-lg hover:bg-fire-orange/80 transition-colors">
                    Message
                  </button>
                  <button className="flex-1 px-4 py-2 bg-fire-gray text-white rounded-lg hover:bg-fire-gray/70 transition-colors">
                    Profile
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'requests' && (
          <div className="space-y-4">
            {friendRequests.map((request) => (
              <div key={request.id} className="bg-fire-dark rounded-xl p-6 flex items-center justify-between">
                <div className="flex items-center space-x-4">
                  <div className="w-16 h-16 bg-fire-gray rounded-full flex items-center justify-center text-3xl">
                    {request.avatar}
                  </div>
                  <div>
                    <h3 className="font-semibold text-xl">{request.name}</h3>
                    <p className="text-gray-400">{request.mutualFriends} mutual friends</p>
                  </div>
                </div>
                <div className="flex space-x-3">
                  <button className="px-6 py-2 bg-fire-orange text-white rounded-lg hover:bg-fire-orange/80 transition-colors flex items-center space-x-2">
                    <Check size={18} />
                    <span>Accept</span>
                  </button>
                  <button className="px-6 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors flex items-center space-x-2">
                    <X size={18} />
                    <span>Decline</span>
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'suggestions' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {friendSuggestions.map((suggestion) => (
              <div key={suggestion.id} className="bg-fire-dark rounded-xl p-6 text-center">
                <div className="w-20 h-20 bg-fire-gray rounded-full flex items-center justify-center text-4xl mx-auto mb-4">
                  {suggestion.avatar}
                </div>
                <h3 className="font-semibold text-xl mb-2">{suggestion.name}</h3>
                <p className="text-gray-400 mb-4">{suggestion.mutualFriends} mutual friends</p>
                <div className="flex space-x-2">
                  <button className="flex-1 px-4 py-2 bg-fire-orange text-white rounded-lg hover:bg-fire-orange/80 transition-colors">
                    Add Friend
                  </button>
                  <button className="flex-1 px-4 py-2 bg-fire-gray text-white rounded-lg hover:bg-fire-gray/70 transition-colors">
                    Remove
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}

        {activeTab === 'movies' && (
          <div className="space-y-6">
            <h2 className="text-2xl font-bold text-white mb-6">Movies Suggested by Friends</h2>
            {movieSuggestions.map((suggestion) => (
              <div key={suggestion.id} className="bg-fire-dark rounded-xl p-6">
                <div className="flex items-start space-x-4 mb-4">
                  <div className="w-12 h-12 bg-fire-gray rounded-full flex items-center justify-center text-2xl">
                    {suggestion.suggestedByAvatar}
                  </div>
                  <div className="flex-1">
                    <div className="flex items-center space-x-2 mb-1">
                      <span className="font-semibold text-white">{suggestion.suggestedBy}</span>
                      <span className="text-gray-400 text-sm">suggested</span>
                    </div>
                    {suggestion.message && (
                      <p className="text-gray-300 text-sm mb-2">"{suggestion.message}"</p>
                    )}
                    <p className="text-gray-500 text-xs">
                      {suggestion.timestamp.toLocaleDateString()}
                    </p>
                  </div>
                </div>
                
                <div className="flex items-center space-x-6">
                  <div className="flex-shrink-0">
                    <MovieCard movie={suggestion.movie} size="small" />
                  </div>
                  
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-white mb-2">{suggestion.movie.title}</h3>
                    <p className="text-gray-300 mb-3">{suggestion.movie.description}</p>
                    <div className="flex items-center space-x-4 mb-4">
                      <span className="text-fire-orange">⭐ {suggestion.movie.rating}</span>
                      <span className="text-gray-400">{suggestion.movie.year}</span>
                      <span className="text-gray-400">{suggestion.movie.duration}</span>
                    </div>
                    <div className="flex space-x-3">
                      <button
                        onClick={() => handlePlayMovie(suggestion.movie)}
                        className="px-4 py-2 bg-fire-orange text-white rounded-lg hover:bg-fire-orange/80 transition-colors flex items-center space-x-2"
                      >
                        <Play size={16} />
                        <span>Play Now</span>
                      </button>
                      <button
                        onClick={() => addToQueue(suggestion.movie)}
                        className="px-4 py-2 bg-fire-gray text-white rounded-lg hover:bg-fire-gray/70 transition-colors flex items-center space-x-2"
                      >
                        <Plus size={16} />
                        <span>Add to Queue</span>
                      </button>
                      <button
                        onClick={() => handleCreateRoom(suggestion.movie)}
                        className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors flex items-center space-x-2"
                      >
                        <Calendar size={16} />
                        <span>Create Room</span>
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default FriendsPage;

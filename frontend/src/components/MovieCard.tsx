
import React, { useState } from 'react';
import { Play, Plus, Info, MoreVertical, Heart, Clock, List, Lock, Share, Users } from 'lucide-react';
import { Movie } from '../types/Movie';
import { useApp } from '../contexts/AppContext';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
  DropdownMenuSub,
  DropdownMenuSubContent,
  DropdownMenuSubTrigger,
} from './ui/dropdown-menu';

interface MovieCardProps {
  movie: Movie;
  size?: 'small' | 'medium' | 'large';
}

const MovieCard = ({ movie, size = 'medium' }: MovieCardProps) => {
  const { 
    setSelectedMovie, 
    setCurrentPage, 
    addToQueue, 
    addToWishlist, 
    addToWatchLater,
    playlists,
    createPlaylist,
    addToPlaylist 
  } = useApp();
  const [showCreatePlaylist, setShowCreatePlaylist] = useState(false);
  const [showSubscriptionModal, setShowSubscriptionModal] = useState(false);
  const [showRecommendModal, setShowRecommendModal] = useState(false);
  const [newPlaylistName, setNewPlaylistName] = useState('');
  const [selectedFriends, setSelectedFriends] = useState<string[]>([]);

  const sizeClasses = {
    small: 'w-48 h-72',
    medium: 'w-56 h-80',
    large: 'w-64 h-96'
  };

  const platformColors = {
    'Netflix': 'bg-red-600',
    'Prime Video': 'bg-blue-600',
    'Hotstar': 'bg-gradient-to-r from-pink-500 to-purple-600',
    'Aha': 'bg-orange-600',
    'SonyLiv': 'bg-violet-600'
  };

  // Predefined friends list
  const friends = [
    { id: '1', name: 'Manasa', avatar: '👩' },
    { id: '2', name: 'Maruthi', avatar: '👨' },
    { id: '3', name: 'Suhasini', avatar: '👩‍🦱' },
    { id: '4', name: 'Harsha', avatar: '👨‍🦲' },
    { id: '5', name: 'Rohith', avatar: '🧑' },
    { id: '6', name: 'Varshith', avatar: '👦' },
    { id: '7', name: 'Hareesh', avatar: '👨' }
  ];

  const isLocked = movie.id.endsWith('3') || movie.id.endsWith('7') || movie.id.endsWith('9');

  const handleMovieClick = () => {
    if (isLocked) {
      setShowSubscriptionModal(true);
      return;
    }
    setSelectedMovie(movie);
    setCurrentPage('detail');
  };

  const handlePlayNow = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (isLocked) {
      setShowSubscriptionModal(true);
      return;
    }
    console.log('Playing movie:', movie.title);
    setSelectedMovie(movie);
    setCurrentPage('detail');
  };

  const handleAddToQueue = (e: React.MouseEvent) => {
    e.stopPropagation();
    if (isLocked) {
      setShowSubscriptionModal(true);
      return;
    }
    console.log('Adding to queue:', movie.title);
    addToQueue(movie);
  };

  const handleCreatePlaylist = () => {
    if (newPlaylistName.trim()) {
      createPlaylist(newPlaylistName);
      addToPlaylist(newPlaylistName, movie);
      console.log('Created playlist and added movie:', newPlaylistName, movie.title);
      setNewPlaylistName('');
      setShowCreatePlaylist(false);
    }
  };

  const handleAddToExistingPlaylist = (playlistId: string) => {
    addToPlaylist(playlistId, movie);
    console.log('Added movie to playlist:', playlistId, movie.title);
  };

  const handleSuggestToFriend = () => {
    if (selectedFriends.length > 0) {
      console.log('Suggesting', movie.title, 'to:', selectedFriends.map(id => friends.find(f => f.id === id)?.name));
      // Here you would typically send the suggestion to your backend
      setShowRecommendModal(false);
      setSelectedFriends([]);
    }
  };

  const toggleFriendSelection = (friendId: string) => {
    setSelectedFriends(prev => 
      prev.includes(friendId) 
        ? prev.filter(id => id !== friendId)
        : [...prev, friendId]
    );
  };

  return (
    <div className={`${sizeClasses[size]} relative group movie-card-hover cursor-pointer flex-shrink-0`}>
      <div 
        className="w-full h-full rounded-xl overflow-hidden bg-fire-gray relative"
        onClick={handleMovieClick}
      >
        <img 
          src={movie.image} 
          alt={movie.title}
          className={`w-full h-full object-cover ${isLocked ? 'opacity-50' : ''}`}
        />
        
        {/* Platform badge */}
        <div className={`absolute top-2 left-2 px-2 py-1 ${platformColors[movie.platform]} text-white text-xs font-bold rounded-full z-10`}>
          {movie.platform}
        </div>

        {/* Lock overlay */}
        {isLocked && (
          <div className="absolute inset-0 bg-black/30 flex items-center justify-center">
            <div className="w-16 h-16 bg-black/70 rounded-full flex items-center justify-center">
              <Lock size={32} className="text-white" />
            </div>
          </div>
        )}

        {/* Three dots menu */}
        <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity duration-300 z-20" onClick={(e) => e.stopPropagation()}>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <button className="w-8 h-8 bg-black/70 hover:bg-black/90 text-white rounded-full flex items-center justify-center">
                <MoreVertical size={16} />
              </button>
            </DropdownMenuTrigger>
            <DropdownMenuContent className="bg-fire-dark border-fire-gray text-white">
              <DropdownMenuItem onClick={handlePlayNow} className="hover:bg-fire-gray/50">
                <Play className="mr-2 h-4 w-4" />
                Play Now
              </DropdownMenuItem>
              <DropdownMenuSeparator className="bg-fire-gray/30" />
              <DropdownMenuItem onClick={handleAddToQueue} className="hover:bg-fire-gray/50">
                <Plus className="mr-2 h-4 w-4" />
                Add to Queue
              </DropdownMenuItem>
              <DropdownMenuSeparator className="bg-fire-gray/30" />
              <DropdownMenuSub>
                <DropdownMenuSubTrigger className="hover:bg-fire-gray/50">
                  <List className="mr-2 h-4 w-4" />
                  Add to Playlist
                </DropdownMenuSubTrigger>
                <DropdownMenuSubContent className="bg-fire-dark border-fire-gray text-white">
                  <DropdownMenuItem onClick={() => setShowCreatePlaylist(true)} className="hover:bg-fire-gray/50">
                    Create New Playlist
                  </DropdownMenuItem>
                  {playlists.length > 0 && <DropdownMenuSeparator className="bg-fire-gray/30" />}
                  {playlists.map((playlist) => (
                    <DropdownMenuItem 
                      key={playlist.id}
                      onClick={() => handleAddToExistingPlaylist(playlist.id)}
                      className="hover:bg-fire-gray/50"
                    >
                      {playlist.name}
                    </DropdownMenuItem>
                  ))}
                </DropdownMenuSubContent>
              </DropdownMenuSub>
              <DropdownMenuSeparator className="bg-fire-gray/30" />
              <DropdownMenuItem onClick={() => setShowRecommendModal(true)} className="hover:bg-fire-gray/50">
                <Share className="mr-2 h-4 w-4" />
                Suggest to a Friend
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>
        
        {/* Gradient overlay */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        
        {/* Movie info overlay */}
        <div className="absolute bottom-0 left-0 right-0 p-4 text-white transform translate-y-full group-hover:translate-y-0 transition-transform duration-300">
          <h3 className="font-bold text-lg mb-1 truncate">{movie.title}</h3>
          <div className="flex items-center justify-between text-sm text-gray-300">
            <span>{movie.year}</span>
            <span className="flex items-center space-x-1">
              <span>⭐</span>
              <span>{movie.rating}</span>
            </span>
          </div>
          <div className="flex items-center space-x-1 mt-2">
            {movie.genre.slice(0, 2).map((g, i) => (
              <span key={i} className="px-2 py-1 bg-fire-orange/20 text-fire-orange text-xs rounded-full">
                {g}
              </span>
            ))}
          </div>
        </div>

        {/* Action buttons */}
        {!isLocked && (
          <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <button
              onClick={handleAddToQueue}
              className="w-12 h-12 bg-fire-orange hover:bg-fire-blue text-white rounded-full flex items-center justify-center transition-colors duration-200"
            >
              <Plus size={20} />
            </button>
          </div>
        )}

        {/* Featured badge */}
        {movie.featured && (
          <div className="absolute bottom-2 right-2 px-3 py-1 bg-fire-orange text-white text-xs font-bold rounded-full">
            FEATURED
          </div>
        )}
      </div>

      {/* Suggest to Friend Modal */}
      {showRecommendModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={() => setShowRecommendModal(false)}>
          <div className="bg-fire-dark p-6 rounded-xl max-w-md mx-4" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-white text-lg font-bold mb-4">Suggest "{movie.title}" to Friends</h3>
            <div className="space-y-2 mb-4 max-h-60 overflow-y-auto">
              {friends.map((friend) => (
                <label key={friend.id} className="flex items-center space-x-3 cursor-pointer p-2 hover:bg-fire-gray/30 rounded">
                  <input
                    type="checkbox"
                    checked={selectedFriends.includes(friend.id)}
                    onChange={() => toggleFriendSelection(friend.id)}
                    className="rounded"
                  />
                  <span className="text-2xl">{friend.avatar}</span>
                  <span className="text-white">{friend.name}</span>
                </label>
              ))}
            </div>
            <div className="flex space-x-4">
              <button
                onClick={handleSuggestToFriend}
                disabled={selectedFriends.length === 0}
                className="flex-1 px-4 py-2 bg-fire-orange text-white rounded-lg hover:bg-fire-orange/80 disabled:bg-gray-600 disabled:cursor-not-allowed transition-colors"
              >
                Send Suggestion
              </button>
              <button
                onClick={() => {
                  setShowRecommendModal(false);
                  setSelectedFriends([]);
                }}
                className="flex-1 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Subscription Modal */}
      {showSubscriptionModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={() => setShowSubscriptionModal(false)}>
          <div className="bg-fire-dark p-8 rounded-xl max-w-md mx-4" onClick={(e) => e.stopPropagation()}>
            <div className="text-center">
              <Lock size={48} className="text-fire-orange mx-auto mb-4" />
              <h3 className="text-white text-xl font-bold mb-4">Premium Content</h3>
              <p className="text-gray-300 mb-6">
                Please subscribe to {movie.platform} to watch "{movie.title}"
              </p>
              <div className="flex space-x-4">
                <button
                  onClick={() => setShowSubscriptionModal(false)}
                  className="flex-1 px-4 py-2 bg-fire-orange text-white rounded-lg hover:bg-fire-orange/80 transition-colors"
                >
                  Subscribe Now
                </button>
                <button
                  onClick={() => setShowSubscriptionModal(false)}
                  className="flex-1 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Create Playlist Modal */}
      {showCreatePlaylist && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={() => setShowCreatePlaylist(false)}>
          <div className="bg-fire-dark p-6 rounded-xl" onClick={(e) => e.stopPropagation()}>
            <h3 className="text-white text-lg font-bold mb-4">Create New Playlist</h3>
            <input
              type="text"
              value={newPlaylistName}
              onChange={(e) => setNewPlaylistName(e.target.value)}
              placeholder="Playlist name"
              className="w-full px-4 py-2 bg-fire-gray text-white rounded-lg mb-4"
            />
            <div className="flex space-x-4">
              <button
                onClick={handleCreatePlaylist}
                className="px-4 py-2 bg-fire-orange text-white rounded-lg"
              >
                Create & Add Movie
              </button>
              <button
                onClick={() => setShowCreatePlaylist(false)}
                className="px-4 py-2 bg-gray-600 text-white rounded-lg"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default MovieCard;

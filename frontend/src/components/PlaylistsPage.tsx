
import React, { useState } from 'react';
import { Plus, Play, Trash2, Film, Users, UserPlus } from 'lucide-react';
import { useApp } from '../contexts/AppContext';
import { movieCategories } from '../data/movieData';

const PlaylistsPage = () => {
  const { playlists, createPlaylist, addToPlaylist, removeFromPlaylist } = useApp();
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newPlaylistName, setNewPlaylistName] = useState('');
  const [selectedPlaylist, setSelectedPlaylist] = useState<string | null>(null);
  const [showMovieSelector, setShowMovieSelector] = useState(false);
  const [isSharedPlaylist, setIsSharedPlaylist] = useState(false);
  const [showAddFriends, setShowAddFriends] = useState(false);
  const [selectedFriends, setSelectedFriends] = useState<string[]>([]);

  // Get all movies from all categories
  const allMovies = Object.values(movieCategories).flat();

  // Default friends list
  const availableFriends = [
    { id: '1', name: 'Manasa', avatar: '👩' },
    { id: '2', name: 'Maruthi', avatar: '👨' },
    { id: '3', name: 'Suhasini', avatar: '👩‍🦱' },
    { id: '4', name: 'Hareesh', avatar: '👨‍🦲' },
    { id: '5', name: 'Rohith', avatar: '🧑' },
    { id: '6', name: 'Varshith', avatar: '👦' },
    { id: '7', name: 'Harsha', avatar: '🧒' }
  ];

  // Default shared playlists with default movies
  const sharedPlaylists = [
    {
      id: 'shared-1',
      name: 'Movie Night Favorites',
      movies: allMovies.slice(0, 5),
      createdAt: new Date(),
      owner: 'Rohith',
      collaborators: ['Varshith', 'Harsha']
    },
    {
      id: 'shared-2',
      name: 'Action Pack',
      movies: allMovies.slice(5, 8),
      createdAt: new Date(),
      owner: 'Varshith',
      collaborators: ['You', 'Rohith']
    }
  ];

  const handleCreatePlaylist = () => {
    if (newPlaylistName.trim()) {
      if (isSharedPlaylist) {
        // Create shared playlist with default movies and selected friends
        const defaultMovies = allMovies.slice(0, 3);
        console.log('Creating shared playlist:', newPlaylistName, 'with friends:', selectedFriends, 'and movies:', defaultMovies);
      } else {
        createPlaylist(newPlaylistName.trim());
      }
      setNewPlaylistName('');
      setShowCreateForm(false);
      setIsSharedPlaylist(false);
      setSelectedFriends([]);
    }
  };

  const handleAddMovie = (playlistId: string, movie: any) => {
    if (isSharedPlaylist) {
      console.log('Adding to shared playlist:', playlistId, movie.title);
    } else {
      addToPlaylist(playlistId, movie);
    }
    setShowMovieSelector(false);
    setSelectedPlaylist(null);
    setIsSharedPlaylist(false);
  };

  const handleAddToSharedPlaylist = (playlistId: string) => {
    setSelectedPlaylist(playlistId);
    setIsSharedPlaylist(true);
    setShowMovieSelector(true);
  };

  const toggleFriendSelection = (friendId: string) => {
    setSelectedFriends(prev => 
      prev.includes(friendId) 
        ? prev.filter(id => id !== friendId)
        : [...prev, friendId]
    );
  };

  return (
    <div className="min-h-screen bg-fire-darker p-8">
      <div className="max-w-6xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-4xl font-bold text-white">Playlists</h1>
          <div className="flex space-x-4">
            <button
              onClick={() => {
                setIsSharedPlaylist(true);
                setShowCreateForm(true);
              }}
              className="bg-fire-blue hover:bg-fire-blue/80 text-white px-6 py-3 rounded-lg flex items-center space-x-2 transition-colors"
            >
              <Users size={20} />
              <span>Create Shared Playlist</span>
            </button>
            <button
              onClick={() => {
                setIsSharedPlaylist(false);
                setShowCreateForm(true);
              }}
              className="bg-fire-orange hover:bg-fire-orange/80 text-white px-6 py-3 rounded-lg flex items-center space-x-2 transition-colors"
            >
              <Plus size={20} />
              <span>Create Playlist</span>
            </button>
          </div>
        </div>

        {/* Create Playlist Form */}
        {showCreateForm && (
          <div className="bg-fire-dark rounded-xl p-6 mb-8">
            <h3 className="text-xl font-semibold text-white mb-4">
              Create New {isSharedPlaylist ? 'Shared ' : ''}Playlist
            </h3>
            <div className="space-y-4">
              <input
                type="text"
                value={newPlaylistName}
                onChange={(e) => setNewPlaylistName(e.target.value)}
                placeholder="Enter playlist name"
                className="w-full bg-fire-gray/30 text-white px-4 py-2 rounded-lg border border-gray-600 focus:border-fire-orange outline-none"
              />
              
              {isSharedPlaylist && (
                <div>
                  <label className="text-white block mb-2">Add Friends:</label>
                  <div className="grid grid-cols-3 gap-2">
                    {availableFriends.map((friend) => (
                      <label key={friend.id} className="flex items-center space-x-2 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={selectedFriends.includes(friend.id)}
                          onChange={() => toggleFriendSelection(friend.id)}
                          className="rounded"
                        />
                        <span className="text-white text-sm">{friend.avatar} {friend.name}</span>
                      </label>
                    ))}
                  </div>
                </div>
              )}
              
              <div className="flex space-x-4">
                <button
                  onClick={handleCreatePlaylist}
                  className="bg-fire-orange hover:bg-fire-orange/80 text-white px-6 py-2 rounded-lg transition-colors"
                >
                  Create
                </button>
                <button
                  onClick={() => {
                    setShowCreateForm(false);
                    setIsSharedPlaylist(false);
                    setSelectedFriends([]);
                  }}
                  className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg transition-colors"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Movie Selector Modal */}
        {showMovieSelector && selectedPlaylist && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50">
            <div className="bg-fire-dark rounded-xl p-6 max-w-4xl w-full mx-4 max-h-[80vh] overflow-y-auto">
              <h3 className="text-xl font-semibold text-white mb-4">Add Movie to Playlist</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mb-6">
                {allMovies.map((movie) => (
                  <div
                    key={movie.id}
                    className="cursor-pointer group"
                    onClick={() => handleAddMovie(selectedPlaylist, movie)}
                  >
                    <div className="aspect-[2/3] rounded-lg overflow-hidden group-hover:scale-105 transition-transform">
                      <img
                        src={movie.image}
                        alt={movie.title}
                        className="w-full h-full object-cover"
                      />
                    </div>
                    <p className="text-white text-sm mt-2 truncate">{movie.title}</p>
                  </div>
                ))}
              </div>
              <button
                onClick={() => {
                  setShowMovieSelector(false);
                  setSelectedPlaylist(null);
                  setIsSharedPlaylist(false);
                }}
                className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        )}

        {/* My Playlists */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6">My Playlists</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {playlists.map((playlist) => (
              <div key={playlist.id} className="bg-fire-dark rounded-xl p-6 hover:bg-fire-gray/20 transition-colors">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-semibold text-white">{playlist.name}</h3>
                  <button
                    onClick={() => {
                      setSelectedPlaylist(playlist.id);
                      setIsSharedPlaylist(false);
                      setShowMovieSelector(true);
                    }}
                    className="bg-fire-orange/20 hover:bg-fire-orange/30 text-fire-orange p-2 rounded-lg transition-colors"
                  >
                    <Plus size={16} />
                  </button>
                </div>
                
                <div className="flex items-center space-x-2 text-gray-400 text-sm mb-4">
                  <Film size={16} />
                  <span>{playlist.movies.length} movies</span>
                </div>

                {playlist.movies.length > 0 ? (
                  <div className="space-y-3">
                    {playlist.movies.slice(0, 3).map((movie) => (
                      <div key={movie.id} className="flex items-center space-x-3">
                        <img
                          src={movie.image}
                          alt={movie.title}
                          className="w-12 h-16 object-cover rounded"
                        />
                        <div className="flex-1">
                          <p className="text-white text-sm font-medium truncate">{movie.title}</p>
                          <p className="text-gray-400 text-xs">{movie.year} • {movie.duration}</p>
                        </div>
                        <button
                          onClick={() => removeFromPlaylist(playlist.id, movie.id)}
                          className="text-gray-400 hover:text-red-400 transition-colors"
                        >
                          <Trash2 size={14} />
                        </button>
                      </div>
                    ))}
                    {playlist.movies.length > 3 && (
                      <p className="text-gray-400 text-sm">+{playlist.movies.length - 3} more movies</p>
                    )}
                  </div>
                ) : (
                  <p className="text-gray-400 text-sm">No movies added yet</p>
                )}

                <div className="flex space-x-2 mt-4">
                  <button className="flex-1 bg-fire-orange hover:bg-fire-orange/80 text-white py-2 px-4 rounded-lg flex items-center justify-center space-x-2 transition-colors">
                    <Play size={16} />
                    <span>Play</span>
                  </button>
                </div>
              </div>
            ))}
            
            {playlists.length === 0 && (
              <div className="col-span-full text-center py-8">
                <Film size={48} className="text-gray-600 mx-auto mb-4" />
                <h3 className="text-xl font-semibold text-white mb-2">No Playlists Yet</h3>
                <p className="text-gray-400 mb-4">Create your first playlist to organize your favorite movies</p>
                <button
                  onClick={() => setShowCreateForm(true)}
                  className="bg-fire-orange hover:bg-fire-orange/80 text-white px-6 py-3 rounded-lg transition-colors"
                >
                  Create Your First Playlist
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Shared Playlists */}
        <div>
          <h2 className="text-2xl font-bold text-white mb-6">Shared Playlists</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {sharedPlaylists.map((playlist) => (
              <div key={playlist.id} className="bg-fire-dark rounded-xl p-6 hover:bg-fire-gray/20 transition-colors border border-fire-orange/20">
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-semibold text-white">{playlist.name}</h3>
                  <button
                    onClick={() => handleAddToSharedPlaylist(playlist.id)}
                    className="bg-fire-orange/20 hover:bg-fire-orange/30 text-fire-orange p-2 rounded-lg transition-colors"
                  >
                    <Plus size={16} />
                  </button>
                </div>
                
                <div className="flex items-center space-x-4 text-gray-400 text-sm mb-4">
                  <div className="flex items-center space-x-1">
                    <Film size={16} />
                    <span>{playlist.movies.length} movies</span>
                  </div>
                  <div className="flex items-center space-x-1">
                    <Users size={16} />
                    <span>{playlist.collaborators.length + 1} members</span>
                  </div>
                </div>

                <div className="mb-4">
                  <p className="text-gray-400 text-xs mb-2">Created by {playlist.owner}</p>
                  <p className="text-gray-400 text-xs">
                    Collaborators: {playlist.collaborators.join(', ')}
                  </p>
                </div>

                {playlist.movies.length > 0 && (
                  <div className="space-y-3 mb-4">
                    {playlist.movies.slice(0, 2).map((movie) => (
                      <div key={movie.id} className="flex items-center space-x-3">
                        <img
                          src={movie.image}
                          alt={movie.title}
                          className="w-12 h-16 object-cover rounded"
                        />
                        <div className="flex-1">
                          <p className="text-white text-sm font-medium truncate">{movie.title}</p>
                          <p className="text-gray-400 text-xs">{movie.year} • {movie.duration}</p>
                        </div>
                      </div>
                    ))}
                    {playlist.movies.length > 2 && (
                      <p className="text-gray-400 text-sm">+{playlist.movies.length - 2} more movies</p>
                    )}
                  </div>
                )}

                <button className="w-full bg-fire-orange hover:bg-fire-orange/80 text-white py-2 px-4 rounded-lg flex items-center justify-center space-x-2 transition-colors">
                  <Play size={16} />
                  <span>Play</span>
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PlaylistsPage;

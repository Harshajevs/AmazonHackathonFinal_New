
import React, { useState } from 'react';
import { useApp } from '../contexts/AppContext';
import MovieCard from './MovieCard';
import { Play, Trash2, Plus, Users } from 'lucide-react';
import { movieCategories } from '../data/movieData';

// Get some default movies from the movie data
const getDefaultMovies = (count: number, offset: number = 0) => {
  const allMovies = Object.values(movieCategories).flat();
  return allMovies.slice(offset, offset + count);
};

const defaultMyPlaylists = [
  {
    id: 'my-favorites',
    name: 'My Favorites',
    movies: getDefaultMovies(4, 0),
    owner: 'You',
    isShared: false
  },
  {
    id: 'watch-tonight',
    name: 'Watch Tonight',
    movies: getDefaultMovies(3, 4),
    owner: 'You',
    isShared: false
  }
];

const defaultSharedPlaylists = [
  {
    id: 'family-night',
    name: 'Family Movie Night',
    movies: getDefaultMovies(5, 7),
    owner: 'Manasa',
    isShared: true,
    collaborators: ['You', 'Manasa', 'Harsha', 'Maruthi']
  },
  {
    id: 'weekend-binge',
    name: 'Weekend Binge Watch',
    movies: getDefaultMovies(4, 12),
    owner: 'Varshith',
    isShared: true,
    collaborators: ['You', 'Rohith', 'Varshith']
  }
];

const MyListPage = () => {
  const { wishlist, watchLater, playlists, createPlaylist, removeFromPlaylist, addToPlaylist } = useApp();
  const [showCreatePlaylist, setShowCreatePlaylist] = useState(false);
  const [newPlaylistName, setNewPlaylistName] = useState('');
  const [showAddToPlaylist, setShowAddToPlaylist] = useState(false);
  const [selectedPlaylistForAdd, setSelectedPlaylistForAdd] = useState('');
  const [selectedPlaylistData, setSelectedPlaylistData] = useState<any>(null);
  const [myPlaylists, setMyPlaylists] = useState(defaultMyPlaylists);
  const [sharedPlaylists, setSharedPlaylists] = useState(defaultSharedPlaylists);

  // Get all available movies
  const allAvailableMovies = Object.values(movieCategories).flat();

  const handleCreatePlaylist = () => {
    if (newPlaylistName.trim()) {
      createPlaylist(newPlaylistName);
      setNewPlaylistName('');
      setShowCreatePlaylist(false);
    }
  };

  const handleAddMovieToPlaylist = (movie: any) => {
    if (selectedPlaylistForAdd && selectedPlaylistData) {
      if (selectedPlaylistData.isShared) {
        // Handle shared playlist - update local state
        setSharedPlaylists(prev => 
          prev.map(playlist => 
            playlist.id === selectedPlaylistForAdd 
              ? { ...playlist, movies: [...playlist.movies, movie] }
              : playlist
          )
        );
        console.log('Added movie to shared playlist:', selectedPlaylistData.name, movie.title);
      } else if (selectedPlaylistData.owner === 'You') {
        // Handle my custom playlists - update local state
        setMyPlaylists(prev => 
          prev.map(playlist => 
            playlist.id === selectedPlaylistForAdd 
              ? { ...playlist, movies: [...playlist.movies, movie] }
              : playlist
          )
        );
        console.log('Added movie to my playlist:', selectedPlaylistData.name, movie.title);
      } else {
        // Handle regular app playlists
        addToPlaylist(selectedPlaylistForAdd, movie);
        console.log('Added movie to app playlist:', selectedPlaylistForAdd, movie.title);
      }
      setShowAddToPlaylist(false);
      setSelectedPlaylistForAdd('');
      setSelectedPlaylistData(null);
    }
  };

  const openAddMovieModal = (playlistId: string, playlistData: any) => {
    setSelectedPlaylistForAdd(playlistId);
    setSelectedPlaylistData(playlistData);
    setShowAddToPlaylist(true);
  };

  const handleRemoveFromMyPlaylist = (playlistId: string, movieId: string) => {
    setMyPlaylists(prev => 
      prev.map(playlist => 
        playlist.id === playlistId 
          ? { ...playlist, movies: playlist.movies.filter(movie => movie.id !== movieId) }
          : playlist
      )
    );
  };

  const handleRemoveFromSharedPlaylist = (playlistId: string, movieId: string) => {
    setSharedPlaylists(prev => 
      prev.map(playlist => 
        playlist.id === playlistId 
          ? { ...playlist, movies: playlist.movies.filter(movie => movie.id !== movieId) }
          : playlist
      )
    );
  };

  const allMyPlaylists = [...playlists, ...myPlaylists];

  return (
    <div className="min-h-screen bg-fire-darker p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <h1 className="text-4xl font-bold text-white">My List</h1>
          <button
            onClick={() => setShowCreatePlaylist(true)}
            className="flex items-center space-x-2 px-4 py-2 bg-fire-orange hover:bg-fire-blue text-white rounded-lg transition-colors duration-200"
          >
            <Plus size={20} />
            <span>Create Playlist</span>
          </button>
        </div>
        
        {/* Wishlist */}
        {wishlist.length > 0 && (
          <div className="mb-12">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <span className="mr-2">❤️</span>
              Wishlist ({wishlist.length})
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-6">
              {wishlist.map((movie) => (
                <MovieCard key={movie.id} movie={movie} />
              ))}
            </div>
          </div>
        )}

        {/* Watch Later */}
        {watchLater.length > 0 && (
          <div className="mb-12">
            <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
              <span className="mr-2">⏰</span>
              Watch Later ({watchLater.length})
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-6">
              {watchLater.map((movie) => (
                <MovieCard key={movie.id} movie={movie} />
              ))}
            </div>
          </div>
        )}

        {/* My Playlists */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
            <span className="mr-2">📝</span>
            My Playlists
          </h2>
          {allMyPlaylists.map((playlist) => (
            <div key={playlist.id} className="mb-8 bg-fire-gray/20 rounded-xl p-6">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-white">{playlist.name}</h3>
                <div className="flex items-center space-x-4">
                  <button
                    onClick={() => openAddMovieModal(playlist.id, playlist)}
                    className="flex items-center space-x-2 px-3 py-1 bg-fire-orange/20 text-fire-orange rounded-lg hover:bg-fire-orange/30 transition-colors duration-200"
                  >
                    <Plus size={16} />
                    <span>Add Movie</span>
                  </button>
                  <div className="flex items-center space-x-2 text-gray-400">
                    <span>{playlist.movies.length} movies</span>
                    <Play size={16} />
                  </div>
                </div>
              </div>
              {playlist.movies.length > 0 ? (
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-4">
                  {playlist.movies.map((movie) => (
                    <div key={movie.id} className="relative group">
                      <MovieCard movie={movie} />
                      <button
                        onClick={() => {
                          if (playlist.owner === 'You' && myPlaylists.find(p => p.id === playlist.id)) {
                            handleRemoveFromMyPlaylist(playlist.id, movie.id);
                          } else {
                            removeFromPlaylist(playlist.id, movie.id);
                          }
                        }}
                        className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 w-8 h-8 bg-red-600 hover:bg-red-700 text-white rounded-full flex items-center justify-center transition-all duration-300"
                      >
                        <Trash2 size={14} />
                      </button>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-400">No movies in this playlist yet</p>
              )}
            </div>
          ))}
        </div>

        {/* Shared Playlists */}
        <div className="mb-12">
          <h2 className="text-2xl font-bold text-white mb-6 flex items-center">
            <span className="mr-2">👥</span>
            Shared Playlists
          </h2>
          {sharedPlaylists.map((playlist) => (
            <div key={playlist.id} className="mb-8 bg-fire-gray/20 rounded-xl p-6">
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h3 className="text-xl font-bold text-white">{playlist.name}</h3>
                  <p className="text-gray-400 text-sm">Created by {playlist.owner}</p>
                </div>
                <div className="flex items-center space-x-4">
                  <button
                    onClick={() => openAddMovieModal(playlist.id, playlist)}
                    className="flex items-center space-x-2 px-3 py-1 bg-fire-orange/20 text-fire-orange rounded-lg hover:bg-fire-orange/30 transition-colors duration-200"
                  >
                    <Plus size={16} />
                    <span>Add Movie</span>
                  </button>
                  <div className="flex items-center space-x-2 text-gray-400">
                    <Users size={16} />
                    <span>{playlist.collaborators.length}</span>
                  </div>
                  <div className="flex items-center space-x-2 text-gray-400">
                    <span>{playlist.movies.length} movies</span>
                    <Play size={16} />
                  </div>
                </div>
              </div>
              <div className="flex items-center space-x-2 mb-4">
                <span className="text-gray-400 text-sm">Collaborators:</span>
                {playlist.collaborators.map((collaborator, index) => (
                  <span key={index} className="text-fire-orange text-sm">
                    {collaborator}{index < playlist.collaborators.length - 1 ? ',' : ''}
                  </span>
                ))}
              </div>
              {playlist.movies.length > 0 ? (
                <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 2xl:grid-cols-6 gap-4">
                  {playlist.movies.map((movie) => (
                    <div key={movie.id} className="relative group">
                      <MovieCard movie={movie} />
                      <button
                        onClick={() => handleRemoveFromSharedPlaylist(playlist.id, movie.id)}
                        className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 w-8 h-8 bg-red-600 hover:bg-red-700 text-white rounded-full flex items-center justify-center transition-all duration-300"
                      >
                        <Trash2 size={14} />
                      </button>
                    </div>
                  ))}
                </div>
              ) : (
                <p className="text-gray-400">No movies in this playlist yet</p>
              )}
            </div>
          ))}
        </div>

        {/* Empty State */}
        {wishlist.length === 0 && watchLater.length === 0 && allMyPlaylists.length === 0 && (
          <div className="text-center text-gray-400 mt-12">
            <h2 className="text-2xl font-bold mb-2">Your list is empty</h2>
            <p>Start adding movies to your wishlist, watch later, or create playlists!</p>
          </div>
        )}

        {/* Create Playlist Modal */}
        {showCreatePlaylist && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={() => setShowCreatePlaylist(false)}>
            <div className="bg-fire-dark p-6 rounded-xl max-w-md w-full mx-4" onClick={(e) => e.stopPropagation()}>
              <h3 className="text-white text-lg font-bold mb-4">Create New Playlist</h3>
              <input
                type="text"
                value={newPlaylistName}
                onChange={(e) => setNewPlaylistName(e.target.value)}
                placeholder="Enter playlist name"
                className="w-full px-4 py-2 bg-fire-gray text-white rounded-lg mb-4 focus:outline-none focus:ring-2 focus:ring-fire-orange"
                autoFocus
              />
              <div className="flex space-x-4">
                <button
                  onClick={handleCreatePlaylist}
                  disabled={!newPlaylistName.trim()}
                  className="flex-1 px-4 py-2 bg-fire-orange hover:bg-fire-blue disabled:bg-gray-600 disabled:cursor-not-allowed text-white rounded-lg transition-colors duration-200"
                >
                  Create
                </button>
                <button
                  onClick={() => setShowCreatePlaylist(false)}
                  className="flex-1 px-4 py-2 bg-gray-600 hover:bg-gray-700 text-white rounded-lg transition-colors duration-200"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Add Movie to Playlist Modal */}
        {showAddToPlaylist && selectedPlaylistData && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50" onClick={() => setShowAddToPlaylist(false)}>
            <div className="bg-fire-dark p-6 rounded-xl max-w-4xl w-full mx-4 max-h-[80vh] overflow-y-auto" onClick={(e) => e.stopPropagation()}>
              <h3 className="text-white text-lg font-bold mb-4">Add Movie to "{selectedPlaylistData.name}"</h3>
              <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 mb-6">
                {allAvailableMovies.map((movie) => (
                  <div
                    key={movie.id}
                    className="cursor-pointer group"
                    onClick={() => handleAddMovieToPlaylist(movie)}
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
                onClick={() => setShowAddToPlaylist(false)}
                className="bg-gray-600 hover:bg-gray-700 text-white px-6 py-2 rounded-lg transition-colors"
              >
                Close
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MyListPage;

import React, { createContext, useContext, useState, ReactNode } from 'react';
import { Movie, ChatMessage, EmojiReaction, User, Playlist, Room } from '../types/Movie';

interface AppContextType {
  currentPage: string;
  setCurrentPage: (page: string) => void;
  selectedMovie: Movie | null;
  setSelectedMovie: (movie: Movie | null) => void;
  movieQueue: Movie[];
  addToQueue: (movie: Movie) => void;
  removeFromQueue: (movieId: string) => void;
  moveToNext: (movieId: string) => void;
  chatMessages: ChatMessage[];
  addChatMessage: (message: string) => void;
  emojiReactions: EmojiReaction[];
  addEmojiReaction: (emoji: string, x: number, y: number) => void;
  roomUsers: User[];
  isInRoom: boolean;
  setIsInRoom: (inRoom: boolean) => void;
  roomName: string;
  setRoomName: (name: string) => void;
  wishlist: Movie[];
  addToWishlist: (movie: Movie) => void;
  removeFromWishlist: (movieId: string) => void;
  watchLater: Movie[];
  addToWatchLater: (movie: Movie) => void;
  removeFromWatchLater: (movieId: string) => void;
  playlists: Playlist[];
  createPlaylist: (name: string) => void;
  addToPlaylist: (playlistId: string, movie: Movie) => void;
  removeFromPlaylist: (playlistId: string, movieId: string) => void;
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  selectedCategory: string;
  setSelectedCategory: (category: string) => void;
  currentRoom: Room | null;
  setCurrentRoom: (room: Room | null) => void;
  selectedRoomMovie: Movie | null;
  setSelectedRoomMovie: (movie: Movie | null) => void;
  addFriendToRoom: (friendName: string) => void;
  selectedPlatform: string;
  setSelectedPlatform: (platform: string) => void;
}

const AppContext = createContext<AppContextType | undefined>(undefined);

export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};

export const AppProvider = ({ children }: { children: ReactNode }) => {
  const [currentPage, setCurrentPage] = useState('home');
  const [selectedMovie, setSelectedMovie] = useState<Movie | null>(null);
  const [selectedRoomMovie, setSelectedRoomMovie] = useState<Movie | null>(null);
  const [movieQueue, setMovieQueue] = useState<Movie[]>([]);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      user: 'Varshith',
      message: 'Hey everyone! Ready for movie night? 🍿',
      timestamp: new Date(),
      avatar: '🎭'
    },
    {
      id: '2',
      user: 'Rohith',
      message: 'Absolutely! What are we watching first?',
      timestamp: new Date(),
      avatar: '🎬'
    }
  ]);
  const [emojiReactions, setEmojiReactions] = useState<EmojiReaction[]>([]);
  const [isInRoom, setIsInRoom] = useState(false);
  const [roomName, setRoomName] = useState("Movie Night Party");
  const [wishlist, setWishlist] = useState<Movie[]>([]);
  const [watchLater, setWatchLater] = useState<Movie[]>([]);
  const [playlists, setPlaylists] = useState<Playlist[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [currentRoom, setCurrentRoom] = useState<Room | null>(null);
  const [selectedPlatform, setSelectedPlatform] = useState('');

  const [roomUsers, setRoomUsers] = useState<User[]>([
    { id: '1', name: 'You', avatar: '🧑🏻‍🦰', isOnline: true },
    { id: '2', name: 'Rohith', avatar: '👨🏻‍🦰', isOnline: true },
    { id: '3', name: 'Varshith', avatar: '🧑🏻‍🦰', isOnline: true },
    { id: '4', name: 'Harsha', avatar: '👩🏻', isOnline: false }
  ]);

  const addToQueue = (movie: Movie) => {
    setMovieQueue(prev => {
      if (prev.find(m => m.id === movie.id)) return prev;
      return [...prev, movie];
    });
  };

  const removeFromQueue = (movieId: string) => {
    setMovieQueue(prev => prev.filter(m => m.id !== movieId));
  };

  const moveToNext = (movieId: string) => {
    setMovieQueue(prev => {
      const movieIndex = prev.findIndex(m => m.id === movieId);
      if (movieIndex === -1) return prev;
      
      const movie = prev[movieIndex];
      const newQueue = prev.filter(m => m.id !== movieId);
      return [movie, ...newQueue];
    });
  };

  const addChatMessage = (message: string) => {
    const newMessage: ChatMessage = {
      id: Date.now().toString(),
      user: 'You',
      message,
      timestamp: new Date(),
      avatar: '🎯'
    };
    setChatMessages(prev => [...prev, newMessage]);
  };

  const addEmojiReaction = (emoji: string, x: number, y: number) => {
    const reaction: EmojiReaction = {
      id: Date.now().toString(),
      emoji,
      x,
      y
    };
    setEmojiReactions(prev => [...prev, reaction]);
    
    setTimeout(() => {
      setEmojiReactions(prev => prev.filter(r => r.id !== reaction.id));
    }, 2000);
  };

  const addToWishlist = (movie: Movie) => {
    setWishlist(prev => {
      if (prev.find(m => m.id === movie.id)) return prev;
      return [...prev, movie];
    });
  };

  const removeFromWishlist = (movieId: string) => {
    setWishlist(prev => prev.filter(m => m.id !== movieId));
  };

  const addToWatchLater = (movie: Movie) => {
    setWatchLater(prev => {
      if (prev.find(m => m.id === movie.id)) return prev;
      return [...prev, movie];
    });
  };

  const removeFromWatchLater = (movieId: string) => {
    setWatchLater(prev => prev.filter(m => m.id !== movieId));
  };

  const createPlaylist = (name: string) => {
    const newPlaylist: Playlist = {
      id: Date.now().toString(),
      name,
      movies: [],
      createdAt: new Date(),
      owner: 'You',
      isShared: false
    };
    setPlaylists(prev => [...prev, newPlaylist]);
  };

  const addToPlaylist = (playlistId: string, movie: Movie) => {
    setPlaylists(prev => prev.map(playlist => 
      playlist.id === playlistId 
        ? { ...playlist, movies: [...playlist.movies.filter(m => m.id !== movie.id), movie] }
        : playlist
    ));
  };

  const removeFromPlaylist = (playlistId: string, movieId: string) => {
    setPlaylists(prev => prev.map(playlist => 
      playlist.id === playlistId 
        ? { ...playlist, movies: playlist.movies.filter(m => m.id !== movieId) }
        : playlist
    ));
  };

  const addFriendToRoom = (friendName: string) => {
    const avatars = ['🎨', '🎸', '🎮', '🎲', '🎳', '🎺', '🎻', '🎹'];
    const randomAvatar = avatars[Math.floor(Math.random() * avatars.length)];
    
    const newFriend: User = {
      id: Date.now().toString(),
      name: friendName,
      avatar: randomAvatar,
      isOnline: true
    };
    
    setRoomUsers(prev => [...prev, newFriend]);
    
    // Add a chat message about the new friend joining
    const joinMessage: ChatMessage = {
      id: Date.now().toString(),
      user: 'System',
      message: `${friendName} joined the room!`,
      timestamp: new Date(),
      avatar: '🤖'
    };
    setChatMessages(prev => [...prev, joinMessage]);
  };

  return (
    <AppContext.Provider value={{
      currentPage,
      setCurrentPage,
      selectedMovie,
      setSelectedMovie,
      movieQueue,
      addToQueue,
      removeFromQueue,
      moveToNext,
      chatMessages,
      addChatMessage,
      emojiReactions,
      addEmojiReaction,
      roomUsers,
      isInRoom,
      setIsInRoom,
      roomName,
      setRoomName,
      wishlist,
      addToWishlist,
      removeFromWishlist,
      watchLater,
      addToWatchLater,
      removeFromWatchLater,
      playlists,
      createPlaylist,
      addToPlaylist,
      removeFromPlaylist,
      searchQuery,
      setSearchQuery,
      selectedCategory,
      setSelectedCategory,
      currentRoom,
      setCurrentRoom,
      selectedRoomMovie,
      setSelectedRoomMovie,
      addFriendToRoom,
      selectedPlatform,
      setSelectedPlatform
    }}>
      {children}
    </AppContext.Provider>
  );
};

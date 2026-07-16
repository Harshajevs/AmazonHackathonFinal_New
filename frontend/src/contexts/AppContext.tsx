import React, { createContext, useContext, useState, useRef, useCallback, ReactNode } from 'react';
import { Movie, ChatMessage, EmojiReaction, User, Playlist, Room } from '../types/Movie';
import { api, toMovie, ApiMovie } from '../lib/api';
import { RoomSocket, RoomEvent } from '../lib/roomSocket';
import { movieData } from '../data/movieData';

export interface RoomSession {
  joinCode: string;
  roomId: string;
  memberId: string;
  role: string;
  membershipToken: string;
}

interface RoomMembershipDto {
  join_code: string;
  room_id: string;
  member_id: string;
  role: string;
  membership_token: string;
  snapshot: RoomSnapshot;
}

interface RoomSnapshot {
  name: string;
  members: SnapshotMember[];
  queue: SnapshotQueueItem[];
  chat_history: { message_id: string; username: string; text: string; at: string }[];
}

interface SnapshotMember {
  member_id: string;
  username: string;
  avatar: string;
  role: string;
  presence: string;
}

interface SnapshotQueueItem {
  item_id: string;
  movie_id: number;
  title: string;
  image: string;
}

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
  roomSession: RoomSession | null;
  createRoom: (name: string, password: string, movie: Movie | null) => Promise<void>;
  joinRoomByCode: (code: string, password: string) => Promise<void>;
  leaveRoom: () => void;
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

const queueItemToMovie = (item: SnapshotQueueItem): Movie => {
  const known = movieData.find((m) => m.id === String(item.movie_id));
  if (known) return known;
  return {
    id: String(item.movie_id),
    title: item.title,
    description: '',
    genre: [],
    duration: '',
    rating: '',
    year: 0,
    image: item.image,
    platform: 'Netflix',
  };
};

const memberToUser = (m: SnapshotMember): User => ({
  id: m.member_id,
  name: m.username,
  avatar: m.avatar || '🧑',
  isOnline: m.presence !== 'offline',
});

export const AppProvider = ({ children }: { children: ReactNode }) => {
  const [currentPage, setCurrentPage] = useState('home');
  const [selectedMovie, setSelectedMovie] = useState<Movie | null>(null);
  const [selectedRoomMovie, setSelectedRoomMovie] = useState<Movie | null>(null);
  const [movieQueue, setMovieQueue] = useState<Movie[]>([]);
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [emojiReactions, setEmojiReactions] = useState<EmojiReaction[]>([]);
  const [isInRoom, setIsInRoom] = useState(false);
  const [roomName, setRoomName] = useState('Movie Night Party');
  const [roomSession, setRoomSession] = useState<RoomSession | null>(null);
  const [wishlist, setWishlist] = useState<Movie[]>([]);
  const [watchLater, setWatchLater] = useState<Movie[]>([]);
  const [playlists, setPlaylists] = useState<Playlist[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [currentRoom, setCurrentRoom] = useState<Room | null>(null);
  const [selectedPlatform, setSelectedPlatform] = useState('');
  const [roomUsers, setRoomUsers] = useState<User[]>([{ id: '1', name: 'You', avatar: '🧑🏻‍🦰', isOnline: true }]);

  const socketRef = useRef<RoomSocket | null>(null);
  // Server queue item ids by movie id, for remove/reorder commands.
  const queueItemIds = useRef<Map<string, string>>(new Map());

  const applyQueue = useCallback((items: SnapshotQueueItem[]) => {
    queueItemIds.current = new Map(items.map((i) => [String(i.movie_id), i.item_id]));
    setMovieQueue(items.map(queueItemToMovie));
  }, []);

  const spawnReaction = useCallback((emoji: string, x: number, y: number) => {
    const reaction: EmojiReaction = { id: crypto.randomUUID(), emoji, x, y };
    setEmojiReactions((prev) => [...prev, reaction]);
    setTimeout(() => {
      setEmojiReactions((prev) => prev.filter((r) => r.id !== reaction.id));
    }, 2000);
  }, []);

  const appendChat = useCallback((id: string, user: string, message: string, avatar: string, at?: string) => {
    setChatMessages((prev) => [...prev, { id, user, message, timestamp: at ? new Date(at) : new Date(), avatar }]);
  }, []);

  const handleRoomEvent = useCallback(
    (event: RoomEvent, session: RoomSession) => {
      const p = event.payload as Record<string, any>;
      switch (event.type) {
        case 'room.snapshot': {
          const snap = p as unknown as RoomSnapshot;
          setRoomName(snap.name);
          setRoomUsers(snap.members.map(memberToUser));
          applyQueue(snap.queue);
          setChatMessages(
            snap.chat_history.map((c) => ({
              id: c.message_id,
              user: c.username,
              message: c.text,
              timestamp: new Date(c.at),
              avatar: '💬',
            })),
          );
          break;
        }
        case 'member.joined':
          setRoomUsers((prev) => [
            ...prev.filter((u) => u.id !== p.member_id),
            { id: p.member_id, name: p.username, avatar: p.avatar || '🧑', isOnline: true },
          ]);
          if (p.member_id !== session.memberId) {
            appendChat(event.event_id ?? crypto.randomUUID(), 'System', `${p.username} joined the room!`, '🤖');
          }
          break;
        case 'member.left':
        case 'member.kicked':
          setRoomUsers((prev) => prev.filter((u) => u.id !== p.member_id));
          appendChat(event.event_id ?? crypto.randomUUID(), 'System', `${p.username} left the room`, '🤖');
          break;
        case 'member.updated':
          setRoomUsers((prev) =>
            prev.map((u) => (u.id === p.member_id ? { ...u, isOnline: p.presence !== 'offline' } : u)),
          );
          break;
        case 'chat.message':
          appendChat(p.message_id, p.username, p.text, p.avatar || '💬', p.at);
          break;
        case 'reaction.created':
          spawnReaction(p.emoji, window.innerWidth / 2 + (Math.random() - 0.5) * 300, window.innerHeight - 160);
          break;
        case 'queue.updated':
          applyQueue(p.queue as SnapshotQueueItem[]);
          break;
        case 'room.ended':
        case 'room.expired':
          socketRef.current?.close();
          socketRef.current = null;
          setRoomSession(null);
          setIsInRoom(false);
          setCurrentPage('home');
          break;
        default:
          break; // poll + moderation events are handled server-side; snapshot refresh covers UI
      }
    },
    [appendChat, applyQueue, spawnReaction],
  );

  const enterRoom = useCallback(
    async (membership: RoomMembershipDto) => {
      const session: RoomSession = {
        joinCode: membership.join_code,
        roomId: membership.room_id,
        memberId: membership.member_id,
        role: membership.role,
        membershipToken: membership.membership_token,
      };
      const socket = new RoomSocket();
      await socket.connect(
        membership.join_code,
        membership.membership_token,
        (event) => handleRoomEvent(event, session),
        () => {
          // Server closed the connection (room ended / network drop).
          setRoomSession(null);
          setIsInRoom(false);
        },
      );
      socketRef.current = socket;
      setRoomSession(session);
      setChatMessages([]);
      setIsInRoom(true);
      setCurrentPage('room');
    },
    [handleRoomEvent],
  );

  const createRoom = useCallback(
    async (name: string, password: string, movie: Movie | null) => {
      const membership = await api<RoomMembershipDto>('/api/rooms', {
        method: 'POST',
        body: JSON.stringify({
          name,
          password: password || null,
          movie_id: movie ? Number(movie.id) : null,
        }),
      });
      setRoomName(name);
      setSelectedRoomMovie(movie);
      await enterRoom(membership);
    },
    [enterRoom],
  );

  const joinRoomByCode = useCallback(
    async (code: string, password: string) => {
      const membership = await api<RoomMembershipDto>(`/api/rooms/${code.trim().toUpperCase()}/join`, {
        method: 'POST',
        body: JSON.stringify({ password: password || null }),
      });
      await enterRoom(membership);
    },
    [enterRoom],
  );

  const leaveRoom = useCallback(() => {
    const socket = socketRef.current;
    if (socket?.connected) {
      socket.send('room.leave');
      socket.close();
    }
    socketRef.current = null;
    setRoomSession(null);
    setRoomUsers([{ id: '1', name: 'You', avatar: '🧑🏻‍🦰', isOnline: true }]);
    setMovieQueue([]);
    setChatMessages([]);
    setIsInRoom(false);
    setCurrentPage('home');
  }, []);

  const addToQueue = (movie: Movie) => {
    const socket = socketRef.current;
    if (socket?.connected) {
      socket.send('queue.add', { movie_id: Number(movie.id), title: movie.title, image: movie.image });
      return; // authoritative queue arrives via queue.updated
    }
    setMovieQueue((prev) => {
      if (prev.find((m) => m.id === movie.id)) return prev;
      return [...prev, movie];
    });
  };

  const removeFromQueue = (movieId: string) => {
    const socket = socketRef.current;
    if (socket?.connected) {
      const itemId = queueItemIds.current.get(movieId);
      if (itemId) socket.send('queue.remove', { item_id: itemId });
      return;
    }
    setMovieQueue((prev) => prev.filter((m) => m.id !== movieId));
  };

  const moveToNext = (movieId: string) => {
    const socket = socketRef.current;
    if (socket?.connected) {
      const ids = movieQueue.map((m) => queueItemIds.current.get(m.id)).filter(Boolean) as string[];
      const target = queueItemIds.current.get(movieId);
      if (target) socket.send('queue.reorder', { item_ids: [target, ...ids.filter((i) => i !== target)] });
      return;
    }
    setMovieQueue((prev) => {
      const movieIndex = prev.findIndex((m) => m.id === movieId);
      if (movieIndex === -1) return prev;
      const movie = prev[movieIndex];
      return [movie, ...prev.filter((m) => m.id !== movieId)];
    });
  };

  const addChatMessage = (message: string) => {
    const socket = socketRef.current;
    if (socket?.connected) {
      socket.send('chat.send', { text: message });
      return; // echoed back via chat.message broadcast
    }
    appendChat(Date.now().toString(), 'You', message, '🎯');
  };

  const addEmojiReaction = (emoji: string, x: number, y: number) => {
    const socket = socketRef.current;
    if (socket?.connected) {
      socket.send('reaction.send', { emoji });
      return; // rendered when the broadcast comes back
    }
    spawnReaction(emoji, x, y);
  };

  const addToWishlist = (movie: Movie) => {
    setWishlist((prev) => {
      if (prev.find((m) => m.id === movie.id)) return prev;
      return [...prev, movie];
    });
    api('/api/library/items', { method: 'POST', body: JSON.stringify({ movie_id: Number(movie.id), kind: 'wishlist' }) }).catch(() => {});
  };

  const removeFromWishlist = (movieId: string) => {
    setWishlist((prev) => prev.filter((m) => m.id !== movieId));
    api(`/api/library/items?movie_id=${movieId}&kind=wishlist`, { method: 'DELETE' }).catch(() => {});
  };

  const addToWatchLater = (movie: Movie) => {
    setWatchLater((prev) => {
      if (prev.find((m) => m.id === movie.id)) return prev;
      return [...prev, movie];
    });
    api('/api/library/items', { method: 'POST', body: JSON.stringify({ movie_id: Number(movie.id), kind: 'watch_later' }) }).catch(() => {});
  };

  const removeFromWatchLater = (movieId: string) => {
    setWatchLater((prev) => prev.filter((m) => m.id !== movieId));
    api(`/api/library/items?movie_id=${movieId}&kind=watch_later`, { method: 'DELETE' }).catch(() => {});
  };

  const createPlaylist = (name: string) => {
    const newPlaylist: Playlist = {
      id: Date.now().toString(),
      name,
      movies: [],
      createdAt: new Date(),
      owner: 'You',
      isShared: false,
    };
    setPlaylists((prev) => [...prev, newPlaylist]);
  };

  const addToPlaylist = (playlistId: string, movie: Movie) => {
    setPlaylists((prev) =>
      prev.map((playlist) =>
        playlist.id === playlistId
          ? { ...playlist, movies: [...playlist.movies.filter((m) => m.id !== movie.id), movie] }
          : playlist,
      ),
    );
  };

  const removeFromPlaylist = (playlistId: string, movieId: string) => {
    setPlaylists((prev) =>
      prev.map((playlist) =>
        playlist.id === playlistId
          ? { ...playlist, movies: playlist.movies.filter((m) => m.id !== movieId) }
          : playlist,
      ),
    );
  };

  const addFriendToRoom = (friendName: string) => {
    // Offline fallback only: with a live room, friends join with the code.
    const avatars = ['🎨', '🎸', '🎮', '🎲', '🎳', '🎺', '🎻', '🎹'];
    const randomAvatar = avatars[Math.floor(Math.random() * avatars.length)];
    setRoomUsers((prev) => [...prev, { id: Date.now().toString(), name: friendName, avatar: randomAvatar, isOnline: true }]);
    appendChat(Date.now().toString(), 'System', `${friendName} joined the room!`, '🤖');
  };

  return (
    <AppContext.Provider
      value={{
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
        roomSession,
        createRoom,
        joinRoomByCode,
        leaveRoom,
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
        setSelectedPlatform,
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

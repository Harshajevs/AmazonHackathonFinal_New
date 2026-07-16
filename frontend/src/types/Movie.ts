
export interface Movie {
  id: string;
  title: string;
  description: string;
  genre: string[];
  duration: string;
  rating: string;
  year: number;
  image: string;
  platform: 'Netflix' | 'Prime Video' | 'Hotstar' | 'Aha';
  featured?: boolean;
}

export interface ChatMessage {
  id: string;
  user: string;
  message: string;
  timestamp: Date;
  avatar: string;
}

export interface EmojiReaction {
  id: string;
  emoji: string;
  x: number;
  y: number;
}

export interface User {
  id: string;
  name: string;
  avatar: string;
  isOnline: boolean;
}

export interface HeroSlide {
  id: string;
  title: string;
  image: string;
  type: string;
}

export interface Playlist {
  id: string;
  name: string;
  movies: Movie[];
  createdAt: Date;
  owner?: string;
  isShared?: boolean;
  collaborators?: string[];
}

export interface Room {
  id: string;
  name: string;
  password?: string;
  selectedMovie?: Movie;
  participants: User[];
}

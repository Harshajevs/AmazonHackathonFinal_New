import { useQuery } from '@tanstack/react-query';

import { api, ApiMovie, ensureSession, toMovie } from '../lib/api';
import { movieCategories } from '../data/movieData';
import { Movie } from '../types/Movie';

export interface HomeRow {
  key: string;
  title: string;
  movies: Movie[];
}

interface CategoryDto {
  key: string;
  title: string;
  movies: ApiMovie[];
}

interface PersonalRecsDto {
  request_id: string;
  active_signals: string[];
  results: { movie: ApiMovie; score: number; explanation: string }[];
}

interface TimeBlockDto {
  key: string;
  label: string;
  vibe: string;
  content_types: string[];
}

/** Bundled-catalog rows used whenever the backend is unreachable (FR-FE-04). */
const fallbackRows = (): HomeRow[] =>
  Object.entries(movieCategories).map(([title, movies]) => ({ key: title, title, movies }));

export const useSession = () =>
  useQuery({
    queryKey: ['session'],
    queryFn: ensureSession,
    staleTime: Infinity,
    retry: 1,
  });

export const useTimeBlock = (enabled: boolean) =>
  useQuery({
    queryKey: ['time-block'],
    queryFn: () => api<TimeBlockDto>('/api/analysis/time-block'),
    enabled,
    staleTime: 5 * 60_000,
    retry: false,
  });

/**
 * Personalized home rows: AI picks + time-block row from the backend,
 * followed by the curated catalog rows. Falls back to bundled data.
 */
export const useHomeRows = () => {
  const session = useSession();
  const online = session.data === true;

  const query = useQuery({
    queryKey: ['home-rows'],
    enabled: online,
    staleTime: 60_000,
    retry: false,
    queryFn: async (): Promise<HomeRow[]> => {
      const [recs, block, categories] = await Promise.all([
        api<PersonalRecsDto>('/api/recommendations/personal', {
          method: 'POST',
          body: JSON.stringify({ limit: 15 }),
        }),
        api<TimeBlockDto>('/api/analysis/time-block'),
        api<CategoryDto[]>('/api/movies/categories'),
      ]);
      const rows: HomeRow[] = [
        {
          key: 'personal',
          title: 'Personal Picks for You',
          movies: recs.results.map((r) => toMovie(r.movie)),
        },
        {
          key: 'time-block',
          title: `${block.label} — ${block.vibe}`,
          movies: recs.results
            .map((r) => toMovie(r.movie))
            .filter((m) => m.genre.some((g) => block.content_types.includes(g)))
            .slice(0, 15),
        },
        ...categories.map((c) => ({ key: c.key, title: c.title, movies: c.movies.map(toMovie) })),
      ];
      return rows.filter((row) => row.movies.length > 0);
    },
  });

  return {
    rows: query.data ?? fallbackRows(),
    isLive: online && query.isSuccess,
    isLoading: session.isLoading || (online && query.isLoading),
  };
};

export interface FriendDto {
  id: number;
  username: string;
  avatar: string;
  status: string;
  mutual_friends: number;
}

export interface FriendsDto {
  friends: FriendDto[];
  requests: FriendDto[];
  suggestions: FriendDto[];
  movie_suggestions: {
    id: number;
    from_username: string;
    from_avatar: string;
    message: string;
    movie: ApiMovie;
    created_at: string;
  }[];
}

export const useFriends = () => {
  const session = useSession();
  return useQuery({
    queryKey: ['friends'],
    queryFn: () => api<FriendsDto>('/api/friends'),
    enabled: session.data === true,
    staleTime: 60_000,
    retry: false,
  });
};

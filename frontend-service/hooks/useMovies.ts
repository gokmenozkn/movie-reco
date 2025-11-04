import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { fetchMovies, sendRatings, fetchRecommendations, toggleFavorite } from '../api/movies';

export const useMovies = () => useQuery({ queryKey: ['movies'], queryFn: fetchMovies });

export const useRecommendations = () =>
  useQuery({ queryKey: ['recommendations'], queryFn: fetchRecommendations });

export const useSendRatings = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: sendRatings,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['recommendations'] }),
  });
};

export const useToggleFavorite = () => {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: toggleFavorite,
    onSuccess: () => qc.invalidateQueries({ queryKey: ['recommendations'] }),
  });
};
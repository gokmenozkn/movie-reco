import { recClient } from './client';
import { Movie, RatingDto } from '../types';

export const fetchMovies = () => recClient.get<Movie[]>('/movies');

export const sendRatings = (ratings: RatingDto[]) =>
  recClient.post('/ratings', { ratings });

export const fetchRecommendations = () =>
  recClient.get<Movie[]>('/recommendations');

export const toggleFavorite = (movieId: number) =>
  recClient.post(`/favorites/${movieId}`);
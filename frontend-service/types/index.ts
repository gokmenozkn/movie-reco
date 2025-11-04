export interface Movie {
  id: number;
  title: string;
  poster: string;
  year: number;
  rating: number;
  plot: string;
}

export interface RatingDto {
  movieId: number;
  rating: number; // 1-5
}

export interface Tokens {
  accessToken: string;
  refreshToken: string;
}
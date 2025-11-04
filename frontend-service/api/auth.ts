import { authClient } from "./client";

export const login = (email: string, password: string) =>
  authClient.post("/auth/login", { email, password });

export const register = (email: string, password: string) =>
  authClient.post("/auth/register", { email, password });

export const refresh = (token: string) =>
  authClient.post("/auth/refresh", { refreshToken: token });

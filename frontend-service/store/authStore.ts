import { create } from 'zustand';
import { Tokens } from '../types';
import * as SecureStore from 'expo-secure-store';

interface State {
  accessToken: string | null;
  refreshToken: string | null;
  // setTokens: (t: Tokens) => Promise<void>;
  setAccessToken: (access_token: string) => Promise<void>;
  setRefreshToken: (refresh_token: string) => Promise<void>;
  logout: () => Promise<void>;
}

export const useAuthStore = create<State>((set) => ({
  accessToken: null,
  refreshToken: null,
  // setTokens: async (tokens: Tokens) => {
  //   await SecureStore.setItemAsync('accessToken', tokens.accessToken);
  //   await SecureStore.setItemAsync('refreshToken', tokens.refreshToken);
  //   set({ accessToken: tokens.accessToken, refreshToken: tokens.refreshToken });
  // },
  setAccessToken: async (token: string) => {
    await SecureStore.setItemAsync('accessToken', token);
    set({ accessToken: token });
  },
  setRefreshToken: async (token: string) => {
    await SecureStore.setItemAsync('refreshToken', token);
    set({ refreshToken: token });
  },
  logout: async () => {
    await SecureStore.deleteItemAsync('accessToken');
    await SecureStore.deleteItemAsync('refreshToken');
    set({ accessToken: null, refreshToken: null });
  },
}));
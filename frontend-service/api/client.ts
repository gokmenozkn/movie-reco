import axios from "axios";
import * as SecureStore from "expo-secure-store";
import Constants from "expo-constants";

const API_AUTH =
  process.env.EXPO_PUBLIC_AUTH_URL; /* Constants.expoConfig?.extra?.AUTH_URL */
const API_REC =
  process.env.EXPO_PUBLIC_REC_URL; /* Constants.expoConfig?.extra?.REC_URL; */

console.log("API Auth:", API_AUTH);

export const authClient = axios.create({ baseURL: API_AUTH });
export const recClient = axios.create({ baseURL: API_REC });

// attach access-token automatically
authClient.interceptors.request.use(async (config) => {
  const token = await SecureStore.getItemAsync("accessToken");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

recClient.interceptors.request.use(async (config) => {
  const token = await SecureStore.getItemAsync("accessToken");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

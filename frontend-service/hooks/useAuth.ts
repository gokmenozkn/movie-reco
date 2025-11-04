import { useMutation } from "@tanstack/react-query";
import { login, register } from "../api/auth";
import { useAuthStore } from "@/store/authStore";

export const useLogin = () => {
  // const setTokens = useAuthStore((s) => s.setTokens);
  const setAccessToken = useAuthStore(s => s.setAccessToken);
  const setRefreshToken = useAuthStore(s => s.setRefreshToken);

  return useMutation({
    mutationFn: ({ email, password }: { email: string; password: string }) =>
      login(email, password),
    onSuccess: ({ data }) => {
      console.log("Başarıyla giriş yaptık. İşte data:", data);
      const token = data?.access_token;
      // setTokens(token);
      setAccessToken(token);
    },
    onError: (error: any) => {
      console.log("Girişte bir hata:", error);
    },
  });
};

export const useRegister = () => {
  // const setTokens = useAuthStore((s) => s.setTokens);
  const setAccessToken = useAuthStore(s => s.setAccessToken);
  const setRefreshToken = useAuthStore(s => s.setRefreshToken);

  return useMutation({
    mutationFn: ({ email, password }: { email: string; password: string }) =>
      register(email, password),
    onSuccess: ({ data }) => {
      // setTokens(data)
      setAccessToken(data.access_token);
    },
    onError: (error: any) => {
      console.log("Üye olurken bir hata:", error);
    },
  });
};

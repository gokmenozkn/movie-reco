import { View, Text, TouchableOpacity, Alert } from "react-native";
import { useLogin } from "@/hooks/useAuth";
import { useForm } from "react-hook-form";
import { Link, router } from "expo-router";
import { AuthForm } from "@/components/AuthForm";
import { SafeAreaView } from "react-native-safe-area-context";
import { z } from "zod";

const loginSchema = z.object({
  email: z.string().email("Geçerli email girin"),
  password: z.string().min(6, "Şifre en az 6 karakter olmalı"),
});

type FormDTO = z.infer<typeof loginSchema>;

export default function LoginScreen() {
  const { mutate, isPending } = useLogin();
  const { setValue, handleSubmit } = useForm<FormDTO>();

  const onSubmit = (data: FormDTO) => {
    mutate(data, {
      onSuccess: () => {
        console.log("Login successful");
        router.replace("/(tabs)");
      },
      onError: (error: any) => {
        console.log("Login error:", error);
        Alert.alert("Login error", "Giriş yaparken hata!");
      },
    });
  };

  return (
    <SafeAreaView className="flex-1 bg-white">
      <View className="flex-1 px-6">
        <AuthForm
          mode="login"
          onSubmit={onSubmit}
          isPending={isPending}
        />

        <View className="items-center mt-6">
          <Link href="/register" asChild>
            <TouchableOpacity>
              <Text className="text-center text-gray-400">
                Hesabın yok mu? <Text className="text-emerald-400 font-semibold">Kayıt ol</Text>
              </Text>
            </TouchableOpacity>
          </Link>
        </View>
      </View>
    </SafeAreaView>
  );
}

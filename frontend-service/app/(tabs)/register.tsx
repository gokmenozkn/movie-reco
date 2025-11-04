import { View, Text, TouchableOpacity } from "react-native";
import { useRegister } from "@/hooks/useAuth";
import { Link, router } from "expo-router";
import { AuthForm } from "@/components/AuthForm";
import { SafeAreaView } from "react-native-safe-area-context";
import { z } from "zod";

const registerSchema = z.object({
  fullName: z.string().min(2, "İsim en az 2 karakter olmalı"),
  email: z.string().email("Geçerli bir email girin"),
  password: z.string().min(6, "Şifre en az 6 karakter olmalı"),
});

type FormDTO = z.infer<typeof registerSchema>;

export default function RegisterScreen() {
  const { mutate, isPending } = useRegister();

  const onSubmit = (data: FormDTO) => {
    mutate(data, {
      onSuccess: () => {
        console.log("Register successful!");
        router.replace("/(tabs)");
      },
      onError: (error: any) => {
        console.log("Register error:", error);
      },
    });
  };

  return (
    <SafeAreaView className="flex-1 bg-white">
      <View className="flex-1 px-6">
        <AuthForm mode="register" onSubmit={onSubmit} isPending={isPending} />

        <View className="items-center mt-6">
          <Link href="/login" asChild>
            <TouchableOpacity>
              <Text className="text-center text-gray-400">
                Zaten hesabın var mı?{" "}
                <Text className="text-emerald-400 font-semibold">
                  Giriş yap
                </Text>
              </Text>
            </TouchableOpacity>
          </Link>
        </View>
      </View>
    </SafeAreaView>
  );
}

import React from "react";
import { View, Text, TouchableOpacity, ActivityIndicator } from "react-native";
import { Control, useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { CustomInput } from "./CustomInput";

const loginSchema = z.object({
  email: z.string().email("Geçerli bir email girin"),
  password: z.string().min(6, "Şifre en az 6 karakter olmalı"),
});

const registerSchema = z.object({
  fullName: z.string().min(2, "İsim en az 2 karakter olmalı"),
  email: z.string().email("Geçerli bir email girin"),
  password: z.string().min(6, "Şifre en az 6 karakter olmalı"),
});

type LoginFormData = z.infer<typeof loginSchema>;
type RegisterFormData = z.infer<typeof registerSchema>;

interface AuthFormProps {
  mode: "login" | "register";
  onSubmit: (data: any) => void;
  isPending: boolean;
}

export const AuthForm: React.FC<AuthFormProps> = ({
  mode,
  onSubmit,
  isPending,
}) => {
  const schema = mode === "login" ? loginSchema : registerSchema;

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm({
    resolver: zodResolver(schema),
    defaultValues:
      mode === "login"
        ? { email: "", password: "" }
        : { fullName: "", email: "", password: "" },
  });

  return (
    <View className="flex-1 justify-center">
      {/* Header */}
      <View className="mb-8">
        <Text className="text-3xl font-bold text-gray-900 text-center mb-2">
          {mode === "login" ? "Hoş Geldiniz" : "Hesap Oluşturun"}
        </Text>
        <Text className="text-lg text-gray-600 text-center">
          {mode === "login"
            ? "Hesabınıza giriş yapın"
            : "Yeni hesabınızı oluşturun"}
        </Text>
      </View>

      {/* Form */}
      <View className="mb-6">
        {mode === "register" && (
          <CustomInput
            control={control}
            name="fullName"
            placeholder="Tam adınız"
            autoCapitalize="words"
          />
        )}

        <CustomInput
          control={control}
          name="email"
          placeholder="E-posta adresiniz"
          keyboardType="email-address"
          autoCapitalize="none"
        />

        <CustomInput
          control={control}
          name="password"
          placeholder="Şifreniz"
          secureTextEntry
        />
      </View>

      {/* Submit Button */}
      <TouchableOpacity
        onPress={handleSubmit(onSubmit)}
        disabled={isPending}
        className={`
          w-full py-4 rounded-lg mb-4
          ${isPending ? "bg-emerald-400" : "bg-emerald-600"}
        `}
      >
        {isPending ? (
          <ActivityIndicator color="#fff" />
        ) : (
          <Text className="text-white text-center font-semibold text-lg">
            {mode === "login" ? "Giriş Yap" : "Kayıt Ol"}
          </Text>
        )}
      </TouchableOpacity>
    </View>
  );
};

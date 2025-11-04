import React, { FC } from "react";
import { TextInput, View, Text } from "react-native";
import { Control, Controller } from "react-hook-form";

interface CustomInputProps {
  control: Control<any>;
  name: string;
  placeholder: string;
  secureTextEntry?: boolean;
  autoCapitalize?: "none" | "sentences" | "words" | "characters";
  keyboardType?: "default" | "email-address" | "numeric" | "phone-pad";
}

export const CustomInput: FC<CustomInputProps> = ({
  control,
  name,
  placeholder,
  secureTextEntry = false,
  autoCapitalize = "none",
  keyboardType = "default",
}) => {
  return (
    <Controller
      control={control}
      name={name}
      render={({
        field: { value, onChange, onBlur },
        fieldState: { error },
      }) => (
        <View className="mb-4">
          <TextInput
            value={value}
            onChangeText={onChange}
            onBlur={onBlur}
            placeholder={placeholder}
            secureTextEntry={secureTextEntry}
            autoCapitalize={autoCapitalize}
            keyboardType={keyboardType}
            className={`
              w-full px-4 py-3 border rounded-lg
              ${error ? "border-red-500 bg-red-50" : "border-gray-300 bg-white"}
              text-base
            `}
            placeholderTextColor="#9CA3AF"
          />
          {error && (
            <Text className="text-red-500 text-sm mt-1 ml-1">
              {error.message}
            </Text>
          )}
        </View>
      )}
    />
  );
};

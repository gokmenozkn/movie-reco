import { useLocalSearchParams } from "expo-router";
import { View, Text, ScrollView, Image } from "react-native";
import { MOVIES } from "@/data/movies";

export default function MovieDetails() {
  const { id } = useLocalSearchParams<{ id: string }>();
  const movie = MOVIES.find((m) => m.id === +id)!;

  return (
    <ScrollView className="flex-1 bg-gray-900">
      <Image
        source={{ uri: movie.poster }}
        className="w-full h-96"
        resizeMode="cover"
      />

      <View className="p-5">
        <Text className="text-white text-3xl font-bold">{movie.title}</Text>
        <Text className="text-gray-400 text-base">{movie.year}</Text>

        <View className="flex-row items-center mt-3">
          {[...Array(5)].map((_, i) => (
            <Text
              key={i}
              className={`text-xl ${i < Math.round(movie.rating / 2) ? "text-amber-400" : "text-gray-600"}`}
            >
              ★
            </Text>
          ))}
          <Text className="text-gray-300 text-base ml-3">
            {movie.rating}/10
          </Text>
        </View>

        <Text className="text-gray-200 mt-5 leading-5">{movie.plot}</Text>
      </View>
    </ScrollView>
  );
}

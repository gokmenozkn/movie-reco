import { useState } from "react";
import { SafeAreaView } from "react-native-safe-area-context";
import { StatusBar } from "expo-status-bar";
import { View, TextInput, FlatList, Text } from "react-native";
import { MovieCard } from "@/components/MovieCard";
import { Movie } from "@/types";

export default function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<Movie[]>([]);

  const handleSearch = (text: string) => {
    setQuery(text);
    // Burada API'ye istek atıp sonuçları 'results' state'ine set edeceksiniz.
  };

  return (
    <SafeAreaView className="flex-1 bg-[#121212] p-4">
      <StatusBar style="light" />
      <TextInput
        placeholder="Film, dizi veya oyuncu ara..."
        placeholderTextColor="#A1A1AA"
        value={query}
        onChangeText={handleSearch}
        className="bg-[#1E1E1E] text-white p-4 rounded-lg text-base mb-4"
        style={{ fontFamily: "Poppins-Regular" }}
      />

      <FlatList
        data={results}
        renderItem={({ item }) => <MovieCard movie={item} />} // Aynı MovieCard bileşeni
        keyExtractor={(item) => String(item.id)}
        numColumns={2} // Grid görünümü
        ListEmptyComponent={() => (
          <View className="flex-1 justify-center items-center mt-20">
            <Text className="text-gray-400 text-lg">Ne izlemek istersin?</Text>
          </View>
        )}
      />
    </SafeAreaView>
  );
}

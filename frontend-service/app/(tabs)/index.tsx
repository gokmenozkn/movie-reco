import {
  Text,
  View,
  FlatList,
  ScrollView,
  ImageBackground,
  TouchableOpacity,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { StatusBar } from "expo-status-bar";
import { Link } from "expo-router";
import { MovieCard } from "@/components/MovieCard";

import { MOVIES } from "@/data/movies";

export default function HomeScreen() {
  const featuredMovie = {
    id: "1",
    title: "Dune: Part Two",
    poster:
      "https://image.tmdb.org/t/p/original/tihf8Trht9zP3scmUQfvGlAY9FU.jpg.",
  };

  return (
    <SafeAreaView className="flex-1 bg-[#121212]">
      <StatusBar style="light" />
      <ScrollView>
        <Link href={`/movie/${featuredMovie.id}`} asChild>
          <ImageBackground
            source={{ uri: featuredMovie.poster }}
            className="w-full h-80 justify-end p-4"
            resizeMode="cover"
          >
            <Text
              className="text-white text-3xl font-bold"
              style={{ fontFamily: "Poppins-Bold" }}
            >
              {featuredMovie.title}
            </Text>
          </ImageBackground>
        </Link>

        {/* Popüler filmler */}
        <View className="p-4 mt-4">
          <Text
            className="text-white text-2xl font-bold mb-3"
            style={{ fontFamily: "Poppins-Bold" }}
          >
            Popüler filmler
          </Text>

          <FlatList
            data={MOVIES}
            renderItem={({ item }) => <MovieCard movie={item} />}
            keyExtractor={(item) => String(item.id)}
            horizontal
            showsHorizontalScrollIndicator={false}
          />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

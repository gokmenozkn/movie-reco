import { Link } from "expo-router";
import { TouchableOpacity, Image, Text } from "react-native";
import { Movie } from "@/types";

type Props = {
  movie: Movie;
};

export const MovieCard = ({ movie }: Props) => {
  return (
    <Link
      href={{
        pathname: "/movie/[id]",
        params: { id: movie.id },
      }}
      asChild
    >
      <TouchableOpacity className="mr-4">
        <Image
          source={{ uri: movie.poster }}
          className="w-36 h-52 rounded-lg bg-gray-700"
        />
        <Text className="text-white mt-2 w-36" numberOfLines={1}>
          {movie.title}
        </Text>
      </TouchableOpacity>
    </Link>
  );
};

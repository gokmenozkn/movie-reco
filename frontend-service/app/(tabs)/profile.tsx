import { View, Text, TouchableOpacity } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

export default function Profile() {
  function logout() {
    console.log("Log out");
  }

  return (
    <View className="flex-1 p-6 bg-gray-50">
      <Text className="text-2xl font-bold mb-6">Profil</Text>

      <View className="bg-white rounded-lg p-4 shadow-sm mb-4">
        <Text className="text-lg font-semibold mb-4">Hesap Ayarları</Text>

        <TouchableOpacity className="py-3 border-b border-gray-200">
          <Text className="text-gray-700">Favori Filmlerim</Text>
        </TouchableOpacity>

        <TouchableOpacity className="py-3 border-b border-gray-200">
          <Text className="text-gray-700">Puanladığım Filmler</Text>
        </TouchableOpacity>
      </View>

      <TouchableOpacity
        onPress={() => logout()}
        className="bg-red-500 py-3 rounded-lg"
      >
        <Text className="text-white text-center font-semibold">Çıkış Yap</Text>
      </TouchableOpacity>
    </View>
  );
}

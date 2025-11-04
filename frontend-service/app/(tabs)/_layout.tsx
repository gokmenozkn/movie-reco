import { Tabs } from "expo-router";
import FontAwesome from "@expo/vector-icons/FontAwesome";
import MaterialIcons from "@expo/vector-icons/MaterialIcons";
import AntDesign from "@expo/vector-icons/AntDesign";
import Ionicons from "@expo/vector-icons/Ionicons";
import { useAuthStore } from "@/store/authStore";

export default function TabLayout() {
  const accessToken = useAuthStore((s) => s.accessToken);

  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: "#F97316", // Aktif sekme rengi (Vurgu Rengi)
        tabBarInactiveTintColor: "#A1A1AA", // Pasif sekme rengi
        tabBarStyle: {
          backgroundColor: "#1E1E1E", // Tab bar arka planı
          borderTopWidth: 0, // Üstteki çizgiyi kaldır
        },
        headerShown: false, // Her sekmenin kendi başlığı olacak
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: "Home",
          tabBarIcon: ({ color }) => (
            <FontAwesome size={28} name="home" color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="search"
        options={{
          title: "Search",
          tabBarIcon: ({ color }) => (
            <FontAwesome size={28} name="search" color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="login"
        options={{
          title: "Login",
          tabBarIcon: ({ color }) => (
            <MaterialIcons size={28} name="login" color={color} />
          ),
          href: accessToken === null ? undefined : null,
        }}
      />
      <Tabs.Screen
        name="register"
        options={{
          title: "Register",
          tabBarIcon: ({ color }) => (
            <AntDesign size={28} name="github" color={color} />
          ),
          href: accessToken === null ? undefined : null,
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: "Profile",
          tabBarIcon: ({ color }) => (
            <Ionicons name="person" size={28} color={color} />
          ),
          href: accessToken === null ? null : "/(tabs)/profile",
        }}
      />
    </Tabs>
  );
}

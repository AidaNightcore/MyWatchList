import { create } from "zustand";
import api from "../services/api"; // Folosește serviciul api.js

export const useAuthStore = create((set) => ({
  user: null,
  accessToken: null,
  refreshToken: null,
  isLoading: false,
  error: null,

  login: async ({ email, password }) => {
    set({ isLoading: true, error: null });
    try {
      // Folosește api în loc de axios direct
      const response = await api.post("api/auth/login", { email, password });
      const { user, access_token, refresh_token } = response.data;

      localStorage.setItem("access_token", access_token); // trebuie să folosești exact key-ul de la api.js
      localStorage.setItem("refresh_token", refresh_token);
      localStorage.setItem("user", JSON.stringify(user));

      set({
        user,
        accessToken: access_token,
        refreshToken: refresh_token,
        isLoading: false,
        error: null,
      });
    } catch (err) {
      set({
        error: err.response?.data?.error || "Login failed.",
        isLoading: false,
      });
    }
  },

  logout: () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    set({
      user: null,
      accessToken: null,
      refreshToken: null,
      error: null,
    });
  },

  restoreSession: () => {
    const user = localStorage.getItem("user");
    const accessToken = localStorage.getItem("access_token");
    const refreshToken = localStorage.getItem("refresh_token");
    set({
      user: user ? JSON.parse(user) : null,
      accessToken,
      refreshToken,
    });
  },
}));

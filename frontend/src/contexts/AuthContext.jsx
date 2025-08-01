import React, { createContext, useContext, useEffect } from "react";
import { useAuthStore } from "../store/authStore";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const {
    user,
    accessToken,
    refreshToken,
    isLoading,
    error,
    login,
    logout,
    restoreSession,
  } = useAuthStore();

  useEffect(() => {
    restoreSession();
  }, [restoreSession]);

  return (
    <AuthContext.Provider
      value={{
        user,
        accessToken,
        refreshToken,
        isLoading,
        error,
        login,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);

import React, { createContext, useContext, useState, useCallback } from "react";
import api from "../services/api"; // Ajustează dacă e nevoie

const WatchlistContext = createContext();

export function WatchlistProvider({ children }) {
  const [watchlist, setWatchlist] = useState({
    watching: [],
    completed: [],
    on_hold: [],
    dropped: [],
    planned: [],
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch watchlist grouped by status (backend /api/watchlists)
  const refreshWatchlist = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get("/api/watchlists");
      setWatchlist(res.data || {});
    } catch (err) {
      setError(err);
    }
    setLoading(false);
  }, []);

  // Adaugă la watchlist (backend /api/watchlists/items POST)
  const addToWatchlist = useCallback(
    async (payload) => {
      try {
        await api.post("/api/watchlists/items", payload);
        await refreshWatchlist();
        return { success: true };
      } catch (err) {
        return {
          success: false,
          error: err?.response?.data?.error || err?.message,
        };
      }
    },
    [refreshWatchlist]
  );

  // Șterge element din watchlist (backend /api/watchlists/items/:id DELETE)
  const deleteFromWatchlist = useCallback(
    async (itemId) => {
      try {
        await api.delete(`/api/watchlists/items/${itemId}`);
        await refreshWatchlist();
        return { success: true };
      } catch (err) {
        return {
          success: false,
          error: err?.response?.data?.error || err?.message,
        };
      }
    },
    [refreshWatchlist]
  );

  // Update element (backend /api/watchlists/items/:id PUT)
  const updateWatchlistItem = useCallback(
    async (itemId, updatePayload) => {
      try {
        await api.put(`/api/watchlists/items/${itemId}`, updatePayload);
        await refreshWatchlist();
        return { success: true };
      } catch (err) {
        return {
          success: false,
          error: err?.response?.data?.error || err?.message,
        };
      }
    },
    [refreshWatchlist]
  );

  // Fetch on mount
  React.useEffect(() => {
    refreshWatchlist();
  }, [refreshWatchlist]);

  return (
    <WatchlistContext.Provider
      value={{
        watchlist,
        loading,
        error,
        refreshWatchlist,
        addToWatchlist,
        deleteFromWatchlist,
        updateWatchlistItem,
      }}
    >
      {children}
    </WatchlistContext.Provider>
  );
}

export function useWatchlist() {
  const ctx = useContext(WatchlistContext);
  if (!ctx)
    throw new Error("useWatchlist must be used within WatchlistProvider");
  return ctx;
}

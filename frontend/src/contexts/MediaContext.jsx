import React, { createContext, useContext, useState, useCallback } from "react";
import { getBooks, getShows, getMovies, getAllTitles } from "../services/media"; // Ajustează path-ul dacă trebuie

const MediaContext = createContext();

function uniqueById(arr) {
  const seen = new Set();
  return arr.filter((item) => {
    if (!item.id || seen.has(item.id)) return false;
    seen.add(item.id);
    return true;
  });
}

export function MediaProvider({ children }) {
  const [books, setBooks] = useState([]);
  const [shows, setShows] = useState([]);
  const [movies, setMovies] = useState([]);
  const [allTitles, setAllTitles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const loadAllMedia = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const [booksData, showsData, moviesData, allTitlesData] =
        await Promise.all([
          getBooks(),
          getShows(),
          getMovies(),
          getAllTitles(),
        ]);
      setBooks(
        uniqueById(booksData || []).sort(
          (a, b) =>
            (b.score ?? 0) - (a.score ?? 0) || a.title.localeCompare(b.title)
        )
      );
      setShows(
        uniqueById(showsData || []).sort(
          (a, b) =>
            (b.score ?? 0) - (a.score ?? 0) || a.title.localeCompare(b.title)
        )
      );
      setMovies(
        uniqueById(moviesData || []).sort(
          (a, b) =>
            (b.score ?? 0) - (a.score ?? 0) || a.title.localeCompare(b.title)
        )
      );

      setAllTitles(
        [...(allTitlesData || [])].sort((a, b) => {
          const da = a.publishDate ? new Date(a.publishDate).getTime() : 0;
          const db = b.publishDate ? new Date(b.publishDate).getTime() : 0;
          return db - da || a.title.localeCompare(b.title);
        })
      );
    } catch (err) {
      setError(err);
    } finally {
      setLoading(false);
    }
  }, []);

  return (
    <MediaContext.Provider
      value={{
        books,
        shows,
        movies,
        allTitles,
        loading,
        error,
        loadAllMedia,
      }}
    >
      {children}
    </MediaContext.Provider>
  );
}

export function useMedia() {
  return useContext(MediaContext);
}

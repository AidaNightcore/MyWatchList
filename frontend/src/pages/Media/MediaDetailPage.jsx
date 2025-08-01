import React from "react";
import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import BookPage from "./BookPage";
import MoviePage from "./MoviePage";
import ShowPage from "./ShowPage";
import api from "../../services/api";

export default function MediaDetailPage() {
  const { titleId } = useParams();
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    setData(null);
    setError(null);
    api
      .get(`/api/media/titles/${titleId}`)
      .then((res) => setData(res.data))
      .catch((err) => {
        setError(err?.response?.data?.error || err.message || "Unknown error");
      });
  }, [titleId]);

  if (error) return <div style={{ color: "red" }}>Error: {error}</div>;
  if (!data) return <div>Loading...</div>;

  if (data.type === "Book" && data.details)
    return <BookPage book={data.details} />;
  if (data.type === "Movie" && data.details)
    return <MoviePage movie={data.details} />;
  if (data.type === "Show" && data.details)
    return <ShowPage show={data.details} />;
  return <div>Unknown type or details missing.</div>;
}

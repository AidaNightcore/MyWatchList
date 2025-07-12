import api from "./api";

export async function getBooks() {
  const res = await api.get("/api/media/books");
  return res.data;
}
export async function getShows() {
  const res = await api.get("/api/media/shows");
  return res.data;
}
export async function getMovies() {
  const res = await api.get("/api/media/movies");
  return res.data;
}
export async function getAllTitles() {
  const res = await api.get("/api/media/titles");
  return res.data;
}

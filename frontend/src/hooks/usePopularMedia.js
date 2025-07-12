import { useState, useEffect } from "react";
import api from "../services/api";

export const usePopularMedia = () => {
  const [popular, setPopular] = useState({ Book: [], Movie: [], Show: [] });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    api
      .get("/media/trending?order_by=score")
      .then((res) => {
        let data = res.data;
        // dacă primești un obiect, fă array din valorile relevante
        if (!Array.isArray(data)) {
          data = Object.values(data).flat();
        }
        const grouped = { Book: [], Movie: [], Show: [] };
        // asigură-te că item.type există și e corect
        data.forEach((item) => {
          if (grouped[item.type] && grouped[item.type].length < 5) {
            grouped[item.type].push(item);
          }
        });
        setPopular(grouped);
      })
      .catch(() => {
        setPopular({ Book: [], Movie: [], Show: [] });
      })
      .finally(() => setLoading(false));
  }, []);

  return { popular, loading };
};

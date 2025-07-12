// import { useEffect, useState } from "react";
// import api from "../services/api";

// function cleanFilters(filters) {
//   const cleaned = {};
//   Object.keys(filters).forEach((key) => {
//     if (filters[key]) cleaned[key] = filters[key];
//   });
//   return cleaned;
// }

// export const useMedia = (filters) => {
//   const [media, setMedia] = useState([]);
//   const [loading, setLoading] = useState(false);

//   useEffect(() => {
//     setLoading(true);
//     api
//       .get("api/media/titles", {
//         params: { ...cleanFilters(filters), order_by: "publishDate" },
//       })
//       .then((res) => {
//         let data = res.data;
//         if (!Array.isArray(data)) data = [];
//         setMedia(data);
//       })
//       .catch(() => setMedia([]))
//       .finally(() => setLoading(false));
//   }, [filters]);

//   return { media, loading };
// };

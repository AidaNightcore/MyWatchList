import React from "react";
import { Card, CardContent, Typography, Box } from "@mui/material";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Legend,
} from "recharts";

const COLORS = [
  "#0088FE",
  "#00C49F",
  "#FFBB28",
  "#FF8042",
  "#9932CC",
  "#4CAF50",
  "#d72660",
  "#8224e3",
  "#feb72b",
];

function buildPieData(obj) {
  return Object.entries(obj || {}).map(([k, v]) => ({ name: k, value: v }));
}

export default function ProfileCharts({ summary }) {
  if (!summary) return null;

  // 1. Pie: Distribuție genuri (toate titlurile)
  const genreData = buildPieData(summary.genre_distribution);

  // 2. Pie: Distribuție statusuri (toate statusurile: planned, completed, watching, dropped, on_hold)
  const statusData = buildPieData(summary.counts);

  // 3. Bar: Comparativ statusuri pe tip (Book, Movie, Show) - calculat din status_by_genre
  // Dacă nu ai deja o mapare gen -> tip, adaptează codul de mai jos:
  // Exemplu mapare de bază (modifică după structura reală a genurilor la tine):
  const genreTypeMap = {
    // Exemplu. Completează după caz!
    Fantasy: "Book",
    "Science Fiction": "Book",
    Adventure: "Book",
    Mystery: "Book",
    Romance: "Book",
    Biography: "Book",
    History: "Book",
    Action: "Movie",
    Animation: "Movie",
    Drama: "Show",
    Comedy: "Show",
    Crime: "Show",
    Thriller: "Movie",
    Documentary: "Movie",
    Horror: "Movie",
    Sitcom: "Show",
    // ... restul genurilor tale ...
  };

  const statusByGenre = summary.status_by_genre || {};
  const typeList = ["Book", "Movie", "Show"];
  const statusList = Object.keys(summary.counts || {});

  // Construiește status_by_type din status_by_genre:
  const statusByType = {};
  Object.entries(statusByGenre).forEach(([genre, statusCounts]) => {
    const type = genreTypeMap[genre] || "Other";
    Object.entries(statusCounts).forEach(([status, count]) => {
      if (!statusByType[type]) statusByType[type] = {};
      statusByType[type][status] = (statusByType[type][status] || 0) + count;
    });
  });

  const barData = statusList.map((status) => ({
    status,
    ...typeList.reduce(
      (acc, type) => ({
        ...acc,
        [type]: statusByType[type]?.[status] || 0,
      }),
      {}
    ),
  }));

  return (
    <Card elevation={2} sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h5" gutterBottom>
          Statistici și Grafice
        </Typography>
        <Box
          sx={{
            width: "100%",
            display: "flex",
            flexWrap: "wrap",
            gap: 4,
            justifyContent: "space-around",
          }}
        >
          {/* Pie 1: Genuri */}
          <Box>
            <Typography align="center" variant="subtitle1" sx={{ mb: 1 }}>
              Distribuție Genuri
            </Typography>
            <ResponsiveContainer width={240} height={240}>
              <PieChart>
                <Pie
                  data={genreData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={90}
                  label
                >
                  {genreData.map((entry, idx) => (
                    <Cell
                      key={`cell-gen-${idx}`}
                      fill={COLORS[idx % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Box>
          {/* Pie 2: Statusuri */}
          <Box>
            <Typography align="center" variant="subtitle1" sx={{ mb: 1 }}>
              Distribuție Statusuri
            </Typography>
            <ResponsiveContainer width={240} height={240}>
              <PieChart>
                <Pie
                  data={statusData}
                  dataKey="value"
                  nameKey="name"
                  cx="50%"
                  cy="50%"
                  outerRadius={90}
                  label
                >
                  {statusData.map((entry, idx) => (
                    <Cell
                      key={`cell-status-${idx}`}
                      fill={COLORS[idx % COLORS.length]}
                    />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </Box>
        </Box>
        {/* Bar chart comparativ statusuri pe tip */}
        <Box sx={{ width: "100%", mt: 5 }}>
          <Typography variant="subtitle1" align="center" sx={{ mb: 1 }}>
            Comparativ statusuri pe tip (Book, Movie, Show)
          </Typography>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={barData}>
              <XAxis dataKey="status" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Legend />
              {typeList.map((type, idx) => (
                <Bar
                  key={type}
                  dataKey={type}
                  fill={COLORS[idx % COLORS.length]}
                  name={type}
                />
              ))}
            </BarChart>
          </ResponsiveContainer>
        </Box>
      </CardContent>
    </Card>
  );
}

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

  const genreData = buildPieData(summary.genre_distribution);
  const statusData = buildPieData(summary.counts);

  // Statusuri și genuri le ai deja, dar trebuie să extragi statusuri pe tip real din status_by_genre și genuri
  // Agregare tipuri pe baza status_by_genre + (dacă ai array de itemi, preferabil parcurgi acei itemi)
  const statusByGenre = summary.status_by_genre || {};

  // Determină dinamic lista de tipuri și statusuri din datele existente
  const tipuriSet = new Set();
  const statusuriSet = new Set();

  // Acest mapping e util doar dacă backend-ul NU returnează lista de itemi cu tipul fiecăruia.
  Object.entries(statusByGenre).forEach(([gen, statObj]) => {
    Object.entries(statObj).forEach(([status, count]) => {
      statusuriSet.add(status);
      // Tipul pentru gen nu se poate determina fără extra date, deci aici NU mai faci mapare gen->tip.
      // Tipurile le determinăm separat, dintr-o listă de itemi dacă backend-ul le expune.
    });
  });

  // Dacă ai nevoie de tipuri per item, ideal e ca backendul să îți returneze și lista de itemi din watchlist
  // Ex: summary.items = [{title:..., status:..., type:...}, ...]
  // Dacă nu, atunci nu poți construi bar chartul "pe tip" corect fără a cere această modificare la backend!

  // Exemplu fallback: folosește status_by_genre și grupează doar pe genuri
  // Dacă ai totuși tipul în status_by_genre (de ex. summary.status_by_type), folosește direct!
  const statusByType = summary.status_by_type || {}; // ideal, vezi dacă backend-ul trimite deja acest câmp
  const typeList = Object.keys(statusByType);
  const statusList = Object.keys(summary.counts || {});

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
          <Box>
            <Typography align="center" variant="subtitle1" sx={{ mb: 1 }}>
              Genre Distribution
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
          <Box>
            <Typography align="center" variant="subtitle1" sx={{ mb: 1 }}>
              Status Distribution
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
        {typeList.length > 0 && (
          <Box sx={{ width: "100%", mt: 5 }}>
            <Typography variant="subtitle1" align="center" sx={{ mb: 1 }}>
              Comparativ statusuri pe tip (Book, Movie, Show, etc.)
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
        )}
      </CardContent>
    </Card>
  );
}

import { Grid, Card, CardContent, Typography } from "@mui/material";

export default function ProfileStats({ stats }) {
  if (!stats) return null; // Defensive!
  return (
    <Grid container spacing={2} sx={{ mb: 3 }}>
      <Grid item xs={6} md={3}>
        <Card>
          <CardContent>
            <Typography variant="h6">Total Books</Typography>
            <Typography variant="h4">{stats.counts?.Book || 0}</Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={6} md={3}>
        <Card>
          <CardContent>
            <Typography variant="h6">Total Movies</Typography>
            <Typography variant="h4">{stats.counts?.Movie || 0}</Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={6} md={3}>
        <Card>
          <CardContent>
            <Typography variant="h6">Pages Read</Typography>
            <Typography variant="h4">{stats.pages_read ?? 0}</Typography>
          </CardContent>
        </Card>
      </Grid>
      <Grid item xs={6} md={3}>
        <Card>
          <CardContent>
            <Typography variant="h6">Minutes Watched</Typography>
            <Typography variant="h4">{stats.minutes_watched ?? 0}</Typography>
          </CardContent>
        </Card>
      </Grid>
    </Grid>
  );
}

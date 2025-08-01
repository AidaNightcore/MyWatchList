import React from "react";
import { Box, Container, Grid, Typography, Link } from "@mui/material";

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 4,
        px: 2,
        mt: "auto",
        bgcolor: "background.footer",
        color: "text.secondary",
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 600 }}>
              MediaTracker
            </Typography>
            <Typography variant="body2">
              Track your favorite movies, TV shows, and books. Join our
              community of media enthusiasts.
            </Typography>
          </Grid>

          <Grid item xs={6} md={2}>
            <Typography
              variant="subtitle1"
              gutterBottom
              sx={{ fontWeight: 600 }}
            >
              Navigation
            </Typography>
            <Link href="/" color="inherit" display="block">
              Home
            </Link>
            <Link href="/media" color="inherit" display="block">
              Browse
            </Link>
            <Link href="/social" color="inherit" display="block">
              Community
            </Link>
            <Link href="/about" color="inherit" display="block">
              About
            </Link>
          </Grid>

          <Grid item xs={6} md={2}>
            <Typography
              variant="subtitle1"
              gutterBottom
              sx={{ fontWeight: 600 }}
            >
              Legal
            </Typography>
            <Link href="/terms" color="inherit" display="block">
              Terms
            </Link>
            <Link href="/privacy" color="inherit" display="block">
              Privacy
            </Link>
            <Link href="/cookies" color="inherit" display="block">
              Cookies
            </Link>
          </Grid>

          <Grid item xs={12} md={4}>
            <Typography
              variant="subtitle1"
              gutterBottom
              sx={{ fontWeight: 600 }}
            >
              Connect
            </Typography>
            <Box display="flex" gap={2}>
              <Link href="https://twitter.com" color="inherit">
                Twitter
              </Link>
              <Link href="https://facebook.com" color="inherit">
                Facebook
              </Link>
              <Link href="https://instagram.com" color="inherit">
                Instagram
              </Link>
              <Link href="https://github.com" color="inherit">
                GitHub
              </Link>
            </Box>
            <Typography variant="body2" mt={2}>
              © {new Date().getFullYear()} MediaTracker. All rights reserved.
            </Typography>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default Footer;

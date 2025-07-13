import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../../contexts/AuthContext"; // ajustează calea dacă e nevoie

export default function ProfileRedirect() {
  const { user, isLoading } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (isLoading) return;
    if (user && user.id) {
      navigate(`/profile/${user.id}`, { replace: true });
    } else {
      navigate("/login", { replace: true });
    }
  }, [user, isLoading, navigate]);

  return <div>Loading profile...</div>;
}

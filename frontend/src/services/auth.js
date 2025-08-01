// In auth service
export const register = async (userData) => {
    const response = await api.post('/auth/register', userData);
    localStorage.setItem('access_token', response.data.access_token);
    localStorage.setItem('refresh_token', response.data.refresh_token);
    return response.data.user;
  };
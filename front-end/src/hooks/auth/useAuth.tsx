import { useQuery } from '@tanstack/react-query'
import useAuthStore from '@/stores/authStore'
import api from '@/api/api'

interface UserProfile {
  id: string
  username: string
  email: string
}

export const useAuth = () => {
  const isAuthorized = useAuthStore(state => state.isAuthorized)

  return useQuery<UserProfile>({
    queryKey: ['auth', 'user'],
    queryFn: async () => {
      const response = await api.get('/auth/me')
      return response.data
    },
    enabled: isAuthorized && !!localStorage.getItem('access'),
    staleTime: 1000 * 60 * 10,
    retry: false
  })
}

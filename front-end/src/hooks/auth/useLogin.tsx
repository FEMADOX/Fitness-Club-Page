import useAuthStore from '@/stores/authStore'
import { BaseFormData } from '@/utils/interfaces'
import { APIResponse } from '@/utils/types'
import { useMutation } from '@tanstack/react-query'
import { useLocation } from 'wouter'
import api from '@/api/api'
import { LOGIN_URL } from '@/api/constants'
import { toast } from 'sonner'
import { AxiosError } from 'axios'

export const useLogin = () => {
  const [, navigate] = useLocation()
  const setIsAuthorized = useAuthStore(state => state.setIsAuthorized)

  return useMutation<APIResponse, AxiosError, BaseFormData>({
    mutationFn: async credentials => {
      const response = await api.post(LOGIN_URL, credentials)
      return response
    },
    onSuccess: response => {
      localStorage.setItem('access', response.data.access)
      localStorage.setItem('refresh', response.data.refresh)

      setIsAuthorized(true)
      toast.success('Login successful', {
        description: response.data.message
      })

      navigate('/')
    },
    onError: error => {
      if (error.response && error.response.status === 400)
        toast.error('Invalid credentials', {
          description: (error.response as APIResponse).data.message
        })
      else
        toast.error('Login failed', {
          description:
            (error.response as APIResponse).data.message || error.message || 'An unexpected error occurred'
        })
    }
  })
}

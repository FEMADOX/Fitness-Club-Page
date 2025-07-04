import useAuthStore from '@/stores/authStore'
import { BaseFormData } from '@/utils/interfaces'
import { APIResponse } from '@/utils/types'
import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useLocation } from 'wouter'
import api from '@/api/api'
import { REGISTER_URL } from '@/api/constants'
import { toast } from 'sonner'
import { AxiosError } from 'axios'

export const useRegister = () => {
  const [, navigate] = useLocation()
  const setIsAuthorized = useAuthStore(state => state.setIsAuthorized)
  const queryClient = useQueryClient()
  return useMutation<APIResponse, AxiosError, BaseFormData>({
    mutationFn: async credentials => {
      const response = await api.post(REGISTER_URL, credentials)
      return response
    },
    onSuccess: response => {
      localStorage.setItem('access', response.data.access)
      localStorage.setItem('refresh', response.data.refresh)

      setIsAuthorized(true)
      toast.success('Login successful', {
        description: response.data.message
      })

      queryClient.invalidateQueries({ queryKey: ['auth'] })

      navigate('/')
    },
    onError: error => {
      toast.error('Registration failed', {
        description:
          (error.response as APIResponse).data.message ||
          error.message ||
          'An unexpected error occurred'
      })
    }
  })
}

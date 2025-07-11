import { ACCESS_TOKEN, REFRESH_TOKEN } from '@/modules/register/domain/constants'
import { useMutation, UseMutationOptions, useQueryClient } from '@tanstack/react-query'
import { AxiosError } from 'axios'
import { toast } from 'sonner'
import { useLocation } from 'wouter'
import { APIResponse } from '../../../../domain/types'
import useAuthStore from '../../../../presentation/stores/authStore'

interface BaseMutationConfig<TVariables> {
  mutationFn: (variables: TVariables) => Promise<APIResponse>
  successMessage?: string
  errorMessage?: string
  redirect?: string
  shouldAuth?: boolean
  // invalidateQueries?: string[]
  onSuccess?: (data: APIResponse) => void
  onError?: (error: AxiosError) => void
}

export const useBaseAuth = <TVariables = any>(
  config: BaseMutationConfig<TVariables>,
  options?: Omit<
    UseMutationOptions<APIResponse, AxiosError, TVariables>,
    'mutationFn' | 'onSuccess' | 'onError'
  >
) => {
  const [, navigate] = useLocation()
  const setIsAuthorized = useAuthStore(state => state.setIsAuthorized)
  // const queryClient = useQueryClient()

  return useMutation<APIResponse, AxiosError, TVariables>({
    mutationFn: config.mutationFn,

    onSuccess: response => {
      // Handle Authentitcation
      if (config.shouldAuth && response.data.access && response.data.refresh) {
        localStorage.setItem(ACCESS_TOKEN, response.data.access)
        localStorage.setItem(REFRESH_TOKEN, response.data.refresh)
        setIsAuthorized(true)
      }

      if (!config.shouldAuth && response.status === 200) {
        localStorage.clear()
        setIsAuthorized(false)
      }

      // Show success message
      if (config.successMessage) {
        toast.success(config.successMessage, {
          description: response.data.message
        })
      }

      // Invalidate queries
      // if (config.invalidateQueries) {
      //   config.invalidateQueries.forEach(queryKey => {
      //     queryClient.invalidateQueries({ queryKey: [queryKey] })
      //   })
      // }

      // Custom callback
      config.onSuccess?.(response)

      // Redirect
      if (config.redirect) {
        navigate(config.redirect)
      }
    },

    onError: error => {
      if (config.onError) {
        config.onError(error)
        return
      }
      console.error(`${config.errorMessage || 'An error occurred'}`, error)

      toast.error(config.errorMessage || 'Operation failed', {
        description:
          (error.response as APIResponse)?.data?.message ||
          error.message ||
          'An unexpected error occurred'
      })
    },

    retry: config.shouldAuth ? 3 : 0,
    retryDelay: 5000,
    ...options
  })
}

import { APIResponse } from '@/domain/types'
import { API_TOKEN_RESPONSES } from '@/modules/register/domain'
import { MutationCache, QueryCache, QueryClient } from '@tanstack/react-query'
import { AxiosError } from 'axios'
import { toast } from 'sonner'

const handleGlobalError = (error: AxiosError, context: 'query' | 'mutation') => {
  const response = error.response as APIResponse
  const status = response.status
  const message = response.data?.message

  console.error(`🔥 Global ${context} error:`, {
    status,
    message,
    url: error.config?.url,
    method: error.config?.method?.toUpperCase()
  })

  // Handle Network errors
  if (!error.response) {
    toast.error('Network error', {
      description: 'Please check your internet connection and try again.'
    })
    return
  }

  // Handle server errors
  if (status >= 500) {
    console.error('⚠️ Server error:', response)
    return
  }

  // Handle mutation-specific errors
  if (context === 'mutation') {
    // Logout on token-related errors
    if ([401, 406].includes(status) && message && message in API_TOKEN_RESPONSES) {
      console.log('🛑 Token-related error detected, logging out...')
      localStorage.clear()

      if (!window.location.pathname.includes('/login')) {
        toast.error('Session expired, please log in again.', {
          description: 'You will be redirected to the login page.'
        })
        window.location.href = '/login'
        return
      }
      return
    }
  }

  // Handle query-specific errors
  if (context === 'query') {
    // Handle specific query errors here if needed
    if (message && status >= 400 && status < 500) {
      console.warn(`⚠️ Query error ${status}:`, message)
      toast.error('An error occurred while fetching data.', {
        description: 'Please try again later.'
      })
      return
    }
    console.warn(`⚠️ Query error ${status}:`, message)
    return
  }
}

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: (failureCount, error) => {
        const axiosError = error as AxiosError
        const status = axiosError.response?.status

        if (status === 401 || status === 403 || status === 404) {
          return false
        }

        // Retry up to 3 times for server error
        return failureCount < 3
      },
      retryDelay: attemptIndex => Math.min(1000 * 2 ** attemptIndex, 30000), // Exponential backoff
      staleTime: 5 * 60 * 1000, // 5 minutes
      gcTime: 10 * 60 * 1000
    },
    mutations: {
      retry: (failureCount, error) => {
        const axiosError = error as AxiosError
        const status = axiosError.response?.status

        // Do not retry on client-related errors
        if (status && status >= 400 && status < 500) {
          return false
        }

        // Retry up to 3 times for server error
        return failureCount < 2
      },
      retryDelay: 1000
    },
  },
  queryCache: new QueryCache({
    onError: (error: AxiosError) => {
      handleGlobalError(error, 'query')
    }
  }),

  mutationCache: new MutationCache({
    onError: (error: AxiosError) => {
      handleGlobalError(error, 'mutation')
    },
    onSuccess: (data, variables, context, mutation) => {
      console.log('✅ Mutation success:', {
        mutationKey: mutation.options.mutationKey,
        data
      })
    }
  })
})

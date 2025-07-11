import api from '@/infrastructure/api/api'
import {
  LOGIN_URL,
  LOGOUT_URL,
  REFRESH_URL,
  REGISTER_URL
} from '@/modules/register/domain/constants'
import { BaseFormData } from '@/modules/register/domain/interfaces'
import { useCallback, useRef } from 'react'
import { APIResponse } from '@/domain/types'
import { useBaseAuth } from './useBaseAuth'
import { useMutation } from '@tanstack/react-query'
import { AxiosError } from 'axios'
import { jwtDecode } from 'jwt-decode'
import useAuthStore from '@/presentation/stores/authStore'

export const useLogin = () =>
  useBaseAuth({
    mutationFn: async (credentials: BaseFormData) => {
      return await api.post(LOGIN_URL, credentials)
    },
    successMessage: 'Login successful!',
    errorMessage: 'Login failed!',
    shouldAuth: true,
    redirect: '/'
  })

export const useLogout = () => {
  const lastExecutionTime = useRef(0)

  // Create a stable throttled function
  const throttledLogout = useCallback(async (credentials: { refresh: string }) => {
    const now = Date.now()
    if (now - lastExecutionTime.current < 2000) {
      throw new Error('Logout request throttled.')
    }
    lastExecutionTime.current = now
    return await api.post(LOGOUT_URL, credentials)
  }, [])

  return useBaseAuth({
    mutationFn: throttledLogout,
    // mutationFn: async (credentials: { refresh: string }) => {
    //   return await api.post(LOGOUT_URL, credentials)
    // },
    successMessage: 'Logout successful!',
    errorMessage: 'Logout failed!',
    shouldAuth: false,
    redirect: '/login',
    onError: error => {
      if (error.message === 'Logout request throttled.') {
        // console.log('🛑 Logout throttled, ignoring')
        return
      }
    }
  })
}

export const useRegister = () =>
  useBaseAuth({
    mutationFn: async (credentials: BaseFormData) => {
      return await api.post(REGISTER_URL, credentials)
    },
    successMessage: 'Registration successful!',
    errorMessage: 'Registration failed!',
    shouldAuth: true,
    redirect: '/'
  })

type AuthTokens = {
  access: string
  refresh: string
}

export const useRefreshToken = () =>
  useMutation<APIResponse, AxiosError, AuthTokens>({
    mutationFn: async (tokens: AuthTokens) => {
      const decode = jwtDecode(tokens.access)
      const tokenExpiration = decode.exp
      const now = Date.now() / 1000

      if (tokenExpiration > now) {
        return await api.post(REFRESH_URL, { refresh: tokens.refresh })
      }
      return
    },
    onSuccess: response => {
      localStorage.setItem('access', response.data.access)
      useAuthStore.getState().setIsAuthorized(true)
    },
    onError: (error: AxiosError) => {
      if ((error.response as APIResponse)?.data?.message === 'Token is blacklisted') {
        localStorage.clear()
        useAuthStore.getState().setIsAuthorized(false)
        return
      }
      console.error('Token refresh failed:', error)
    }
  })

/* eslint-disable react-hooks/exhaustive-deps */
import { ACCESS_TOKEN, REFRESH_TOKEN, REFRESH_URL } from '@/modules/register/domain/constants'
import useAuthStore from '@/presentation/stores/authStore'
import { useEffect } from 'react'
import { Redirect } from 'wouter'
import { useRefreshToken } from '@/modules/register/interactors/mutations'

const ProtectedRoute = ({ children, url }) => {
  const { isAuthorized, setIsAuthorized } = useAuthStore()
  const { mutate, isPending } = useRefreshToken()
  const tokens = {
    access: localStorage.getItem(ACCESS_TOKEN),
    refresh: localStorage.getItem(REFRESH_TOKEN)
  }

  useEffect(() => {
    if (!tokens.access || !tokens.refresh) {
      setIsAuthorized(false)
      return
    }
    mutate(tokens)
  }, [])

  if (isPending) return <h1>LOADING...</h1>

  return isAuthorized ? children : <Redirect to={url} />
}

const ProtectedRegistrationRoute = ({ children, url }) => {
  const { isAuthorized, setIsAuthorized } = useAuthStore()
  const { mutate, isPending } = useRefreshToken()
  const tokens = {
    access: localStorage.getItem(ACCESS_TOKEN),
    refresh: localStorage.getItem(REFRESH_TOKEN)
  }

  useEffect(() => {
    if (!tokens.access || !tokens.refresh) {
      setIsAuthorized(false)
      return
    }
    mutate(tokens)
  }, [])

  if (isPending) return <h1>LOADING...</h1>

  return !isAuthorized ? children : <Redirect to={url} />
}
export { ProtectedRoute, ProtectedRegistrationRoute }

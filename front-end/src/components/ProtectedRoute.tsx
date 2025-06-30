import { useEffect, useState } from 'react'
import { jwtDecode } from 'jwt-decode'
import { ACCESS_TOKEN, REFRESH_TOKEN } from './api/constants'
import api from './api/api'
import { Redirect } from 'wouter'

const ProtectedRoute = ({ children }) => {
  const [isAuthorized, setIsAuthorized] = useState(null)

  useEffect(() => {
    auth().catch(() => setIsAuthorized(false))
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  const refreshToken = async () => {
    const refreshToken = localStorage.getItem(REFRESH_TOKEN)
    try {
      const response = await api.post('/api/token/refresh/', { refresh: refreshToken })
      if (response.status === 200) {
        localStorage.setItem(ACCESS_TOKEN, response.data.access)
        setIsAuthorized(true)
      }
      if (response.status !== 200) {
        console.error('Failed to refresh token')
        setIsAuthorized(false)
      }
    } catch (error) {
      console.error(error)
      setIsAuthorized(false)
    }
  }

  const auth = async () => {
    const token = localStorage.getItem(ACCESS_TOKEN)
    if (!token) {
      setIsAuthorized(false)
      return
    }
    const decode = jwtDecode(token)
    const tokenExpiration = decode.exp
    const now = Date.now() / 1000

    if (tokenExpiration < now) {
      await refreshToken()
    } else {
      setIsAuthorized(true)
    }
  }

  if (isAuthorized === null) {
    return <div>Loading...</div>
  }

  return isAuthorized ? children : <Redirect to="/login" />
}

export default ProtectedRoute

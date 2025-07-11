import api from '@/infrastructure/api/api'
import { LOGOUT_URL } from '@/modules/register/domain/constants'
import useAuthStore from '@/presentation/stores/authStore'
import { useLayoutEffect, useState } from 'react'
import { Redirect } from 'wouter'
import { useLogout } from '../../modules/register/interactors/mutations'

const Logout = () => {
  const [redirect, setRedirect] = useState(false)
  const { isAuthorized, setIsAuthorized } = useAuthStore()
  const { mutate } = useLogout()

  useLayoutEffect(() => {
    const logout = async () => {
      if (!isAuthorized) {
        setRedirect(true)
        return
      }

      const refresh = localStorage.getItem('refresh')
      mutate({ refresh })

      //   try {
      //     const response = await api.post(LOGOUT_URL, { refresh: refresh })
      //     console.log('✅ Logout API success:', response.status)
      //   } catch (error) {
      //     console.log('⚠️ Logout API failed, cleaning locally anyway')
      //     console.log('Error:', error.response)
      //   } finally {
      //     localStorage.clear()
      //     setIsAuthorized(false)
      //     setRedirect(true)
      //   }
    }

    logout()
  }, [isAuthorized, setIsAuthorized])

  if (redirect) return <Redirect to="/login" />

  return null

  // useEffect(() => {
  //   const logout = async () => {
  //     if (!isAuthorized) return

  //     const refreshToken = localStorage.getItem('refresh')

  //     try {
  //       const response = await api.post(LOGOUT_URL, { refresh: refreshToken })
  //       if (response.status === 200) {
  //         localStorage.clear()
  //         setIsAuthorized(false)
  //         setRedirect(true)
  //       }
  //       if (response.status === 400) {
  //         localStorage.clear()
  //         setRedirect(true)
  //       }
  //     } catch (error) {
  //       console.log('Logout Catch Error')
  //       if (error instanceof AxiosError) {
  //         if (error.response?.status === 400 || error.response?.status === 406) {
  //           localStorage.clear()
  //           setIsAuthorized(false)
  //           setRedirect(true)
  //           return
  //         }
  //         console.error('Error response:', error.response?.data?.message)
  //         return
  //       }
  //       console.error('Logout failed:', error)
  //     }
  //   }
  //   logout()
  // }, [])
}

export default Logout

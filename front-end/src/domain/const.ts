import { CookieOptions } from './types'

export const cookies = {
  set: (name: string, value: string, options: CookieOptions = {}) => {
    let cookieParts = [`${encodeURIComponent(name)}=${encodeURIComponent(value)}`]

    if (options.expires) {
      const expires =
        options.expires instanceof Date ? options.expires : new Date(Date.now() + options.expires)
      cookieParts.push(`Expires=${expires.toUTCString()}`)
    }
    if (options.maxAge) {
      cookieParts.push(`Max-Age=${options.maxAge}`)
    }
    if (options.domain) {
      cookieParts.push(`Domain=${options.domain}`)
    }
    if (options.path) {
      cookieParts.push(`Path=${options.path}`)
    }
    if (options.httpOnly) {
      cookieParts.push('HttpOnly')
    }
    if (options.secure) {
      cookieParts.push('Secure')
    }
    if (options.sameSite) {
      cookieParts.push(`SameSite=${options.sameSite}`)
    }

    document.cookie = cookieParts.join('; ')
  },
  get: (name: string): string | null => {
    const nameEQ = encodeURIComponent(name) + '='
    const cookies = document.cookie.split(';')

    for (let cookie of cookies) {
      let c = cookie.trim()
      if (c.indexOf(nameEQ) === 0) return decodeURIComponent(c.substring(nameEQ.length))
    }
    return null
  },
  remove: (name: string, options: Omit<CookieOptions, 'expires' | 'maxAge'> = {}) => {
    cookies.set(name, '', {
      ...options,
      expires: new Date(0) // Set expiration date to the past to remove the cookie
    })
  },
  exist: (name: string): boolean => {
    return cookies.get(name) !== null
  }
}

export const COOKIE_NAMES = {
  ACCESS_TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
  USER_DATA: 'auth_user_data',
  REMEMBER_ME: 'auth_remember_me'
} as const

export const COOKIE_CONFIGS = {
  SESSION: {
    path: '/',
    secure: import.meta.env.PROD,
    sameSite: 'Lax' as const
  },
  PERSISTENT: {
    path: '/',
    secure: import.meta.env.PROD,
    sameSite: 'Lax' as const,
    expires: 30 // 30 días
  },
  REMEMBER_ME_SHORT: {
    path: '/',
    secure: import.meta.env.PROD,
    sameSite: 'Lax' as const,
    expires: 7 // 7 días
  }
} as const

export type APIResponse = {
  data: {
    access?: string
    refresh?: string
    message: string
  }
  status: number
}
export interface CookieOptions {
  domain?: string
  expires?: Date | number
  httpOnly?: boolean
  maxAge?: number
  path?: string
  secure?: boolean
  sameSite?: 'Strict' | 'Lax' | 'None'
}

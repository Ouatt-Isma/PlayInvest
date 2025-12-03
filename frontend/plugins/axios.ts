// plugins/axios.ts
import axios from 'axios'

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const { token, logout, isTokenExpired } = useAuth()

  const api = axios.create({
    baseURL: config.public.apiBase,
    withCredentials: true,
    timeout: 15000,
  })

  // Attach token + check expiration
  api.interceptors.request.use((req) => {
    const jwt = token.value

    if (jwt) {
      if (isTokenExpired(jwt)) {
        logout()
        return Promise.reject(new Error("Token expired"))
      }

      req.headers = req.headers || {}
      req.headers.Authorization = `Bearer ${jwt}`
    }

    // Forward cookies during SSR
    if (process.server) {
      const cookie = useRequestHeaders(['cookie']).cookie
      if (cookie) {
        req.headers = req.headers || {}
        req.headers.Cookie = cookie
      }
    }

    return req
  })

  // Auto logout on backend 401
  api.interceptors.response.use(
    res => res,
    err => {
      if (err.response?.status === 401) {
        logout()
      }
      return Promise.reject(err)
    }
  )

  return { provide: { axios: api } }
})

import axios from 'axios'

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const api = axios.create({
    baseURL: config.public.apiBase,
    withCredentials: true,
    timeout: 15000,
  })

  api.interceptors.request.use((req) => {
    // Bearer from non-HttpOnly cookie, if applicable
    const token = useCookie('token').value
    if (token) {
      req.headers = req.headers || {}
      req.headers.Authorization = `Bearer ${token}`
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

  return { provide: { axios: api } }
})

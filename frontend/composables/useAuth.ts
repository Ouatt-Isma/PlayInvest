// composables/useAuth.ts
import { ref, computed } from 'vue'
import { useRouter, useCookie } from '#app'
import { jwtDecode } from "jwt-decode"

interface LightUser {
  id: number
  email: string
  name: string
  avatar_url?: string
}

const user = ref<LightUser | null>(null)
const token = ref<string | null>(null)
const isInitialized = ref(false)

export function useAuth() {
  const router = useRouter()

  // ----------------------------------------------------
  // TOKEN EXPIRATION CHECK
  // ----------------------------------------------------
  function isTokenExpired(tok: string | null) {
    if (!tok) return true
    try {
      const { exp } = jwtDecode<{ exp: number }>(tok)
      return Date.now() >= exp * 1000
    } catch {
      return true
    }
  }

  // ----------------------------------------------------
  // INITIALIZE AUTH FROM COOKIES (RUNS ONCE)
  // ----------------------------------------------------
  function init() {
    if (isInitialized.value) return

    const tokenCookie = useCookie<string | null>('token')
    const userCookie = useCookie<LightUser | null>('user')
    const avatarCookie = useCookie<string | null>('avatar_url')

    // 1) HANDLE TOKEN
    if (tokenCookie.value) {
      // EXPIRED TOKEN → AUTO LOGOUT
      if (isTokenExpired(tokenCookie.value)) {
        tokenCookie.value = null
        userCookie.value = null
        avatarCookie.value = null
        token.value = null
        user.value = null
        isInitialized.value = true
        return
      }

      // VALID TOKEN
      token.value = tokenCookie.value
    }

    // 2) HANDLE USER
    if (userCookie.value) {
      const lightUser = userCookie.value

      let avatar_url: string | null = null

      if (import.meta.client) {
        // Client: prefer localStorage (avatar may be updated locally)
        avatar_url = localStorage.getItem('avatar_url') || avatarCookie.value || null
      } else {
        // SSR: cookies only
        avatar_url = avatarCookie.value || null
      }

      // Normalize avatar path
      if (avatar_url) {
        avatar_url = avatar_url
          .replace('/_nuxt/public', '')
          .replace('/public', '')
          .replace(/^\/+/, '/')
      }

      user.value = { ...lightUser, avatar_url: avatar_url || undefined }
    }

    isInitialized.value = true
  }

  // ----------------------------------------------------
  // LOGIN USER
  // ----------------------------------------------------
  function login(userData: any, authToken: string) {
    const isProd = process.env.NODE_ENV === 'production'

    const tokenCookie = useCookie<string>('token', {
      sameSite: 'lax',
      secure: isProd,
      path: '/',
    })
    const userCookie = useCookie<LightUser>('user', {
      sameSite: 'lax',
      secure: isProd,
      path: '/',
    })
    const avatarCookie = useCookie<string>('avatar_url', {
      sameSite: 'lax',
      secure: isProd,
      path: '/',
    })

    let { avatar_url, ...lightUser } = userData

    // Normalize incoming avatar
    if (avatar_url?.startsWith('/_nuxt/public')) {
      avatar_url = avatar_url.replace('/_nuxt/public', '')
    }
    if (avatar_url?.startsWith('/public')) {
      avatar_url = avatar_url.replace('/public', '')
    }

    if (import.meta.client && avatar_url) {
      localStorage.setItem('avatar_url', avatar_url)
    }

    // Update global state
    token.value = authToken
    user.value = { ...lightUser, avatar_url }

    // Persist in cookies
    tokenCookie.value = authToken
    userCookie.value = lightUser
    avatarCookie.value = avatar_url || ''
  }

  // ----------------------------------------------------
  // LOGOUT USER
  // ----------------------------------------------------
  function logout() {
    const tokenCookie = useCookie<string | null>('token')
    const userCookie = useCookie<LightUser | null>('user')
    const avatarCookie = useCookie<string | null>('avatar_url')

    token.value = null
    user.value = null

    tokenCookie.value = null
    userCookie.value = null
    avatarCookie.value = null

    if (import.meta.client) {
      localStorage.removeItem('avatar_url')
    }

    router.push('/login')
  }

  // ----------------------------------------------------
  // CHECK AUTH (RUNS INIT)
  // ----------------------------------------------------
  function checkAuth() {
    if (!isInitialized.value) {
      init()
    }
    return isAuthenticated.value
  }

  // ----------------------------------------------------
  // COMPUTED: IS THE USER LOGGED IN?
  // ----------------------------------------------------
  const isAuthenticated = computed(() => !!user.value && !!token.value)

  return {
    user,
    token,
    isInitialized,
    init,
    login,
    logout,
    checkAuth,
    isAuthenticated,
    isTokenExpired, // exposed for axios plugin
  }
}

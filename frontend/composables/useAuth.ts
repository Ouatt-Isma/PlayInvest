// composables/useAuth.ts
import { ref, computed } from 'vue'
import { useRouter, useCookie } from '#app'

interface LightUser {
  id: number
  email: string
  name: string
  // add other fields you need
}

const user = ref<LightUser & { avatar_url?: string } | null>(null)
const token = ref<string | null>(null)
const isInitialized = ref(false)

export function useAuth() {
  const router = useRouter()

  /** Initialize authentication state (runs once globally) */
  function init() {
    if (isInitialized.value) return

    const tokenCookie = useCookie<string | null>('token')
    const userCookie = useCookie<LightUser | null>('user')
    const avatarCookie = useCookie<string | null>('avatar_url') // ✅ read avatar cookie for SSR

    if (tokenCookie.value) {
      token.value = tokenCookie.value
    }

    if (userCookie.value) {
      const lightUser = userCookie.value
      let avatar_url: string | null = null

      if (import.meta.client) {
        // ✅ Client side — prefer localStorage, fallback to cookie
        avatar_url = localStorage.getItem('avatar_url') || avatarCookie.value || null
      } else {
        // ✅ SSR — no access to localStorage
        avatar_url = avatarCookie.value || null
      }

      // ✅ Normalize potential wrong paths
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

  /** Log in the user and store credentials in cookies/localStorage */
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

    // ✅ Normalize if necessary
    if (avatar_url?.startsWith('/_nuxt/public')) {
      avatar_url = avatar_url.replace('/_nuxt/public', '')
    }
    if (avatar_url?.startsWith('/public')) {
      avatar_url = avatar_url.replace('/public', '')
    }

    if (import.meta.client && avatar_url) {
      localStorage.setItem('avatar_url', avatar_url)
    }

    // ✅ Update global refs
    token.value = authToken
    user.value = { ...lightUser, avatar_url }

    // ✅ Persist to cookies
    tokenCookie.value = authToken
    userCookie.value = lightUser
    avatarCookie.value = avatar_url || ''
  }

  /** Log out and clear all credentials */
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

  /** Check authentication state (ensures init runs) */
  function checkAuth() {
    if (!isInitialized.value) {
      init()
    }
    return isAuthenticated.value
  }

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
  }
}

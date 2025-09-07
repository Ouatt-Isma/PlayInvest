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

  function init() {
    if (isInitialized.value) return

    const tokenCookie = useCookie<string | null>('token')
    const userCookie = useCookie<LightUser | null>('user')

    if (tokenCookie.value) {
      token.value = tokenCookie.value
    }

    if (userCookie.value) {
      const lightUser = userCookie.value
      let avatar_url: string | null = null

      if (import.meta.client) {
        avatar_url = localStorage.getItem('avatar_url')
      }

      user.value = { ...lightUser, avatar_url: avatar_url || undefined }
    }

    isInitialized.value = true
  }

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

    const { avatar_url, ...lightUser } = userData

    if (import.meta.client && avatar_url) {
      localStorage.setItem('avatar_url', avatar_url)
    }

    token.value = authToken
    user.value = { ...lightUser, avatar_url }

    tokenCookie.value = authToken
    userCookie.value = lightUser // 🚨 store as object (no stringify)
  }

  function logout() {
    const tokenCookie = useCookie<string | null>('token')
    const userCookie = useCookie<LightUser | null>('user')

    token.value = null
    user.value = null

    tokenCookie.value = null
    userCookie.value = null

    if (import.meta.client) {
      localStorage.removeItem('avatar_url')
    }

    router.push('/login')
  }

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

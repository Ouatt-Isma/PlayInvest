// composables/useAuth.ts
import { ref, computed } from 'vue'
import { useRouter, useCookie } from '#app'

const user = ref<any | null>(null)
const token = ref<string | null>(null)
const isInitialized = ref(false)

export function useAuth() {
  const router = useRouter()

  function init() {
    if (isInitialized.value) return

    const tokenCookie = useCookie<string | null>('token')
    const userCookie = useCookie<string | null>('user')

    if (tokenCookie.value) {
      token.value = tokenCookie.value
    }

    if (userCookie.value) {
      try {
        const lightUser = JSON.parse(userCookie.value)
        const avatar_url = localStorage.getItem('avatar_url') || null

        user.value = { ...lightUser, avatar_url }
      } catch (e) {
        console.error('[init] failed to parse user cookie:', e)
        user.value = null
      }
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
    const userCookie = useCookie<string>('user', {
      sameSite: 'lax',
      secure: isProd,
      path: '/',
    })

    const { avatar_url, ...lightUser } = userData
    if (avatar_url) {
      localStorage.setItem('avatar_url', avatar_url)
    }

    token.value = authToken
    user.value = { ...lightUser, avatar_url }   // ✅ keep avatar in memory too

    tokenCookie.value = authToken
    userCookie.value = JSON.stringify(lightUser)

    console.log('[login] token =', authToken)
    console.log('[login] userData =', userData)
    console.log('[login] userCookie.value =', userCookie.value)
  }

  function logout() {
    const tokenCookie = useCookie<string | null>('token')
    const userCookie = useCookie<string | null>('user')

    token.value = null
    user.value = null

    tokenCookie.value = null
    userCookie.value = null
    localStorage.removeItem('avatar_url')

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

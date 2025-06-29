// composables/useUser.ts
import { ref } from 'vue'

export interface UserCookie {
  id: number
  username: string
  first_name: string
  avatar_url?: string
  token: string 
}

<script setup lang="ts">
import { ref } from 'vue'
// import type {UserCookie} from '@/composables/useUser'
import axios from 'axios'
// const usercook = useCookie<UserCookie>('user', { path: '/' })
const avatarUrltmp =  ref('')

onMounted(() => {
  const storedAvatar = localStorage.getItem('avatar_url')
  if (storedAvatar) {
    avatarUrltmp.value = storedAvatar
  }
  else{
    avatarUrltmp.value = 'icons/default.png'
  }
})

const toastMessage = ref('')
const showToast = ref(false)


const form = ref({
  first_name: '',
  last_name: '',
  birthdate: null,
  phone_number: '',
  username: '',
  email:'',
})

onMounted(async () => {
  const token = localStorage.getItem("token") // ✅ Safe inside onMounted

  if (!token) {
    console.warn("No token found in localStorage")
    return
  }

  try {
    
    const res = await axios.get('http://localhost:8000/users/me', {
    headers: {
        Authorization: `Bearer ${token}`
    }
    })
    const user = res.data

    form.value.first_name = user.first_name || ''
    form.value.last_name = user.last_name || ''
    form.value.birthdate = user.birthdate || null
    form.value.phone_number = user.phone_number || ''
    form.value.username = user.username || ''
    form.value.email = user.email || ''
  } catch (err) {
    console.error("Erreur en récupérant l'utilisateur :", err)
  }
})

const updateProfile = async ()  => {
  const token = localStorage.getItem("token") // ✅ Safe inside onMounted

  if (!token) {
    console.warn("No token found in localStorage")
    return
  }
  try {
    console.log('Infos envoyées:', form.value)
    const payload = {
      ...form.value,
      avatar_url: avatarUrl.value  // ← ajoute ici l'avatar sélectionné
    }
    // Cast as indexable object for safe mutation
    const cleanedPayload: { [key: string]: any } = { ...payload };
    Object.keys(cleanedPayload).forEach(key => {
    if (cleanedPayload[key] === '') {
      cleanedPayload[key] = null;
    }
    });
    const res = await axios.put('http://localhost:8000/users/me', cleanedPayload, {
      headers: {
        Authorization: `Bearer ${token}`  // assure-toi que `token` est défini
      }
    })
    localStorage.setItem("first_name", form.value.first_name)
    localStorage.setItem("avatar_url", avatarUrl.value )
    
    console.log('Profil mis à jour avec succès:', res.data)
    toastMessage.value = '✅ Profil mis à jour avec succès!'
    showToast.value = true
    setTimeout(() => {
      showToast.value = false
    }, 3000)

  } catch (err) {
    console.error('Erreur lors de la mise à jour du profil:', err)
    const error_value = "Erreur lors de la mise à jour du profil: "+err
    toastMessage.value = '❌ ' + error_value
    showToast.value = true
    setTimeout(() => {
      showToast.value = false
    }, 3000)

    // Afficher un message d'erreur si besoin
  }

}
const showAvatarList = ref(false)
const avatarUrl = ref(avatarUrltmp)
const avatarOptions = Object.values(
  import.meta.glob('/public/icons/avatars/*.png', { eager: true, as: 'url' })
)

function selectAvatar(url: string) {
  avatarUrl.value = url
  showAvatarList.value = false // cacher la liste après sélection
}

function toggleAvatarList() {
  showAvatarList.value = !showAvatarList.value
}

function downloadAvatar() {
  if (!avatarUrl.value) return

  const link = document.createElement('a')
  link.href = avatarUrl.value
  link.download = 'avatar.png' // tu peux rendre le nom dynamique si besoin
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}
</script>

<template>
  <div class="bg-white dark:bg-gray-900 text-gray-900 dark:text-white p-6 rounded-lg shadow-md w-full">
    <h2 class="text-2xl font-bold mb-6">Informations personnelles</h2>

    
    <!-- Avatar Preview and Actions -->
    <div class="flex items-center space-x-4 mb-6">
  <img :src="avatarUrl" alt="Avatar" class="w-20 h-20 rounded-full border" @click="toggleAvatarList"/>
  <div class="space-x-2">
    <!-- <button @click="downloadAvatar" class="bg-teal-800 text-white px-4 py-2 rounded">Télécharger</button> -->
    <button @click="avatarUrl = ''" class="border px-4 py-2 rounded">Supprimer</button>
  </div>
</div>

<!-- Liste d'avatars à sélectionner -->
<div v-if="showAvatarList" class="grid grid-cols-5 gap-4">
  <div
    v-for="(avatar, index) in avatarOptions"
    :key="index"
    @click="selectAvatar(avatar)"
    class="cursor-pointer border rounded-full p-1 hover:ring-2 hover:ring-teal-600"
    :class="{ 'ring-2 ring-teal-800': avatar === avatarUrl }"
  >
    <img :src="avatar" class="w-16 h-16 rounded-full" />
  </div>
</div>

    <form @submit.prevent="updateProfile" class="space-y-6">
      <div class="grid grid-cols-2 gap-4">
        <div>
          <label class="block text-sm font-medium">Prénom</label>
          <input v-model="form.first_name" type="text" class="w-full mt-1 rounded border p-2" />
        </div>
        <div>
          <label class="block text-sm font-medium">Nom de famille</label>
          <input v-model="form.last_name" type="text" class="w-full mt-1 rounded border p-2" />
        </div>
        <div>
          <label class="block text-sm font-medium">Nom d'utilisateur</label>
          <input v-model="form.username" type="text" class="w-full mt-1 rounded border p-2" />
        </div>
        <div>
          <label class="block text-sm font-medium">Date de naissance</label>
          <input v-model="form.birthdate" type="date" class="w-full mt-1 rounded border p-2" />
        </div>
        <div>
          <label class="block text-sm font-medium">Numéro de téléphone</label>
          <input v-model="form.phone_number" type="text" class="w-full mt-1 rounded border p-2" />
        </div>
      </div>

      <div>
        <label class="block text-sm font-medium">Votre e-mail</label>
        <input v-model="form.email" type="email" class="w-full bg-gray-100 text-gray-500" readonly disable />
      </div>

      <!-- <div>
        <label class="block text-sm font-medium">Nouvel e-mail</label>
        <input v-model="form.new_email" type="email" class="w-full mt-1 rounded border p-2" />
      </div> -->

      <button type="submit" class="bg-teal-800 text-white px-6 py-3 rounded mt-4">
        Sauvegarder
      </button>
    </form>
    <transition name="fade">
      <div
        v-if="showToast"
        class="fixed top-6 right-6 bg-white shadow-lg rounded px-6 py-4 border border-gray-200 text-sm text-gray-800 z-50"
      >
        {{ toastMessage }}
      </div>
    </transition>
  </div>
  
</template>

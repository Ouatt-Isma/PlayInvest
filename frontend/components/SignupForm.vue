<!-- 
<script setup>
defineProps({
  submitForm: {
    type: Function,
    required: true
  }
});
</script>

<template>
  <div class="w-full max-w-md space-y-6">
    <h1 class="text-2xl font-bold text-gray-800 text-center">
      Inscrivez-vous pour un compte
    </h1>

    <form class="space-y-4" @submit.prevent="submitForm">
      <input
        type="text"
        placeholder="Nom d'utilisateur"
        class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring focus:border-teal-600"
      />
      <input
        type="email"
        placeholder="Email"
        class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring focus:border-teal-600"
      />
      <div class="relative">
        <input
          type="password"
          placeholder="Mot de passe"
          class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring focus:border-teal-600 pr-10"
        />
        <span class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 cursor-pointer">
          👁️
        </span>
      </div>
      <p class="text-sm text-gray-500">Votre mot de passe doit comporter au moins 8 caractères</p>

      <div class="flex items-start space-x-2">
        <input type="checkbox" id="terms" class="mt-1" />
        <label for="terms" class="text-sm text-gray-600">
          En créant un compte, vous acceptez les
          <a href="#" class="text-teal-700 font-medium hover:underline">Conditions d'utilisation</a>
          et notre
          <a href="#" class="text-teal-700 font-medium hover:underline">Politique de confidentialité</a>.
        </label>
      </div>

      <button
        type="submit"
        class="w-full bg-[#0D5254] hover:bg-teal-900 text-white py-3 rounded-lg font-semibold transition duration-200"
      >
        S'inscrire
      </button>
    </form>

    <div class="relative">
      <div class="absolute inset-0 flex items-center">
        <div class="w-full border-t border-gray-300"></div>
      </div>
      <div class="relative flex justify-center text-sm">
        <span class="bg-white px-2 text-gray-500">Ou inscrivez-vous avec</span>
      </div>
    </div>

    <div class="flex gap-4 justify-between">
      <button class="w-full border py-2 rounded-lg flex justify-center items-center gap-2">
        <img src="/logos/google.webp" class="h-5" />
        <span>Google</span>
      </button>
      <button class="w-full border py-2 rounded-lg flex justify-center items-center gap-2">
        <img src="/logos/facebook.webp" class="h-5" />
        <span>Facebook</span>
      </button>
    </div>

    <p class="text-center text-sm text-gray-500">
      Vous avez déjà un compte ?
      <a href="/login" class="text-teal-700 font-medium hover:underline">Connectez-vous</a>
    </p>
  </div>
</template> -->



<script setup>
import { reactive } from 'vue'

const showPassword = ref(false)

const togglePassword = () => {
  showPassword.value = !showPassword.value
}
const props = defineProps({
  submitForm: {
    type: Function,
    required: true
  }
})

const form = reactive({
  username: '',
  email: '',
  password: '',
  referrer_id:'',
})

const handleSubmit = () => {
  props.submitForm({ ...form })
}
</script>

<template>
  <div class="w-full max-w-md space-y-6">
    <h1 class="text-2xl font-bold text-gray-800 text-center">
      Inscrivez-vous pour un compte
    </h1>

    <form class="space-y-4" @submit.prevent="handleSubmit">
      <input
        v-model="form.username"
        type="text"
        placeholder="Nom d'utilisateur"
        class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring focus:border-teal-600"
      />
      <input
        v-model="form.email"
        type="email"
        placeholder="Email"
        class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring focus:border-teal-600"
      />
      <input
        v-model="form.referrer_id"
        type="text"
        placeholder="Nom d'utilisateur du parrain"
        class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring focus:border-teal-600"
      />
      <div class="relative">
        <input
          v-model="form.password"
          :type="showPassword ? 'text' : 'password'"
          placeholder="Mot de passe"
          class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring focus:border-teal-600 pr-10"
        />
        <span class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 cursor-pointer"
        @click="togglePassword">
          {{ showPassword ? '🙈' : '👁️' }}
        </span>
      </div>
      <div class="flex items-start space-x-2">
        <input type="checkbox" id="terms" class="mt-1" required/>
        <label for="terms" class="text-sm text-gray-600">
          En créant un compte, vous acceptez les
          <a href="#" class="text-teal-700 font-medium hover:underline">Conditions d'utilisation</a>
          et notre
          <a href="#" class="text-teal-700 font-medium hover:underline">Politique de confidentialité</a>.
        </label>
      </div>
      <!-- Terms, button, etc remain unchanged -->
      <button
        type="submit"
        class="w-full bg-[#0D5254] hover:bg-teal-900 text-white py-3 rounded-lg font-semibold transition duration-200"
      >
        S'inscrire
      </button>
    </form>

    <div class="relative">
      <div class="absolute inset-0 flex items-center">
        <div class="w-full border-t border-gray-300"></div>
      </div>
      <div class="relative flex justify-center text-sm">
        <span class="bg-white px-2 text-gray-500">Ou inscrivez-vous avec</span>
      </div>
    </div>

    <div class="flex gap-4 justify-between">
      <NuxtLink to="/account" class="w-full border py-2 rounded-lg flex justify-center items-center gap-2">
        <img src="/logos/google.webp" class="h-5" />
        <span>Google</span>
        </NuxtLink>
      <NuxtLink to="/account" class="w-full border py-2 rounded-lg flex justify-center items-center gap-2">
     
        <img src="/logos/facebook.webp" class="h-5" />
        <span>Facebook</span>
      </NuxtLink>
    </div>

    <p class="text-center text-sm text-gray-500">
      Vous avez déjà un compte ?
      <a href="/login" class="text-teal-700 font-medium hover:underline">Connectez-vous</a>
    </p>
  </div>
</template>


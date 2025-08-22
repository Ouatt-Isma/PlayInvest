<script setup>
import { reactive } from 'vue'
import countries from '@/assets/data/countries.json'

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
  currency: '',
  profession: '',
  living_country: '',
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
      <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Nom d'utilisateur <span class="text-red-500">*</span>
      </label>
      <input
        v-model="form.username"
        type="text"
        class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring focus:border-teal-600"
      />
      </div>
      <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Addresse mail <span class="text-red-500">*</span>
      </label>
      <input
        v-model="form.email"
        type="email"
        class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring focus:border-teal-600"
      />
      </div>
      <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">
        Nom d'utilisateur du parrain
      </label>
      <input
        v-model="form.referrer_id"
        type="text"
        class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring focus:border-teal-600"
      />
      </div>
      <div class="relative">
        <label class="block text-sm font-medium text-gray-700 mb-1">
        Mot d passe <span class="text-red-500">*</span>
      </label>
        <!-- <input
          v-model="form.password"
          :type="showPassword ? 'text' : 'password'"
          placeholder="Mot de passe"
          class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring focus:border-teal-600 pr-10"
        /> -->
        <input
          v-model="form.password"
          :type="showPassword ? 'text' : 'password'"
          class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring focus:border-teal-600 pr-10"
        />
        <span class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 cursor-pointer"
        @click="togglePassword">
          {{ showPassword ? '🙈' : '👁️' }}
        </span>
      </div>

<div class="grid grid-cols-2 gap-4">
  <!-- Devise -->
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-1">
      Devise <span class="text-red-500">*</span>
    </label>
    <select
      v-model="form.currency"
      required
      class="w-full border border-gray-300 rounded-lg px-4 py-3 bg-white focus:outline-none focus:ring focus:border-teal-600"
    >
      <option value="" disabled></option>
      <option value="EUR">Euro (EUR)</option>
      <option value="USD">Dollar Américain (USD)</option>
      <option value="XOF">Franc CFA (XOF)</option>
    </select>
  </div>

  <!-- Profession -->
  <div>
    <label class="block text-sm font-medium text-gray-700 mb-1">
      Profession 
    </label>
    <input
      v-model="form.profession"
      type="text"
      class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring focus:border-teal-600"
    />
  </div>
</div>


<div>
  <label class="block text-sm font-medium text-gray-700 mb-1">
    Pays de résidence 
  </label>
  <select
    v-model="form.living_country"
    class="w-full border border-gray-300 rounded-lg px-4 py-3 bg-white focus:outline-none focus:ring focus:border-teal-600"
  >
    <option value="" disabled>Sélectionnez un pays</option>
    <option
      v-for="country in countries"
      :key="country.code"
      :value="country.code"
    >
      {{ country.name }}
    </option>
  </select>
</div>


        <p class="text-sm text-gray-500 text-center">
          <span class="text-red-500">*</span> Champs obligatoires
        </p>
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


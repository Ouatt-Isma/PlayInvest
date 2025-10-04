<script setup>
import { reactive, ref, computed } from 'vue'
import countries from '@/assets/data/countries.json'

const showPassword = ref(false)
const showConfirmPassword = ref(false)

const togglePassword = () => (showPassword.value = !showPassword.value)
const toggleConfirmPassword = () => (showConfirmPassword.value = !showConfirmPassword.value)

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
  confirm_password: '',
  referrer_id: '',
  currency: '',
  profession: '',
  living_country: ''
})

const passwordError = ref('')
const confirmError = ref('')

const validatePassword = (password) => {
  if (password.length < 8) return "Au moins 8 caractères"
  if (!/[A-Z]/.test(password)) return "Doit contenir une majuscule"
  if (!/[a-z]/.test(password)) return "Doit contenir une minuscule"
  if (!/[0-9]/.test(password)) return "Doit contenir un chiffre"
  // if (!/[!@#$%^&*(),.?\":{}|<>]/.test(password)) return "Doit contenir un caractère spécial"
  return ""
}

// ✅ Computed rules list for visual feedback
const passwordRules = computed(() => {
  const pwd = form.password
  return [
    { text: "Au moins 8 caractères", valid: pwd.length >= 8 },
    { text: "Contient une majuscule", valid: /[A-Z]/.test(pwd) },
    { text: "Contient une minuscule", valid: /[a-z]/.test(pwd) },
    { text: "Contient un chiffre", valid: /[0-9]/.test(pwd) },
    // { text: "Contient un caractère spécial (!@#$...)", valid: /[!@#$%^&*(),.?\":{}|<>]/.test(pwd) },
  ]
})

const handleSubmit = () => {
  passwordError.value = validatePassword(form.password)
  confirmError.value = form.password !== form.confirm_password ? "Les mots de passe ne correspondent pas" : ""
  if (passwordError.value || confirmError.value) return
  const { confirm_password, ...dataToSubmit } = form
  props.submitForm(dataToSubmit)
}
</script>

<template>
  <div class="w-full max-w-md space-y-6">
    <h1 class="text-2xl font-bold text-gray-800 text-center">
      Inscrivez-vous pour un compte
    </h1>

    <form class="space-y-4" @submit.prevent="handleSubmit">

      <!-- Username -->
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

      <!-- Email -->
      <div>
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Adresse mail <span class="text-red-500">*</span>
        </label>
        <input
          v-model="form.email"
          type="email"
          class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring focus:border-teal-600"
        />
      </div>

      <!-- Referrer -->
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

      <!-- Password -->
      <div class="relative">
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Mot de passe <span class="text-red-500">*</span>
        </label>
        <input
          v-model="form.password"
          :type="showPassword ? 'text' : 'password'"
          class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring focus:border-teal-600 pr-10"
          autocomplete="new-password"
          />
        <span
    class="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-500 hover:text-gray-700 cursor-pointer"
    @click="togglePassword"
  >
    <!-- 👁 Eye -->
    <svg v-if="!showPassword" xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z" />
    </svg>

    <!-- 🚫 Eye Slash -->
    <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M13.875 18.825A10.05 10.05 0 0112 19c-4.477 0-8.268-2.943-9.542-7a9.956 9.956 0 012.67-4.592M6.223 6.223A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.542 7a9.956 9.956 0 01-4.06 5.233M9.88 9.88a3 3 0 104.24 4.24" />
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
        d="M3 3l18 18" />
    </svg>
  </span>
        <p v-if="passwordError" class="text-red-500 text-sm mt-1">{{ passwordError }}</p>

        <!-- ✅ Password rule checklist -->
        <ul class="mt-2 space-y-1 text-sm">
          <li
            v-for="rule in passwordRules"
            :key="rule.text"
            class="flex items-center"
            :class="rule.valid ? 'text-green-600' : 'text-gray-500'"
          >
            <span class="mr-2">
              {{ rule.valid ? '✅' : '⚪' }}
            </span>
            {{ rule.text }}
          </li>
        </ul>
      </div>

      <!-- Confirm password -->
      <div class="relative">
        <label class="block text-sm font-medium text-gray-700 mb-1">
          Confirmez le mot de passe <span class="text-red-500">*</span>
        </label>
        <input
          v-model="form.confirm_password"
          :type="showPassword ? 'text' : 'password'"
          class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring focus:border-teal-600 pr-10"
          autocomplete="new-password"
          />
        <p v-if="confirmError" class="text-red-500 text-sm mt-1">{{ confirmError }}</p>
      </div>

      <!-- Currency / Profession -->
      <div class="grid grid-cols-2 gap-4">
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

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">Profession</label>
          <input
            v-model="form.profession"
            type="text"
            class="w-full border border-gray-300 rounded-lg px-4 py-3 focus:outline-none focus:ring focus:border-teal-600"
          />
        </div>
      </div>

      <!-- Country -->
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
        <input type="checkbox" id="terms" class="mt-1" required />
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
        <div class="w-full border-t border-gray-300">

        </div> 
      </div> 
      <div class="relative flex justify-center text-sm"> 
        <span class="bg-white px-2 text-gray-500">Ou inscrivez-vous avec</span> 
      </div> 
    </div> 
    <div class="flex gap-4 justify-between"> 
      <NuxtLink to="/account" class="w-full border py-2 rounded-lg flex justify-center items-center gap-2"> <img src="/logos/google.webp" class="h-5" /> <span>Google</span> 
      </NuxtLink> 
      <NuxtLink to="/account" class="w-full border py-2 rounded-lg flex justify-center items-center gap-2"> <img src="/logos/facebook.webp" class="h-5" /> <span>Facebook</span> </NuxtLink> 
    </div> <p class="text-center text-sm text-gray-500"> Vous avez déjà un compte ? <a href="/login" class="text-teal-700 font-medium hover:underline">Connectez-vous</a> </p> 
  </div>
</template>

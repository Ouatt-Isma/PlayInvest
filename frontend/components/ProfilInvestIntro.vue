<template>
  <div class="container mx-auto max-w-xl p-4">
    <div class="bg-white border rounded-2xl shadow p-6">
      <h2 class="text-xl font-bold mb-2">Profil Investisseur</h2>
      <p class="text-gray-600 mb-4">
        Faites le test, découvrez votre profil et débloquez des contenus adaptés.
      </p>

      <!-- ✅ IF loading -->
      <div v-if="loading" class="text-gray-500 text-sm mb-4">
        Chargement du profil en cours...
      </div>

      <!-- ✅ IF user has a profile -->
      <div v-else-if="profile" class="flex flex-col gap-4 mb-4">
        <div class="flex items-center gap-3">
          <span
            class="bg-blue-100 text-blue-800 font-semibold border border-blue-300 px-3 py-1 rounded-full text-sm"
          >
            🎯 Profil actuel : {{ profile }}
          </span>
        </div>

        <a
          href="/profil-investisseur"
          class="bg-yellow-500 hover:bg-yellow-600 text-white font-semibold px-4 py-2 rounded-lg inline-flex items-center gap-2 justify-center"
        >
          🔁 Refaire le test
        </a>
      </div>

      <!-- ✅ ELSE: if no profile yet -->
      <div v-else class="flex items-center gap-4 flex-wrap mb-4">
        <a
          href="/profil-investisseur"
          class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded-lg inline-flex items-center gap-2"
        >
          👉 Faire le test maintenant
        </a>
        <span
          class="bg-green-100 text-green-800 font-semibold border border-green-300 px-3 py-1 rounded-full text-sm"
        >
          +100 € fictifs à débloquer
        </span>
      </div>

      <p class="text-gray-600 text-sm leading-relaxed">
        Connaître votre profil investisseur, c’est comprendre votre rapport au risque et vos objectifs financiers.
        Le test PlayInvest, composé de 30 questions, évalue votre tolérance au risque et vous attribue un profil :
        <em>Prudent</em>, <em>Modéré</em>, <em>Équilibré</em>, <em>Dynamique</em> ou <em>Audacieux</em>.
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";

// ✅ Reactive state
const profile = ref(null);
const loading = ref(true);

const config = useRuntimeConfig()
const apiBase = config.public.apiBase
const token = useCookie("token").value;

// ✅ Fetch the profile from the API
async function fetchProfile() {
  try {
    const res = await axios.get(`${apiBase}/api/investor_profil`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    profile.value = res.data?.profile_level || null; // adjust field name if different
  } catch (err) {
    console.error("Erreur lors du chargement du profil :", err);
    profile.value = null;
  } finally {
    loading.value = false;
  }
}

// ✅ Call API on mount
onMounted(() => {
  fetchProfile();
});
</script>

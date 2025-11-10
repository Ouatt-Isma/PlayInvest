<template>
  <div class="container mx-auto max-w-5xl py-8 px-4">
    <!-- Header -->
    <div class="flex items-center gap-4 mb-6">
      <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-blue-600 to-green-500 grid place-items-center text-white font-bold">PI</div>
      <div>
        <h1 class="text-2xl sm:text-3xl font-bold">Test de Profil Investisseur — 30 questions</h1>
        <p class="text-gray-500 text-sm">Déterminez votre profil (Prudent → Audacieux) selon vos objectifs et votre tolérance au risque.</p>
      </div>
    </div>

    <!-- Main Layout -->
    <div class="grid lg:grid-cols-[1fr_320px] gap-6">
      <!-- Left: Quiz -->
      <main>
        <!-- Quiz Form -->
        <div v-if="!showResult" class="card">
          <div class="flex flex-wrap gap-2 mb-3">
            <span class="chip">{{ answered }}/30 répondues</span>
            <span class="chip">Durée ~ 5 min</span>
            <span class="chip">Barème 1 à 5 pts / question</span>
          </div>

          <!-- Progress Bar -->
          <div class="h-2 bg-gray-100 border border-gray-200 rounded-full overflow-hidden mb-6">
            <div class="h-full bg-gradient-to-r from-blue-600 to-green-500 transition-all duration-300" :style="{ width: `${(answered/30)*100}%` }"></div>
          </div>

          <!-- Questions -->
          <form @submit.prevent="calculateProfile" class="space-y-4">
            <fieldset v-for="(q, idx) in questions" :key="q.id" class="border border-gray-200 rounded-xl p-4">
              <h3 class="font-semibold text-base mb-2">{{ idx + 1 }}. {{ q.label }}</h3>
              <div class="grid gap-2">
                <label
                  v-for="(opt, j) in q.opt"
                  :key="j"
                  class="flex items-start gap-2 bg-gray-50 hover:bg-gray-100 border border-gray-200 rounded-lg p-2 cursor-pointer"
                >
                  <input
                    type="radio"
                    :name="`q${q.id}`"
                    :value="opt.s"
                    v-model="answers[q.id]"
                    @change="updateProgress"
                    class="mt-1 accent-green-600"
                  />
                  <span><strong>{{ String.fromCharCode(65 + j) }}.</strong> {{ opt.t }}</span>
                </label>
              </div>
            </fieldset>
            <div class="flex gap-3 mt-4">
              <button type="submit" class="bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg font-semibold">
                Calculer mon profil
              </button>
            </div>
          </form>
        </div>

        <!-- Result Card -->
        <div v-else class="card space-y-3">
          <div class="flex flex-wrap gap-2 items-center">
            <span :class="['badge', profileBadgeClass]">{{ profileResult.name }}</span>
            <span class="chip">Score: {{ totalScore }} / 150</span>
          </div>
          <p class="text-lg font-semibold">{{ profileResult.emoji }} Votre résultat : Profil {{ profileResult.name }}</p>
          <p class="text-gray-500 text-sm">Score typique : {{ profileResult.range[0] }}–{{ profileResult.range[1] }}</p>
          <p>{{ profileResult.desc }}</p>

          <div class="grid gap-4 mt-3">
            <div class="q">
              <h3 class="font-semibold">🧩 Allocation recommandée</h3>
              <ul class="list-disc list-inside text-gray-600 text-sm">
                <li v-for="a in profileResult.alloc" :key="a">{{ a }}</li>
              </ul>
            </div>

            <div class="q">
              <h3 class="font-semibold">🧠 Comportements & pièges fréquents</h3>
              <ul class="list-disc list-inside text-gray-600 text-sm">
                <li v-for="b in profileResult.biases" :key="b">{{ b }}</li>
              </ul>
            </div>

            <div class="q">
              <h3 class="font-semibold">📚 Conseils pour progresser</h3>
              <ul class="list-disc list-inside text-gray-600 text-sm">
                <li v-for="l in profileResult.learning" :key="l">{{ l }}</li>
              </ul>
            </div>

            <div class="q">
              <h3 class="font-semibold">⚠️ Risques à surveiller</h3>
              <ul class="list-disc list-inside text-gray-600 text-sm">
                <li v-for="r in profileResult.risks" :key="r">{{ r }}</li>
              </ul>
            </div>
          </div>

          <div class="flex gap-3 mt-4">
            <button @click="resetForm" class="border border-gray-300 px-4 py-2 rounded-lg hover:bg-gray-100">
              Modifier mes réponses
            </button>
            <button @click="exportJson" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
              Exporter JSON
            </button>
          </div>
        </div>
      </main>

      <!-- Right Panel -->
      <aside>
        <div class="card sticky top-4">
          <h3 class="font-semibold mb-2">Barème & Profils</h3>
          <ul class="text-sm text-gray-600 space-y-1">
            <li><strong>30–55</strong> : <span class="badge r-prudent">Prudent</span></li>
            <li><strong>56–85</strong> : <span class="badge r-modere">Modéré</span></li>
            <li><strong>86–115</strong> : <span class="badge r-equilibre">Équilibré</span></li>
            <li><strong>116–135</strong> : <span class="badge r-dynamique">Dynamique</span></li>
            <li><strong>136–150</strong> : <span class="badge r-audacieux">Audacieux</span></li>
          </ul>
          <p class="text-gray-500 text-xs mt-2">
            Répondez à toutes les questions. Chaque choix vaut 1 à 5 points.
          </p>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";
const config = useRuntimeConfig()
const apiBase = config.public.apiBase 
// -------------------- Data --------------------
const showResult = ref(false);
const answered = ref(0);
const totalScore = ref(0);
const answers = ref({});
const profileResult = ref(null);

// Your quiz data (same as before)
import { questions, profiles } from "@/data/investQuizData"; // put the arrays in a separate file

// -------------------- Methods --------------------
function updateProgress() {
  answered.value = Object.keys(answers.value).length;
}

function calculateProfile() {
  if (answered.value < 30) {
    alert(`Veuillez répondre à toutes les questions (${30 - answered.value} manquantes).`);
    return;
  }

  let score = 0;
  for (const k in answers.value) score += Number(answers.value[k]);
  totalScore.value = score;

  const prof = profiles.find(p => score >= p.range[0] && score <= p.range[1]);
  if (!prof) return alert("Score hors barème.");
  profileResult.value = prof;
  showResult.value = true;

  // Send result + reward
  sendRewardAndResult(prof, score);
}

async function sendRewardAndResult(profile, score) {
  const token = localStorage.getItem("token");
  const fieldName = "profil_investisseur_completed";
  const amount = 100;

  try {
    const token = useCookie("token").value
    // Save quiz result
    await axios.post(
      `${apiBase}/api/profile_quiz_result?profile=${profile.name}&score=${score}/`,
      { headers: { Authorization: `Bearer ${token}` } }
    );

    // Reward the user
    
    const response = await axios.get(`${apiBase}/api/reward?field_name=profile`,{
    headers: {
      Authorization: `Bearer ${token}`  // assure-toi que `token` est défini
    }});

    alert(response.data.message || "Profil enregistré et récompense ajoutée !");
  } catch (err) {
    alert("Erreur lors de l'enregistrement ou de la récompense.");
    console.error(err);
  }
}

function resetForm() {
  showResult.value = false;
  answers.value = {};
  answered.value = 0;
}

function exportJson() {
  const payload = {
    createdAt: new Date().toISOString(),
    score: totalScore.value,
    profile: profileResult.value.name,
    answers: answers.value
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = "profil-investisseur-playinvest.json";
  a.click();
  URL.revokeObjectURL(url);
}

// -------------------- Computed --------------------
const profileBadgeClass = computed(() => {
  if (!profileResult.value) return "";
  return {
    "r-prudent": profileResult.value.name === "Prudent",
    "r-modere": profileResult.value.name === "Modéré",
    "r-equilibre": profileResult.value.name === "Équilibré",
    "r-dynamique": profileResult.value.name === "Dynamique",
    "r-audacieux": profileResult.value.name === "Audacieux"
  };
});
</script>

<style scoped>
.card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 1rem;
  padding: 1.5rem;
  box-shadow: 0 6px 16px rgba(2, 6, 23, 0.08);
}
.q {
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 0.75rem;
  padding: 0.75rem;
}
.chip {
  background: #f8fafc;
  border: 1px solid #e5e7eb;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  color: #475569;
}
.badge {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-weight: 700;
  font-size: 0.75rem;
}
.r-prudent {
  background: #dcfce7;
  color: #065f46;
  border: 1px solid #86efac;
}
.r-modere {
  background: #dbeafe;
  color: #1e3a8a;
  border: 1px solid #93c5fd;
}
.r-equilibre {
  background: #fef3c7;
  color: #7c2d12;
  border: 1px solid #fcd34d;
}
.r-dynamique {
  background: #ffe4d5;
  color: #7c2d12;
  border: 1px solid #fdba74;
}
.r-audacieux {
  background: #fee2e2;
  color: #7f1d1d;
  border: 1px solid #fecaca;
}
</style>

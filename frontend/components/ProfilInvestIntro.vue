<template>
  <div class="container mx-auto max-w-xl p-4">
    <div class="bg-white border rounded-2xl shadow p-6">
      <h2 class="text-xl font-bold">Profil Investisseur</h2>
      <p class="text-gray-600 mb-4">
        Faites le test, découvrez votre profil et débloquez des contenus adaptés.
      </p>

      <div class="flex items-center gap-4 flex-wrap mb-4">
        <a
          href="/profil-investisseur"
          class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-4 py-2 rounded-lg inline-flex items-center gap-2"
        >
          👉 Faire le test maintenant
        </a>
        
        <span class="bg-green-100 text-green-800 font-semibold border border-green-300 px-3 py-1 rounded-full text-sm">
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

<!-- <script setup>
import axios from "axios";

async function startTest() {
  const token = localStorage.getItem("token");
  const fieldName = "profil_investisseur";
  const amount = 100;

  try {
    const res = await axios.post(
      `http://localhost:8000/api/reward?field_name=${fieldName}&amount=${amount}`,
      {},
      { headers: { Authorization: `Bearer ${token}` } }
    );
    alert(res.data.message);
  } catch (err) {
    alert(err.response?.data?.detail || "Erreur lors du déblocage de la récompense");
  }

  // ✅ Go to the quiz page
  window.location.href = "/play_invest_profil_investisseur.html";
}
</script> -->

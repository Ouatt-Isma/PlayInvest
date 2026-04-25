<template>
  <div>
    <!-- HERO -->
    <div class="hero">
      <div class="hero-label">Outils d'analyse</div>
      <div class="hero-title">Analyses</div>
      <p class="hero-sub">Évaluez vos investissements avec rigueur. Trois approches complémentaires pour prendre des décisions éclairées sur les marchés africains et européens.</p>
      <div class="hero-markets">
        <div v-for="market in markets" :key="market" class="market-chip">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/></svg>
          {{ market }}
        </div>
      </div>
    </div>

    <!-- TABS NAV -->
    <nav class="tabs-nav" role="tablist">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        class="tab-btn"
        :class="{ active: activeTab === tab.id }"
        :aria-selected="activeTab === tab.id"
        role="tab"
        @click="activeTab = tab.id"
      >
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" v-html="tab.icon"></svg>
        {{ tab.label }}
      </button>
    </nav>

    <main class="content">

      <!-- ONGLET 1 — ANALYSE FONDAMENTALE -->
      <div v-show="activeTab === 'fondamentale'" role="tabpanel">
        <div class="section-head">
          <div class="section-tag">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
            Fondamentale
          </div>
          <div class="section-title">Qu'est-ce que l'analyse fondamentale ?</div>
          <p class="section-intro">L'analyse fondamentale consiste à évaluer la valeur réelle d'une entreprise en étudiant ses activités, ses données financières, son modèle économique et son environnement. L'objectif est de déterminer si une action est sous-évaluée ou surévaluée par le marché.</p>
        </div>

        <!-- Connaître l'entreprise -->
        <div class="entreprise-box">
          <div class="entreprise-box-header def-box-header">
            <div class="def-box-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>
            </div>
            <div>
              <div class="def-box-title">Connaître l'entreprise et ses activités</div>
              <div class="def-box-sub">La première question avant tout chiffre : que fait cette entreprise ?</div>
            </div>
          </div>
          <div class="ent-grid">
            <div v-for="item in entrepriseItems" :key="item.label" class="ent-item">
              <div class="ent-icon">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" v-html="item.icon"></svg>
              </div>
              <div class="ent-label">{{ item.label }}</div>
              <div class="ent-desc">{{ item.desc }}</div>
            </div>
          </div>
          <div class="ent-note">Avant d'étudier un seul ratio financier, posez-vous cette question simple : <strong>est-ce que je comprends ce que fait vraiment cette entreprise et pourquoi elle gagne de l'argent ?</strong> Si la réponse est non, aucun chiffre ne vous sauvera d'une mauvaise décision d'investissement.</div>
        </div>

        <!-- Valeur intrinsèque -->
        <div class="def-box">
          <div class="def-box-header">
            <div class="def-box-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 8v4l3 3"/></svg>
            </div>
            <div>
              <div class="def-box-title">Valeur intrinsèque vs prix de marché</div>
              <div class="def-box-sub">Ce que l'entreprise vaut vraiment, indépendamment du cours boursier</div>
            </div>
          </div>
          <div class="def-box-body">
            <p>Un actif a une valeur intrinsèque — ce qu'il vaut vraiment, indépendamment de ce que le marché en pense à un instant donné. L'analyse fondamentale cherche à calculer cette valeur en se basant sur les résultats financiers passés, les perspectives de croissance et le contexte sectoriel. Quand le prix de marché est inférieur à la valeur intrinsèque, l'action représente une opportunité potentielle. À l'inverse, si le prix dépasse largement la valeur estimée, la prudence s'impose.</p>
          </div>
        </div>

        <!-- Pillars -->
        <div class="pillars">
          <div v-for="pillar in fondamentalePillars" :key="pillar.name" class="pillar" :class="pillar.color">
            <div class="pillar-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" v-html="pillar.icon"></svg>
            </div>
            <div class="pillar-name">{{ pillar.name }}</div>
            <div class="pillar-desc">{{ pillar.desc }}</div>
          </div>
        </div>

        <div class="divider"></div>

        <div class="selector-card">
          <div class="selector-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
            Sélectionner un actif à analyser
          </div>
          <div class="selector-row">
            <div class="selector-wrap">
              <select v-model="selectFondamentale">
                <option value="" disabled>— Choisir un actif —</option>
              </select>
            </div>
            <button class="btn-analyse" @click="lancerAnalyse('fondamentale')">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/><polyline points="16 7 22 7 22 13"/></svg>
              Lancer l'analyse
            </button>
          </div>
          <p class="selector-hint">Les actifs seront disponibles prochainement.</p>
        </div>

        <div class="result-placeholder">
          <template v-if="resultFondamentale">
            <p>Analyse en cours pour <strong style="color:var(--green)">{{ resultFondamentale }}</strong>…</p>
          </template>
          <template v-else>
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/></svg>
            <p>Sélectionnez un actif pour afficher son analyse fondamentale complète.</p>
          </template>
        </div>
      </div>

      <!-- ONGLET 2 — ANALYSE TECHNIQUE -->
      <div v-show="activeTab === 'technique'" role="tabpanel">
        <div class="section-head">
          <div class="section-tag">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
            Technique
          </div>
          <div class="section-title">Qu'est-ce que l'analyse technique ?</div>
          <p class="section-intro">L'analyse technique étudie l'évolution des cours et des volumes d'échange pour anticiper les mouvements futurs d'un actif. Elle repose sur l'idée que l'histoire des prix se répète, et que toute l'information disponible est déjà reflétée dans le cours. Contrairement à l'analyse fondamentale, elle ne s'intéresse pas à la valeur de l'entreprise mais au comportement du marché.</p>
        </div>

        <div class="def-box">
          <div class="def-box-header">
            <div class="def-box-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
            </div>
            <div>
              <div class="def-box-title">Le principe de l'analyse technique</div>
              <div class="def-box-sub">Lire le marché dans les graphiques</div>
            </div>
          </div>
          <div class="def-box-body">
            <p>L'analyste technique lit les graphiques comme un langage. Il identifie des tendances (haussières, baissières, latérales), des niveaux de support et résistance, des figures chartistes (tête-épaules, double sommet, triangle…) et utilise des indicateurs mathématiques pour mesurer la force ou la faiblesse d'un mouvement. L'objectif est de déterminer le meilleur moment pour entrer ou sortir d'une position, indépendamment de la qualité intrinsèque de l'actif.</p>
          </div>
        </div>

        <div class="indicators">
          <div v-for="ind in indicators" :key="ind.name" class="indicator">
            <div class="ind-dot" :class="ind.color"></div>
            <div>
              <div class="ind-name">{{ ind.name }}</div>
              <div class="ind-desc">{{ ind.desc }}</div>
            </div>
          </div>
        </div>

        <div class="divider"></div>

        <div class="selector-card">
          <div class="selector-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
            Sélectionner un actif à analyser
          </div>
          <div class="selector-row">
            <div class="selector-wrap">
              <select v-model="selectTechnique">
                <option value="" disabled>— Choisir un actif —</option>
              </select>
            </div>
            <button class="btn-analyse" @click="lancerAnalyse('technique')">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
              Lancer l'analyse
            </button>
          </div>
          <p class="selector-hint">Les actifs seront disponibles prochainement.</p>
        </div>

        <div class="result-placeholder">
          <template v-if="resultTechnique">
            <p>Analyse en cours pour <strong style="color:var(--green)">{{ resultTechnique }}</strong>…</p>
          </template>
          <template v-else>
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/></svg>
            <p>Sélectionnez un actif pour afficher son graphique et ses indicateurs techniques.</p>
          </template>
        </div>
      </div>

      <!-- ONGLET 3 — ANALYSE COMPARATIVE -->
      <div v-show="activeTab === 'comparative'" role="tabpanel">
        <div class="section-head">
          <div class="section-tag">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
            Comparative
          </div>
          <div class="section-title">Qu'est-ce que l'analyse comparative ?</div>
          <p class="section-intro">L'analyse comparative — aussi appelée analyse par les comparables ou "peer analysis" — consiste à évaluer un actif en le mettant en regard d'entreprises similaires du même secteur ou du même marché. Elle permet de détecter les anomalies de valorisation et de construire des estimations de valeur implicite à partir des multiples du groupe de référence.</p>
        </div>

        <div class="def-box">
          <div class="def-box-header">
            <div class="def-box-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
            </div>
            <div>
              <div class="def-box-title">Le principe des comparables</div>
              <div class="def-box-sub">Évaluer par rapport à un groupe de référence</div>
            </div>
          </div>
          <div class="def-box-body">
            <p>L'analyse comparative repose sur un principe simple : un actif ne peut être jugé qu'en le mettant en perspective. Elle consiste à identifier un groupe d'entreprises comparables — même secteur, taille similaire, profil de risque proche — puis à comparer leurs ratios de valorisation, leurs niveaux de rentabilité et leur croissance. Cette mise en regard permet de détecter les anomalies : une entreprise moins valorisée que ses pairs n'est pas forcément une opportunité, mais elle mérite une analyse approfondie. À l'inverse, une prime de valorisation élevée peut se justifier par une meilleure qualité ou une croissance supérieure. L'analyse comparative est également un outil de valorisation à part entière : en appliquant le multiple médian du groupe comparable à l'entreprise étudiée, on obtient une estimation de sa valeur implicite de marché.</p>
          </div>
        </div>

        <div class="pillars">
          <div v-for="pillar in comparativePillars" :key="pillar.name" class="pillar" :class="pillar.color">
            <div class="pillar-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" v-html="pillar.icon"></svg>
            </div>
            <div class="pillar-name">{{ pillar.name }}</div>
            <div class="pillar-desc">{{ pillar.desc }}</div>
          </div>
        </div>

        <div class="divider"></div>

        <div class="selector-card">
          <div class="selector-label">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
            Sélectionner les deux actifs à comparer
          </div>
          <div class="selector-row">
            <div class="comparative-col">
              <span class="comparative-col-label">Actif A</span>
              <div class="selector-wrap">
                <select v-model="selectComparativeA">
                  <option value="" disabled>— Choisir un actif —</option>
                </select>
              </div>
            </div>
            <div class="selector-vs">VS</div>
            <div class="comparative-col">
              <span class="comparative-col-label">Actif B</span>
              <div class="selector-wrap">
                <select v-model="selectComparativeB">
                  <option value="" disabled>— Choisir un actif —</option>
                </select>
              </div>
            </div>
            <button class="btn-analyse btn-compare" @click="lancerComparative">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
              Comparer
            </button>
          </div>
          <p class="selector-hint">Les actifs seront disponibles prochainement. Vous pourrez comparer deux valeurs côte à côte.</p>
        </div>

        <div class="result-placeholder" :class="{ 'result-error-a': errorComparativeA, 'result-error-b': errorComparativeB }">
          <template v-if="resultComparative">
            <p>Comparaison en cours : <strong style="color:var(--green)">{{ resultComparative.a }}</strong> <span style="color:var(--ink3);margin:0 6px">vs</span> <strong style="color:var(--teal)">{{ resultComparative.b }}</strong>…</p>
          </template>
          <template v-else>
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/></svg>
            <p>Sélectionnez deux actifs pour afficher leur analyse comparative côte à côte.</p>
          </template>
        </div>
      </div>

    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const activeTab = ref('fondamentale')

const markets = ['BRVM — Abidjan', 'NSE — Lagos', 'JSE — Johannesburg', 'Euronext — Paris', 'XETRA — Frankfurt', 'LSE — Londres']

const tabs = [
  {
    id: 'fondamentale',
    label: 'Analyse fondamentale',
    icon: '<path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>'
  },
  {
    id: 'technique',
    label: 'Analyse technique',
    icon: '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>'
  },
  {
    id: 'comparative',
    label: 'Analyse comparative',
    icon: '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><rect x="14" y="14" width="7" height="7"/>'
  }
]

const entrepriseItems = [
  {
    label: "Secteur d'activité",
    desc: "Banque, télécoms, agroalimentaire, industrie, énergie, immobilier ? Le secteur détermine les ratios de référence et les risques typiques.",
    icon: '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>'
  },
  {
    label: "Modèle économique",
    desc: "Comment l'entreprise gagne-t-elle de l'argent ? Vente de produits, abonnements, commissions, concessions ? La qualité du modèle conditionne la pérennité des résultats.",
    icon: '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/>'
  },
  {
    label: "Implantation géographique",
    desc: "L'entreprise opère-t-elle localement, à l'échelle régionale ou internationale ? La diversification géographique réduit les risques pays.",
    icon: '<path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/>'
  },
  {
    label: "Avantage concurrentiel",
    desc: "Qu'est-ce qui différencie cette entreprise de ses concurrents ? Marque, réseau, technologie, coûts bas ? Un avantage durable protège les marges à long terme.",
    icon: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>'
  },
  {
    label: "Management & gouvernance",
    desc: "Qui dirige ? L'équipe dirigeante est-elle expérimentée, transparente et bien alignée avec les intérêts des actionnaires ?",
    icon: '<circle cx="12" cy="7" r="4"/><path d="M5.5 21a7.5 7.5 0 0 1 13 0"/>'
  },
  {
    label: "Histoire & réputation",
    desc: "Depuis combien d'années l'entreprise existe-t-elle ? A-t-elle traversé des crises ? Sa réputation sur son marché local est un actif immatériel précieux.",
    icon: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/>'
  }
]

const fondamentalePillars = [
  { color: 'green', name: 'États financiers', desc: 'Bilan, compte de résultat, tableau de flux — les bases chiffrées de toute analyse.', icon: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/>' },
  { color: 'teal', name: 'Rentabilité', desc: "ROE, ROA, marges — l'efficacité avec laquelle l'entreprise génère du profit.", icon: '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>' },
  { color: 'orange', name: 'Solidité financière', desc: 'Gearing, liquidité, couverture des intérêts — la résistance aux chocs.', icon: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>' },
  { color: 'green', name: 'Croissance', desc: "CAGR, BNPA, perspectives sectorielles — le potentiel futur de l'entreprise.", icon: '<line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/>' },
  { color: 'teal', name: 'Valorisation', desc: 'PER, P/B, DCF — les multiples qui comparent le prix à la valeur réelle.', icon: '<path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>' },
  { color: 'orange', name: 'Contexte macro', desc: "Taux, inflation, politique sectorielle — l'environnement qui influence l'entreprise.", icon: '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>' }
]

const indicators = [
  { color: '', name: 'Moyennes mobiles (MM)', desc: 'Lissent les prix sur une période pour révéler la tendance de fond. La MM20 est court terme, la MM200 est long terme.' },
  { color: 'teal', name: 'RSI — Relative Strength Index', desc: "Oscille entre 0 et 100. En dessous de 30 : survente. Au-dessus de 70 : surachat." },
  { color: 'orange', name: 'MACD', desc: "Mesure l'écart entre deux moyennes mobiles exponentielles. Le croisement de ses lignes génère des signaux d'achat/vente." },
  { color: '', name: 'Bandes de Bollinger', desc: "Couloir dynamique de volatilité. Un cours qui touche la bande inférieure est potentiellement en survente." },
  { color: 'teal', name: 'Volumes', desc: "Confirment ou infirment les mouvements de prix. Une hausse sans volume est fragile." },
  { color: 'orange', name: 'Supports & résistances', desc: "Niveaux de prix où l'actif a historiquement rebondi ou marqué une pause. Clés pour la gestion du risque." }
]

const comparativePillars = [
  { color: 'green', name: 'Multiples de valorisation', desc: 'PER, P/B, VE/EBITDA — comparés aux médianes sectorielles et aux moyennes historiques.', icon: '<path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>' },
  { color: 'teal', name: 'Rentabilité comparée', desc: "ROE, ROA, marges — positionnement de l'entreprise face à ses concurrents directs.", icon: '<polyline points="22 7 13.5 15.5 8.5 10.5 2 17"/>' },
  { color: 'orange', name: 'Benchmarking sectoriel', desc: "Croissance du CA, EBITDA, dividendes — où se situe l'actif dans son secteur ?", icon: '<line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18" y2="4"/><line x1="6" y1="20" x2="6" y2="16"/>' },
  { color: 'green', name: 'Comparaison régionale', desc: "Positionnement géographique et concurrentiel par rapport aux marchés de référence.", icon: '<circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>' }
]

// Selector state
const selectFondamentale = ref('')
const selectTechnique = ref('')
const selectComparativeA = ref('')
const selectComparativeB = ref('')

// Result state
const resultFondamentale = ref('')
const resultTechnique = ref('')
const resultComparative = ref(null)
const errorComparativeA = ref(false)
const errorComparativeB = ref(false)

function lancerAnalyse(type) {
  if (type === 'fondamentale') {
    if (!selectFondamentale.value) return
    resultFondamentale.value = selectFondamentale.value
  } else {
    if (!selectTechnique.value) return
    resultTechnique.value = selectTechnique.value
  }
}

function lancerComparative() {
  errorComparativeA.value = !selectComparativeA.value
  errorComparativeB.value = !selectComparativeB.value
  if (errorComparativeA.value || errorComparativeB.value) {
    setTimeout(() => {
      errorComparativeA.value = false
      errorComparativeB.value = false
    }, 1500)
    return
  }
  resultComparative.value = { a: selectComparativeA.value, b: selectComparativeB.value }
}
</script>

<style scoped>
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --green:#0F7A5A;
  --green2:#15A878;
  --green3:#D6F4EC;
  --green4:#EBF9F5;
  --teal:#0D5C6E;
  --bg:#F7F8F6;
  --white:#FFFFFF;
  --ink:#111C18;
  --ink2:#3D4D45;
  --ink3:#7A8C84;
  --line:#DDE6E1;
  --line2:#C8D8D0;
  --mono-bg:#E8F4EF;
  --mono:#1A4035;
  --orange:#E8660A;
  --orange2:#FDE9D9;
  --blue:#1A5FA8;
  --blue2:#E6F0FB;
}

/* ── HERO ── */
.hero{background:linear-gradient(135deg,var(--teal) 0%,var(--green) 100%);padding:2.5rem 2rem 2rem;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;right:-60px;top:-60px;width:280px;height:280px;border-radius:50%;background:rgba(255,255,255,0.04)}
.hero::after{content:'';position:absolute;left:45%;bottom:-80px;width:200px;height:200px;border-radius:50%;background:rgba(255,255,255,0.03)}
.hero-label{font-size:11px;font-weight:700;color:var(--green3);letter-spacing:0.14em;text-transform:uppercase;margin-bottom:0.4rem}
.hero-title{font-family:'Syne',sans-serif;font-size:32px;font-weight:800;color:#fff;line-height:1.1;letter-spacing:-0.02em;margin-bottom:0.4rem}
.hero-sub{font-size:14px;color:rgba(255,255,255,0.7);font-weight:300;max-width:560px;line-height:1.6;margin-bottom:1.25rem}
.hero-markets{display:flex;gap:8px;flex-wrap:wrap}
.market-chip{display:flex;align-items:center;gap:5px;padding:4px 10px;border-radius:100px;background:rgba(255,255,255,0.12);border:1px solid rgba(255,255,255,0.2);font-size:11px;font-weight:600;color:rgba(255,255,255,0.9);letter-spacing:0.04em}
.market-chip svg{width:11px;height:11px}

/* ── TABS NAV ── */
.tabs-nav{background:var(--white);border-bottom:1px solid var(--line);padding:0 2rem;display:flex;gap:0;position:sticky;top:0;z-index:100;box-shadow:0 2px 8px rgba(0,0,0,0.04)}
.tab-btn{padding:1rem 1.5rem;border:none;background:none;font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:var(--ink3);cursor:pointer;border-bottom:2.5px solid transparent;transition:all 0.18s;display:flex;align-items:center;gap:8px;white-space:nowrap;letter-spacing:0.01em}
.tab-btn:hover{color:var(--green)}
.tab-btn.active{color:var(--green);border-bottom-color:var(--green)}
.tab-btn svg{width:16px;height:16px;flex-shrink:0}

/* ── CONTENT ── */
.content{max-width:1100px;margin:0 auto;padding:2rem 2rem 5rem}

/* ── SECTION HEADER ── */
.section-head{margin-bottom:1.75rem}
.section-tag{display:inline-flex;align-items:center;gap:6px;padding:4px 12px;border-radius:100px;background:var(--green3);font-size:11px;font-weight:700;color:var(--green);letter-spacing:0.06em;text-transform:uppercase;margin-bottom:0.75rem}
.section-tag svg{width:12px;height:12px}
.section-title{font-family:'Syne',sans-serif;font-size:24px;font-weight:800;color:var(--ink);letter-spacing:-0.02em;margin-bottom:0.5rem}
.section-intro{font-size:14px;color:var(--ink2);line-height:1.8;font-weight:300;max-width:700px}

/* ── DEF BOX ── */
.def-box{background:var(--white);border:1px solid var(--line);border-radius:14px;overflow:hidden;margin-bottom:1.25rem}
.def-box-header{padding:1.1rem 1.5rem;background:linear-gradient(135deg,var(--green) 0%,var(--teal) 100%);display:flex;align-items:center;gap:12px}
.def-box-icon{width:38px;height:38px;background:rgba(255,255,255,0.15);border-radius:9px;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.def-box-icon svg{width:18px;height:18px;color:#fff}
.def-box-title{font-family:'Syne',sans-serif;font-size:15px;font-weight:700;color:#fff}
.def-box-sub{font-size:12px;color:rgba(255,255,255,0.7);margin-top:2px;font-weight:300}
.def-box-body{padding:1.1rem 1.5rem}
.def-box-body p{font-size:13.5px;color:var(--ink2);line-height:1.8;font-weight:300}

/* ── ENTREPRISE BOX ── */
.entreprise-box{margin-bottom:1.25rem}
.entreprise-box-header{padding:1.1rem 1.5rem;background:linear-gradient(135deg,#1A5FA8 0%,#0D5C6E 100%);display:flex;align-items:center;gap:12px;border-radius:14px;margin-bottom:10px}
.ent-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin-bottom:10px}
.ent-item{background:var(--white);border:1px solid var(--line);border-radius:10px;padding:1rem 1.1rem;display:flex;flex-direction:column;gap:8px}
.ent-label{font-size:13px;font-weight:700;color:var(--ink);font-family:'Syne',sans-serif}
.ent-desc{font-size:12px;color:var(--ink3);line-height:1.6;font-weight:300}
.ent-icon{width:32px;height:32px;border-radius:8px;background:var(--blue2);display:flex;align-items:center;justify-content:center;flex-shrink:0}
.ent-icon svg{width:15px;height:15px;color:var(--blue)}
.ent-note{background:var(--white);border:1px solid var(--line);border-radius:10px;padding:1rem 1.25rem;font-size:13px;color:var(--ink2);line-height:1.75;font-weight:300}

/* ── PILLARS ── */
.pillars{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin-bottom:1.25rem}
.pillar{background:var(--white);border:1px solid var(--line);border-radius:10px;padding:1rem 1.1rem}
.pillar-icon{width:32px;height:32px;border-radius:8px;display:flex;align-items:center;justify-content:center;margin-bottom:0.6rem}
.pillar-icon svg{width:16px;height:16px}
.pillar-name{font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:var(--ink);margin-bottom:4px}
.pillar-desc{font-size:12px;color:var(--ink3);line-height:1.6;font-weight:300}
.pillar.green .pillar-icon{background:var(--green3)}
.pillar.green .pillar-icon svg{color:var(--green)}
.pillar.teal .pillar-icon{background:#e1f0f5}
.pillar.teal .pillar-icon svg{color:var(--teal)}
.pillar.orange .pillar-icon{background:var(--orange2)}
.pillar.orange .pillar-icon svg{color:var(--orange)}

/* ── SELECTOR CARD ── */
.selector-card{background:var(--white);border:1.5px solid var(--line2);border-radius:14px;padding:1.5rem;margin-bottom:1.25rem}
.selector-label{font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:var(--ink);margin-bottom:0.75rem;display:flex;align-items:center;gap:8px}
.selector-label svg{width:16px;height:16px;color:var(--green)}
.selector-row{display:flex;gap:12px;align-items:center;flex-wrap:wrap}
.selector-wrap{position:relative;flex:1;min-width:180px;max-width:320px}
.selector-wrap select{width:100%;padding:10px 36px 10px 14px;border:1.5px solid var(--line2);border-radius:8px;font-size:14px;font-family:'Nunito',sans-serif;font-weight:500;background:var(--bg);color:var(--ink);outline:none;appearance:none;-webkit-appearance:none;cursor:pointer;transition:border-color 0.2s,background 0.2s}
.selector-wrap select:focus{border-color:var(--green);background:var(--white)}
.selector-wrap::after{content:'';position:absolute;right:12px;top:50%;transform:translateY(-50%);width:0;height:0;border-left:5px solid transparent;border-right:5px solid transparent;border-top:5px solid var(--ink3);pointer-events:none}
.selector-hint{font-size:12px;color:var(--ink3);font-weight:300;font-style:italic;margin-top:8px}
.selector-vs{font-family:'Syne',sans-serif;font-size:13px;font-weight:800;color:var(--ink3);flex-shrink:0}
.comparative-col{display:flex;flex-direction:column;gap:4px;flex:1;min-width:160px;max-width:280px}
.comparative-col-label{font-size:11px;font-weight:600;color:var(--ink3);letter-spacing:0.04em;text-transform:uppercase}
.comparative-col .selector-wrap{flex:none;max-width:100%}
.btn-analyse{padding:10px 20px;background:var(--green);border:none;border-radius:8px;font-family:'Syne',sans-serif;font-size:13px;font-weight:700;color:#fff;cursor:pointer;transition:background 0.15s;display:flex;align-items:center;gap:6px;white-space:nowrap}
.btn-analyse:hover{background:var(--teal)}
.btn-analyse svg{width:14px;height:14px}
.btn-compare{align-self:flex-end}

/* ── RESULT PLACEHOLDER ── */
.result-placeholder{background:var(--mono-bg);border:1px dashed var(--line2);border-radius:10px;padding:2rem;text-align:center}
.result-placeholder svg{color:var(--ink3);margin-bottom:0.75rem;opacity:0.4}
.result-placeholder p{font-size:13px;color:var(--ink3);font-weight:300}

/* ── INDICATORS ── */
.indicators{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;margin-bottom:1.25rem}
.indicator{background:var(--white);border:1px solid var(--line);border-radius:10px;padding:1rem 1.1rem;display:flex;gap:10px;align-items:flex-start}
.ind-dot{width:8px;height:8px;border-radius:50%;background:var(--green);margin-top:5px;flex-shrink:0}
.ind-dot.teal{background:var(--teal)}
.ind-dot.orange{background:var(--orange)}
.ind-name{font-weight:600;font-size:13px;color:var(--ink);margin-bottom:2px}
.ind-desc{font-size:12px;color:var(--ink3);line-height:1.6;font-weight:300}

/* ── DIVIDER ── */
.divider{height:1px;background:var(--line);margin:1.5rem 0}

/* ── RESPONSIVE ── */
@media(max-width:640px){
  .hero{padding:1.75rem 1rem 1.5rem}
  .hero-title{font-size:24px}
  .tabs-nav{padding:0 0.5rem;overflow-x:auto;scrollbar-width:none}
  .tabs-nav::-webkit-scrollbar{display:none}
  .tab-btn{padding:0.85rem 0.9rem;font-size:12px}
  .content{padding:1.25rem 1rem 3rem}
  .pillars,.ent-grid,.indicators{grid-template-columns:1fr}
}
</style>

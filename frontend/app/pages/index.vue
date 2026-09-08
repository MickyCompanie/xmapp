<template>
  <!-- Conteneur global appliquant le thème Christmas -->
  <div data-theme="christmas" class="min-h-screen bg-base-100 text-neutral font-sans flex flex-col md:flex-row">

    <!-- BARRE NAV SIDERIGHT / DESKTOP -->
    <aside class="w-full md:w-64 bg-base-200 border-r border-base-300 p-4 flex flex-col justify-between">
      <div class="space-y-6">
        <!-- Logo & Titre -->
        <div class="flex items-center gap-3 px-2">
          <div class="w-10 h-10 rounded-full bg-primary flex items-center justify-center text-white text-xl font-bold shadow">
            🎄
          </div>
          <div>
            <h1 class="font-bold text-lg text-primary leading-tight">xmapp Admin</h1>
            <span class="text-xs text-neutral/70">Gestion de Noël</span>
          </div>
        </div>

        <!-- Menu Navigation -->
        <ul class="menu bg-base-100 rounded-box p-2 gap-1 shadow-sm">
          <li><a class="active bg-primary text-primary-content font-semibold">📊 Tableau de bord</a></li>
          <li><a>🎁 Demandes de Remboursement</a></li>
          <li><a>📜 Historique des Biles</a></li>
          <li><a>⚙️ Configuration</a></li>
        </ul>
      </div>

      <!-- Footer Sidebar -->
      <div class="p-3 bg-base-300/50 rounded-box text-xs text-center">
        Environnement : <span class="badge badge-accent badge-sm font-semibold">Docker Dev</span>
      </div>
    </aside>

    <!-- CONTENU PRINCIPAL -->
    <main class="flex-1 p-6 space-y-6 overflow-y-auto">

      <!-- HEADER / TOPBAR -->
      <header class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 bg-base-200 p-4 rounded-box shadow-sm border border-base-300">
        <div>
          <h2 class="text-2xl font-extrabold text-primary">Aperçu Général</h2>
          <p class="text-sm text-neutral/70">Bienvenue sur votre interface de suivi des remboursements festifs.</p>
        </div>
        
        <!-- Actions & Profil -->
        <div class="flex items-center gap-3">
          <button class="btn btn-primary btn-sm">
            ➕ Nouvelle Demande
          </button>
          <button class="btn btn-secondary btn-sm">
            💾 Exporter
          </button>
          <div class="avatar placeholder">
            <div class="bg-neutral text-neutral-content rounded-full w-9">
              <span class="text-xs">PN</span>
            </div>
          </div>
        </div>
      </header>

      <!-- CARTES DES STATISTIQUES (Testing Primary, Secondary, Accent) -->
      <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div v-for="(stat, index) in stats" :key="index" class="card bg-base-200 border border-base-300 shadow-sm p-4">
          <span class="text-xs font-semibold text-neutral/60 uppercase tracking-wider">{{ stat.title }}</span>
          <div class="text-3xl font-black my-1" :class="stat.color">{{ stat.value }}</div>
          <span class="text-xs text-neutral/80">{{ stat.desc }}</span>
        </div>
      </section>

      <!-- SECTION TABLEAU ET FORMULAIRE DE TEST -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- Tableau des derniers remboursements -->
        <div class="lg:col-span-2 bg-base-200 p-5 rounded-box border border-base-300 shadow-sm space-y-4">
          <div class="flex justify-between items-center">
            <h3 class="font-bold text-lg text-secondary flex items-center gap-2">
              📋 Demandes Récentes
            </h3>
            <span class="badge badge-outline text-xs">Mise à jour directe</span>
          </div>

          <div class="overflow-x-auto">
            <table class="table table-zebra w-full bg-base-100 rounded-lg">
              <thead>
                <tr class="text-neutral/70">
                  <th>ID</th>
                  <th>Utilisateur</th>
                  <th>Montant</th>
                  <th>Statut</th>
                  <th>Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in repayments" :key="item.id">
                  <td class="font-mono text-xs font-bold">{{ item.id }}</td>
                  <td>{{ item.user }}</td>
                  <td class="font-bold">{{ item.amount }}</td>
                  <td>
                    <span :class="['badge', item.badge, 'badge-sm font-semibold']">
                      {{ item.status }}
                    </span>
                  </td>
                  <td>
                    <button class="btn btn-ghost btn-xs text-primary">Détails</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Panneau d'Avancement et Tests de Couleurs -->
        <div class="bg-base-200 p-5 rounded-box border border-base-300 shadow-sm space-y-5">
          <h3 class="font-bold text-lg text-primary">🎨 Palette de Couleurs</h3>
          <p class="text-xs text-neutral/70">Vérification du contraste des boutons et barres de progression.</p>

          <!-- Test Barres de progression -->
          <div class="space-y-3">
            <div>
              <div class="flex justify-between text-xs mb-1">
                <span>Budget Consommé (Rouge Primary)</span>
                <span class="font-bold">75%</span>
              </div>
              <progress class="progress progress-primary w-full" value="75" max="100"></progress>
            </div>

            <div>
              <div class="flex justify-between text-xs mb-1">
                <span>Cadeaux Empaquetés (Vert Secondary)</span>
                <span class="font-bold">90%</span>
              </div>
              <progress class="progress progress-secondary w-full" value="90" max="100"></progress>
            </div>

            <div>
              <div class="flex justify-between text-xs mb-1">
                <span>Distribution Étoiles (Or Accent)</span>
                <span class="font-bold">40%</span>
              </div>
              <progress class="progress progress-accent w-full" value="40" max="100"></progress>
            </div>
          </div>

          <div class="divider my-2"></div>

          <!-- Test Badges et Boutons -->
          <div class="space-y-2">
            <span class="text-xs font-semibold block text-neutral/70">Boutons Thématiques :</span>
            <div class="flex flex-wrap gap-2">
              <button class="btn btn-primary btn-xs">Primary</button>
              <button class="btn btn-secondary btn-xs">Secondary</button>
              <button class="btn btn-accent btn-xs">Accent</button>
              <button class="btn btn-neutral btn-xs">Neutral</button>
            </div>
          </div>
        </div>

      </div>

    </main>
  </div>
</template> 

<script setup>
// Données de démonstration
const stats = [
  { title: "Remboursements du Mois", value: "12 450 €", desc: "↗︎ 14% de plus que nov.", color: "text-primary" },
  { title: "Demandes en Attente", value: "28", desc: "Traitement prioritaire", color: "text-accent" },
  { title: "Budget Lutins Reçu", value: "98.5%", desc: "Objectif presque atteint", color: "text-secondary" },
  { title: "Cadeaux Validés", value: "142", desc: "Livraison programmée", color: "text-neutral" },
]

const repayments = [
  { id: "REMB-001", user: "Nicolas S.", amount: "150.00 €", status: "Validé", badge: "badge-secondary" },
  { id: "REMB-002", user: "Rudolph R.", amount: "45.90 €", status: "En attente", badge: "badge-accent" },
  { id: "REMB-003", user: "Elf #4", amount: "890.00 €", status: "Refusé", badge: "badge-error" },
  { id: "REMB-004", user: "Marie C.", amount: "210.50 €", status: "Validé", badge: "badge-secondary" },
]
</script>
<template>
  <div class="grid grid-cols-1 gap-y-5">
      <!-- HEADER / TOPBAR -->
      <PageTitle title="Aperçu Général" description="Bienvenue sur votre interface de suivi des remboursements festifs." >
        <div class="flex items-center gap-2">
            <button class="btn btn-primary btn-xs sm:btn-sm">
              ➕ <span class="hidden xs:inline">Nouvelle</span> Demande
            </button>
            <button class="btn btn-secondary btn-xs sm:btn-sm">
              💾 Exporter
            </button>
          </div>
          <div class="avatar placeholder">
            <div class="bg-neutral text-neutral-content rounded-full w-8 sm:w-9">
              <span class="text-xs">PN</span>
            </div>
          </div>
      </PageTitle>

      <!-- CARTES DES STATISTIQUES -->
      <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
        <div v-for="(stat, index) in stats" :key="index" class="card bg-base-200 border border-base-300 shadow-sm p-4">
          <span class="text-xs font-semibold text-neutral/60 uppercase tracking-wider">{{ stat.title }}</span>
          <div class="text-2xl sm:text-3xl font-black my-1" :class="stat.color">{{ stat.value }}</div>
          <span class="text-xs text-neutral/80">{{ stat.desc }}</span>
        </div>
      </section>

      <!-- SECTION TABLEAU ET PANNEAU DE TEST -->
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">

        <!-- Tableau des derniers remboursements -->
        <div class="lg:col-span-2 bg-base-200 p-4 sm:p-5 rounded-box border border-base-300 shadow-sm space-y-4">
          <div class="flex flex-col xs:flex-row justify-between items-start xs:items-center gap-2">
            <h3 class="font-bold text-base sm:text-lg text-secondary flex items-center gap-2">
              📋 Demandes Récentes
            </h3>
            <span class="badge badge-outline text-xs">Mise à jour directe</span>
          </div>

          <!-- Conteneur avec scroll horizontal pour mobiles -->
          <div class="overflow-x-auto -mx-2 sm:mx-0">
            <table class="table table-sm sm:table-md table-zebra w-full bg-base-100 rounded-lg min-w-[500px]">
              <thead>
                <tr class="text-neutral/70 text-xs">
                  <th>ID</th>
                  <th>Utilisateur</th>
                  <th>Montant</th>
                  <th>Statut</th>
                  <th class="text-right">Action</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="item in repayments" :key="item.id">
                  <td class="font-mono text-xs font-bold">{{ item.id }}</td>
                  <td class="text-xs sm:text-sm">{{ item.user }}</td>
                  <td class="font-bold text-xs sm:text-sm">{{ item.amount }}</td>
                  <td>
                    <span :class="['badge', item.badge, 'badge-xs sm:badge-sm font-semibold']">
                      {{ item.status }}
                    </span>
                  </td>
                  <td class="text-right">
                    <button class="btn btn-ghost btn-xs text-primary">Détails</button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Panneau d'Avancement et Tests de Couleurs -->
        <div class="bg-base-200 p-4 sm:p-5 rounded-box border border-base-300 shadow-sm space-y-5">
          <div>
            <h3 class="font-bold text-base sm:text-lg text-primary">🎨 Palette de Couleurs</h3>
            <p class="text-xs text-neutral/70">Vérification du contraste des boutons et barres de progression.</p>
          </div>

          <!-- Test Barres de progression -->
          <div class="space-y-3">
            <div>
              <div class="flex justify-between text-xs mb-1">
                <span>Budget Consommé (Primary)</span>
                <span class="font-bold">75%</span>
              </div>
              <progress class="progress progress-primary w-full" value="75" max="100"></progress>
            </div>

            <div>
              <div class="flex justify-between text-xs mb-1">
                <span>Cadeaux Empaquetés (Secondary)</span>
                <span class="font-bold">90%</span>
              </div>
              <progress class="progress progress-secondary w-full" value="90" max="100"></progress>
            </div>

            <div>
              <div class="flex justify-between text-xs mb-1">
                <span>Distribution Étoiles (Accent)</span>
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
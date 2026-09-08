<template>
  <div>
    <!-- NAVBAR -->
    <div class="navbar bg-base-100 shadow">
      <div class="flex-1">
        <a class="btn btn-ghost text-xl">DaisyUI Demo</a>
      </div>
      <div class="flex-none gap-2">
        <button class="btn btn-primary">Login</button>
      </div>
    </div>

    <!-- HERO -->
    <div class="hero min-h-[60vh] bg-base-200">
      <div class="hero-content text-center">
        <div class="max-w-md">
          <h1 class="text-5xl font-bold">DaisyUI + Nuxt</h1>
          <p class="py-6">
            Une page d’exemple identique à celle de la documentation DaisyUI,
            adaptée pour Nuxt avec ton thème Noël.
          </p>
          <button class="btn btn-secondary">Commencer</button>
        </div>
      </div>
    </div>

    <!-- CARDS -->
    <div class="p-10 grid grid-cols-1 md:grid-cols-3 gap-6">
      <div class="card bg-base-100 shadow-xl">
        <figure>
          <img src="https://picsum.photos/400/200" alt="Demo" />
        </figure>
        <div class="card-body">
          <h2 class="card-title">Card 1</h2>
          <p>Une carte simple comme dans la doc DaisyUI.</p>
          <div class="card-actions justify-end">
            <button class="btn btn-primary">Voir</button>
          </div>
        </div>
      </div>

      <div class="card bg-base-100 shadow-xl">
        <figure>
          <img src="https://picsum.photos/400/201" alt="Demo" />
        </figure>
        <div class="card-body">
          <h2 class="card-title">Card 2</h2>
          <p>Encore une carte, même style que la doc.</p>
          <div class="card-actions justify-end">
            <button class="btn btn-secondary">Voir</button>
          </div>
        </div>
      </div>

      <div class="card bg-base-100 shadow-xl">
        <figure>
          <img src="https://picsum.photos/400/202" alt="Demo" />
        </figure>
        <div class="card-body">
          <h2 class="card-title">Card 3</h2>
          <p>Et une troisième pour compléter la grille.</p>
          <div class="card-actions justify-end">
            <button class="btn btn-accent">Voir</button>
          </div>
        </div>
      </div>
    </div>

    <!-- FOOTER -->
    <footer class="footer footer-center p-10 bg-base-300 text-base-content rounded">
      <nav class="grid grid-flow-col gap-4">
        <a class="link link-hover">About</a>
        <a class="link link-hover">Contact</a>
        <a class="link link-hover">Jobs</a>
        <a class="link link-hover">Press</a>
      </nav>
      <p>© 2026 DaisyUI Demo — Nuxt Edition</p>
    </footer>
  </div>
</template>

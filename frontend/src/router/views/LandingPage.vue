<template>
  <div class="container vh-100 d-flex justify-content-center align-items-center">
    <div class="text-center" style="max-width: 680px; width: 100%;">

      <h2 class="fw-bold mb-1">Placement Portal</h2>
      <p class="text-muted mb-4">Select how you want to sign in</p>

      <div class="row g-3 justify-content-center">

        <!-- Student -->
        <div class="col-12 col-sm-4">
          <div
            class="card shadow-sm border-0 h-100 role-card"
            @click="router.push('/login'); sessionStorage.setItem('login_role_hint', 'student')"
          >
            <div class="card-body py-4 px-3 d-flex flex-column align-items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="role-icon text-primary" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 3.741-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" />
              </svg>
              <h6 class="fw-semibold mb-0">Student</h6>
              <p class="text-muted small mb-2 text-center">Browse drives &amp; track applications</p>
              <span class="btn btn-outline-primary btn-sm w-100 mt-auto">Login</span>
              <router-link to="/student/register" class="small text-muted text-decoration-none mt-1" @click.stop>Register</router-link>
            </div>
          </div>
        </div>

        <!-- Company  -->
        <div class="col-12 col-sm-4">
          <div
            class="card shadow-sm border-0 h-100 role-card"
            @click="router.push('/login'); sessionStorage.setItem('login_role_hint', 'company')"
          >
            <div class="card-body py-4 px-3 d-flex flex-column align-items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="role-icon text-success" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 21h19.5m-18-18v18m10.5-18v18m6-13.5V21M6.75 6.75h.75m-.75 3h.75m-.75 3h.75m3-6h.75m-.75 3h.75m-.75 3h.75M6.75 21v-3.375c0-.621.504-1.125 1.125-1.125h2.25c.621 0 1.125.504 1.125 1.125V21M3 3h12m-.75 4.5H21m-3.75 3.75h.008v.008h-.008v-.008Zm0 3h.008v.008h-.008v-.008Zm0 3h.008v.008h-.008v-.008Z" />
              </svg>
              <h6 class="fw-semibold mb-0">Company</h6>
              <p class="text-muted small mb-2 text-center">Post drives &amp; hire students</p>
              <span class="btn btn-outline-success btn-sm w-100 mt-auto">Login</span>
              <router-link to="/company/register" class="small text-muted text-decoration-none mt-1" @click.stop>Register</router-link>
            </div>
          </div>
        </div>

        <!-- Admin -->
        <div class="col-12 col-sm-4">
          <div
            class="card shadow-sm border-0 h-100 role-card"
            @click="router.push('/login'); sessionStorage.setItem('login_role_hint', 'admin')"
          >
            <div class="card-body py-4 px-3 d-flex flex-column align-items-center gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="role-icon text-danger" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" d="M9 12.75 11.25 15 15 9.75m-3-7.036A11.959 11.959 0 0 1 3.598 6 11.99 11.99 0 0 0 3 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285Z" />
              </svg>
              <h6 class="fw-semibold mb-0">Admin</h6>
              <p class="text-muted small mb-2 text-center">Manage companies &amp; drives</p>
              <span class="btn btn-outline-danger btn-sm w-100 mt-auto">Login</span>
              <span class="small mt-1" style="height: 1.25rem; display: block;">&nbsp;</span>
            </div>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
</script>

<style scoped>
.role-card {
  cursor: pointer;
  transition: box-shadow 0.2s, transform 0.2s;
}
.role-card:hover {
  box-shadow: 0 4px 16px rgba(0,0,0,0.12) !important;
  transform: translateY(-2px);
}
.role-icon {
  width: 40px;
  height: 40px;
}
</style>

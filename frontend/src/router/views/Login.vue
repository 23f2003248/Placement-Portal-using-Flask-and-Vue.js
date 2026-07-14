<template>
  <div class="container vh-100 d-flex justify-content-center align-items-center">
    <div class="card shadow col-11 col-sm-8 col-md-6 col-lg-4">
      <div class="card-body p-4">

        <router-link to="/" class="text-muted text-decoration-none small d-block mb-3">
          ← Back
        </router-link>

        <h3 class="text-center mb-4">Login</h3>

        <form @submit.prevent="login">
          <div class="mb-3">
            <label for="loginmail" class="form-label">Email</label>
            <input
              type="email"
              class="form-control"
              id="loginmail"
              placeholder="Enter your email"
              v-model="email"
            />
          </div>

          <div class="mb-4">
            <label for="loginpass" class="form-label">Password</label>
            <input
              type="password"
              class="form-control"
              id="loginpass"
              placeholder="Enter your password"
              v-model="password"
            />
          </div>

          <button type="submit" class="btn btn-success w-100">
            Sign In
          </button>
        </form>

      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  import {useRouter} from 'vue-router'

  const email = ref('')
  const password = ref('')
  const router = useRouter()

  async function login() {
    try{
      const response = await axios.post(
        "http://127.0.0.1:5000/login", 
        {
          email: email.value, 
          password: password.value,
        },
      )
      localStorage.setItem('access_token', response.data.access_token)
      localStorage.setItem('role', response.data.role)
      localStorage.setItem('id', response.data.id)

      const role = response.data.role 
      if (role == 'admin'){
        router.push('/admin/dashboard')
      }
      if (role == 'student'){
        router.push('/student/dashboard')
      }
      if (role == 'company'){
        router.push('/company/dashboard')
      }
    }
    catch(error){
      console.error(error)
      alert(error.response?.data?.error || error.message)
    }
  }
</script>

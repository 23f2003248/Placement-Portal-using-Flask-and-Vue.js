
<template>
  <div class="container vh-100 d-flex justify-content-center align-items-center">
    <div class="card shadow-lg border-0 col-11 col-sm-9 col-md-7 col-lg-5">
      <div class="card-body p-4 p-md-5">

        <h2 class="text-center fw-bold mb-4">Company Registration</h2>

        <form @submit.prevent="company_register">  
          <div class="mb-3">
            <input
              type="text"
              class="form-control"
              placeholder="Company Name"
              v-model = "name"
            />
          </div>

          <div class="mb-3">
            <input
              type="email"
              class="form-control"
              placeholder="HR Contact Email"
              v-model = "hr_contact"
            />
          </div>

          <div class="mb-3">
            <input
              type="url"
              class="form-control"
              placeholder="Company Website"
              v-model = "website"
            />
          </div>

          <div class="mb-3">
            <input
              type="email"
              class="form-control"
              placeholder="Login Email"
              v-model = "email"
            />
          </div>

          <div class="mb-4">
            <input
              type="password"
              class="form-control"
              placeholder="Password"
              v-model = "password"
            />
          </div>

          <button
            type="submit"
            class="btn btn-success w-100"
          >
            Register Company
          </button>
        </form>

      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  import { useRouter } from 'vue-router'

  const name = ref('')
  const email = ref('')
  const password = ref('')
  const hr_contact = ref('')
  const website = ref('')

  const router = useRouter()

  async function company_register() {
    console.log('started')
    try{
      const response = await axios.post(
        "https://placement-portal-using-flask-and-vue-js.onrender.com/company/register/",
        {
          'name': name.value,
          'email': email.value,
          'password': password.value,
          'hr_contact': hr_contact.value,
          'website': website.value,
        }  
      )
      router.push("/login/")
    }
    catch(error){
      console.error(error)

      alert(
        error.response?.data?.error ||
        error.message ||
        "Something went wrong"
      )
}
  }

</script>

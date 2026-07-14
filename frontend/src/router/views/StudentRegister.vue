<template>
  <div class="container vh-100 d-flex justify-content-center align-items-center">
    <div class="card shadow-lg border-0 col-11 col-sm-9 col-md-7 col-lg-5">
      <div class="card-body p-4 p-md-5">

        <h2 class="text-center fw-bold mb-4">Student Registration</h2>

        <form @submit.prevent="student_register">

          <div class="mb-3">
            <input
              type="text"
              class="form-control"
              placeholder="Full Name"
              v-model="name"
            />
          </div>

          <div class="mb-3">
            <input
              type="email"
              class="form-control"
              placeholder="Email Address"
              v-model="email"
            />
          </div>

          <div class="mb-3">
            <input
              type="password"
              class="form-control"
              placeholder="Password"
              v-model="password"
            />
          </div>

          <div class="mb-3"> Branch 
            <select class="form-select" v-model="branch"> 
              <option selected disabled>Select Branch</option>
              <option>CSE</option>
              <option>IT</option>
              <option>ECE</option>
              <option>EE</option>
              <option>ME</option>
            </select>
            
          </div>

          <div class="mb-3"> Year
            <select class="form-select" v-model="year">
              <option selected disabled>Select Year</option>
              <option>1</option>
              <option>2</option>
              <option>3</option>
              <option>4</option>
              
            </select>
          </div>

          <div class="mb-3">
            <input
              type="number"
              step="0.01"
              class="form-control"
              placeholder="CGPA"
              v-model="cgpa"
            />
          </div>

          <div class="mb-4">
            <label class="form-label fw-semibold">Resume</label>
            <input
              type="file"
              class="form-control"
            />
          </div>

          <button
            type="submit"
            class="btn btn-success w-100"
          >
            Register
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
  const branch = ref('')
  const year = ref('')
  const cgpa = ref('')
  const resume = ref('')

  const router = useRouter()

  async function student_register() {
    try{
      const response = await axios.post(
        "http://127.0.0.1:5000/student/register/",
        {
          'name': name.value,
          'email': email.value,
          'password': password.value,
          'branch': branch.value,
          'cgpa': cgpa.value,
          'year': year.value,
          'resume': resume.value
        }  
      )
      router.push("/login/")
    }
    catch(error){
      console.error(error)
      alert(error.response.data.error)
    }
  }

</script>
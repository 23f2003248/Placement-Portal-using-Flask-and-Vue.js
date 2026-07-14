<template>
  <div class="container vh-100 d-flex justify-content-center align-items-center">
    <div class="card shadow-lg border-0 rounded-4 col-11 col-sm-10 col-md-8 col-lg-6">
      <div class="card-body p-4 p-md-5">

        <h2 class="text-center fw-bold mb-1">Create Drive</h2>

        <p class="text-center text-muted mb-4">
          Post a new placement opportunity
        </p>

        <form @submit.prevent="create_drive">

          <div class="mb-3">
            <input
              type="text"
              class="form-control"
              placeholder="Job Title"
              v-model="job_title"
              required
            />
          </div>

          <div class="mb-3">
            <textarea
              class="form-control"
              rows="4"
              placeholder="Job Description"
              v-model="job_desc"
              required
            ></textarea>
          </div>

          <div class="mb-3">
            <label class="form-label fw-semibold">
              Eligible Branches
            </label>

            <div class="row">
              <div class="col-md-4">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="cse" v-model="branches.CSE">
                  <label class="form-check-label" for="cse">
                    CSE
                  </label>
                </div>
              </div>

              <div class="col-md-4">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="it" v-model="branches.IT">
                  <label class="form-check-label" for="it">
                    IT
                  </label>
                </div>
              </div>

              <div class="col-md-4">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="ece" v-model="branches.ECE">
                  <label class="form-check-label" for="ece">
                    ECE
                  </label>
                </div>
              </div>

              <div class="col-md-4 mt-2">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="ee" v-model="branches.EE">
                  <label class="form-check-label" for="ee">
                    EE
                  </label>
                </div>
              </div>

              <div class="col-md-4 mt-2">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="me" v-model="branches.ME">
                  <label class="form-check-label" for="me">
                    ME
                  </label>
                </div>
              </div>
            </div>
          </div>

          <div class="mb-3">
            <select class="form-select" v-model="elig_year" required>
              <option value="" disabled>
                Select Eligible Year
              </option>
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
              placeholder="Minimum CGPA"
              v-model="elig_min_cgpa"
              required
            />
          </div>

          <div class="mb-4">
            <label class="form-label text-muted">
              Application Deadline
            </label>

            <input
              type="date"
              class="form-control"
              v-model="application_deadline"
              required
            />
          </div>

          <div class="d-flex gap-2">
            <button
              type="button"
              class="btn btn-outline-secondary w-50"
              @click="router.push('/company/dashboard')"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="btn btn-success w-50"
            >
              Create Drive
            </button>
          </div>

        </form>

      </div>
    </div>
  </div>
</template>

<script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  import { useRouter } from 'vue-router'

  const router = useRouter()
  const job_title = ref('')
  const job_desc = ref('')
  const branches = ref({
    CSE: false,
    IT: false,
    ECE: false,
    EE: false,
    ME: false
  })
  const elig_year = ref('')
  const elig_min_cgpa = ref('')
  const application_deadline = ref('')

  async function create_drive() {
    try {
      const selectedBranches = Object.keys(branches.value)
        .filter(key => branches.value[key])
        .join(', ')
      
      if (!job_title.value || !job_desc.value || !selectedBranches || !elig_year.value || !elig_min_cgpa.value || !application_deadline.value) {
        alert("Please fill all fields and select at least one branch.")
        return
      }

      const access_token = localStorage.getItem('access_token')
      const response = await axios.post(
        "http://127.0.0.1:5000/drive/register/",
        {
          job_title: job_title.value,
          job_desc: job_desc.value,
          elig_branch: selectedBranches,
          elig_year: elig_year.value,
          elig_min_cgpa: elig_min_cgpa.value,
          application_deadline: application_deadline.value
        },
        {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        }
      )
      alert(response.data.message)
      router.push('/company/dashboard')
    } catch (error) {
      alert(error.response?.data?.error || error.message)
    }
  }
</script>
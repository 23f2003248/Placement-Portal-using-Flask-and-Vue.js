<template>
  <div class="container-fluid px-4 py-3">

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h3 class="mb-1 fw-bold">Student Dashboard</h3>
        <p class="text-muted mb-0">
          Welcome, {{ profile.name || 'Student' }}! Explore placement opportunities and track your applications.
        </p>
      </div>

      <button class="btn btn-outline-danger px-4 rounded-3 fw-semibold" @click="logout">
        Logout
      </button>
    </div>

    <!-- Stats Cards -->
    <div class="row mb-4">
      <div class="col-md-4 mb-3">
        <div class="card border-0 shadow-sm rounded-4 h-100" style="background-color: #dbeafe;">
          <div class="card-body">
            <h6 class="text-muted">Applications</h6>
            <h2 class="fw-bold mb-0">{{ applications.length }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-4 mb-3">
        <div class="card border-0 shadow-sm rounded-4 h-100" style="background-color: #fce7f3;">
          <div class="card-body">
            <h6 class="text-muted">Shortlisted</h6>
            <h2 class="fw-bold mb-0">{{ shortlisted }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-4 mb-3">
        <div class="card border-0 shadow-sm rounded-4 h-100" style="background-color: #fef3c7;">
          <div class="card-body">
            <h6 class="text-muted">Selected</h6>
            <h2 class="fw-bold mb-0">{{ selected }}</h2>
          </div>
        </div>
      </div>
    </div>

    <div class="row">
      <!-- Left Column: Drives and Applications -->
      <div class="col-lg-8">
        
        <!-- Available Drives -->
        <div class="card border-0 shadow-sm rounded-4 mb-4">
          <div class="card-header bg-white fw-semibold py-3 border-0">
            Available Drives
          </div>

          <div class="card-body pt-0">
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead>
                  <tr>
                    <th>Company</th>
                    <th>Job Title</th>
                    <th>Job Description</th>
                    <th>Branch</th>
                    <th>Year</th>
                    <th>Min CGPA</th>
                    <th>Deadline</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="drive in drives" :key="drive.drive_id">
                    <td class="fw-semibold">{{ drive.company_name }}</td>
                    <td>{{ drive.job_title }}</td>
                    <td><small class="text-muted">{{ drive.job_desc }}</small></td>
                    <td><span class="badge bg-secondary">{{ drive.elig_branch }}</span></td>
                    <td>{{ drive.elig_year }}</td>
                    <td>{{ drive.elig_cgpa }}</td>
                    <td>{{ new Date(drive.application_deadline).toLocaleDateString() }}</td>
                    <td>
                      <button class="btn btn-success btn-sm px-3 rounded-pill" @click="register_applications(drive.drive_id)">
                        Apply
                      </button>
                    </td>
                  </tr>
                  <tr v-if="drives.length === 0">
                    <td colspan="8" class="text-center text-muted py-4">
                      No drives available
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <!-- My Applications -->
        <div class="card border-0 shadow-sm rounded-4 mb-4">
          <div class="card-header bg-white fw-semibold d-flex justify-content-between align-items-center py-3 border-0">
            <span>My Applications</span>
            <button class="btn btn-outline-success btn-sm px-3 rounded-pill" @click="export_csv">
              Export CSV
            </button>
          </div>

          <div class="card-body pt-0">
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead>
                  <tr>
                    <th>Application ID</th>
                    <th>Company</th>
                    <th>Job Title</th>
                    <th>Applied On</th>
                    <th>Interview Date</th>
                    <th>Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="app in applications" :key="app.application_id">
                    <td>#{{ app.application_id }}</td>
                    <td class="fw-semibold">{{ app.company_name }}</td>
                    <td>{{ app.job_title }}</td>
                    <td>{{ new Date(app.application_date).toLocaleDateString() }}</td>
                    <td>
                      <span v-if="app.interview_date" class="text-primary fw-semibold">
                        {{ new Date(app.interview_date).toLocaleString() }}
                      </span>
                      <span v-else class="text-muted">-</span>
                    </td>
                    <td>
                      <span class="badge rounded-pill px-3 py-2 text-capitalize" :class="{
                        'bg-warning text-dark': app.status === 'applied',
                        'bg-info': app.status === 'shortlisted',
                        'bg-primary': app.status === 'interview_scheduled',
                        'bg-success': app.status === 'selected',
                        'bg-danger': app.status === 'rejected'
                      }">
                        {{ app.status }}
                      </span>
                    </td>
                  </tr>
                  <tr v-if="applications.length === 0">
                    <td colspan="6" class="text-center text-muted py-4">
                      No applications yet
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

      </div>

      <!-- Right Column: Profile Edit & Resume -->
      <div class="col-lg-4">
        
        <!-- Profile Card -->
        <div class="card border-0 shadow-sm rounded-4 mb-4">
          <div class="card-header bg-white fw-semibold py-3 border-0">
            My Profile Details
          </div>
          <div class="card-body pt-0">
            <form @submit.prevent="update_profile">
              <div class="mb-3">
                <label class="form-label text-muted small fw-semibold">Full Name</label>
                <input type="text" class="form-control rounded-3" v-model="profile.name" required />
              </div>
              <div class="mb-3">
                <label class="form-label text-muted small fw-semibold">Email Address</label>
                <input type="email" class="form-control rounded-3" v-model="profile.email" required />
              </div>
              <div class="mb-3">
                <label class="form-label text-muted small fw-semibold">Branch</label>
                <select class="form-select rounded-3" v-model="profile.branch" required>
                  <option disabled value="">Select Branch</option>
                  <option>CSE</option>
                  <option>IT</option>
                  <option>ECE</option>
                  <option>EE</option>
                  <option>ME</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label text-muted small fw-semibold">Year</label>
                <select class="form-select rounded-3" v-model="profile.year" required>
                  <option disabled value="">Select Year</option>
                  <option>1</option>
                  <option>2</option>
                  <option>3</option>
                  <option>4</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label text-muted small fw-semibold">CGPA</label>
                <input type="number" step="0.01" class="form-control rounded-3" v-model="profile.cgpa" required />
              </div>
              <button type="submit" class="btn btn-primary w-100 rounded-3 fw-semibold py-2">
                Save Changes
              </button>
            </form>
          </div>
        </div>

        <!-- Resume Upload Card -->
        <div class="card border-0 shadow-sm rounded-4 mb-4">
          <div class="card-header bg-white fw-semibold py-3 border-0">
            My Resume
          </div>
          <div class="card-body pt-0">
            <div v-if="profile.resume" class="mb-3 p-3 bg-light rounded-3 d-flex justify-content-between align-items-center">
              <span class="text-truncate me-2 small text-muted">Resume URL linked</span>
              <a :href="profile.resume" target="_blank" class="btn btn-sm btn-outline-secondary rounded-pill">
                View Resume
              </a>
            </div>
            <div v-else class="alert alert-warning py-2 small rounded-3">
              No resume uploaded yet.
            </div>

            <div class="mb-3">
              <label class="form-label text-muted small fw-semibold">Upload New Resume (PDF/Doc)</label>
              <input type="file" class="form-control rounded-3" @change="handle_file_change" accept=".pdf,.doc,.docx" />
            </div>
            <button class="btn btn-outline-primary w-100 rounded-3 fw-semibold py-2" @click="upload_resume">
              Upload Resume
            </button>
          </div>
        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
  import axios from 'axios'
  import { useRouter } from 'vue-router'
  import { ref, computed, onMounted } from 'vue'

  const router = useRouter()
  const drives = ref([])
  const applications = ref([])
  const student_id = localStorage.getItem('id')
  
  const profile = ref({
    name: '',
    email: '',
    branch: '',
    year: '',
    cgpa: '',
    resume: ''
  })

  const resumeFile = ref(null)

  function handle_file_change(event) {
    resumeFile.value = event.target.files[0]
  }

  async function fetch_profile() {
    try {
      const response = await axios.get(`https://placement-portal-using-flask-and-vue-js.onrender.com/student/${student_id}`)
      profile.value = response.data
    } catch (error) {
      console.error(error)
    }
  }

  async function update_profile() {
    try {
      const access_token = localStorage.getItem('access_token')
      const response = await axios.put(
        `https://placement-portal-using-flask-and-vue-js.onrender.com/student/update/${student_id}`,
        {
          name: profile.value.name,
          email: profile.value.email,
          branch: profile.value.branch,
          year: profile.value.year,
          cgpa: profile.value.cgpa
        },
        {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        }
      )
      alert(response.data.message)
      fetch_profile()
    } catch (error) {
      alert(error.response?.data?.error || error.message)
    }
  }

  async function upload_resume() {
    if (!resumeFile.value) {
      alert("Please select a file first.")
      return
    }
    try {
      const access_token = localStorage.getItem('access_token')
      const formData = new FormData()
      formData.append('resume', resumeFile.value)
      
      const response = await axios.post(
        "https://placement-portal-using-flask-and-vue-js.onrender.com/student/upload_resume",
        formData,
        {
          headers: {
            Authorization: `Bearer ${access_token}`,
            'Content-Type': 'multipart/form-data'
          }
        }
      )
      alert(response.data.message)
      profile.value.resume = response.data.resume_url
      fetch_profile()
    } catch (error) {
      alert(error.response?.data?.error || error.message)
    }
  }

  async function fetch_drives(){
    try{
      const access_token = localStorage.getItem('access_token')
      const response = await axios.get(
        'https://placement-portal-using-flask-and-vue-js.onrender.com/drive/all/',
        {
          headers: {
            Authorization:`Bearer ${access_token}`
          }
        }
      )
      drives.value = response.data
    }
    catch(error){
      console.error(error)
    }
  }

  async function register_applications(drive_id) {
    try{
      const access_token = localStorage.getItem('access_token')
      const response = await axios.post(
        "https://placement-portal-using-flask-and-vue-js.onrender.com/application/register",
        {
          drive_id: drive_id
        },
        {
          headers :{
            Authorization: `Bearer ${access_token}`
          } 
        }
      )
      alert(response.data.message)
      fetch_my_applications()
    }
    catch(error){
      alert(error.response?.data?.error || error.message)
    }
  }  

  async function fetch_my_applications() {
    try{
      const access_token = localStorage.getItem('access_token')
      const response = await axios.get(
        'https://placement-portal-using-flask-and-vue-js.onrender.com/application/my/',
        {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        } 
      )
      applications.value = response.data
    }
    catch(error){
      console.error(error)
    }
  }

  const shortlisted = computed(() => 
    applications.value.filter(a => a.status === 'shortlisted' || a.status === 'interview_scheduled').length
  )

  const selected = computed(() => 
    applications.value.filter(a => a.status === 'selected').length
  )

  function logout() {
    localStorage.clear()
    router.push('/login')
  }

  onMounted(() => {
    fetch_profile()
    fetch_drives()
    fetch_my_applications()
  })
  
  async function export_csv() {
    try{
      const access_token = localStorage.getItem('access_token')
      const response = await axios.post(
        'https://placement-portal-using-flask-and-vue-js.onrender.com/application/export/',
        {},
        {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        } 
      )
      alert(response.data.message)
    }
    catch(error){
      alert(error.response?.data?.error || error.message) 
    }
  }
</script>
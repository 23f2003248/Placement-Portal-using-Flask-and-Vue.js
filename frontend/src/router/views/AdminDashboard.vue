<template>
  <div class="container-fluid px-4 py-3">

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h3 class="mb-1 fw-bold">Admin Dashboard</h3>
        <p class="text-muted mb-0">
          Manage students, companies and placement drives
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
            <h6 class="text-muted">Total Students</h6>
            <h2 class="fw-bold mb-0">{{ students.length }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-4 mb-3">
        <div class="card border-0 shadow-sm rounded-4 h-100" style="background-color: #fce7f3;">
          <div class="card-body">
            <h6 class="text-muted">Total Companies</h6>
            <h2 class="fw-bold mb-0">{{ companies.length }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-4 mb-3">
        <div class="card border-0 shadow-sm rounded-4 h-100" style="background-color: #fef3c7;">
          <div class="card-body">
            <h6 class="text-muted">Total Drives</h6>
            <h2 class="fw-bold mb-0">{{ drives.length }}</h2>
          </div>
        </div>
      </div>
    </div>

    <!-- Search -->
    <div class="card border-0 shadow-sm rounded-4 mb-4">
      <div class="card-body">
        <div class="input-group">
          <input
            type="text"
            class="form-control rounded-start-3"
            placeholder="Search by student name, company, branch, resume..."
            v-model="searchQuery"
            @keyup.enter="search"
          />
          <button class="btn btn-dark rounded-end-3 px-4" @click="search">
            Search
          </button>
        </div>
      </div>
    </div>

    <!-- Search Results Section -->
    <div class="card border-0 shadow-sm rounded-4 mb-4 bg-light" v-if="isSearching">
      <div class="card-header bg-transparent border-0 fw-semibold d-flex justify-content-between align-items-center pt-3">
        <span>Search Results for "{{ searchQuery }}"</span>
        <button class="btn btn-sm btn-outline-secondary rounded-pill" @click="clear_search">
          Clear Results
        </button>
      </div>
      <div class="card-body pt-0">
        <div class="row">
          
          <!-- Students Matches -->
          <div class="col-md-6 mb-3">
            <div class="card border-0 rounded-3 shadow-sm h-100">
              <div class="card-header bg-white fw-semibold small">Matched Students</div>
              <div class="card-body p-0">
                <div class="list-group list-group-flush rounded-3">
                  <div class="list-group-item" v-for="student in searchResults.students" :key="student.id">
                    <div class="d-flex justify-content-between align-items-center">
                      <div>
                        <h6 class="mb-0 fw-semibold">{{ student.name }}</h6>
                        <small class="text-muted">{{ student.email }} | Branch: {{ student.branch }} | CGPA: {{ student.cgpa }}</small>
                      </div>
                      <span class="badge" :class="student.is_active ? 'bg-success' : 'bg-danger'">
                        {{ student.is_active ? 'Active' : 'Blacklisted' }}
                      </span>
                    </div>
                  </div>
                  <div class="p-3 text-center text-muted small" v-if="searchResults.students.length === 0">
                    No student matches found
                  </div>
                </div>
              </div>
            </div>
          </div>

          <!-- Companies Matches -->
          <div class="col-md-6 mb-3">
            <div class="card border-0 rounded-3 shadow-sm h-100">
              <div class="card-header bg-white fw-semibold small">Matched Companies</div>
              <div class="card-body p-0">
                <div class="list-group list-group-flush rounded-3">
                  <div class="list-group-item" v-for="company in searchResults.companies" :key="company.id">
                    <div class="d-flex justify-content-between align-items-center">
                      <div>
                        <h6 class="mb-0 fw-semibold">{{ company.name }}</h6>
                        <small class="text-muted">{{ company.email }} | HR: {{ company.hr_contact }} | Status: {{ company.approval_status }}</small>
                      </div>
                      <span class="badge" :class="company.is_active ? 'bg-success' : 'bg-danger'">
                        {{ company.is_active ? 'Active' : 'Blacklisted' }}
                      </span>
                    </div>
                  </div>
                  <div class="p-3 text-center text-muted small" v-if="searchResults.companies.length === 0">
                    No company matches found
                  </div>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>

    <!-- Pending Approvals -->
    <div class="row">
      
      <!-- Pending Companies -->
      <div class="col-lg-6 mb-4">
        <div class="card border-0 shadow-sm rounded-4 h-100">
          <div class="card-header bg-white fw-semibold py-3 border-0">
            Pending Company Approvals
          </div>
          <div class="card-body pt-0">
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead>
                  <tr>
                    <th>Company Name</th>
                    <th>HR Contact</th>
                    <th>Website</th>
                    <th class="text-end">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="company in companies.filter(c => c.approval_status === 'pending')" :key="company.id">
                    <td class="fw-semibold">{{ company.name }}</td>
                    <td>{{ company.hr_contact }}</td>
                    <td><small><a :href="company.website" target="_blank">{{ company.website }}</a></small></td>
                    <td class="text-end">
                      <div class="d-flex justify-content-end gap-2">
                        <button class="btn btn-success btn-sm px-3 rounded-pill fw-semibold" @click="approve_company(company.id, 'approved')">
                          Approve
                        </button>
                        <button class="btn btn-outline-danger btn-sm px-3 rounded-pill" @click="approve_company(company.id, 'rejected')">
                          Reject
                        </button>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="companies.filter(c => c.approval_status === 'pending').length === 0">
                    <td colspan="4" class="text-center text-muted py-3">
                      No pending company registrations
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Pending Drives -->
      <div class="col-lg-6 mb-4">
        <div class="card border-0 shadow-sm rounded-4 h-100">
          <div class="card-header bg-white fw-semibold py-3 border-0">
            Pending Drive Approvals
          </div>
          <div class="card-body pt-0">
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead>
                  <tr>
                    <th>Company</th>
                    <th>Job Title</th>
                    <th>CGPA / Year</th>
                    <th class="text-end">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="drive in drives.filter(d => d.status === 'pending')" :key="drive.drive_id">
                    <td class="fw-semibold">{{ drive.company_name }}</td>
                    <td>{{ drive.job_title }}</td>
                    <td><small class="text-muted">Min: {{ drive.elig_cgpa }} | Yr: {{ drive.elig_year }}</small></td>
                    <td class="text-end">
                      <div class="d-flex justify-content-end gap-2">
                        <button class="btn btn-success btn-sm px-3 rounded-pill fw-semibold" @click="approve_drive(drive.drive_id, 'approved')">
                          Approve
                        </button>
                        <button class="btn btn-outline-danger btn-sm px-3 rounded-pill" @click="approve_drive(drive.drive_id, 'rejected')">
                          Reject
                        </button>
                      </div>
                    </td>
                  </tr>
                  <tr v-if="drives.filter(d => d.status === 'pending').length === 0">
                    <td colspan="4" class="text-center text-muted py-3">
                      No pending drive approvals
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

    </div>

    <!-- Management Tables (Tabs-like Layout) -->
    <div class="row">
      
      <!-- Company Records -->
      <div class="col-lg-6 mb-4">
        <div class="card border-0 shadow-sm rounded-4">
          <div class="card-header bg-white fw-semibold py-3 border-0">
            All Company Records
          </div>
          <div class="card-body pt-0">
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Status</th>
                    <th>Active</th>
                    <th class="text-end">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="company in companies" :key="company.id">
                    <td class="fw-semibold">{{ company.name }}</td>
                    <td>
                      <span class="badge text-capitalize" :class="{
                        'bg-warning text-dark': company.approval_status === 'pending',
                        'bg-success': company.approval_status === 'approved',
                        'bg-danger': company.approval_status === 'rejected'
                      }">
                        {{ company.approval_status }}
                      </span>
                    </td>
                    <td>
                      <span class="badge" :class="company.is_active ? 'bg-success' : 'bg-danger'">
                        {{ company.is_active ? 'Yes' : 'No' }}
                      </span>
                    </td>
                    <td class="text-end">
                      <button v-if="company.is_active" class="btn btn-outline-danger btn-sm rounded-pill px-3" @click="set_company_active_status(company.id, false)">
                        Blacklist
                      </button>
                      <button v-else class="btn btn-outline-success btn-sm rounded-pill px-3" @click="set_company_active_status(company.id, true)">
                        Reactivate
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

      <!-- Student Records -->
      <div class="col-lg-6 mb-4">
        <div class="card border-0 shadow-sm rounded-4">
          <div class="card-header bg-white fw-semibold py-3 border-0">
            All Student Records
          </div>
          <div class="card-body pt-0">
            <div class="table-responsive">
              <table class="table table-hover align-middle mb-0">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Branch</th>
                    <th>CGPA</th>
                    <th>Active</th>
                    <th class="text-end">Actions</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="student in students" :key="student.id">
                    <td class="fw-semibold">{{ student.name }}</td>
                    <td>{{ student.branch }}</td>
                    <td>{{ student.cgpa }}</td>
                    <td>
                      <span class="badge" :class="student.is_active ? 'bg-success' : 'bg-danger'">
                        {{ student.is_active ? 'Yes' : 'No' }}
                      </span>
                    </td>
                    <td class="text-end">
                      <button v-if="student.is_active" class="btn btn-outline-danger btn-sm rounded-pill px-3" @click="set_student_active_status(student.id, false)">
                        Blacklist
                      </button>
                      <button v-else class="btn btn-outline-success btn-sm rounded-pill px-3" @click="set_student_active_status(student.id, true)">
                        Reactivate
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>

    </div>

  </div>
</template>

<script setup>
  import { ref, onMounted } from 'vue'
  import axios from 'axios'
  import { useRouter } from 'vue-router'

  const router = useRouter()
  const students = ref([])
  const drives = ref([])
  const companies = ref([])

  const searchQuery = ref('')
  const searchResults = ref({ students: [], companies: [] })
  const isSearching = ref(false)

  async function fetch_all_students(){
    try{
      const access_token = localStorage.getItem('access_token')
      const response = await axios.get(
        "https://placement-portal-using-flask-and-vue-js.onrender.com/student/all/",
        {
          headers:{
            Authorization: `Bearer ${access_token}`
          }
        }
      )
      students.value = response.data
    }
    catch(error){
      console.error(error)
    }
  }

  async function fetch_all_drives(){
    try{
      const access_token = localStorage.getItem('access_token')
      const response = await axios.get(
        "https://placement-portal-using-flask-and-vue-js.onrender.com/drive/all/admin/",
        {
          headers:{
            Authorization: `Bearer ${access_token}`
          }
        }
      )
      drives.value = response.data
    }
    catch(error){
      console.error(error)
    }
  }

  async function fetch_all_companies(){
    try{
      const access_token = localStorage.getItem('access_token')
      const response = await axios.get(
        "https://placement-portal-using-flask-and-vue-js.onrender.com/company/all/",
        {
          headers:{
            Authorization: `Bearer ${access_token}`
          }
        }
      )
      companies.value = response.data
    }
    catch(error){
      console.error(error)
    }
  }

  async function approve_company(id, status = 'approved') {
    try{
      const access_token = localStorage.getItem('access_token')
      const response = await axios.put(
        `https://placement-portal-using-flask-and-vue-js.onrender.com/admin/company/approve/${id}`,
        {
          status: status
        },
        {
          headers:{
            Authorization: `Bearer ${access_token}`
          }
        }
      )
      alert(response.data.message)
      fetch_all_companies()
    }
    catch(error){
      alert(error.response?.data?.error || error.message)
    }
  }

  async function approve_drive(id, status = 'approved') {
    try{
      const access_token = localStorage.getItem('access_token')
      const response = await axios.put(
        `https://placement-portal-using-flask-and-vue-js.onrender.com/admin/drive/approve/${id}`,
        {
          status: status
        },
        {
          headers:{
            Authorization: `Bearer ${access_token}`
          }
        }
      )
      alert(response.data.message)
      fetch_all_drives()
    }
    catch(error){
      alert(error.response?.data?.error || error.message)
    }
  }

  async function set_company_active_status(id, is_active) {
    try {
      const access_token = localStorage.getItem('access_token')
      const response = await axios.put(
        `https://placement-portal-using-flask-and-vue-js.onrender.com/admin/company/blacklist/${id}`,
        {
          is_active: is_active
        },
        {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        }
      )
      alert(response.data.message)
      fetch_all_companies()
    } catch(error) {
      alert(error.response?.data?.error || error.message)
    }
  }

  async function set_student_active_status(id, is_active) {
    try {
      const access_token = localStorage.getItem('access_token')
      const response = await axios.put(
        `https://placement-portal-using-flask-and-vue-js.onrender.com/admin/student/blacklist/${id}`,
        {
          is_active: is_active
        },
        {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        }
      )
      alert(response.data.message)
      fetch_all_students()
    } catch(error) {
      alert(error.response?.data?.error || error.message)
    }
  }

  async function search() {
    if (!searchQuery.value.trim()) {
      clear_search()
      return
    }
    try {
      const access_token = localStorage.getItem('access_token')
      const response = await axios.get(
        `https://placement-portal-using-flask-and-vue-js.onrender.com/admin/search/?q=${searchQuery.value}`,
        {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        }
      )
      searchResults.value = response.data
      isSearching.value = true
    } catch (error) {
      alert(error.response?.data?.error || error.message)
    }
  }

  function clear_search() {
    searchQuery.value = ''
    searchResults.value = { students: [], companies: [] }
    isSearching.value = false
  }

  function logout() {
    localStorage.clear()
    router.push('/login')
  }

  onMounted(() => {
    fetch_all_students()
    fetch_all_companies()
    fetch_all_drives()
  })
</script>
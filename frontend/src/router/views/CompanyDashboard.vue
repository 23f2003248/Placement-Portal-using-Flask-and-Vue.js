<template>
  <div class="container-fluid px-4 py-3">

    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
      <div>
        <h3 class="mb-1 fw-bold">Company Dashboard</h3>
        <p class="text-muted mb-0">
          Welcome, {{ companyName || 'Company' }}! Manage drives and review student applications.
        </p>
      </div>

      <div class="d-flex gap-2">
        <button class="btn btn-success rounded-3 fw-semibold" @click="router.push('/drive/create')">
          + Create Drive
        </button>
        <button class="btn btn-outline-danger px-4 rounded-3 fw-semibold" @click="logout">
          Logout
        </button>
      </div>
    </div>

    <!-- Stats Cards -->
    <div class="row mb-4">
      <div class="col-md-4 mb-3">
        <div class="card border-0 shadow-sm rounded-4 h-100" style="background-color: #dbeafe;">
          <div class="card-body">
            <h6 class="text-muted">Total Drives</h6>
            <h2 class="fw-bold mb-0">{{ drives.length }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-4 mb-3">
        <div class="card border-0 shadow-sm rounded-4 h-100" style="background-color: #fce7f3;">
          <div class="card-body">
            <h6 class="text-muted">Selected Drive Applicants</h6>
            <h2 class="fw-bold mb-0">{{ applications.length }}</h2>
          </div>
        </div>
      </div>

      <div class="col-md-4 mb-3">
        <div class="card border-0 shadow-sm rounded-4 h-100" style="background-color: #fef3c7;">
          <div class="card-body">
            <h6 class="text-muted">Shortlisted / Scheduled</h6>
            <h2 class="fw-bold mb-0">
              {{ applications.filter(a => a.status === 'shortlisted' || a.status === 'interview_scheduled').length }}
            </h2>
          </div>
        </div>
      </div>
    </div>

    <!-- My Drives -->
    <div class="card border-0 shadow-sm rounded-4 mb-4">
      <div class="card-header bg-white fw-semibold py-3 border-0">
        My Placement Drives
      </div>

      <div class="card-body pt-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead>
              <tr>
                <th>Job Title</th>
                <th>Eligible Branch</th>
                <th>Year</th>
                <th>CGPA</th>
                <th>Deadline</th>
                <th>Approval Status</th>
                <th class="text-end">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="drive in drives" :key="drive.drive_id" :class="{'table-active': selectedDriveId === drive.drive_id}">
                <td class="fw-semibold">{{ drive.job_title }}</td>
                <td><span class="badge bg-secondary">{{ drive.elig_branch }}</span></td>
                <td>Year {{ drive.elig_year }}</td>
                <td>{{ drive.elig_cgpa }}</td>
                <td>{{ new Date(drive.application_deadline).toLocaleDateString() }}</td>
                <td>
                  <span class="badge text-capitalize" :class="{
                    'bg-warning text-dark': drive.status === 'pending',
                    'bg-success': drive.status === 'approved',
                    'bg-danger': drive.status === 'rejected'
                  }">
                    {{ drive.status }}
                  </span>
                </td>
                <td class="text-end">
                  <div class="d-flex justify-content-end gap-2">
                    <button class="btn btn-primary btn-sm px-3 rounded-pill" @click="select_drive(drive)">
                      View Applicants
                    </button>
                    <button class="btn btn-outline-danger btn-sm rounded-pill" @click="delete_drive(drive.drive_id)">
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
              <tr v-if="drives.length === 0">
                <td colspan="7" class="text-center text-muted py-3">
                  No drives found
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Applications Received -->
    <div class="card border-0 shadow-sm rounded-4 mb-4" v-if="selectedDriveId">
      <div class="card-header bg-white fw-semibold py-3 border-0 d-flex justify-content-between align-items-center">
        <span>Applications for <strong class="text-primary">{{ selectedDriveTitle }}</strong></span>
        <span class="badge bg-light text-dark">{{ applications.length }} applicant(s)</span>
      </div>

      <div class="card-body pt-0">
        <div class="table-responsive">
          <table class="table table-hover align-middle mb-0">
            <thead>
              <tr>
                <th>Student Name</th>
                <th>Branch</th>
                <th>Year</th>
                <th>CGPA</th>
                <th>Resume</th>
                <th>Interview Date</th>
                <th>Status</th>
                <th class="text-end">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="app in applications" :key="app.application_id">
                <td class="fw-semibold">{{ app.student_name }}</td>
                <td>{{ app.branch }}</td>
                <td>Year {{ app.year }}</td>
                <td>{{ app.cgpa }}</td>
                <td>
                  <a v-if="app.resume" :href="app.resume" target="_blank" class="btn btn-outline-secondary btn-sm rounded-pill px-3">
                    View Resume
                  </a>
                  <span v-else class="text-muted small">No Resume</span>
                </td>
                <td>
                  <span v-if="app.interview_date" class="text-primary fw-semibold small">
                    {{ new Date(app.interview_date).toLocaleString() }}
                  </span>
                  <span v-else class="text-muted small">-</span>
                </td>
                <td>
                  <span class="badge rounded-pill text-capitalize px-3 py-2" :class="{
                    'bg-warning text-dark': app.status === 'applied',
                    'bg-info': app.status === 'shortlisted',
                    'bg-primary': app.status === 'interview_scheduled',
                    'bg-success': app.status === 'selected',
                    'bg-danger': app.status === 'rejected'
                  }">
                    {{ app.status }}
                  </span>
                </td>
                <td class="text-end">
                  <div class="d-flex justify-content-end gap-2 align-items-center">
                    
                    <!-- If Applied -->
                    <template v-if="app.status === 'applied'">
                      <button class="btn btn-info btn-sm rounded-pill px-3 fw-semibold text-white" @click="update_status(app.application_id, 'shortlisted')">
                        Shortlist
                      </button>
                      <button class="btn btn-outline-danger btn-sm rounded-pill px-3" @click="update_status(app.application_id, 'rejected')">
                        Reject
                      </button>
                    </template>

                    <!-- If Shortlisted -->
                    <template v-if="app.status === 'shortlisted'">
                      <div class="input-group input-group-sm w-auto">
                        <input type="datetime-local" class="form-control form-control-sm rounded-start-pill" :id="'date-' + app.application_id" />
                        <button class="btn btn-outline-primary btn-sm rounded-end-pill" @click="schedule_interview(app.application_id)">
                          Schedule
                        </button>
                      </div>
                      <button class="btn btn-success btn-sm rounded-pill px-3 fw-semibold" @click="update_status(app.application_id, 'selected')">
                        Select
                      </button>
                      <button class="btn btn-outline-danger btn-sm rounded-pill px-3" @click="update_status(app.application_id, 'rejected')">
                        Reject
                      </button>
                    </template>

                    <!-- If Interview Scheduled -->
                    <template v-if="app.status === 'interview_scheduled'">
                      <button class="btn btn-success btn-sm rounded-pill px-3 fw-semibold" @click="update_status(app.application_id, 'selected')">
                        Select
                      </button>
                      <button class="btn btn-outline-danger btn-sm rounded-pill px-3" @click="update_status(app.application_id, 'rejected')">
                        Reject
                      </button>
                    </template>

                    <!-- If Selected or Rejected -->
                    <span v-if="app.status === 'selected' || app.status === 'rejected'" class="text-muted small">
                      Closed
                    </span>

                  </div>
                </td>
              </tr>
              <tr v-if="applications.length === 0">
                <td colspan="8" class="text-center text-muted py-3">
                  No applicants for this drive yet
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
  import axios from "axios"
  import { ref, onMounted } from 'vue'
  import { useRouter } from 'vue-router'

  const router = useRouter()
  const company_id = localStorage.getItem('id')
  const companyName = ref('')
  const drives = ref([])
  const selectedDriveId = ref(null)
  const selectedDriveTitle = ref('')
  const applications = ref([])

  async function fetch_company_profile() {
    try {
      const response = await axios.get(`https://placement-portal-using-flask-and-vue-js.onrender.com/company/${company_id}/`)
      companyName.value = response.data.name
    } catch(err) {
      console.error(err)
    }
  }

  async function fetch_company_drives(){
    try{
      const access_token = localStorage.getItem('access_token')
      const response = await axios.get(
        "https://placement-portal-using-flask-and-vue-js.onrender.com/drive/company/",
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

  function select_drive(drive) {
    selectedDriveId.value = drive.drive_id
    selectedDriveTitle.value = drive.job_title
    fetch_applications(drive.drive_id)
  }

  async function fetch_applications(drive_id) {
    try{
      const access_token = localStorage.getItem('access_token')
      const response = await axios.get(
        `https://placement-portal-using-flask-and-vue-js.onrender.com/application/drive/${drive_id}`,
        {
          headers:{
            Authorization : `Bearer ${access_token}`
          }
        }
      )
      applications.value = response.data
    }
    catch(error){
      alert(error.response?.data?.error || error.message)
    }
  }

  async function update_status(app_id, status) {
    try{
      const access_token = localStorage.getItem('access_token')
      const response = await axios.put(
        `https://placement-portal-using-flask-and-vue-js.onrender.com/application/update/${app_id}`,
        {
          status: status
        },
        {
          headers:{
            Authorization : `Bearer ${access_token}`
          }
        }
      )
      alert(response.data.message)
      fetch_applications(selectedDriveId.value)
    }
    catch(error){
      alert(error.response?.data?.error || error.message)
    }
  }

  async function schedule_interview(app_id) {
    const inputElement = document.getElementById('date-' + app_id)
    if (!inputElement || !inputElement.value) {
      alert("Please select a date and time.")
      return
    }
    
    try {
      const access_token = localStorage.getItem('access_token')
      const response = await axios.put(
        `https://placement-portal-using-flask-and-vue-js.onrender.com/application/update/${app_id}`,
        {
          interview_date: inputElement.value
        },
        {
          headers:{
            Authorization : `Bearer ${access_token}`
          }
        }
      )
      alert(response.data.message)
      fetch_applications(selectedDriveId.value)
    } catch (error) {
      alert(error.response?.data?.error || error.message)
    }
  }

  async function delete_drive(drive_id) {
    if (!confirm("Are you sure you want to delete this placement drive?")) {
      return
    }
    try {
      const access_token = localStorage.getItem('access_token')
      const response = await axios.delete(
        `https://placement-portal-using-flask-and-vue-js.onrender.com/drive/delete/${drive_id}`,
        {
          headers: {
            Authorization: `Bearer ${access_token}`
          }
        }
      )
      alert(response.data.message)
      if (selectedDriveId.value === drive_id) {
        selectedDriveId.value = null
        selectedDriveTitle.value = ''
        applications.value = []
      }
      fetch_company_drives()
    } catch (error) {
      alert(error.response?.data?.error || error.message)
    }
  }

  function logout() {
    localStorage.clear()
    router.push('/login')
  }

  onMounted(() => {
    fetch_company_profile()
    fetch_company_drives()
  })
</script>
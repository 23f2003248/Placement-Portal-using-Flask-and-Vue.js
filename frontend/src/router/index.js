import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from './views/LandingPage.vue'
import Login from './views/Login.vue'
import StudentRegister from './views/StudentRegister.vue'
import CompanyRegister from './views/CompanyRegister.vue'
import StudentDashboard from './views/StudentDashboard.vue'
import CompanyDashboard from './views/CompanyDashboard.vue'
import AdminDashboard from './views/AdminDashboard.vue'
import CreateDrive from './views/CreateDrive.vue'


const routes =[
  { path: '/', component: LandingPage },
  {path: '/login', component : Login},
  {path: '/student/register', component : StudentRegister},
  {path: '/company/register', component : CompanyRegister},
  {path: '/student/dashboard', component : StudentDashboard},
  {path: '/company/dashboard', component : CompanyDashboard},
  {path: '/admin/dashboard', component : AdminDashboard},
  {path: '/drive/create', component : CreateDrive}
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router

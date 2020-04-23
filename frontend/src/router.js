import AudioRecorder from 'vue-audio-recorder'
import FormSelectPlugin from 'bootstrap-vue'
import Vue from 'vue'
import VueRouter from 'vue-router'
import store from '@/store.js'

import SignupComponent from "@/views/signup.vue"
import ConfirmComponent from "@/views/confirm.vue"
import DashboardComponent  from "@/views/Dashboard.vue"

Vue.use(AudioRecorder)
Vue.use(FormSelectPlugin)
Vue.use(VueRouter)

let router = new VueRouter({
    routes: [
        {
            path: '/',
            name: "dashboard",
            component: DashboardComponent,
            meta: { auth: true }
        },
        {
            path: "/signup",
            name: "signup",
            component: SignupComponent,
            meta: { auth: false }
        },
        {
            path: "/confirm",
            name: "confirm",
            component: ConfirmComponent,
            meta: { auth: false }
        },
    ],
})

router.beforeEach((to, from, next) =>  {
  if (to.meta.auth && !store.getters.isLoggedIn) {
    next({name: 'signup'})
  } else if (store.getters.isLoggedIn && (to.name === "signup" || to.name === "confirm")) {
    next({name: 'dashboard'})
  } else {
    next()
  }
})

export default router

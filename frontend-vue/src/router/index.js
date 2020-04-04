import AudioRecorder from 'vue-audio-recorder'
import FormSelectPlugin from 'bootstrap-vue'
import Vue from 'vue'
import VueRouter from 'vue-router'

import SignupComponent from "../views/signup.vue"
import ConfirmComponent from "../views/confirm.vue"
import SubmitComponent from "../views/submit.vue"
import RetrieveComponent from "../views/retrieve.vue"

Vue.use(AudioRecorder)
Vue.use(FormSelectPlugin)
Vue.use(VueRouter)

export default new VueRouter({
    routes: [
        {
            path: '/',
            redirect: {
                name: "signup"
            }
        },
        {
            path: "/signup",
            name: "signup",
            component: SignupComponent
        },
        {
            path: "/confirm",
            name: "confirm",
            component: ConfirmComponent
        },
        {
            path: "/submit",
            name: "submit",
            component: SubmitComponent
        },
        {
            path: "/retrieve",
            name: "retrieve",
            component: RetrieveComponent
        }
    ]
})

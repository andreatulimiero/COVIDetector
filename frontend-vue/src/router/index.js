import Vue from 'vue'
import VueRouter from 'vue-router'
import SignupComponent from "../views/signup.vue"
import SubmitComponent from "../views/submit.vue"
import RetrieveComponent from "../views/retrieve.vue"

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

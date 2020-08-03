<template>
  <div>
    <p>Secret page</p>
    <div v-for="user in users" :key="user.id">
      <ul>
        <li>Public ID: {{ user.public_id }}</li>
        <li>Email: {{ user.email }}</li>
      </ul>
    </div>
  </div>
</template>

<script>
    // import { mapState } from "vuex"

    export default {
        middleware: "auth-admin",

        // async fetch({ $axios, store }) {
        //     const response = await $axios.$get("/user")
        //     const users = response.data
        //     store.commit("SET_USERS", users) // 'SET_USERS', users) // try: 'store.commit('user/SET_USERS', …' when using file other than index.js
        // },

        // computed: {
        //     ...mapState(["users"])
        // }
    }
</script>

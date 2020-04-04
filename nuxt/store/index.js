// import axios from '@/plugins/axios'

export const state = () => ({
  users: [],
})

export const mutations = {
  SET_USERS(state, payload) {
    state.users = payload
  },
}

// export const actions = {
//   async nuxtServerInit({ commit }) {
//     const response = await axios.get('/user')
//     const users = response.data
//     commit('SET_USERS', users)
//   }
// }

// import axios from '@/plugins/axios'

export const state = () => ({
  users: [],
  self : [],
  self_tax_records: []
})

export const mutations = {
  SET_USERS(state, payload) {
    state.users = payload
  },
  SET_SELF(state, payload) {
    state.self = payload
  },
  SET_SELF_TAX_RECORDS(state, payload) {
    state.self_tax_records = payload
  },
}

// export const actions = {
//   async nuxtServerInit({ commit }) {
//     const response = await axios.get('/user')
//     const users = response.data
//     commit('SET_USERS', users)
//   }
// }

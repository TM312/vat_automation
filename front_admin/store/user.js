export const state = () => ({
  users: [],
  user: [],
  self_user: [],
  actions: []
})

export const mutations = {
  SET_USERS(state, users) {
    state.users = users
  },
  SET_USER(state, user) {
    state.user = user
  },
  SET_SELF_USER(state, user) {
    state.self_user = user
  },
  SET_ACTIONS(state, actions) {
    state.actions = actions
  }
}

export const actions = {
  async get_all({ commit }) {
    const res = await this.$repositories.user.get_all()
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_USERS', data.data)
    } else {
      // Handle error here
    }
  },

  async get_actions({ commit }) {
    const res = await this.$repositories.user.get_actions()
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_USERS', data.data)
    } else {
      // Handle error here
    }
  },

  async get_by_id({ commit }, user_public_id) {

    const res = await this.$repositories.user.get_by_id(user_public_id)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_USER', data.data)
    } else {
      // Handle error here
    }
  },

  async get_self({ commit }) {
    const res = await this.$repositories.user.get_self()
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_SELF_USER', data.data)
    } else {
      // Handle error here
    }
  },

  async create({ commit }, user_data) {
    const res = await this.$repositories.user.create(user_data)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_USER', data.data)
    } else {
      // Handle error here
    }
  },

  async update({ commit }, user_public_id, data_changes) {
    const res = await this.$repositories.user.update(user_public_id, data_changes)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_USER', data.data)
    } else {
      // Handle error here
    }
  },

  async delete_user({ commit }, user_public_id) {
    const res = await this.$repositories.user.delete(user_public_id)
    const { status, data } = res
    if (status === 200 && data.data) {
      // Remove from store
      commit('SET_USER', [])
    } else {
      // Handle error here
    }
  }
}

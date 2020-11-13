export const state = () => ({
  transaction_types: [],
  transaction_type: []
})

export const mutations = {
  SET_TRANSACTION_TYPES(state, transaction_types) {
    state.transaction_types = transaction_types
  },
  SET_TRANSACTION_TYPE(state, transaction_type) {
    state.transaction_type = transaction_type
  },
  // https://stackoverflow.com/questions/55781792/how-to-update-object-in-vuex-store-array
  UPDATE_IN_LIST(state, transaction_type) {
    var index = state.transaction_types.findIndex(el => (el.code === transaction_type.code))
    state.transaction_types = [
      ...state.transaction_types.slice(0, index),
      transaction_type,
      ...state.transaction_types.slice(index + 1)
    ]
  }
}

export const actions = {
  async get_all({ commit }) {
    const res = await this.$repositories.transaction_type.get_all()
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_TRANSACTION_TYPES', data.data)
    } else {
      // Handle error here
    }
  },

  async create({ commit }, transaction_type_data) {
    const res = await this.$repositories.transaction_type.create(transaction_type_data)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_TRANSACTION_TYPE', data.data)
    } else {
      // Handle error here
    }
  },

  async get_by_code({ commit }, transaction_type_code) {

    const res = await this.$repositories.transaction_type.get_by_code(transaction_type_code)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_TRANSACTION_TYPE', data.data)
    } else {
      // Handle error here
    }
  },

  async update_in_list({ commit }, payload) {
    const transaction_type_code = payload.shift()
    const data_changes = payload[0]
    const res = await this.$repositories.transaction_type.update(transaction_type_code, data_changes)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('UPDATE_IN_LIST', data.data)
    } else {
      // Handle error here
    }
  },

  async delete_by_code({ commit }, transaction_type_code) {
    const res = await this.$repositories.transaction_type.delete(transaction_type_code)
    const { status, data } = res
    if (status === 200 && data.data) {
      // Remove from store
      commit('SET_TRANSACTION_TYPE', [])
    } else {
      // Handle error here
    }
  }
}

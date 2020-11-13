export const state = () => ({
  transaction_types_public: [],
  transaction_type_public: []
})

export const mutations = {
  SET_TRANSACTION_TYPES_PUBLIC(state, transaction_types_public) {
    state.transaction_types_public = transaction_types_public
  },
  SET_TRANSACTION_TYPE_PUBLIC(state, transaction_type_public) {
    state.transaction_type_public = transaction_type_public
  },
  // https://stackoverflow.com/questions/55781792/how-to-update-object-in-vuex-store-array
  UPDATE_IN_LIST(state, transaction_type_public) {
    var index = state.transaction_types_public.findIndex(el => (el.public_id === transaction_type_public.public_id))
    state.transaction_types_public = [
      ...state.transaction_types_public.slice(0, index),
      transaction_type_public,
      ...state.transaction_types_public.slice(index + 1)
    ]
  }
}

export const actions = {
  async get_all({ commit }) {
    const res = await this.$repositories.transaction_type_public.get_all()
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_TRANSACTION_TYPES_PUBLIC', data.data)
    } else {
      // Handle error here
    }
  },

  async create({ commit }, transaction_type_public_data) {
    const res = await this.$repositories.transaction_type_public.create(transaction_type_public_data)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_TRANSACTION_TYPE_PUBLIC', data.data)
    } else {
      // Handle error here
    }
  },

  async get_by_public_id({ commit }, transaction_type_public_public_id) {

    const res = await this.$repositories.transaction_type_public.get_by_public_id(transaction_type_public_public_id)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_TRANSACTION_TYPE_PUBLIC', data.data)
    } else {
      // Handle error here
    }
  },

  async update_in_list({ commit }, payload) {
    const transaction_type_public_public_id = payload.shift()
    const data_changes = payload[0]
    const res = await this.$repositories.transaction_type_public.update(transaction_type_public_public_id, data_changes)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('UPDATE_IN_LIST', data.data)
    } else {
      // Handle error here
    }
  },

  async delete_by_public_id({ commit }, transaction_type_public_public_id) {
    const res = await this.$repositories.transaction_type_public.delete(transaction_type_public_public_id)
    const { status, data } = res
    if (status === 200 && data.data) {
      // Remove from store
      commit('SET_TRANSACTION_TYPE_PUBLIC', [])
    } else {
      // Handle error here
    }
  }
}

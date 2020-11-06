export const state = () => ({
  tax_rate_types: [],
  tax_rate_type: []
})

export const mutations = {
  SET_TAX_RATE_TYPES(state, tax_rate_types) {
    state.tax_rate_types = tax_rate_types
  },
  SET_TAX_RATE_TYPE(state, tax_rate_type) {
    state.tax_rate_type = tax_rate_type
  }
}

export const actions = {
  async get_all({ commit }) {
    const res = await this.$repositories.tax_rate_type.get_all()
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_TAX_RATE_TYPES', data.data)
    } else {
      // Handle error here
    }
  },

  async create({ commit }, tax_rate_type_data) {
    const res = await this.$repositories.tax_rate_type.create(tax_rate_type_data)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_TAX_RATE_TYPE', data.data)
    } else {
      // Handle error here
    }
  },

  async get_by_code({ commit }, tax_rate_type_code) {

    const res = await this.$repositories.tax_rate_type.get_by_code(tax_rate_type_code)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_TAX_RATE_TYPE', data.data)
    } else {
      // Handle error here
    }
  },

  async update({ commit }, tax_rate_type_code, data_changes) {
    const res = await this.$repositories.tax_rate_type.update(tax_rate_type_code, data_changes)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_TAX_RATE_TYPE', data.data)
    } else {
      // Handle error here
    }
  },

  async delete_by_code({ commit }, tax_rate_type_code) {
    const res = await this.$repositories.tax_rate_type.delete(tax_rate_type_code)
    const { status, data } = res
    if (status === 200 && data.data) {
      // Remove from store
      commit('SET_TAX_RATE_TYPE', [])
    } else {
      // Handle error here
    }
  }
}

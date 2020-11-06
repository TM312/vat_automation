export const state = () => ({
  vat_thresholds: [],
  vat_threshold: []
})

export const getters = {
  getByCountryCode: state => countryCode => state.vat_thresholds.find(vat_threshold => vat_threshold.country_code === countryCode)
}

export const mutations = {
  SET_VAT_THRESHOLDS(state, vat_thresholds) {
    state.vat_thresholds = vat_thresholds
  },
  SET_VAT_THRESHOLD(state, vat_threshold) {
    state.vat_threshold = vat_threshold
  }
}

export const actions = {
  async get_all({ commit }) {
    const res = await this.$repositories.vat_threshold.get_all()
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_VAT_THRESHOLDS', data.data)
    } else {
      // Handle error here
    }
  },

  async create({ commit }, vat_threshold_data) {
    const res = await this.$repositories.vat_threshold.create(vat_threshold_data)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_VAT_THRESHOLD', data.data)
    } else {
      // Handle error here
    }
  },

  async get_by_public_id({ commit }, vat_threshold_public_id) {

    const res = await this.$repositories.vat_threshold.get_by_public_id(vat_threshold_public_id)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_VAT_THRESHOLD', data.data)
    } else {
      // Handle error here
    }
  },

  async update({ commit }, vat_threshold_public_id, data_changes) {
    const res = await this.$repositories.vat_threshold.update(vat_threshold_public_id, data_changes)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_VAT_THRESHOLD', data.data)
    } else {
      // Handle error here
    }
  },

  async delete_by_public_id({ commit }, vat_threshold_public_id) {
    const res = await this.$repositories.vat_threshold.delete(vat_threshold_public_id)
    const { status, data } = res
    if (status === 200 && data.data) {
      // Remove from store
      commit('SET_VAT_THRESHOLD', [])
    } else {
      // Handle error here
    }
  }
}

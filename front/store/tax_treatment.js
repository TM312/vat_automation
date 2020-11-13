export const state = () => ({
  tax_treatments: [],
  tax_treatment: []
})

export const getters = {
  getByCode: state => taxTreatmentCode => state.tax_treatments.find(taxTreatment => taxTreatment.code === taxTreatmentCode)
}

export const mutations = {
  SET_TAX_TREATMENTS(state, tax_treatments) {
    state.tax_treatments = tax_treatments
  },
  SET_TAX_TREATMENT(state, tax_treatment) {
    state.tax_treatment = tax_treatment
  },
  // https://stackoverflow.com/questions/55781792/how-to-update-object-in-vuex-store-array
  UPDATE_IN_LIST(state, tax_treatment) {
    var index = state.tax_treatments.findIndex(el => (el.code === tax_treatment.code))
    state.tax_treatments = [
      ...state.tax_treatments.slice(0, index),
      tax_treatment,
      ...state.tax_treatments.slice(index + 1)
    ]
  }
}

export const actions = {
  async get_all({ commit }) {
    const res = await this.$repositories.tax_treatment.get_all()
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_TAX_TREATMENTS', data.data)
    } else {
      // Handle error here
    }
  },

  async create({ commit }, tax_treatment_data) {
    const res = await this.$repositories.tax_treatment.create(tax_treatment_data)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_TAX_TREATMENT', data.data)
    } else {
      // Handle error here
    }
  },

  async get_by_code({ commit }, tax_treatment_code) {

    const res = await this.$repositories.tax_treatment.get_by_code(tax_treatment_code)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_TAX_TREATMENT', data.data)
    } else {
      // Handle error here
    }
  },

  async update_in_list({ commit }, payload) {
    const tax_treatment_code = payload.shift()
    const data_changes = payload[0]
    const res = await this.$repositories.tax_treatment.update(tax_treatment_code, data_changes)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('UPDATE_IN_LIST', data.data)
    } else {
      // Handle error here
    }
  },

  async delete_by_code({ commit }, tax_treatment_code) {
    const res = await this.$repositories.tax_treatment.delete(tax_treatment_code)
    const { status, data } = res
    if (status === 200 && data.data) {
      // Remove from store
      commit('SET_TAX_TREATMENT', [])
    } else {
      // Handle error here
    }
  }
}

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

  async update({ commit }, tax_treatment_code, data_changes) {
    const res = await this.$repositories.tax_treatment.update(tax_treatment_code, data_changes)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_TAX_TREATMENT', data.data)
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

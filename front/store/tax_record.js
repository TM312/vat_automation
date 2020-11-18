export const state = () => ({
  tax_records: [],
  tax_record: []
})

export const mutations = {

  PUSH_TAX_RECORD(state, payload) {
    state.tax_records.push(payload)
  },

  // https://stackoverflow.com/questions/55781792/how-to-update-object-in-vuex-store-array
  UPDATE_IN_LIST(state, tax_record) {
    var index = state.tax_records.findIndex(el => (el.code === tax_record.code))
    if (index === -1) {
      state.tax_records.push(tax_record)

    } else {
      state.tax_records = [
        ...state.tax_records.slice(0, index),
        tax_record,
        ...state.tax_records.slice(index + 1)
      ]
    }
  },

  SET_TAX_RECORDS(state, payload) {
    state.tax_records = payload
  },
  SET_SELLER_FIRM_TAX_RECORDS(state, payload) {
    state.tax_records = payload
  },
  SET_TAX_RECORD(state, tax_record) {
    state.tax_record = tax_record
  },
  // !!!! NOT SURE IF WORKING maybe position of tax_record in array required
  SPLICE_TAX_RECORDS(state, payload) {
    state.tax_records.splice(payload, 1)
  },

  CLEAR_TAX_RECORDS(state) {
    state.tax_records = []
  },

  CLEAR_STATE(state) {
    state.tax_record = []
    state.tax_records = []
  },
}

export const actions = {


  async get_all({ commit }) {
    const res = await this.$repositories.tax_record.get_all()
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_TAX_RECORDS', data.data)
    } else {
      // Handle error here
    }
  },

  async get_by_public_id({ commit }, tax_record_public_id) {

    const res = await this.$repositories.tax_record.get_by_public_id(tax_record_public_id)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_TAX_RECORD', data.data)
    } else {
      // Handle error here
    }
  },

  async get_or_create({ commit }, payload) {
    const seller_firm_public_id = payload.shift()
    const parameters = payload[0]
    const res = await this.$repositories.tax_record.get_or_create(seller_firm_public_id, parameters)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('UPDATE_IN_LIST', data.data)
    } else {
      // Handle error here
    }
  },

  async download_by_id({ commit }, tax_record_public_id) {

    const res = await this.$repositories.tax_record.download_by_id(tax_record_public_id)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_TAX_RECORD', data.data)
    } else {
      // Handle error here
    }
  },


  async delete_by_public_id({ commit }, tax_record_public_id) {
    const res = await this.$repositories.tax_record.delete_by_public_id(tax_record_public_id)
    const { status, data } = res
    if (status === 200 && data.data) {
      // Remove from store
      commit('SPLICE_TAX_RECORDS', data.data)
    } else {
      // Handle error here
    }
  },

  async get_all_by_seller_firm_public_id({ commit }, seller_firm_public_id) {
    const res = await this.$repositories.tax_record.get_all_by_seller_firm_public_id(seller_firm_public_id)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_SELLER_FIRM_TAX_RECORDS', data.data)
    } else {
      // Handle error here
    }
  },

  async clear_tax_records({ commit }) {
    commit('CLEAR_TAX_RECORDS')
  },


  async clear_state({ commit }) {
    commit('CLEAR_STATE')
  },

  // async create_by_seller_firm_public_id({ commit }, data_array) {
  //     const seller_firm_public_id = data_array.shift()
  //     const tax_record_data = data_array[0]
  //     const res = await this.$repositories.tax_record.create_by_seller_firm_public_id(seller_firm_public_id, tax_record_data)
  //     const { status, data } = res
  //     if (status === 200 && data.data) {
  //         console.log(data.data)
  //         commit('SET_TAX_RECORD', data.data)
  //     } else {
  //         // Handle error here
  //     }
  // }

}

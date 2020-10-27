export const state = () => ({
  transactions: [],
  transaction: [],
})

export const getters = {
  getTransactionsByTaxTreatmentCode: state => taxTreatmentCode => state.transactions.filter(transaction => transaction.tax_treatment_code === taxTreatmentCode)
}

export const mutations = {
  SET_TRANSACTIONS(state, payload) {
    state.transactions = payload
  },

  SET_TRANSACTION(state, payload) {
    state.transaction = payload
  },

  PUSH_TRANSACTIONS(state, payload) {
    for (let i = 0; i < payload.length; i++)
      if (state.transactions.includes(payload[i]) === false) state.transactions.push(payload[i])
  }
}

export const actions = {
  async get_all({ commit }) {
    const res = await this.$repositories.transaction.get_all()
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_TRANSACTIONS', data.data)
    } else {
      // Handle error here
    }
  },

  async get_by_id({ commit }, transaction_id) {

    const res = await this.$repositories.transaction.get_by_id(transaction_id)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_TRANSACTION', data.data)
    } else {
      // Handle error here
    }
  },

  async get_by_public_id({ commit }, transaction_public_id) {

    const res = await this.$repositories.transaction.get_by_public_id(transaction_public_id)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_TRANSACTION', data.data)
    } else {
      // Handle error here
    }
  },

  async get_by_tax_record({ commit }, params) {

    const res = await this.$repositories.transaction.get_by_tax_record(params)
    const { status, data } = res
    if (status === 200 && data.data) {
      if (params['page'] === 1) {
        commit('SET_TRANSACTIONS', data.data)
      } else {
        commit('PUSH_TRANSACTIONS', data.data)
      }
    } else {
      // Handle error here
    }
  },

  async get_by_tax_record_tax_treatment({ commit }, params) {

    const res = await this.$repositories.transaction.get_by_tax_record_tax_treatment(params)
    const { status, data } = res
    if (status === 200 && data.data) {
      if (params['page'] === 1) {
        commit('SET_TRANSACTIONS', data.data)
      } else {
        commit('PUSH_TRANSACTIONS', data.data)
      }
    } else {
      // Handle error here
    }
  },
}

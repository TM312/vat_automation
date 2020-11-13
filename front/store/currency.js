export const state = () => ({
  currencies: [],
  currency: []
})

export const getters = {
  getNameByCode: state => currencyCode => state.currencies.find(currency => currency.code === currencyCode).name
}

export const mutations = {
  SET_CURRENCIES(state, currencies) {
    state.currencies = currencies
  },
  SET_CURRENCY(state, currency) {
    state.currency = currency
  },
  // https://stackoverflow.com/questions/55781792/how-to-update-object-in-vuex-store-array
  UPDATE_IN_LIST(state, currency) {
    var index = state.currencies.findIndex(el => (el.code === currency.code))
    state.currencies = [
      ...state.currencies.slice(0, index),
      currency,
      ...state.currencies.slice(index + 1)
    ]
  }
}

export const actions = {
  async get_all({ commit }) {
    const res = await this.$repositories.currency.get_all()
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_CURRENCIES', data.data)
    } else {
      // Handle error here
    }
  },

  async create({ commit }, currency_data) {
    const res = await this.$repositories.currency.create(currency_data)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_CURRENCY', data.data)
    } else {
      // Handle error here
    }
  },

  async get_by_code({ commit }, currency_code) {

    const res = await this.$repositories.currency.get_by_code(currency_code)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_CURRENCY', data.data)
    } else {
      // Handle error here
    }
  },

  async update_in_list({ commit }, payload) {
    const currency_code = payload.shift()
    const data_changes = payload[0]
    const res = await this.$repositories.currency.update(currency_code, data_changes)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('UPDATE_IN_LIST', data.data)
    } else {
      // Handle error here
    }
  },

  async delete_by_code({ commit }, currency_code) {
    const res = await this.$repositories.currency.delete(currency_code)
    const { status, data } = res
    if (status === 200 && data.data) {
      // Remove from store
      commit('SET_CURRENCY', [])
    } else {
      // Handle error here
    }
  }
}

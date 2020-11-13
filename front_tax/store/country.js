export const state = () => ({
  eu: [],
  countries: [],
  country: []
})

export const getters = {
  countryNameByCode: state => countryCode => state.countries.find(country => country.code === countryCode).name,
  getInclCurrencyOnly: state => state.countries.filter(country => !!country.currency_code)
}

export const mutations = {
  SET_COUNTRIES(state, countries) {
    state.countries = countries
  },
  SET_COUNTRY(state, country) {
    state.country = country
  },
  SET_EU(state, eu) {
    state.eu = eu
  },

  // https://stackoverflow.com/questions/55781792/how-to-update-object-in-vuex-store-array
  UPDATE_IN_LIST(state, country) {
    var index = state.countries.findIndex(el => (el.code === country.code))
    state.countries = [
      ...state.countries.slice(0, index),
      country,
      ...state.countries.slice(index + 1)
    ]
  }
}

export const actions = {
  async get_all({ commit }) {
    const res = await this.$repositories.country.get_all()
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_COUNTRIES', data.data)
    } else {
      // Handle error here
    }
  },

  async create({ commit }, country_data) {
    const res = await this.$repositories.country.create(country_data)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_COUNTRY', data.data)
    } else {
      // Handle error here
    }
  },

  async get_by_code({ commit }, country_code) {

    const res = await this.$repositories.country.get_by_code(country_code)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_COUNTRY', data.data)
    } else {
      // Handle error here
    }
  },

  async get_eu_by_date({ commit }, date_string) {

    const res = await this.$repositories.country.get_eu_by_date(date_string)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_EU', data.data)
    } else {
      // Handle error here
    }
  },

  async update_in_list({ commit }, payload) {
    const country_code = payload.shift()
    const data_changes = payload[0]
    const res = await this.$repositories.country.update(country_code, data_changes)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('UPDATE_IN_LIST', data.data)
    } else {
      // Handle error here
    }
  },

  async delete_by_code({ commit }, country_code) {
    const res = await this.$repositories.country.delete(country_code)
    const { status, data } = res
    if (status === 200 && data.data) {
      // Remove from store
      commit('SET_COUNTRY', [])
    } else {
      // Handle error here
    }
  }
}

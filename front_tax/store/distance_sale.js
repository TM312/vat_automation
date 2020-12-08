export const state = () => ({
  distance_sales: [],
  distance_sale: []
})


export const getters = {
  getPANEU: state => state.distance_sales.filter(distance_sale => ['DE', 'FR', 'PL', 'CZ', 'GB', 'IT', 'ES', 'NL'].includes(distance_sale.arrival_country_code))
}

export const mutations = {
  SET_DISTANCE_SALES(state, payload) {
    state.distance_sales = payload
  },
  SET_DISTANCE_SALE(state, payload) {
    state.distance_sale = payload
  }
}

export const actions = {
  async get_all({ commit }) {
    const res = await this.$repositories.distance_sale.get_all()
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_DISTANCE_SALES', data.data)
    } else {
      // Handle error here
    }
  },

  async create({ commit }, distance_sale_data) {
    const res = await this.$repositories.distance_sale.create(distance_sale_data)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_DISTANCE_SALE', data.data)

    } else {
      // Handle error here
    }
  },

  async create_by_seller_firm_public_id({ commit }, data_array) {
    const seller_firm_public_id = data_array.shift()
    const distance_sale_data = data_array[0]

    const res = await this.$repositories.distance_sale.create_by_seller_firm_public_id(seller_firm_public_id, distance_sale_data)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_DISTANCE_SALE', data.data)

    } else {
      // Handle error here
    }
  },

  async get_by_public_id({ commit }, distance_sale_public_id) {

    const res = await this.$repositories.distance_sale.get_by_public_id(distance_sale_public_id)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_DISTANCE_SALE', data.data)
    } else {
      // Handle error here
    }
  },

  async update_by_public_id({ commit }, distance_sale_public_id, data_changes) {
    const res = await this.$repositories.distance_sale.update_by_public_id(distance_sale_public_id, data_changes)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_DISTANCE_SALE', data.data)
    } else {
      // Handle error here
    }
  },

  async delete_by_public_id({ commit }, distance_sale_public_id) {
    const res = await this.$repositories.distance_sale.delete_by_public_id(distance_sale_public_id)
    const { status, message, data } = res
    if (status === 200 && data.data) {
      // Remove from store
      commit('SET_DISTANCE_SALE', [])
      return message

    } else {
      // Handle error here
    }
  },

  async upload(distance_sale_information_files) {
    const res = await this.$repositories.distance_sale.upload(distance_sale_information_files)
    const { status, message } = res
    if (status === 200 && message) {
      // Display Notification
    } else {
      // Handle error here
    }
  }
}

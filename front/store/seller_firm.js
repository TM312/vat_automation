export const state = () => ({
  seller_firms: [],
  seller_firm: []
})


export const getters = {
  vatNumberByCountryCode: state => countryCode => state.seller_firm.vat_numbers.find(el => el.country_code === countryCode),
  getPANEUDistanceSales: state => state.seller_firm.distance_sales.filter(distance_sale => ['DE', 'FR', 'PL', 'CZ', 'GB', 'IT', 'ES'].includes(distance_sale.arrival_country_code))
}

export const mutations = {
  CLEAR_SELLER_FIRM(state) {
    state.seller_firm = []
  },

  CLEAR_ACCOUNTS(state) {
    while (state.seller_firm.accounts.length) {
      state.seller_firm.accounts.pop()
    }
  },

  CLEAR_ITEMS(state) {
    while (state.seller_firm.items.length) {
      state.seller_firm.items.pop()
    }
  },

  CLEAR_VAT_NUMBERS(state) {
    while (state.seller_firm.vat_numbers.length) {
      state.seller_firm.vat_numbers.pop()
    }
  },

  CLEAR_DISTANCE_SALES(state) {
    while (state.seller_firm.distance_sales.length) {
      state.seller_firm.distance_sales.pop()
    }
  },


  SET_SELLER_FIRMS(state, seller_firms) {
    state.seller_firms = seller_firms
  },

  SET_SELLER_FIRM(state, seller_firm) {
    state.seller_firm = seller_firm
  },

  // if check is necessary -> if (state.seller_firm.accounts.includes(account) === false) state.seller_firm.accounts.push(account)

  PUSH_ACCOUNT(state, account) {
    state.seller_firm.accounts.push(account)
  },

  PUSH_ACCOUNTS(state, accounts) {
    state.seller_firm.accounts.push(...accounts)
  },

  PUSH_ITEM(state, item) {
    state.seller_firm.items.push(item)
  },

  PUSH_ITEMS(state, items) {
    state.seller_firm.items.push(...items)
  },

  PUSH_DISTANCE_SALE(state, distance_sale) {
    state.seller_firm.distance_sales.push(distance_sale)
  },

  PUSH_DISTANCE_SALES(state, distance_sales) {
    state.seller_firm.distance_sales.push(...distance_sales)
  },

  PUSH_VAT_NUMBER(state, vat_number) {
    state.seller_firm.vat_numbers.push(vat_number)
  },

  PUSH_VAT_NUMBERS(state, vat_numbers) {
    state.seller_firm.vat_numbers.push(...vat_numbers)
  },

  // https://stackoverflow.com/questions/55781792/how-to-update-object-in-vuex-store-array
  UPDATE_VAT_NUMBER(state, vat_number) {
    var index = state.seller_firm.vat_numbers.findIndex(el => (el.country_code === vat_number.country_code && el.number === vat_number.number))
    state.seller_firm.vat_numbers = [
      ...state.seller_firm.vat_numbers.slice(0, index),
      vat_number,
      ...state.seller_firm.vat_numbers.slice(index + 1)
    ]
  }
}


export const actions = {
  async clear_seller_firm({ commit }) {
    commit('CLEAR_SELLER_FIRM')
  },

  async get_all({ commit }) {
    const res = await this.$repositories.seller_firm.get_all()
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_SELLER_FIRMS', data.data)
    } else {
      // Handle error here
    }
  },

  async get_sample({ commit }) {
    const res = await this.$repositories.seller_firm.get_sample()
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_SELLER_FIRM', data.data)
    } else {
      // Handle error here
    }
  },

  async create({ commit }, seller_firm_data) {
    const res = await this.$repositories.seller_firm.create(seller_firm_data)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_SELLER_FIRM', data.data)
    } else {
      // Handle error here
    }
  },

  async get_by_public_id({ commit }, seller_firm_public_id) {

    const res = await this.$repositories.seller_firm.get_by_public_id(seller_firm_public_id)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_SELLER_FIRM', data.data)
    } else {
      // Handle error here
    }
  },

  async update({ commit }, payload ) {
    const seller_firm_public_id = payload.shift()
    const data_changes = payload[0]

    const res = await this.$repositories.seller_firm.update(seller_firm_public_id, data_changes)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_SELLER_FIRM', data.data)
    } else {
      // Handle error here
    }
  },

  async delete_by_public_id({ commit }, seller_firm_public_id) {
    const res = await this.$repositories.seller_firm.delete_by_public_id(seller_firm_public_id)
    const { status, data } = res
    if (status === 200 && data.data) {
      // Remove from store
      commit('SET_SELLER_FIRM', [])
    } else {
      // Handle error here
    }
  },


  // async upload_create(seller_firm_information_files) {
  //     const res = await this.$repositories.seller_firm.upload_create(seller_firm_information_files)
  //     const { status, message } = res
  //     if (status === 200 && message) {
  //         // Display Notification
  //     } else {
  //         // Handle error here
  //     }
  // },

  // async upload(account_information_files) {
  //     const res = await this.$repositories.account.upload(account_information_files)
  //     const { status, message } = res
  //     if (status === 200 && message) {
  //         // Display Notification
  //     } else {
  //         // Handle error here
  //     }
  // }


}

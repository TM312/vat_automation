export const state = () => ({
    currencies: [],
    currency: []
})

export const mutations = {
    SET_CURRENCIES(state, currencies) {
        state.currencies = currencies
    },
    SET_CURRENCY(state, currency) {
        state.currency = currency
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

    async update({ commit }, currency_code, data_changes) {
        const res = await this.$repositories.currency.update(currency_code, data_changes)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_CURRENCY', data.data)
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

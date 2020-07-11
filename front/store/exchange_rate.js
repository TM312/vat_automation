export const state = () => ({
    exchange_rates: [],
    exchange_rate: []
})

export const mutations = {
    SET_EXCHANGE_RATES(state, exchange_rates) {
        state.exchange_rates = exchange_rates
    },
    SET_EXCHANGE_RATE(state, exchange_rate) {
        state.exchange_rate = exchange_rate
    }
}

export const actions = {
    async get_all({ commit }) {
        const res = await this.$repositories.exchange_rate.get_all()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_EXCHANGE_RATES', data.data)
        } else {
            // Handle error here
        }
    },

    async create({ commit }, exchange_rate_data) {
        const res = await this.$repositories.exchange_rate.create(exchange_rate_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_EXCHANGE_RATE', data.data)
        } else {
            // Handle error here
        }
    },

    async get_by_id({ commit }, exchange_rate_id) {

        const res = await this.$repositories.exchange_rate.get_by_id(exchange_rate_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_EXCHANGE_RATE', data.data)
        } else {
            // Handle error here
        }
    },

    async update({ commit }, exchange_rate_id, data_changes) {
        const res = await this.$repositories.exchange_rate.update(exchange_rate_id, data_changes)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_EXCHANGE_RATE', data.data)
        } else {
            // Handle error here
        }
    },

    async delete_by_id({ commit }, exchange_rate_id) {
        const res = await this.$repositories.exchange_rate.delete(exchange_rate_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_EXCHANGE_RATE', [])
        } else {
            // Handle error here
        }
    }
}

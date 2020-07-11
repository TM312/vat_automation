export const state = () => ({
    customer_firms: [],
    customer_firm: []
})

export const mutations = {
    SET_CUSTOMER_FIRMS(state, customer_firms) {
        state.customer_firms = customer_firms
    },
    SET_CUSTOMER_FIRM(state, customer_firm) {
        state.customer_firm = customer_firm
    }
}

export const actions = {
    async get_all({ commit }) {
        const res = await this.$repositories.customer_firm.get_all()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_CUSTOMER_FIRMS', data.data)
        } else {
            // Handle error here
        }
    },

    async create({ commit }, customer_firm_data) {
        const res = await this.$repositories.customer_firm.create(customer_firm_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_CUSTOMER_FIRM', data.data)
        } else {
            // Handle error here
        }
    },

    async get_by_id({ commit }, customer_firm_id) {

        const res = await this.$repositories.customer_firm.get_by_id(customer_firm_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_CUSTOMER_FIRM', data.data)
        } else {
            // Handle error here
        }
    },

    async update({ commit }, customer_firm_id, data_changes) {
        const res = await this.$repositories.customer_firm.update(customer_firm_id, data_changes)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_CUSTOMER_FIRM', data.data)
        } else {
            // Handle error here
        }
    },

    async delete_by_id({ commit }, customer_firm_id) {
        const res = await this.$repositories.customer_firm.delete(customer_firm_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_CUSTOMER_FIRM', [])
        } else {
            // Handle error here
        }
    }
}

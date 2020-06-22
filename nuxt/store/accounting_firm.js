export const state = () => ({
    accounting_firms: [],
    accounting_firm: []
})

export const mutations = {
    SET_ACCOUNTING_FIRMS(state, accounting_firms) {
        state.accounting_firms = accounting_firms
    },
    SET_ACCOUNTING_FIRM(state, accounting_firm) {
        state.accounting_firm = accounting_firm
    }
}

export const actions = {
    async get_all({ commit }) {
        const res = await this.$repositories.accounting_firm.get_all()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_ACCOUNTING_FIRMS', data.data)
        } else {
            // Handle error here
        }
    },

    async create({ commit }, accounting_firm_data) {
        const res = await this.$repositories.accounting_firm.create(accounting_firm_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_ACCOUNTING_FIRM', data.data)
        } else {
            // Handle error here
        }
    },

    async get_by_id({ commit }, accounting_firm_id) {

        const res = await this.$repositories.accounting_firm.get_by_id(accounting_firm_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_ACCOUNTING_FIRM', data.data)
        } else {
            // Handle error here
        }
    },

    async update({ commit }, accounting_firm_id, data_changes) {
        const res = await this.$repositories.accounting_firm.update(accounting_firm_id, data_changes)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_ACCOUNTING_FIRM', data.data)
        } else {
            // Handle error here
        }
    },

    async delete_by_id({ commit }, accounting_firm_id) {
        const res = await this.$repositories.accounting_firm.delete(accounting_firm_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_ACCOUNTING_FIRM', [])
        } else {
            // Handle error here
        }
    }
}

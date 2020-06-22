export const state = () => ({
    tax_auditors: [],
    tax_auditor: [],
    self_tax_auditor: []
})

export const mutations = {
    SET_TAX_AUDITORS(state, tax_auditors) {
        state.tax_auditors = tax_auditors
    },
    SET_TAX_AUDITOR(state, tax_auditor) {
        state.tax_auditor = tax_auditor
    },
    SET_SELF_TAX_AUDITOR(state, tax_auditor) {
        state.self_tax_auditor = tax_auditor
    }
}

export const actions = {
    async get_all({ commit }) {
        const res = await this.$repositories.tax_auditor.get_all()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TAX_AUDITORS', data.data)
        } else {
            // Handle error here
        }
    },

    async get_by_id({ commit }, tax_auditor_id) {

        const res = await this.$repositories.tax_auditor.get_by_id(tax_auditor_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TAX_AUDITOR', data.data)
        } else {
            // Handle error here
        }
    },

    async get_self({ commit }) {
        const res = await this.$repositories.tax_auditor.get_self()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_SELF_TAX_AUDITOR', data.data)
        } else {
            // Handle error here
        }
    },

    async create({ commit }, tax_auditor_data) {
        const res = await this.$repositories.tax_auditor.create(tax_auditor_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TAX_AUDITOR', data.data)
        } else {
            // Handle error here
        }
    },

    async update({ commit }, tax_auditor_id, data_changes) {
        const res = await this.$repositories.tax_auditor.update(tax_auditor_id, data_changes)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TAX_AUDITOR', data.data)
        } else {
            // Handle error here
        }
    },

    async delete_by_id({ commit }, tax_auditor_id) {
        const res = await this.$repositories.tax_auditor.delete(tax_auditor_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_TAX_AUDITOR', [])
        } else {
            // Handle error here
        }
    }
}

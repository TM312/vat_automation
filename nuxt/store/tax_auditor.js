export const state = () => ({
    tax_auditors: [],
    tax_auditor: []
})

export const mutations = {
    SET_TAX_AUDITORS(state, tax_auditors) {
        state.tax_auditors = tax_auditors
    },
    SET_TAX_AUDITOR(state, tax_auditor) {
        state.tax_auditor = tax_auditor
    }
}

export const actions = {
    async get_tax_auditors({ commit }) {
        const res = await this.$repositories.tax_auditor.get_all()
        const { status, data } = res
        if (status === 200 && data.success && data.code) {
            const { data } = data
            commit('SET_TAX_AUDITORS', data)
        } else {
            // Handle error here
        }
    },

    async get_tax_auditor({ commit }, tax_auditor) {
        const res = await this.$repositories.tax_auditor.get_by_id(tax_auditor)
        const { status, data } = res
        if (status === 200 && data.success && data.code) {
            const { data } = data
            commit('SET_TAX_AUDITOR', data)
        } else {
            // Handle error here
        }
    },

    async create_tax_auditor({ commit }, id, tax_auditor) {
        const res = await this.$repositories.tax_auditor.create(id, tax_auditor)
        const { status, data } = res
        if (status === 200 && data.success && data.code) {
            const { data } = data
            commit('SET_TAX_AUDITOR', data)
        } else {
            // Handle error here
        }
    },

    async update_tax_auditor({ commit }, id, tax_auditor) {
        const res = await this.$repositories.tax_auditor.update(id, tax_auditor)
        const { status, data } = res
        if (status === 200 && data.success && data.code) {
            const { data } = data
            commit('SET_TAX_AUDITOR', data)
        } else {
            // Handle error here
        }
    },

    async delete_tax_auditor({ commit }, id) {
        const res = await this.$repositories.tax_auditor.delete(id)
        const { status, data } = res
        if (status === 200 && data.success && data.code) {
            // Remove from store
            commit('SET_TAX_AUDITOR', [])
        } else {
            // Handle error here
        }
    }
}

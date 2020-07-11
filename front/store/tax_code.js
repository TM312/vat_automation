export const state = () => ({
    tax_codes: [],
    tax_code: []
})

export const mutations = {
    SET_TAX_CODES(state, tax_codes) {
        state.tax_codes = tax_codes
    },
    SET_TAX_CODE(state, tax_code) {
        state.tax_code = tax_code
    }
}

export const actions = {
    async get_all({ commit }) {
        const res = await this.$repositories.tax_code.get_all()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TAX_CODES', data.data)
        } else {
            // Handle error here
        }
    },

    async create({ commit }, tax_code_data) {
        const res = await this.$repositories.tax_code.create(tax_code_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TAX_CODE', data.data)
        } else {
            // Handle error here
        }
    },

    async get_by_code({ commit }, tax_code_code) {

        const res = await this.$repositories.tax_code.get_by_code(tax_code_code)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TAX_CODE', data.data)
        } else {
            // Handle error here
        }
    },

    async update({ commit }, tax_code_code, data_changes) {
        const res = await this.$repositories.tax_code.update(tax_code_code, data_changes)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TAX_CODE', data.data)
        } else {
            // Handle error here
        }
    },

    async delete_by_code({ commit }, tax_code_code) {
        const res = await this.$repositories.tax_code.delete(tax_code_code)
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_TAX_CODE', [])
        } else {
            // Handle error here
        }
    }
}

export const state = () => ({
    tax_records: [],
    seller_firm_tax_records: [],
    tax_record: []
})

export const mutations = {
    SET_TAX_RECORDS(state, tax_records) {
        state.tax_records = tax_records
    },
    SET_SELLER_FIRM_TAX_RECORDS(state, tax_records) {
        state.seller_firm_tax_records = tax_records
    },
    SET_TAX_RECORD(state, tax_record) {
        state.tax_record = tax_record
    }
}

export const actions = {
    async get_all({ commit }) {
        const res = await this.$repositories.tax_record.get_all()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TAX_RECORDS', data.data)
        } else {
            // Handle error here
        }
    },

    async generate({ commit }, tax_record_data) {
        const res = await this.$repositories.tax_record.generate(tax_record_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TAX_RECORD', data.data)
        } else {
            // Handle error here
        }
    },

    async download_by_id({ commit }, tax_record_public_id) {

        const res = await this.$repositories.tax_record.download_by_id(tax_record_public_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TAX_RECORD', data.data)
        } else {
            // Handle error here
        }
    },


    async delete_by_id({ commit }, tax_record_public_id) {
        const res = await this.$repositories.tax_record.delete(tax_record_public_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_TAX_RECORD', [])
        } else {
            // Handle error here
        }
    },

    async get_all_by_seller_firm_public_id({ commit }, seller_firm_public_id) {
        const res = await this.$repositories.tax_record.get_all_by_seller_firm_public_id(seller_firm_public_id)
        const { status, data } = res
        if (status === 200 && data.message) {
            commit('SET_SELLER_FIRM_TAX_RECORDS', data.data)
        } else {
            // Handle error here
        }
    }
}

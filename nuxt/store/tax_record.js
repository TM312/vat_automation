export const state = () => ({
    tax_records: [],
    tax_record: []
})

export const mutations = {
    SET_TAX_RECORDS(state, tax_records) {
        state.tax_records = tax_records
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

    async create({ commit }, tax_record_data) {
        const res = await this.$repositories.tax_record.create(tax_record_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TAX_RECORD', data.data)
        } else {
            // Handle error here
        }
    },

    async get_by_id({ commit }, tax_record_id) {

        const res = await this.$repositories.tax_record.get_by_id(tax_record_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TAX_RECORD', data.data)
        } else {
            // Handle error here
        }
    },

    async update({ commit }, tax_record_id, data_changes) {
        const res = await this.$repositories.tax_record.update(tax_record_id, data_changes)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TAX_RECORD', data.data)
        } else {
            // Handle error here
        }
    },

    async delete_by_id({ commit }, tax_record_id) {
        const res = await this.$repositories.tax_record.delete(tax_record_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_TAX_RECORD', [])
        } else {
            // Handle error here
        }
    },

    async upload(tax_record_information_files) {
        const res = await this.$repositories.tax_record.upload(tax_record_information_files)
        const { status, message } = res
        if (status === 200 && message) {
            // Display Notification
        } else {
            // Handle error here
        }
    }
}

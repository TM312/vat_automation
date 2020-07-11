export const state = () => ({
    transaction_inputs: [],
    transaction_input: []
})

export const mutations = {
    SET_TRANSACTION_INPUTS(state, transaction_inputs) {
        state.transaction_inputs = transaction_inputs
    },
    SET_TRANSACTION_INPUT(state, transaction_input) {
        state.transaction_input = transaction_input
    }
}

export const actions = {
    async get_all({ commit }) {
        const res = await this.$repositories.transaction_input.get_all()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TRANSACTION_INPUTS', data.data)
        } else {
            // Handle error here
        }
    },

    async get_by_id({ commit }, transaction_input_id) {

        const res = await this.$repositories.transaction_input.get_by_id(transaction_input_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TRANSACTION_INPUT', data.data)
        } else {
            // Handle error here
        }
    },

    async update({ commit }, transaction_input_id, data_changes) {
        const res = await this.$repositories.transaction_input.update(transaction_input_id, data_changes)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TRANSACTION_INPUT', data.data)
        } else {
            // Handle error here
        }
    },

    async delete_by_id({ commit }, transaction_input_id) {
        const res = await this.$repositories.transaction_input.delete(transaction_input_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_TRANSACTION_INPUT', [])
        } else {
            // Handle error here
        }
    },

    async upload(transaction_input_files) {
        const res = await this.$repositories.transaction_input.upload(transaction_input_files)
        const { status, message } = res
        if (status === 200 && message) {
            // Display Notification
        } else {
            // Handle error here
        }
    }
}

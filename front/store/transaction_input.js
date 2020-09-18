export const state = () => ({
    transaction_inputs: [],
    transaction_input: []
})

export const mutations = {

    CLEAR_TRANSACTION_INPUTS(state) {
        while (state.transaction_inputs.length) {
            state.transaction_inputs.pop()
        }
    },

    SET_TRANSACTION_INPUTS(state, payload) {
        state.transaction_inputs = payload
    },

    SET_TRANSACTION_INPUT(state, payload) {
        state.transaction_input = payload
    },

    UPDATE_TRANSACTION_INPUTS(state, payload) {
        Object.assign(state.transaction_inputs[payload.index], payload.transaction_input);
    },

    PUSH_TRANSACTION_INPUTS(state, payload) {
        for (let i = 0; i < payload.length; i++)
            if (state.transaction_inputs.includes(payload[i]) === false) state.transaction_inputs.push(payload[i])
    },

    PUSH_TRANSACTION_INPUT(state, payload) {
        state.transaction_inputs.push(payload)
    },

    PUSH_TRANSACTION_INPUTS_DIRECT(state, payload) {
        state.transaction_inputs.push(...payload)
    },


}

// export const getters = {
//     transactionInputsChannelCode: state => channelCode => state.transaction_input.transaction_inputs.filter(transaction_input => transaction_input.channel_code === channelCode)
// }


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


    async delete_all({ commit }) {
        const res = await this.$repositories.transaction_input.delete_all()
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_TRANSACTION_INPUTS', [])
        } else {
            // Handle error here
        }
    },

    async get_by_public_id({ commit }, transaction_input_public_id) {

        const res = await this.$repositories.transaction_input.get_by_public_id(transaction_input_public_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TRANSACTION_INPUT', data.data)
        } else {
            // Handle error here
        }
    },

    async get_by_seller_firm_public_id({ commit }, params) {

        const res = await this.$repositories.transaction_input.get_by_seller_firm_public_id(params)
        const { status, data } = res
        if (status === 200 && data.data) {
            if (params['page'] === 1) {
                commit('SET_TRANSACTION_INPUTS', data.data)
            } else {
                commit('PUSH_TRANSACTION_INPUTS', data.data)
            }
        } else {
            // Handle error here
        }
    },


    async update_by_public_id({ commit }, transaction_input_public_id, data_changes) {
        const res = await this.$repositories.transaction_input.update_by_public_id(transaction_input_public_id, data_changes)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TRANSACTION_INPUT', data.data)
        } else {
            // Handle error here
        }
    },

    async delete_by_public_id({ commit }, transaction_input_public_id) {
        const res = await this.$repositories.transaction_input.delete_by_public_id(transaction_input_public_id)
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

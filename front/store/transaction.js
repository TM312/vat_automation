export const state = () => ({
    transactions: [],
    transaction: []
})

export const mutations = {
    SET_TRANSACTIONS(state, transactions) {
        state.transactions = transactions
    },
    SET_TRANSACTION(state, transaction) {
        state.transaction = transaction
    }
}

export const actions = {
    async get_all({ commit }) {
        const res = await this.$repositories.transaction.get_all()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TRANSACTIONS', data.data)
        } else {
            // Handle error here
        }
    },

    async get_by_id({ commit }, transaction_id) {

        const res = await this.$repositories.transaction.get_by_id(transaction_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TRANSACTION', data.data)
        } else {
            // Handle error here
        }
    }
}

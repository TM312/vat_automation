export const state = () => ({
    accounts: [],
    account: []
})

export const mutations = {
    SET_ACCOUNTS(state, accounts) {
        state.accounts = accounts
    },
    SET_ACCOUNT(state, account) {
        state.account = account
    }
}

export const actions = {
    async get_all({ commit }) {
        const res = await this.$repositories.account.get_all()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_ACCOUNTS', data.data)
        } else {
            // Handle error here
        }
    },

    async get_by_public_id({ commit }, account_public_id) {

        const res = await this.$repositories.account.get_by_public_id(account_public_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_ACCOUNT', data.data)
        } else {
            // Handle error here
        }
    },

    async create({ commit }, account_data) {
        const res = await this.$repositories.account.create(account_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_ACCOUNT', data.data)
        } else {
            // Handle error here
        }
    },

    async create_by_seller_firm_public_id({ commit }, data_array) {
        const seller_firm_public_id = data_array.shift()
        const account_data = data_array[0]

        const res = await this.$repositories.account.create_by_seller_firm_public_id(seller_firm_public_id, account_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_ACCOUNT', data.data)

        } else {
            // Handle error here
        }
    },



    async update_by_public_id({ commit }, account_public_id, data_changes) {
        const res = await this.$repositories.account.update_by_public_id(account_public_id, data_changes)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_ACCOUNT', data.data)
        } else {
            // Handle error here
        }
    },


    async delete_by_public_id({ commit }, account_public_id) {
        const res = await this.$repositories.account.delete_by_public_id(account_public_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_ACCOUNT', [])
        } else {
            // Handle error here
        }
    },

    async upload(account_information_files) {
        const res = await this.$repositories.account.upload(account_information_files)
        const { status, message } = res
        if (status === 200 && message) {
            // Display Notification
        } else {
            // Handle error here
        }
    }
}

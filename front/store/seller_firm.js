export const state = () => ({
    seller_firms: [],
    seller_firm: []
})


export const mutations = {
    SET_SELLER_FIRMS(state, seller_firms) {
        state.seller_firms = seller_firms
    },
    SET_SELLER_FIRM(state, seller_firm) {
        state.seller_firm = seller_firm
    }
}

export const getters = {
    // countEmployees: state => state.seller_firm.employees.length,
    countAccounts: state => state.seller_firm.accounts.length,
    // countDistanceSales: state => state.seller_firm.distance_sales.length,
    countItems: state => state.seller_firm.len_items, //!!! does this work?
    countVatNumbers: state => state.seller_firm.vat_numbers.length,
    //countTransactionInputsSellerFirm: state => state.seller_firm.accounts.map(account => account.transaction_inputs),
    // publicId: state => state.seller_firm.public_id,
    // transactionInputs: state => state.seller_firm.accounts.map(account => account.transaction_inputs),
    // transactions: state => state.seller_firm.accounts.map(account => account.transactions)
    accountTransactionInputs: state => channelCode => {
        return state.seller_firm.accounts.filter(account => account.channel_code === channelCode).transaction_inputs
    }
}

export const actions = {
    async get_all({ commit }) {
        const res = await this.$repositories.seller_firm.get_all()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_SELLER_FIRMS', data.data)
        } else {
            // Handle error here
        }
    },

    async create({ commit }, seller_firm_data) {
        const res = await this.$repositories.seller_firm.create(seller_firm_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_SELLER_FIRM', data.data)
        } else {
            // Handle error here
        }
    },

    async get_by_public_id({ commit }, seller_firm_public_id) {

        const res = await this.$repositories.seller_firm.get_by_public_id(seller_firm_public_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_SELLER_FIRM', data.data)
        } else {
            // Handle error here
        }
    },

    async update({ commit }, seller_firm_id, data_changes) {
        const res = await this.$repositories.seller_firm.update(seller_firm_id, data_changes)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_SELLER_FIRM', data.data)
        } else {
            // Handle error here
        }
    },

    async create_as_client({ commit }, seller_firm_data) {
        const res = await this.$repositories.seller_firm.create_as_client(seller_firm_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_SELLER_FIRM', data.data)
        } else {
            // Handle error here
        }
    },

    async delete_by_public_id({ commit }, seller_firm_public_id) {
        const res = await this.$repositories.seller_firm.delete_by_public_id(seller_firm_public_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_SELLER_FIRM', [])
        } else {
            // Handle error here
        }
    },


    // async upload_create(seller_firm_information_files) {
    //     const res = await this.$repositories.seller_firm.upload_create(seller_firm_information_files)
    //     const { status, message } = res
    //     if (status === 200 && message) {
    //         // Display Notification
    //     } else {
    //         // Handle error here
    //     }
    // },

    // async upload(account_information_files) {
    //     const res = await this.$repositories.account.upload(account_information_files)
    //     const { status, message } = res
    //     if (status === 200 && message) {
    //         // Display Notification
    //     } else {
    //         // Handle error here
    //     }
    // }


}

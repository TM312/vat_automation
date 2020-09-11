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
    },

    // if check is necessary -> if (state.seller_firm.accounts.includes(account) === false) state.seller_firm.accounts.push(account)

    PUSH_ACCOUNT(state, account) {
        state.seller_firm.accounts.push(account)
    },

    PUSH_ACCOUNTS(state, accounts) {
        state.seller_firm.accounts.push(...accounts)
    },

    PUSH_ITEM(state, item) {
        state.seller_firm.items.push(item)
    },

    PUSH_ITEMS(state, items) {
        state.seller_firm.items.push(...items)
    },

    PUSH_DISTANCE_SALE(state, distance_sale) {
        state.seller_firm.distance_sales.push(distance_sale)
    },

    PUSH_DISTANCE_SALES(state, distance_sales) {
        state.seller_firm.distance_sales.push(...distance_sales)
    },

    PUSH_VAT_NUMBER(state, vat_number) {
        state.seller_firm.vat_numbers.push(vat_number)
    },

    PUSH_VAT_NUMBERS(state, vat_numbers) {
        state.seller_firm.vat_numbers.push(...vat_numbers)
    }
}

export const getters = {
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

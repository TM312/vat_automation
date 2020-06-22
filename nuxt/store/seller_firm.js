export const state = () => ({
    seller_firms: [],
    client_seller_firms: [],
    seller_firm: []
})

export const mutations = {
    SET_SELLER_FIRMS(state, seller_firms) {
        state.seller_firms = seller_firms
    },
    SET_CLIENT_SELLER_FIRMS(state, seller_firms) {
        state.client_seller_firms = seller_firms
    },
    SET_SELLER_FIRM(state, seller_firm) {
        state.seller_firm = seller_firm
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

    async get_by_id({ commit }, seller_firm_id) {

        const res = await this.$repositories.seller_firm.get_by_id(seller_firm_id)
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

    async delete_by_id({ commit }, seller_firm_id) {
        const res = await this.$repositories.seller_firm.delete(seller_firm_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_SELLER_FIRM', [])
        } else {
            // Handle error here
        }
    },

    async get_clients({ commit }) {
        const res = await this.$repositories.seller_firm.get_clients()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_CLIENT_SELLER_FIRMS', data.data)
        } else {
            // Handle error here
        }
    },

    async upload(seller_firm_information_files) {
        const res = await this.$repositories.seller_firm.upload(seller_firm_information_files)
        const { status, message } = res
        if (status === 200 && message) {
            // Display Notification
        } else {
            // Handle error here
        }
    }
}

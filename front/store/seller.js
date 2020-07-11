export const state = () => ({
    sellers: [],
    seller: [],
    // self_seller: []
})

export const mutations = {
    SET_SELLERS(state, sellers) {
        state.sellers = sellers
    },
    SET_SELLER(state, seller) {
        state.seller = seller
    },
    // SET_SELF_SELLER(state, seller) {
    //     state.self_seller = seller
    // }
}

export const actions = {
    async get_all({ commit }) {
        const res = await this.$repositories.seller.get_all()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_SELLERS', data.data)
        } else {
            // Handle error here
        }
    },

    async get_by_id({ commit }, seller_id) {

        const res = await this.$repositories.seller.get_by_id(seller_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_SELLER', data.data)
        } else {
            // Handle error here
        }
    },


    async create({ commit }, seller_data) {
        const res = await this.$repositories.seller.create(seller_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_SELLER', data.data)
        } else {
            // Handle error here
        }
    },



    async update({ commit }, seller_id, data_changes) {
        const res = await this.$repositories.seller.update(seller_id, data_changes)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_SELLER', data.data)
        } else {
            // Handle error here
        }
    },

    async delete_by_id({ commit }, seller_id) {
        const res = await this.$repositories.seller.delete(seller_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_SELLER', [])
        } else {
            // Handle error here
        }
    }
}

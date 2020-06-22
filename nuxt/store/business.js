export const state = () => ({
    businesses: [],
    business: []
})

export const mutations = {
    SET_BUSINESSES(state, businesses) {
        state.businesses = businesses
    },
    SET_BUSINESS(state, business) {
        state.business = business
    }
}

export const actions = {
    async get_all({ commit }) {
        const res = await this.$repositories.business.get_all()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_BUSINESSES', data.data)
        } else {
            // Handle error here
        }
    },

    // async create({ commit }, business_data) {
    //     const res = await this.$repositories.business.create(business_data)
    //     const { status, data } = res
    //     if (status === 200 && data.data) {
    //         commit('SET_BUSINESS', data.data)
    //     } else {
    //         // Handle error here
    //     }
    // },

    async get_by_id({ commit }, business_id) {

        const res = await this.$repositories.business.get_by_id(business_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_BUSINESS', data.data)
        } else {
            // Handle error here
        }
    },

    async update({ commit }, business_id, data_changes) {
        const res = await this.$repositories.business.update(business_id, data_changes)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_BUSINESS', data.data)
        } else {
            // Handle error here
        }
    },

    async delete_by_id({ commit }, business_id) {
        const res = await this.$repositories.business.delete(business_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_BUSINESS', [])
        } else {
            // Handle error here
        }
    }
}

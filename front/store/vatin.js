export const state = () => ({
    vatins: [],
    vatin: []
})

export const mutations = {
    SET_VATINS(state, vatins) {
        state.vatins = vatins
    },
    SET_VATIN(state, vatin) {
        state.vatin = vatin
    }
}

export const actions = {
    async get_all({ commit }) {
        const res = await this.$repositories.vatin.get_all()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_VATINS', data.data)
        } else {
            // Handle error here
        }
    },

    async create({ commit }, vatin_data) {
        const res = await this.$repositories.vatin.create(vatin_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_VATIN', data.data)
        } else {
            // Handle error here
        }
    },

    async create_by_seller_firm_public_id({ commit }, data_array) {
        const seller_firm_public_id = data_array.shift()
        const vatin_data = data_array[0]

        const res = await this.$repositories.vatin.create_by_seller_firm_public_id(seller_firm_public_id, vatin_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_VATIN', data.data)

        } else {
            // Handle error here
        }
    },

    async verify({ commit }, vatin_data) {
        const res = await this.$repositories.vatin.verify(vatin_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_VATIN', data.data)
        } else {
            // Handle error here
        }
    },

    async get_by_id({ commit }, vatin_id) {

        const res = await this.$repositories.vatin.get_by_id(vatin_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_VATIN', data.data)
        } else {
            // Handle error here
        }
    },

    async update({ commit }, vatin_id, data_changes) {
        const res = await this.$repositories.vatin.update(vatin_id, data_changes)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_VATIN', data.data)
        } else {
            // Handle error here
        }
    },

    async delete_by_public_id({ commit }, vatin_public_id) {
        const res = await this.$repositories.vatin.delete_by_public_id(vatin_public_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_VATIN', [])
        } else {
            // Handle error here
        }
    },

    async upload(vatin_information_files) {
        const res = await this.$repositories.vatin.upload(vatin_information_files)
        const { status, message } = res
        if (status === 200 && message) {
            // Display Notification
        } else {
            // Handle error here
        }
    }
}

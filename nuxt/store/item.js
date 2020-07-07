export const state = () => ({
    items: [],
    item: []
})

export const mutations = {
    SET_ITEMS(state, items) {
        state.items = items
    },
    SET_ITEM(state, item) {
        state.item = item
    }
}

export const actions = {
    async get_all({ commit }) {
        const res = await this.$repositories.item.get_all()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_ITEMS', data.data)
        } else {
            // Handle error here
        }
    },

    async get_by_id({ commit }, item_id) {

        const res = await this.$repositories.item.get_by_id(item_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_ITEM', data.data)
        } else {
            // Handle error here
        }
    },

    async create({ commit }, item_data) {
        const res = await this.$repositories.item.create(item_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_ITEM', data.data)
        } else {
            // Handle error here
        }
    },

    async create_by_seller_firm_public_id({ commit }, data_array) {
        const seller_firm_public_id = data_array.shift()
        const item_data = data_array[0]

        const res = await this.$repositories.item.create_by_seller_firm_public_id(seller_firm_public_id, item_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_ITEM', data.data)

        } else {
            // Handle error here
        }
    },


    async update({ commit }, item_id, data_changes) {
        const res = await this.$repositories.item.update(item_id, data_changes)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_ITEM', data.data)
        } else {
            // Handle error here
        }
    },

    async delete_by_id({ commit }, item_id) {
        const res = await this.$repositories.item.delete(item_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_ITEM', [])
        } else {
            // Handle error here
        }
    },

    async delete_by_public_id({ commit }, item_public_id) {
        const res = await this.$repositories.item.delete_by_public_id(item_public_id)
        const { status, message, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_ITEM', [])
            return message

        } else {
            // Handle error here
        }
    },


    async upload(item_information_files) {
        const res = await this.$repositories.item.upload(item_information_files)
        const { status, message } = res
        if (status === 200 && message) {
            // Display Notification
        } else {
            // Handle error here
        }
    }
}

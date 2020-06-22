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

    async create({ commit }, item_data) {
        const res = await this.$repositories.item.create(item_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_ITEM', data.data)
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

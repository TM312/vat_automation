export const state = () => ({
    channels: [],
    channel: []
})

export const mutations = {
    SET_CHANNELS(state, channels) {
        state.channels = channels
    },
    SET_CHANNEL(state, channel) {
        state.channel = channel
    }
}

export const actions = {
    async get_all({ commit }) {
        const res = await this.$repositories.channel.get_all()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_CHANNELS', data.data)
        } else {
            // Handle error here
        }
    },

    async create({ commit }, channel_data) {
        const res = await this.$repositories.channel.create(channel_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_CHANNEL', data.data)
        } else {
            // Handle error here
        }
    },

    async get_by_code({ commit }, channel_code) {

        const res = await this.$repositories.channel.get_by_code(channel_code)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_CHANNEL', data.data)
        } else {
            // Handle error here
        }
    },

    async update({ commit }, channel_code, data_changes) {
        const res = await this.$repositories.channel.update(channel_code, data_changes)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_CHANNEL', data.data)
        } else {
            // Handle error here
        }
    },

    async delete_by_code({ commit }, channel_code) {
        const res = await this.$repositories.channel.delete(channel_code)
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_CHANNEL', [])
        } else {
            // Handle error here
        }
    }
}

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
  },
  UPDATE_CHANNEL_IN_LIST(state, currency) {
    var index = state.currencies.findIndex(el => (el.code === currency.code))
    state.currencies = [
      ...state.currencies.slice(0, index),
      currency,
      ...state.currencies.slice(index + 1)
    ]
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

  async update_in_list({ commit }, payload) {
    const channel_code = payload.shift()
    const data_changes = payload[0]
    const res = await this.$repositories.channel.update(channel_code, data_changes)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('UPDATE_CHANNEL_IN_LIST', data.data)
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

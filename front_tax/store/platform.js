export const state = () => ({
  platforms: [],
  platform: []
})

export const mutations = {
  SET_PLATFORMS(state, platforms) {
    state.platforms = platforms
  },
  SET_PLATFORM(state, platform) {
    state.platform = platform
  },

  // https://stackoverflow.com/questions/55781792/how-to-update-object-in-vuex-store-array
  UPDATE_IN_LIST(state, platform) {
    var index = state.platforms.findIndex(el => (el.code === platform.code))
    state.platforms = [
      ...state.platforms.slice(0, index),
      platform,
      ...state.platforms.slice(index + 1)
    ]
  }
}

export const actions = {
  async get_all({ commit }) {
    const res = await this.$repositories.platform.get_all()
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_PLATFORMS', data.data)
    } else {
      // Handle error here
    }
  },

  async create({ commit }, platform_data) {
    const res = await this.$repositories.platform.create(platform_data)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_PLATFORM', data.data)
    } else {
      // Handle error here
    }
  },

  async get_by_id({ commit }, platform_id) {

    const res = await this.$repositories.platform.get_by_id(platform_id)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_PLATFORM', data.data)
    } else {
      // Handle error here
    }
  },

  async update_in_list({ commit }, payload) {
    const platform_code = payload.shift()
    const data_changes = payload[0]
    const res = await this.$repositories.platform.update(platform_code, data_changes)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('UPDATE_IN_LIST', data.data)
    } else {
      // Handle error here
    }
  },

  async delete_by_id({ commit }, platform_id) {
    const res = await this.$repositories.platform.delete(platform_id)
    const { status, data } = res
    if (status === 200 && data.data) {
      // Remove from store
      commit('SET_PLATFORM', [])
    } else {
      // Handle error here
    }
  }
}

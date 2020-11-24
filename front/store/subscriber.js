export const state = () => ({
  subscribers: [],
  subscriber: [],
})

export const mutations = {
  SET_SELLER(state, subscriber) {
    state.subscriber = subscriber
  }
}

export const actions = {


  async create({ commit }, subscriber_data) {
    const res = await this.$repositories.subscriber.create(subscriber_data)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_SELLER', data.data)
    } else {
      // Handle error here
    }
  },

  async update({ commit }, subscriber_id, data_changes) {
    const res = await this.$repositories.subscriber.update(subscriber_id, data_changes)
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_SELLER', data.data)
    } else {
      // Handle error here
    }
  },

  async delete_by_id({ commit }, subscriber_id) {
    const res = await this.$repositories.subscriber.delete(subscriber_id)
    const { status, data } = res
    if (status === 200 && data.data) {
      // Remove from store
      commit('SET_SELLER', [])
    } else {
      // Handle error here
    }
  }
}

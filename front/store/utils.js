export const state = () => ({
  notifications: []
})

export const mutations = {
  SET_NOTIFICATIONS(state, notifications) {
    state.notifications = notifications
  },

  PULL_NOTIFICATIONS(state, notifications) {
    for (let i = 0; i < notifications.length; i++)
      state.notifications.push(notifications[i])
  }
}

export const actions = {
  async get_all_key_account_notifications({ commit }) {
    const res = await this.$repositories.utils.get_by_seller_firm_public_id()
    const { status, data } = res
    if (status === 200 && data.data) {
      commit('SET_NOTIFICATIONS', data.data)
    }
  }

}

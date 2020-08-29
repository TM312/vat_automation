export const state = () => ({
    progress: 0,
    result: []

})

export const mutations = {
    SET_PROGRESS(state, progress) {
        state.progress = progress
    },

    SET_RESULT(state, result) {
        state.result = result
    }
}

export const actions = {
    async get({ commit }) {
        const res = await this.$repositories.status.get()
        const { status, data } = res
        if (status === 200 && data) {
            commit('SET_RESULT', data)
        } else {
            // Handle error here
        }
    }
}

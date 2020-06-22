export const state = () => ({
    bundles: [],
    bundle: []
})

export const mutations = {
    SET_BUNDLES(state, bundles) {
        state.bundles = bundles
    },
    SET_BUNDLE(state, bundle) {
        state.bundle = bundle
    }
}

export const actions = {
    async get_all({ commit }) {
        const res = await this.$repositories.bundle.get_all()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_BUNDLES', data.data)
        } else {
            // Handle error here
        }
    },

    async create({ commit }, bundle_data) {
        const res = await this.$repositories.bundle.create(bundle_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_BUNDLE', data.data)
        } else {
            // Handle error here
        }
    },

    async get_by_id({ commit }, bundle_id) {

        const res = await this.$repositories.bundle.get_by_id(bundle_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_BUNDLE', data.data)
        } else {
            // Handle error here
        }
    },

    async update({ commit }, bundle_id, data_changes) {
        const res = await this.$repositories.bundle.update(bundle_id, data_changes)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_BUNDLE', data.data)
        } else {
            // Handle error here
        }
    },

    async delete_by_id({ commit }, bundle_id) {
        const res = await this.$repositories.bundle.delete(bundle_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_BUNDLE', [])
        } else {
            // Handle error here
        }
    }
}

export const state = () => ({
    vats: [],
    vat: []
})

export const mutations = {
    SET_VATS(state, vats) {
        state.vats = vats
    },
    SET_VAT(state, vat) {
        state.vat = vat
    }
}

export const actions = {
    async get_all({ commit }) {
        const res = await this.$repositories.vat.get_all()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_VATS', data.data)
        } else {
            // Handle error here
        }
    },

    async create({ commit }, vat_data) {
        const res = await this.$repositories.vat.create(vat_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_VAT', data.data)
        } else {
            // Handle error here
        }
    },

    async get_by_id({ commit }, vat_id) {

        const res = await this.$repositories.vat.get_by_id(vat_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_VAT', data.data)
        } else {
            // Handle error here
        }
    },

    async update({ commit }, vat_id, data_changes) {
        const res = await this.$repositories.vat.update(vat_id, data_changes)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_VAT', data.data)
        } else {
            // Handle error here
        }
    },

    async delete_by_id({ commit }, vat_id) {
        const res = await this.$repositories.vat.delete(vat_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_VAT', [])
        } else {
            // Handle error here
        }
    }
}

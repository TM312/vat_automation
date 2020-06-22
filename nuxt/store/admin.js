export const state = () => ({
    admins: [],
    admin: [],
    // self_admin: []
})

export const mutations = {
    SET_ADMINS(state, admins) {
        state.admins = admins
    },
    SET_ADMIN(state, admin) {
        state.admin = admin
    },
    // SET_SELF_ADMIN(state, admin) {
    //     state.self_admin = admin
    // }
}

export const actions = {
    async get_all({ commit }) {
        const res = await this.$repositories.admin.get_all()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_ADMINS', data.data)
        } else {
            // Handle error here
        }
    },

    async get_by_id({ commit }, admin_id) {

        const res = await this.$repositories.admin.get_by_id(admin_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_ADMIN', data.data)
        } else {
            // Handle error here
        }
    },

    // async get_self({ commit }) {
    //     const res = await this.$repositories.admin.get_self()
    //     const { status, data } = res
    //     if (status === 200 && data.data) {
    //         commit('SET_SELF_ADMIN', data.data)
    //     } else {
    //         // Handle error here
    //     }
    // },

    async create({ commit }, admin_data) {
        const res = await this.$repositories.admin.create(admin_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_ADMIN', data.data)
        } else {
            // Handle error here
        }
    },

    async update({ commit }, admin_id, data_changes) {
        const res = await this.$repositories.admin.update(admin_id, data_changes)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_ADMIN', data.data)
        } else {
            // Handle error here
        }
    },

    async delete_by_id({ commit }, admin_id) {
        const res = await this.$repositories.admin.delete(admin_id)
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_ADMIN', [])
        } else {
            // Handle error here
        }
    }
}

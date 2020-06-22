export const state = () => ({
    countries: [],
    country: []
})

export const mutations = {
    SET_COUNTRIES(state, countries) {
        state.countries = countries
    },
    SET_COUNTRY(state, country) {
        state.country = country
    }
}

export const actions = {
    async get_all({ commit }) {
        const res = await this.$repositories.country.get_all()
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_COUNTRIES', data.data)
        } else {
            // Handle error here
        }
    },

    async create({ commit }, country_data) {
        const res = await this.$repositories.country.create(country_data)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_COUNTRY', data.data)
        } else {
            // Handle error here
        }
    },

    async get_by_code({ commit }, country_code) {

        const res = await this.$repositories.country.get_by_code(country_code)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_COUNTRY', data.data)
        } else {
            // Handle error here
        }
    },

    async update({ commit }, country_code, data_changes) {
        const res = await this.$repositories.country.update(country_code, data_changes)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_COUNTRY', data.data)
        } else {
            // Handle error here
        }
    },

    async delete_by_code({ commit }, country_code) {
        const res = await this.$repositories.country.delete(country_code)
        const { status, data } = res
        if (status === 200 && data.data) {
            // Remove from store
            commit('SET_COUNTRY', [])
        } else {
            // Handle error here
        }
    }
}

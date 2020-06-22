export const state = () => ({
    template: [],
})

export const mutations = {
    SET_TEMPLATE(state, template) {
        state.template = template
    }
}

export const actions = {
    async get_by_name({ commit }, template_filename) {

        const res = await this.$repositories.template.get_by_id(template_filename)
        const { status, data } = res
        if (status === 200 && data.data) {
            commit('SET_TEMPLATE', data.data)
        } else {
            // Handle error here
        }
    }
}

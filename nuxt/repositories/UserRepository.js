const resource = '/user'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    get_by_id(user_public_id) {
        return $axios.get(`${resource}/${user_public_id}`)
    },

    get_self() {
        return $axios.get(`${resource}/self`)
    },

    update(user_public_id, payload) {
        return $axios.put(`${resource}/${user_public_id}`, payload)
    },

    delete_by_id(user_public_id) {
        return $axios.delete(`${resource}/${user_public_id}`)
    },

    get_actions() {
        return $axios.get(`${resource}/actions`)
    }
})

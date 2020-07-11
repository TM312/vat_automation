const resource = '/user/admin'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    create(payload) {
        return $axios.post(`${resource}/`, payload)
    },

    get_by_id(admin_id) {
        return $axios.get(`${resource}/${admin_id}`)
    },

    // get_self() {
    //     return $axios.get(`${resource}/self`)
    // },

    update(admin_id, payload) {
        return $axios.put(`${resource}/${admin_id}`, payload)
    },

    delete_by_id(admin_id) {
        return $axios.delete(`${resource}/${admin_id}`)
    }
})

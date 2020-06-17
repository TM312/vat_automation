const resource = '/user/tax_auditor'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}`)
    },

    create(payload) {
        return $axios.post(`${resource}`, payload)
    },

    get_by_id(id) {
        return $axios.get(`${resource}/${id}`)
    },

    // get_self() {
    //     return $axios.get(`${resource}/self`)
    // }

    update(id, payload) {
        return $axios.put(`${resource}/${id}`, payload)
    },

    delete_by_id(id) {
        return $axios.delete(`${resource}/${id}`)
    }
})

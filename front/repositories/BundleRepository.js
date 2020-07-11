const resource = '/bundle'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    create(payload) {
        return $axios.post(`${resource}/`, payload)
    },

    get_by_id(bundle_id) {
        return $axios.get(`${resource}/${bundle_id}`)
    },

    update(bundle_id, payload) {
        return $axios.put(`${resource}/${bundle_id}`, payload)
    },

    delete_by_id(bundle_id) {
        return $axios.delete(`${resource}/${bundle_id}`)
    }
})

const resource = '/bundle'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    create(payload) {
        return $axios.post(`${resource}/`, payload)
    },

    get_by_public_id(bundle_public_id) {
        console.log('in repository: bundle_public_id ->', bundle_public_id)
        return $axios.get(`${resource}/${bundle_public_id}`)
    },

    update_by_public_id(bundle_public_id, payload) {
        return $axios.put(`${resource}/${bundle_public_id}`, payload)
    },

    delete_by_public_id(bundle_public_id) {
        return $axios.delete(`${resource}/${bundle_public_id}`)
    }
})

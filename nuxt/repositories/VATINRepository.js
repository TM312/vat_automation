const resource = '/tax/vatin'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    create(payload) {
        return $axios.post(`${resource}/`, payload)
    },

    get_by_id(vatin_id) {
        return $axios.get(`${resource}/${vatin_id}`)
    },

    update(vatin_id, payload) {
        return $axios.put(`${resource}/${vatin_id}`, payload)
    },

    delete_by_id(vatin_id) {
        return $axios.delete(`${resource}/${vatin_id}`)
    },

    upload(payload) {
        return $axios.post(`${resource}/csv`, payload)
    }
})

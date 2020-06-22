const resource = '/item'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    create(payload) {
        return $axios.post(`${resource}/`, payload)
    },

    get_by_id(item_id) {
        return $axios.get(`${resource}/${item_id}`)
    },

    update(item_id, payload) {
        return $axios.put(`${resource}/${item_id}`, payload)
    },

    delete_by_id(item_id) {
        return $axios.delete(`${resource}/${item_id}`)
    },

    upload(payload) {
        return $axios.post(`${resource}/csv`, payload)
    }
})

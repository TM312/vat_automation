const resource = '/exchange_rate'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    create(payload) {
        return $axios.post(`${resource}/`, payload)
    },

    get_by_id(exchange_rate_id) {
        return $axios.get(`${resource}/${exchange_rate_id}`)
    },

    update(exchange_rate_id, payload) {
        return $axios.put(`${resource}/${exchange_rate_id}`, payload)
    },

    delete_by_id(exchange_rate_id) {
        return $axios.delete(`${resource}/${exchange_rate_id}`)
    }
})

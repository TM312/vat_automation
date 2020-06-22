const resource = '/transaction_input'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    get_by_id(transaction_input_id) {
        return $axios.get(`${resource}/${transaction_input_id}`)
    },

    update(transaction_input_id, payload) {
        return $axios.put(`${resource}/${transaction_input_id}`, payload)
    },

    delete_by_id(transaction_input_id) {
        return $axios.delete(`${resource}/${transaction_input_id}`)
    },

    upload(payload) {
        return $axios.post(`${resource}/csv`, payload)
    }
})

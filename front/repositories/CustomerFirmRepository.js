const resource = '/business/customer_firm'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    create(payload) {
        return $axios.post(`${resource}/`, payload)
    },

    get_by_id(customer_firm_id) {
        return $axios.get(`${resource}/${customer_firm_id}`)
    },

    update(customer_firm_id, payload) {
        return $axios.put(`${resource}/${customer_firm_id}`, payload)
    },

    delete_by_id(customer_firm_id) {
        return $axios.delete(`${resource}/${customer_firm_id}`)
    }
})

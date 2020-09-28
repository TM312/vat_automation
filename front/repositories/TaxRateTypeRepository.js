const resource = '/tax/tax_rate_type'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    create(payload) {
        return $axios.post(`${resource}/`, payload)
    },

    get_by_code(tax_rate_type) {
        return $axios.get(`${resource}/${tax_rate_type}`)
    },

    update(tax_rate_type, payload) {
        return $axios.put(`${resource}/${tax_rate_type}`, payload)
    },

    delete_by_code(tax_rate_type) {
        return $axios.delete(`${resource}/${tax_rate_type}`)
    }

})

const resource = '/tax/tax_treatment'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    create(payload) {
        return $axios.post(`${resource}/`, payload)
    },

    get_by_code(tax_treatment) {
        return $axios.get(`${resource}/${tax_treatment}`)
    },

    update(tax_treatment, payload) {
        return $axios.put(`${resource}/${tax_treatment}`, payload)
    },

    delete_by_code(tax_treatment) {
        return $axios.delete(`${resource}/${tax_treatment}`)
    }

})

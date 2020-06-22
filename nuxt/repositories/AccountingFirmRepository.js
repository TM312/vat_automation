const resource = '/business/accounting_firm'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    create(payload) {
        return $axios.post(`${resource}/`, payload)
    },

    get_by_id(accounting_firm_id) {
        return $axios.get(`${resource}/${accounting_firm_id}`)
    },

    update(accounting_firm_id, payload) {
        return $axios.put(`${resource}/${accounting_firm_id}`, payload)
    },

    delete_by_id(accounting_firm_id) {
        return $axios.delete(`${resource}/${accounting_firm_id}`)
    }
})

const resource = '/user/tax_auditor'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    create(payload) {
        return $axios.post(`${resource}/`, payload)
    },

    get_by_id(tax_auditor_id) {
        return $axios.get(`${resource}/${tax_auditor_id}`)
    },

    get_self() {
        return $axios.get(`${resource}/self`)
    },

    update(tax_auditor_id, payload) {
        return $axios.put(`${resource}/${tax_auditor_id}`, payload)
    },

    delete_by_id(tax_auditor_id) {
        return $axios.delete(`${resource}/${tax_auditor_id}`)
    }
})

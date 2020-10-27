const resource = '/transaction'
export default ($axios) => ({
    get_all() {
        return $axios.get(`${resource}/`)
    },

    get_by_id(transaction_id) {
        return $axios.get(`${resource}/${transaction_id}`)
    },

    get_by_tax_record_tax_treatment(params) {
        return $axios.get(`${resource}/tax_record/`, { params })
    },

    get_by_tax_record(params) {
        return $axios.get(`${resource}/tax_record/init`, { params })
    },

})

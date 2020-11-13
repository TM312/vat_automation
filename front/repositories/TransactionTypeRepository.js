const resource = '/transaction_type'
export default ($axios) => ({
  get_all() {
    return $axios.get(`${resource}/`)
  },

  create(payload) {
    return $axios.post(`${resource}/`, payload)
  },

  get_by_code(transaction_type_code) {
    return $axios.get(`${resource}/${transaction_type_code}`)
  },

  update(transaction_type_code, payload) {
    return $axios.put(`${resource}/${transaction_type_code}`, payload)
  },

  delete_by_code(transaction_type_code) {
    return $axios.delete(`${resource}/${transaction_type_code}`)
  }

})

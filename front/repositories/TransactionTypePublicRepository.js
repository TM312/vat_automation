const resource = '/transaction_type_public'
export default ($axios) => ({
  get_all() {
    return $axios.get(`${resource}/`)
  },

  create(payload) {
    return $axios.post(`${resource}/`, payload)
  },

  get_by_public_id(transaction_type_public_public_id) {
    return $axios.get(`${resource}/${transaction_type_public_public_id}`)
  },

  update(transaction_type_public_public_id, payload) {
    return $axios.put(`${resource}/${transaction_type_public_public_id}`, payload)
  },

  delete_by_public_id(transaction_type_public_public_id) {
    return $axios.delete(`${resource}/${transaction_type_public_public_id}`)
  }

})

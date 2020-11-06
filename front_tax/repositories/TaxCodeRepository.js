const resource = '/tax/tax_code'
export default ($axios) => ({
  get_all() {
    return $axios.get(`${resource}/`)
  },

  create(payload) {
    return $axios.post(`${resource}/`, payload)
  },

  get_by_code(tax_code) {
    return $axios.get(`${resource}/${tax_code}`)
  },

  update(tax_code, payload) {
    return $axios.put(`${resource}/${tax_code}`, payload)
  },

  delete_by_code(tax_code) {
    return $axios.delete(`${resource}/${tax_code}`)
  }

})

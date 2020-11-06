const resource = '/tax_record'
export default ($axios) => ({
  get_all() {
    return $axios.get(`${resource}/`)
  },

  get_by_public_id(tax_record_public_id) {
    return $axios.get(`${resource}/${tax_record_public_id}`)
  },

  delete_by_public_id(tax_record_public_id) {
    return $axios.delete(`${resource}/${tax_record_public_id}`)
  },

  get_all_by_seller_firm_public_id(seller_firm_public_id) {
    return $axios.get(`${resource}/seller_firm/${seller_firm_public_id}`)
  },

  create_by_seller_firm_public_id(seller_firm_public_id, payload) {
    return $axios.post(`${resource}/seller_firm/${seller_firm_public_id}`, payload)
  }

})

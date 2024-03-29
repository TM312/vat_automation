const resource = '/item'
export default ($axios) => ({
  get_all() {
    return $axios.get(`${resource}/`)
  },

  create(payload) {
    return $axios.post(`${resource}/`, payload)
  },

  create_by_seller_firm_public_id(seller_firm_public_id, payload) {
    return $axios.post(`${resource}/seller_firm/${seller_firm_public_id}`, payload)
  },

  get_by_public_id(item_public_id) {
    return $axios.get(`${resource}/${item_public_id}`)
  },

  update_by_public_id(item_public_id, payload) {
    return $axios.put(`${resource}/${item_public_id}`, payload)
  },

  delete_by_public_id(item_public_id) {
    return $axios.delete(`${resource}/${item_public_id}`)
  },

  upload(payload) {
    return $axios.post(`${resource}/csv`, payload)
  }
})

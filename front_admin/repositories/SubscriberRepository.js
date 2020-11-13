const resource = '/user/subscriber'
export default ($axios) => ({
  get_all() {
    return $axios.get(`${resource}/`)
  },

  create(payload) {
    return $axios.post(`${resource}/`, payload)
  },

  delete_by_id(seller_id) {
    return $axios.delete(`${resource}/${seller_id}`)
  }
})

const resource = '/user/seller'
export default ($axios) => ({
  get_all() {
    return $axios.get(`${resource}/`)
  },

  create(payload) {
    return $axios.post(`${resource}/`, payload)
  },

  get_by_id(seller_id) {
    return $axios.get(`${resource}/${seller_id}`)
  },

  // get_self() {
  //     return $axios.get(`${resource}/self`)
  // },

  update(seller_id, payload) {
    return $axios.put(`${resource}/${seller_id}`, payload)
  },

  delete_by_id(seller_id) {
    return $axios.delete(`${resource}/${seller_id}`)
  }
})

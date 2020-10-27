const resource = '/channel'
export default ($axios) => ({
  get_all() {
    return $axios.get(`${resource}/`)
  },

  create(payload) {
    return $axios.post(`${resource}/`, payload)
  },

  get_by_code(channel_code) {
    return $axios.get(`${resource}/${channel_code}`)
  },

  update(channel_code, payload) {
    return $axios.put(`${resource}/${channel_code}`, payload)
  },

  delete_by_code(channel_code) {
    return $axios.delete(`${resource}/${channel_code}`)
  }

})

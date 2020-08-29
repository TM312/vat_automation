const resource = '/utils'
export default ($axios) => ({
    get() {
        return $axios.get(`${resource}/tasks`)
    },
})

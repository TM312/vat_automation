export const state = () => ({
    status_account: [],
    status_item: [],
    status_vat_number: [],
    status_distance_sale: []
})

export const mutations = {
    SET_STATUS(state, status) {
        if (status['object'] === 'account') {
            state.status_account = status
        } else if (status['object'] === 'item') {
            state.status_item = status
        } else if (status['object'] === 'vat_number') {
            state.status_vat_number = status
        } else if (status['object'] === 'distance_sale') {
            state.status_distance_sale = status
        }
    },
}

// export const actions = {
//     async get({ commit }) {
//         const res = await this.$repositories.status.get()
//         const { status, data } = res
//         if (status === 200 && data) {
//             commit('SET_RESULT', data)
//         } else {
//             // Handle error here
//         }
//     }
// }

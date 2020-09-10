export const state = () => ({
    status_account_targets: [],
    status_item_targets: [],
    status_vat_number_targets: [],
    status_distance_sale_targets: [],
    status_transaction_input_targets: []
})


export const getters = {
    percStatusAccountTargets: state => state.status_account_targets.map(accountTarget => (accountTarget.current / accountTarget.total).toFixed(2)),
    percStatusItemTargets: state => state.status_item_targets.map(itemTarget => (itemTarget.current / itemTarget.total).toFixed(2)),
    percStatusVatNumberTargets: state => state.status_vat_number_targets.map(vatNumberTarget => (vatNumberTarget.current / vatNumberTarget.total).toFixed(2)),
    percStatusDistanceSaleTargets: state => state.status_distance_sale_targets.map(distanceSaleTarget => (distanceSaleTarget.current / distanceSaleTarget.total).toFixed(2)),
    percStatusTransactionInputTargets: state => state.status_transaction_input_targets.map(transactionInputTarget => (transactionInputTarget.current / transactionInputTarget.total).toFixed(2)),

    // https://stackoverflow.com/questions/11301438/return-index-of-greatest-value-in-an-array
    // https://vuex.vuejs.org/guide/getters.html#property-style-access
    /*eslint-disable */
    status_account_targets_lowest: (state, getters) => getters.percStatusAccountTargets.reduce((iMin, x, i, arr) => x > arr[iMin] ? i : iMin, 0),
    status_item_targets_lowest: (state, getters) => getters.percStatusItemTargets.reduce((iMin, x, i, arr) => x > arr[iMin] ? i : iMin, 0),
    status_vat_number_targets_lowest: (state, getters) => getters.percStatusVatNumberTargets.reduce((iMin, x, i, arr) => x > arr[iMin] ? i : iMin, 0),
    status_distance_sale_targets_lowest: (state, getters) => getters.percStatusDistanceSaleTargets.reduce((iMin, x, i, arr) => x > arr[iMin] ? i : iMin, 0),
    status_transaction_input_targets_lowest: (state, getters) => getters.percStatusTransactionInputTargets.reduce((iMin, x, i, arr) => x > arr[iMin] ? i : iMin, 0),

    status_account_lowest: (state, getters) => (state.status_account_targets.length > 0) ? state.status_account_targets[getters.status_account_targets_lowest] : null,
    status_item_lowest: (state, getters) => (state.status_item_targets.length > 0) ? state.status_item_targets[getters.status_item_targets_lowest] : null,
    status_vat_number_lowest: (state, getters) => (state.status_vat_number_targets.length > 0) ? state.status_vat_number_targets[getters.status_vat_number_targets_lowest] : null,
    status_distance_sale_lowest: (state, getters) => (state.status_distance_sale_targets.length > 0) ? state.status_distance_sale_targets[getters.status_distance_sale_targets_lowest] : null,
    status_transaction_input_lowest: (state, getters) => (state.status_transaction_input_targets.length > 0) ? state.status_transaction_input_targets[getters.status_transaction_input_targets_lowest] : null

    // doneStatusAccountTargets: state => state.statusAccountTargets.map(file => file.done),
    // doneStatusItemTargets: state => state.statusItemTargets.map(file => file.done),
    // doneStatusVatNumberTargets: state => state.statusVatNumberTargets.map(file => file.done),
    // doneStatusDistanceSaleTargets: state => state.statusDistanceSaleTargets.map(file => file.done),
    // doneStatusTransactionInputTargets: state => state.statusTransactionInputTargets.map(file => file.done)


    /*eslint-disable */
}
// mutations: receive the state as the first argumen, you can pass an additional argument to store.commit, which is called the payload for the mutation
export const mutations = {

    // considering reactive property: https://stackoverflow.com/questions/51149729/updating-state-of-vuex-array-when-one-item-has-some-changes/51153076
    SET_STATUS_ACCOUNT_TARGETS(state, payload) {
        Object.assign(state.status_account_targets[payload.index], payload.status);
    },
    SET_STATUS_ITEM_TARGETS(state, payload) {
        Object.assign(state.status_item_targets[payload.index], payload.status);
    },
    SET_STATUS_VAT_NUMBER_TARGETS(state, payload) {
        Object.assign(state.status_vat_number_targets[payload.index], payload.status);
    },
    SET_STATUS_DISTANCE_SALE_TARGETS(state, payload) {
        Object.assign(state.status_distance_sale_targets[payload.index], payload.status);
    },

    SET_STATUS_TRANSACTION_INPUT_TARGETS(state, payload) {
        Object.assign(state.status_transaction_input_targets[payload.index], payload.status);
    },

    PUSH_ACCOUNT_TARGET(state, payload) {
        state.status_account_targets.push(payload)
    },

    PUSH_ITEM_TARGET(state, payload) {
        state.status_item_targets.push(payload)
    },

    PUSH_VAT_NUMBER_TARGET(state, payload) {
        state.status_vat_number_targets.push(payload)
    },

    PUSH_DISTANCE_SALE_TARGET(state, payload) {
        state.status_distance_sale_targets.push(payload)
    },

    PUSH_TRANSACTION_INPUT_TARGET(state, payload) {
        state.status_transaction_input_targets.push(payload)
    },

    CLEAR_ALL(state) {
        state.status_account_targets = []
        state.status_item_targets = []
        state.status_vat_number_targets = []
        state.status_distance_sale_targets = []
        state.status_transaction_input_targets = []
    },
    CLEAR_STATUS_ACCOUNT_TARGETS(state) {
        state.status_account_targets = []
    },
    CLEAR_STATUS_ITEM_TARGETS(state) {
        state.status_item_targets = []
    },
    CLEAR_STATUS_VAT_NUMBER_TARGETS(state) {
        state.status_vat_number_targets = []
    },
    CLEAR_STATUS_DISTANCE_SALE_TARGETS(state) {
        state.status_distance_sale_targets = []
    },
    CLEAR_STATUS_TRANSACTION_INPUT_TARGETS(state) {
        state.status_transaction_input_targets = []
    }
}


export const actions = {
    async clear_all({ commit }) {
        commit('CLEAR_ALL')
    },

    async handle_status({ commit, state }, status) {
        if (status.object === 'account') {
            const index = state.status_account_targets.findIndex(e => e.target === status.target)
            if (index === -1) {
                commit('PUSH_ACCOUNT_TARGET', status)
            } else {
                const payload = {status : status, index: index}
                commit('SET_STATUS_ACCOUNT_TARGETS', payload)
            }

        } else if (status.object === 'item') {
            const index = state.status_item_targets.findIndex(e => e.target === status.target)
            if (index === -1) {
                commit('PUSH_ITEM_TARGET', status)
            } else {
                const payload = {status : status, index: index}
                commit('SET_STATUS_ITEM_TARGETS', payload)
            }
        } else if (status.object === 'vatin') {
            const index = state.status_vat_number_targets.findIndex(e => e.target === status.target)
            if (index === -1) {
                commit('PUSH_VAT_NUMBER_TARGET', status)
            } else {
                const payload = {status : status, index: index}
                commit('SET_STATUS_VAT_NUMBER_TARGETS', payload)
            }

        } else if (status.object === 'distance_sale') {
            const index = state.status_distance_sale_targets.findIndex(e => e.target === status.target)
            if (index === -1) {
                commit('PUSH_DISTANCE_SALE_TARGET', status)
            } else {
                const payload = {status : status, index: index}
                commit('SET_STATUS_DISTANCE_SALE_TARGETS', payload)
            }

        } else if (status.object === 'transaction_input') {
            const index = state.status_transaction_input_targets.findIndex(e => e.target === status.target)
            if (index === -1) {
                commit('PUSH_TRANSACTION_INPUT_TARGET', status)
            } else {
                const payload = {status : status, index: index}
                commit('SET_STATUS_TRANSACTION_INPUT_TARGETS', payload)
            }
        }
    }
}

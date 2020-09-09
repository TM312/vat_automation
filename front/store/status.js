export const state = () => ({
    status_account_files: [],
    status_item_files: [],
    status_vat_number_files: [],
    status_distance_sale_files: [],
    status_transaction_input_files: []
})


export const getters = {
    percStatusAccountFiles: state => state.status_account_files.map(accountFile => (accountFile.current / accountFile.total).toFixed(2)),
    percStatusItemFiles: state => state.status_item_files.map(itemFile => (itemFile.current / itemFile.total).toFixed(2)),
    percStatusVatNumberFiles: state => state.status_vat_number_files.map(vatNumberFile => (vatNumberFile.current / vatNumberFile.total).toFixed(2)),
    percStatusDistanceSaleFiles: state => state.status_distance_sale_files.map(distanceSaleFile => (distanceSaleFile.current / distanceSaleFile.total).toFixed(2)),
    percStatusTransactionInputFiles: state => state.status_transaction_input_files.map(transactionInputFile => (transactionInputFile.current / transactionInputFile.total).toFixed(2)),

    // https://stackoverflow.com/questions/11301438/return-index-of-greatest-value-in-an-array
    // https://vuex.vuejs.org/guide/getters.html#property-style-access
    /*eslint-disable */
    status_account_files_lowest: (state, getters) => getters.percStatusAccountFiles.reduce((iMin, x, i, arr) => x > arr[iMin] ? i : iMin, 0),
    status_item_files_lowest: (state, getters) => getters.percStatusItemFiles.reduce((iMin, x, i, arr) => x > arr[iMin] ? i : iMin, 0),
    status_vat_number_files_lowest: (state, getters) => getters.percStatusVatNumberFiles.reduce((iMin, x, i, arr) => x > arr[iMin] ? i : iMin, 0),
    status_distance_sale_files_lowest: (state, getters) => getters.percStatusDistanceSaleFiles.reduce((iMin, x, i, arr) => x > arr[iMin] ? i : iMin, 0),
    status_transaction_input_files_lowest: (state, getters) => getters.percStatusTransactionInputFiles.reduce((iMin, x, i, arr) => x > arr[iMin] ? i : iMin, 0),

    status_account_lowest: (state, getters) => (state.status_account_files.length > 0) ? state.status_account_files[getters.status_account_files_lowest] : null,
    status_item_lowest: (state, getters) => (state.status_item_files.length > 0) ? state.status_item_files[getters.status_item_files_lowest] : null,
    status_vat_number_lowest: (state, getters) => (state.status_vat_number_files.length > 0) ? state.status_vat_number_files[getters.status_vat_number_files_lowest] : null,
    status_distance_sale_lowest: (state, getters) => (state.status_distance_sale_files.length > 0) ? state.status_distance_sale_files[getters.status_distance_sale_files_lowest] : null,
    status_transaction_input_lowest: (state, getters) => (state.status_transaction_input_files.length > 0) ? state.status_transaction_input_files[getters.status_transaction_input_files_lowest] : null


    /*eslint-disable */
}
// mutations: receive the state as the first argumen, you can pass an additional argument to store.commit, which is called the payload for the mutation
export const mutations = {

    // considering reactive property: https://stackoverflow.com/questions/51149729/updating-state-of-vuex-array-when-one-item-has-some-changes/51153076
    SET_STATUS_ACCOUNT_FILES(state, payload) {
        const accountFile = state.status_account_files.find(accountFile => accountFile.original_filename === payload.original_filename);
        Object.assign(accountFile, payload);
    },
    SET_STATUS_ITEM_FILES(state, payload) {
        const itemFile = state.status_item_files.find(itemFile => itemFile.original_filename === payload.original_filename);
        Object.assign(itemFile, payload);
    },
    SET_STATUS_VAT_NUMBER_FILES(state, payload) {
        const vatNumberFile = state.status_vat_number_files.find(vatNumberFile => vatNumberFile.original_filename === payload.original_filename);
        Object.assign(vatNumberFile, payload);
    },
    SET_STATUS_DISTANCE_SALE_FILES(state, payload) {
        const distanceSaleFile = state.status_distance_sale_files.find(distanceSaleFile => distanceSaleFile.original_filename === payload.original_filename);
        Object.assign(distanceSaleFile, payload);
    },

    SET_STATUS_TRANSACTION_INPUT_FILES(state, payload) {
        const transactionInputFile = state.status_transaction_input_files.find(transactionInputFile => transactionInputFile.original_filename === payload.original_filename);
        Object.assign(transactionInputFile, payload);
    },

    PUSH_ACCOUNT_FILE(state, payload) {
        state.status_account_files.push(payload)
    },

    PUSH_ITEM_FILE(state, payload) {
        state.status_item_files.push(payload)
    },

    PUSH_VAT_NUMBER_FILE(state, payload) {
        state.status_vat_number_files.push(payload)
    },

    PUSH_DISTANCE_SALE_FILE(state, payload) {
        state.status_distance_sale_files.push(payload)
    },

    PUSH_TRANSACTION_INPUT_FILE(state, payload) {
        state.status_transaction_input_files.push(payload)
    },

    CLEAR_ALL(state) {
        state.status_account_files = []
        state.status_item_files = []
        state.status_vat_number_files = []
        state.status_distance_sale_files = []
        state.status_transaction_input_files = []
    },
    CLEAR_STATUS_ACCOUNT_FILES(state) {
        console.log('CLEAR_STATUS_ACCOUNT_FILES')
        state.status_account_files = []
    },
    CLEAR_STATUS_ITEM_FILES(state) {
        state.status_item_files = []
    },
    CLEAR_STATUS_VAT_NUMBER_FILES(state) {
        state.status_vat_number_files = []
    },
    CLEAR_STATUS_DISTANCE_SALE_FILES(state) {
        console.log('CLEAR_STATUS_DISTANCE_SALE_FILES')
        state.status_distance_sale_files = []
    },
    CLEAR_STATUS_TRANSACTION_INPUT_FILES(state) {
        state.status_transaction_input_files = []
    }
}


export const actions = {
    clear_all({ commit }) {
        commit('CLEAR_ALL')
    },

    handle_status({ commit, state }, status) {
        if (status.object === 'account') {
            if (state.status_account_files.length === 0) {
                commit('PUSH_ACCOUNT_FILE', status)
            } else {
                commit('SET_STATUS_ACCOUNT_FILES', status)
            }

        } else if (status.object === 'item') {
            if (state.status_item_files.length === 0) {
                commit('PUSH_ITEM_FILE', status)
            } else {
                commit('SET_STATUS_ITEM_FILES', status)
            }
        } else if (status.object === 'vat_number') {
            if (state.status_vat_number_files.length === 0) {
                commit('PUSH_VAT_NUMBER_FILE', status)
            } else {
                commit('SET_STATUS_VAT_NUMBER_FILES', status)
            }

        } else if (status.object === 'distance_sale') {
            if (state.status_distance_sale_files.length === 0) {
                commit('PUSH_DISTANCE_SALE_FILE', status)
            } else {
                commit('SET_STATUS_DISTANCE_SALE_FILES', status)
            }

        } else if (status.object === 'transaction_input') {
            if (state.status_transaction_input_files.length === 0) {
                commit('PUSH_TRANSACTION_INPUT_FILE', status)
            } else {
                commit('SET_STATUS_TRANSACTION_INPUT_FILES', status)
            }
        }
    }
}

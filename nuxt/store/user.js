// export const state = () => ({
//   users: []
// })

// export const mutations = {
//   SET_USERS(state, payload) {
//     state.users = payload
//   }
// }

// // add(state, value) {
// // 	merge(state.user, value)
// // },
// // remove(state, { user }) {
// // 	state.user.filter(c => user.public_id !== c.public_id)
// // },
// // setusers(state, form) {
// // 	state.user = form
// // }
// // };

// // export const actions = {
// // 	async get({ commit }) {
// // 		await this.$axios.get(`/users`)
// // 			.then((res) => {
// // 				if (res.status === 200) {
// // 					commit('set', res.data)
// // 				}
// // 			})
// // 	},
// // 	async show({ commit }, params) {
// // 		await this.$axios.get(`/users/${params.owner_id}`)
// // 			.then((res) => {
// // 				if (res.status === 200) {
// // 					commit('mergeusers', res.data)
// // 				}
// // 			})
// // 	},
// // 	async set({ commit }, users) {
// // 		await commit('set', users)
// // 	},
// // 	async form({ commit }, form) {
// // 		await commit('mergeusers', form)
// // 	},
// // 	async add({ commit }, user) {
// // 		await commit('add', user)
// // 	},
// // 	create({ commit }, params) {
// // 		return this.$axios.post(`/users`, { user: params })
// // 	},
// // 	update({ commit }, params) {
// // 		return this.$axios.put(`/users/${params.id}`, { user: params })
// // 	},
// // 	delete({ commit }, params) {
// // 		return this.$axios.delete(`/users/${params.id}`)
// // 	}
// // };

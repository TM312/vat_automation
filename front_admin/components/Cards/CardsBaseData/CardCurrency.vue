<template>
  <b-card class="h-100">
    <b-card-title>
      <b-row>
        <b-col cols="auto">
          <b-form-input
            v-if="edit"
            v-model="form.name"
          />
          <span v-else>{{ currency.name }}</span>
        </b-col>
        <b-col cols="auto ml-auto">
          <b-button
            variant="outline-warning"
            size="sm"
            :pressed.sync="edit"
          >
            <b-icon icon="pencil-square" /> Edit
          </b-button>
        </b-col>
      </b-row>
    </b-card-title>
    <b-card-sub-title>
      <b-row>
        <b-col cols="auto">
          <b-form-input
            v-if="edit"
            v-model="form.code"
          />
          <span v-else>{{ currency.code }}</span>
        </b-col>
        <b-col cols="auto ml-auto">
          <b-button
            v-show="edit"
            variant="success"
            size="sm"
            :disabled="buttonBusy"
            @click="updateCurrency()"
          >
            Update
          </b-button>
        </b-col>
      </b-row>
    </b-card-sub-title>
  </b-card>
</template>

<script>
export default {
  name: "CardCurrency",

  props: {
    currency: {
      type: Object,
      required: true,
    },
  },

  data() {
    return {
      buttonBusy: false,
      edit: false,
      form: {
        name: null,
        code: null,
      },
    }
  },

  watch: {
    /*eslint-disable */
            edit(newVal) {
                if (newVal) {
                    this.form.name = this.currency.name
                    this.form.code = this.currency.code
                }
            },
        },

        methods: {
            removeEmpty() {
                const data_changes = {};
                const obj = this.form;

                Object.keys(obj).forEach((key) => {
                    if (obj[key] && typeof obj[key] === "object") {
                        data_changes[key] = this.removeEmpty(obj[key]); // recurse
                    } else if (obj[key] != null && obj[key] != this.currency[key]) {
                        data_changes[key] = obj[key]; // copy value
                    }
                });

                return data_changes;
            },

            async updateCurrency() {
                this.buttonBusy = true;
                const { store } = this.$nuxt.context;
                const currency_code = this.currency.code;
                const data_changes = this.removeEmpty();
                console.log(data_changes);
                const payload = [currency_code, data_changes];
                await store.dispatch("currency/update", payload);
                this.makeToast();
                this.buttonBusy = false;
            },

            makeToast() {
                this.$bvToast.toast(
                    `Currency "${this.currency.code}" has been successfully updated!`,
                    {
                        title: "Success",
                        variant: "success",
                        autoHideDelay: 5000,
                    }
                );
            },
        },
    };
</script>

<style>
</style>

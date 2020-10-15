<template>
  <b-tabs content-class="mt-3">
    <b-tab title="Base Data" active>
      <b-card-group deck>
        <b-card class="mb-5" header="Static Data" title="">
          <b-card-text>
            <b>Public ID:</b> <br />
            <b>Address:</b> <br />
            <b>Establishment Country:</b> <br />
            <br />
            <b>Created On:</b> <br />
            <b>Created By:</b> <br />
          </b-card-text>
        </b-card>

        <b-card class="mb-5">
          <template v-slot:header>
            <b-row>
              <b-col cols="auto" class="mr-auto">
                <h6 class="mb-0">
                  Accounts
                </h6>
              </b-col>
              <b-col cols="auto">
                <b-form-checkbox name="check-button" switch />
              </b-col>
            </b-row>
          </template>
          <b-card-text>
            <div>
              <div>
                <b-table borderless busy :fields="fieldsAccounts">
                  <template v-slot:table-busy>
                    <div class="text-center text-secondary my-2">
                      <b-spinner class="align-middle" />
                      <strong>Loading...</strong>
                    </div>
                  </template>
                </b-table>
              </div>
            </div>
          </b-card-text>
        </b-card>
      </b-card-group>
      <b-card-group deck>
        <b-card class="mb-5">
          <template v-slot:header>
            <b-row>
              <b-col cols="auto" class="mr-auto">
                <h6 class="mb-0">
                  Vat Numbers
                </h6>
              </b-col>
              <b-col cols="auto">
                <b-form-checkbox name="check-button" switch />
              </b-col>
            </b-row>
          </template>
          <b-card-text>
            <div>
              <div>
                <b-table borderless busy :fields="fieldsVatNumbers">
                  <template v-slot:table-busy>
                    <div class="text-center text-secondary my-2">
                      <b-spinner class="align-middle" />
                      <strong>Loading...</strong>
                    </div>
                  </template>
                </b-table>
              </div>
            </div>
          </b-card-text>
        </b-card>



        <b-card class="mb-5">
          <template v-slot:header>
            <b-row>
              <b-col cols="auto" class="mr-auto">
                <h6 class="mb-0">
                  Distance Sales
                </h6>
              </b-col>
              <b-col cols="auto">
                <b-form-checkbox name="check-button" switch />
              </b-col>
            </b-row>
          </template>
          <b-card-text>
            <div>
              <div>
                <b-table borderless busy :fields="fieldsDistanceSales">
                  <template v-slot:table-busy>
                    <div class="text-center text-secondary my-2">
                      <b-spinner class="align-middle" />
                      <strong>Loading...</strong>
                    </div>
                  </template>
                </b-table>
              </div>
            </div>
          </b-card-text>
        </b-card>
      </b-card-group>
    </b-tab>
    <b-tab title="Items" disabled />
    <b-tab title="Transactions" disabled />
  </b-tabs>
</template>

<script>
    export default {
        name:'OverviewBaseDataLoading',
        data() {
            return {
                fieldsVatNumbers: [
                    { key: "vatin", label: "VATIN", sortable: false },
                    { key: "valid", sortable: false },
                    { key: "request_date", sortable: true },
                    { key: "valid_from", sortable: true },
                    { key: "valid_to", sortable: true },
                    { key: "initial_tax_date", sortable: true }

                ],

                fieldsAccounts: [
                    { key: 'channel_code', label: 'Channel', sortable: true },
                    { key: 'given_id', label: "Account ID", sortable: false },
                ],

                fieldsDistanceSales: [
                    { key: "platform", sortable: false },
                    { key: "arrival_country", sortable: true },
                    { key: "active", sortable: true },
                ]
            }
        },
    }
</script>

<style>
</style>

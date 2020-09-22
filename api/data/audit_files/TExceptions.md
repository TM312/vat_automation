T-Exceptions

# Adhoc user feedback (no storage in db)
# Info
1. Data processing success
2. Progress status update
3. Transaction input duplicate, i.e. already processed


## Warning

### Error
1. Object can't be identified based on information provided, e.g. no account based on account_given_id
2. Cell in csv file can't be read
3. Value in cell does not meet expected format, e.g. integer expected, failure to transform cell value to integer
4. Updating transaction input failed
5. Creating transaction input failed
6. Set(/updating) transaction input as processed failed


# Notifications (stored in db relating to transaction)

## Info
1. Item Weights not matching
2. Item names not matching
3. Customer Firm name not matching (calc -> VIES Information)
4. Vat number not able to validate because of age


## Warning
1. Tax Calculation Dates not matching
2. Invoice currency codes not matching
3. Tax Rates not matching
4. Tax codes not matching

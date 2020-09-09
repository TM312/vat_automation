T-Test

Cases:
# Correct
## SALE
###   LOCAL_SALE
###   LOCAL_SALE_REVERSE_CHARGE
###   DISTANCE_SALE
###   INTRA_COMMUNITY_SALE
###   EXPORT

## REFUND
###   LOCAL_SALE
###   LOCAL_SALE_REVERSE_CHARGE
###   DISTANCE SALE
###   INTRA-COMMUNITY SALE
###   EXPORT

## ACQUISITION
###   LOCAL_ACQUISITION
###   INTRA_COMMUNITY_ACQUISITION
###   IMPORT

## MOVEMENT
###   INTRA_COMMUNITY SALE
###   EXPORT
###   INTRA_COMMUNITY_ACQUISITION
###   IMPORT

## RETURN
###   INTRA_COMMUNITY SALE
###   INTRA_COMMUNITY_ACQUISITION


# Info
## Item Weights not matching
## Item Names not matching
## Customer Vatin invalid
## Customer Firm name not matching with vatin
## Old Transaction -> Vatin not validated


# Warning
## Item Tax Codes not matching
## Vat Rates not matching

# Error
## TI Error
### Account unavailable
### Item unavailable
### Currency unavailable
### Departure Country unavailable (evtl. mit spezifischem Fall in T Error)
### Arrival Country unavailable (evtl. mit spezifischem Fall in T Error)


## T Error
### Transaction Type unavailable
### Exchange rate unavailable
### Vatin validation unavailable

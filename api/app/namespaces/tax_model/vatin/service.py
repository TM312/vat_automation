from vies import MEMBER_COUNTRY_CODES, VATIN_MAX_LENGTH, logger

class SellerFirmService:

    def input_precheck(vat_data):

        if isinstance(vat_data, str):
            vat = VATIN.from_str(vat_data)

        elif isinstance(vat_data, list):

            if not re.match(r"^[a-zA-Z]", vat_data[1]):
                vat = VATIN(vat_data[0], vat_data[1])

            elif VATIN.from_str(vat_data[1]).country_code == VATIN(vat_data[0], vat_data[1]).country_code:
                vat = VATIN.from_str(vat_data[1])

            else:
                raise Exception("country codes dont match")

        return vat



# # TEST
# value1 = ['DE', 'DE190200766']
# value2 = ['DE', '190200766']
# value3 = 'DE190200766'
# value4 = ['DE', 'IT190200766']
# values = [value1, value2, value3, value4]
# for value in values:
#     print(value)
#     vat = vat_precheck(value)
#     print("vat country code: {}".format(vat.country_code))
#     print("vat number: {}".format(vat.number))
#     print("")


    def is_valid(self):
        try:
            self.verify()
            self.validate()
        except HTTPException:
            return False
        else:
            return True

    def verify_country_code(self):
        if not re.match(r"^[a-zA-Z]", self.country_code):
            msg = "{} is not a valid ISO_3166-1 country code.".format(
                self.country_code)
            raise HTTPException(msg)
            #return msg
        elif self.country_code not in MEMBER_COUNTRY_CODES:
            msg = "{} is not a european member state.".format(
                self.country_code)
            raise HTTPException(msg)
            #return msg

    def verify_regex(self):
        country = dict(
            map(
                lambda x, y: (x, y),
                ("country", "validator", "formatter"),
                VIES_OPTIONS[self.country_code],
            )
        )
        if not country["validator"].match("{}{}".format(self.country_code, self.number)):
            msg = "{} does not match the country's VAT ID specifications.".format(
                self.country_code)
            raise HTTPException(msg)
            #return msg

    def verify(self):
        self.verify_country_code()
        self.verify_regex()

    def validate(self):
        if not self.data.valid:
            msg = "{} is not a valid VATIN.".format(self.country_code)
            raise HTTPException(msg)
            #return msg

from .service import TemplateService



ns = Namespace("utils", description="Utilities Related Operations")  # noqa
ns.add_model(transaction_dto.name)



@ns.route("/template/<string:name>")
class TemplateResource(Resource):
    @login_required
    # @confirmation_required
    # @ns.expect(transaction_dto, validate=True)
    def get(self, name):
        """Download A Template"""
        filename = name.split('.')[0] + '.csv'
        return TemplateService.download_file(filename)

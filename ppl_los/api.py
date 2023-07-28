from account.api import AccountController
from applicant.api import ApplicantController
from application.api import ApplicantDetailController
from question.api import QuestionController
from section.api import SectionController
from survey.api import SurveyController
from .ninjaJWTController import TokenObtainPairController, TokenVerificationController
from loanproduct.api import LoanProductController
from ninja_extra import NinjaExtraAPI
from comment.api import CommentController
from financial.api import FinancialController

api = NinjaExtraAPI()
api.register_controllers(TokenObtainPairController)
api.register_controllers(TokenVerificationController)
api.register_controllers(AccountController)
api.register_controllers(ApplicantController)
api.register_controllers(ApplicantDetailController)
api.register_controllers(QuestionController)
api.register_controllers(LoanProductController)
api.register_controllers(SectionController)
api.register_controllers(SurveyController)
api.register_controllers(CommentController)
api.register_controllers(FinancialController)


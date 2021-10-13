from authorization.models import Balance, User
from authorization.services.balance import CreateBalanceRecordDTO
from services.abstracts import IService


class BalanceRecordCreateMixin(IService):
    BALANCE_ACTION = NotImplemented

    def __init__(self, dto: CreateBalanceRecordDTO):
        self._dto = dto
        self._instance = Balance()

    def _set_client(self):
        self._instance.client = User.objects.get(id=self._dto.client_id)

    def _set_date(self):
        if self._dto.date is not None:
            self._instance.date = self._dto.date

    def _set_sum_in_jpy(self):
        self._instance.sum_in_jpy = self._dto.sum_in_jpy

    def _set_sum_in_usa(self):
        if self._dto.sum_in_usa is not None:
            self._instance.sum_in_usa = self._dto.sum_in_usa

    def _set_rate(self):
        if self._dto.rate is not None:
            self._instance.rate = self._dto.rate

    def _set_payment_type(self):
        self._instance.payment_type = self._dto.payment_type

    def _set_sender_name(self):
        self._instance.sender_name = self._dto.sender_name

    def _set_comment(self):
        self._instance.comment = self._dto.comment

    def _set_balance_action(self):
        self._instance.balance_action = self.BALANCE_ACTION

    def _save(self) -> Balance:
        return self._instance.save()

    def execute(self) -> Balance:
        self._set_client()
        self._set_date()
        self._set_sum_in_jpy()
        self._set_sum_in_usa()
        self._set_rate()
        self._set_payment_type()
        self._set_sender_name()
        self._set_comment()
        self._set_balance_action()
        return self._save()


class BalanceReplenishmentCreateService(BalanceRecordCreateMixin):
    BALANCE_ACTION = Balance.BALANCE_ACTION_REPLENISHMENT


class BalanceWithdrawalCreateService(BalanceRecordCreateMixin):
    BALANCE_ACTION = Balance.BALANCE_ACTION_WITHDRAWAL

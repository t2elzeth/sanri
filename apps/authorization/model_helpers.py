class UserBalance:
    def __init__(self, user):
        """

        @type user: authorization.models.User
        """
        self.replenishments = sum(
            [
                balance.sum_in_jpy
                for balance in user.balances.all()
                if balance.balance_action
                   == balance.BALANCE_ACTION_REPLENISHMENT
            ]
        )

        self.withdrawals = sum(
            [
                balance.sum_in_jpy
                for balance in user.balances.all()
                if balance.balance_action == balance.BALANCE_ACTION_WITHDRAWAL
            ]
        )

        self.amount = self.replenishments - self.withdrawals


class UserWorksBy:
    def __init__(self, user):
        """

        @type user: authorization.models.User
        """
        self._user = user

    @property
    def by_fact(self) -> bool:
        return self._user.atWhatPrice == self._user.AT_WHAT_PRICE_BY_FACT

    @property
    def by_fob(self) -> bool:
        return self._user.atWhatPrice == self._user.AT_WHAT_PRICE_BY_FOB

    @property
    def by_fob2(self) -> bool:
        return self._user.atWhatPrice == self._user.AT_WHAT_PRICE_BY_FOB2

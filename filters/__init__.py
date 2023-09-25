from loader import dp
from .admins_filter import AdminFilter, BotAdminFilter
from .group_filter import IsGroupFilter
from .private_filter import IsPrivateFilter


if __name__ == "filters":
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(BotAdminFilter)
    dp.filters_factory.bind(IsPrivateFilter)
    dp.filters_factory.bind(IsGroupFilter)

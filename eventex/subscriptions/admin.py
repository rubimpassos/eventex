from django.contrib import admin
from django.utils.timezone import now

from eventex.subscriptions.models import Subscription


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'cpf', 'created_at', 'subscribed_today', 'paid')
    date_hierarchy = 'created_at'
    search_fields = ('name', 'email', 'phone', 'cpf', 'created_at')
    list_filter = ('paid', 'created_at')

    actions = ['mark_has_paid']

    def subscribed_today(self, obj):
        return obj.created_at.date() == now().date()

    def mark_has_paid(self, request, queryset):
        count = queryset.update(paid=True)
        if count == 1:
            msg = "{} inscrição foi marcada como paga."
        else:
            msg = "{} inscrições foram marcadas como paga."

        self.message_user(request, msg.format(count))

    mark_has_paid.short_description = "Marcar como pago"

    subscribed_today.short_description = 'inscrito hoje?'
    subscribed_today.boolean = True


admin.site.register(Subscription, SubscriptionAdmin)

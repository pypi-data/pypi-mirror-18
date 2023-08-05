from django.forms import PasswordInput
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


class PasswordStrengthInput(PasswordInput):
    """
    Form widget to show the user how strong his/her password is.
    """

    def render(self, name, value, attrs=None):
        strength_markup = """
        <div style="margin-top: 10px;">
            <div class="progress" style="margin-bottom: 10px;">
                <div class="progress-bar progress-bar-warning password_strength_bar"
                     role="progressbar"
                     aria-valuenow="0"
                     aria-valuemin="0"
                     aria-valuemax="5"
                     style="width: 0%%">
                </div>
            </div>
            <p class="text-muted password_strength_info hidden">
                <span class="label label-danger">
                    %s
                </span>
                <span style="margin-left:5px;">
                    %s
                </span>
            </p>
        </div>
        """ % (_('Warning'), _('<em class="password_strength_time"></em>'))

        try:
            self.attrs['class'] = '%s password_strength'.strip() % self.attrs['class']
        except KeyError:
            self.attrs['class'] = 'password_strength'

        return mark_safe(super(PasswordInput, self).render(name, value, attrs) + strength_markup)

    class Media:
        js = (
            'django_password_strength_sk/js/zxcvbn-async.js',
            'django_password_strength_sk/js/password_strength.js',
        )


class PasswordConfirmationInput(PasswordInput):
    """
    Form widget to confirm the users password by letting him/her type it again.
    """

    def __init__(self, confirm_with=None, attrs=None, render_value=False):
        super(PasswordConfirmationInput, self).__init__(attrs, render_value)
        self.confirm_with=confirm_with

    def render(self, name, value, attrs=None):
        if self.confirm_with:
            self.attrs['data-confirm-with'] = 'id_%s' % self.confirm_with

        confirmation_markup = """
        <div style="margin-top: 10px;" class="hidden password_strength_info">
            <p class="text-muted">
                <span class="label label-danger">
                    %s
                </span>
                <span style="margin-left:5px;">%s</span>
            </p>
        </div>
        """ % (_('Warning'), _('Your passwords don\'t match.'))

        try:
            self.attrs['class'] = '%s password_confirmation'.strip() % self.attrs['class']
        except KeyError:
            self.attrs['class'] = 'password_confirmation'

        return mark_safe( super(PasswordInput, self).render(name, value, attrs) + confirmation_markup )

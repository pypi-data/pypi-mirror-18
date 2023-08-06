import exceptions
import platform

from behave import step, then

from installib.windows import (
    get_registry_from_wow6432_microsoft_windows_current_version_uninstall,
    get_registry_from_microsoft_windows_current_version_uninstall, uninstall_windows_application
)


__all__ = (
    'step_read_application_windows_uninstall_registry', 'step_read_application_wow6432_windows_uninstall_registry',
    'step_assert_contact', 'step_assert_display_name', 'step_assert_display_version', 'step_assert_help_link',
    'step_assert_help_telephone', 'step_assert_publisher', 'step_assert_url_info',
    'step_uninstall_application_from_windows', 'step_guess_architecture'
)


@step('I guess OS architecture')
def step_guess_architecture(context):
    context.os_architecture = platform.architecture()[0]


@step('I read "{product_code}" application from windows uninstall registry')
def step_read_application_windows_uninstall_registry(context, product_code):
    context.registry = get_registry_from_microsoft_windows_current_version_uninstall(product_code)


@step('I read "{product_code}" 32bit application from windows uninstall registry')
def step_read_application_wow6432_windows_uninstall_registry(context, product_code):
    os_architecture = platform.architecture()[0]
    if os_architecture == "32bit":
        context.registry = get_registry_from_microsoft_windows_current_version_uninstall(product_code)
    elif os_architecture == "64bit":
        context.registry = get_registry_from_wow6432_microsoft_windows_current_version_uninstall(product_code)
    else:
        raise exceptions.BaseException("I couldn't guess OS architecture")


@step('I uninstall "{product_code}" application from Windows System')
def step_uninstall_application_from_windows(context, product_code):
    uninstall_windows_application(product_code)


@then('contact is equal to "{contact}"')
def step_assert_contact(context, contact):
    assert context.registry.contact == contact, "%s is not equal to %s" % (context.registry.contact, contact)


@then('display name is equal to "{display_name}"')
def step_assert_display_name(context, display_name):
    assert context.registry.display_name == display_name, "%s is not equal to %s" % (context.registry.display_name,
                                                                                     display_name)


@then('display version is equal to "{version}"')
def step_assert_display_version(context, version):
    assert context.registry.display_version == version, "%s is not equal to %s" % (context.registry.display_version,
                                                                                   version)


@then('help link is equal to "{link}"')
def step_assert_help_link(context, link):
    assert context.registry.help_link == link, "%s is not equal to %s" % (context.registry.help_link, link)


@then('help telephone is equal to "{telephone}"')
def step_assert_help_telephone(context, telephone):
    assert context.registry.help_telephone == telephone, "%s is not equal to %s" % (context.registry.help_telephone,
                                                                                    telephone)


@then('url info about is equal to "{url_info_about}"')
def step_assert_url_info(context, url_info_about):
    assert context.registry.url_info_about == url_info_about, "%s is not equal to %s" % (context.registry.url_info_about,
                                                                                         url_info_about)


@then('publisher about is equal to "{publisher}"')
def step_assert_publisher(context, publisher):
    assert context.registry.publisher == publisher, "%s is not equal to %s" % (context.registry.publisher,
                                                                               publisher)

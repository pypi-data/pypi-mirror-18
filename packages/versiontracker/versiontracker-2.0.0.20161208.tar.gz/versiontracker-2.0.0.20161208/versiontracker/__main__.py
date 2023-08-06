from argparse import ArgumentParser

from termcolor import colored

from versiontracker import (
    iter_software_ids_by_spider, iter_version_info, MissingSpiders,
    SoftwareEntryDefinitionError, supported_software, UnknownSoftwareIDs)
from versiontracker._version import __version__


def _colored_software_id(product):
    return colored(product, attrs=('bold',))


def _print_product(data):
    formatted_data = {
        'product': _colored_software_id(data["id"]),
        'version': colored(data["version"], "green"),
        'url': colored(data["url"], "magenta"),
    }
    template = "{product}: {version} @ {url}"
    if "date" in data and data["date"]:
        formatted_data['date'] = colored(
            data["date"].strftime("%Y-%m-%d"), "cyan")
        template = "{product}: {version} ({date}) @ {url}"
    print(template.format(**formatted_data))


def build_argument_parser():
    parser = ArgumentParser(
        description="Prints the latest stable version, release date and "
                    "reference URL of the specified software products.")
    parser.add_argument(
        'products', nargs='*', metavar='product', default=supported_software(),
        help="ID of a software product whose latest stable version you want "
             "to know. Use -l to get a list of available IDs. If omitted, "
             "all supported products are selected.")
    parser.add_argument(
        '-l', '--list-ids', action='store_true', dest='list_ids',
        help="Lists IDs of supported software products.")
    parser.add_argument('-s', '--spider',
        help="Prints results for all software that uses the specified spider.")
    parser.add_argument('-v', '--version', action='version',
                        version='%(prog)s {}'.format(__version__))
    return parser


def main():
    options = build_argument_parser().parse_args()
    if options.list_ids:
        for software_id in sorted(supported_software()):
            print(_colored_software_id(software_id))
    else:
        if options.spider:
            options.products = iter_software_ids_by_spider(options.spider)
        try:
            items = list(iter_version_info(options.products))
            for item in sorted(items, key=lambda k: k['id']):
                _print_product(item)
        except MissingSpiders as error:
            print(
                "{} The spiders defined for the following specified software"
                "IDs are not known: {}."
                "".format(colored("Error:", 'red'), ', '.join(
                    u'{} ({})'.format(_colored_software_id(software_id),
                                      error.data[software_id])
                    for software_id in sorted(error.data.keys()))))
        except SoftwareEntryDefinitionError as error:
            details = []
            for software_id in sorted(error.errors.keys()):
                entry_details = []
                entry_errors = error.errors[software_id]
                for field in sorted(entry_errors.keys()):
                    items = entry_errors[field]
                    if items:
                        entry_details.append("- {}: {}.".format(
                            field.replace('_', ' ').capitalize(),
                            ', '.join(items)))
                details.append("- {}:\n{}".format(
                    _colored_software_id(software_id),
                    '\n'.join(' '*4 + entry_detail
                              for entry_detail in entry_details)))
            details = '\n'.join(details)
            print("{} The following definition errors were found:\n"
                  "{}"
                  "\n\nIf you are not extending software tracking data, "
                  "please report this issue to the Version Tracker developers."
                  "".format(colored("Error:", 'red'), details))
        except UnknownSoftwareIDs as error:
            print(
                "{} The following specified software IDs are not known: {}.\n"
                "Use the -l option to get a list of supported software IDs"
                "".format(colored("Error:", 'red'), ', '.join(
                    _colored_software_id(software_id)
                    for software_id in error.software_ids)))


if __name__ == '__main__':
    main()

from littler.adapters.grawadapter import GrawAdapter


# Map of the adapter classes that this package contains
adapters_map = dict()
adapters_map['graw'] = GrawAdapter


def get_adapter(type_, data_source, source_id, source_string, name, datetime):
    """Factory function. Configure and return a adapter for the data source"""
    ad = adapters_map[type_]()
    ad.set_source_str(source_string)
    ad.set_id(source_id)
    ad.set_datetime(datetime)
    ad.set_name(name)
    ad.parse_data_source(data_source)
    return ad

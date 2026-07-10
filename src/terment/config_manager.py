import yaml
from terment.providers import Provider, provider_list


def load_config():
    with open("config.yaml", "r") as config:
        data = yaml.safe_load(config)
    return data


def get_selected_provider():
    config_data = load_config().get("model")
    selected_model = config_data.get("default")
    selected_provider = config_data.get("provider")
    # return selected_provider, selected_model
    for provider in provider_list:
        if provider.name == selected_provider:
            return {"provider": provider, "model": selected_model}
    else:
        raise ValueError("Selected Provider not found in list of provider.")

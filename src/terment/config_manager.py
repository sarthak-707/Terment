import yaml
from pathlib import Path
from terment.providers import provider_list

CONFIG_PATH = Path.home() / ".terment" / "config.yaml"
CONFIG_PATH.parent.mkdir(exist_ok=True, parents=True)
CONFIG_PATH.touch(exist_ok=True)


def load_config():
    with open(CONFIG_PATH, "r") as config:
        data = yaml.safe_load(config)
        if data is not None:
            return data
        else:
            raise FileNotFoundError(
                "Config was not found, create a valid config using config.yaml.example"
            )


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

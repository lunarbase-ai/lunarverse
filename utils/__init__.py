import json
import os
import ast
import re

BASE_COMPONENT_CLASS_NAME = "BaseComponent"

from langchain_openai import AzureChatOpenAI


def generate_readme(
    context: str,
    api_key: str,
    endpoint: str,
    deployment: str,
    version: str,
    max_tokens: int = 100,
):
    llm = AzureChatOpenAI(
        deployment_name=deployment,
        temperature=0.7,
        max_tokens=max_tokens,
        timeout=None,
        max_retries=2,
        openai_api_key=api_key,
        azure_endpoint=endpoint,
        openai_api_version=version,
    )

    messages = [
        (
            "system",
            "You are a helpful assistant that writes documentation for software code where each class is called a component. Write README documentation for a component with the user provided details. Do not generate example usages.",
        ),
        ("user", context),
    ]

    response = llm.invoke(messages)

    return response.content


def generate_component_readme(component_path: str):
    if not os.path.isdir(component_path):
        raise ValueError(f"Path {component_path} not found!")

    main_class = os.path.join(component_path, "__init__.py")
    try:
        with open(os.path.abspath(main_class), "r") as f:
            source_code = f.read()
    except FileNotFoundError:
        raise FileNotFoundError("Main class in __init__.py not found: no such file!")

    tree = ast.parse(source_code)
    component_class_defs = [
        node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)
    ]
    if len(component_class_defs) < 1:
        raise ValueError(
            f"No class definition found in __init__.py. A component definition must inherit from {BASE_COMPONENT_CLASS_NAME} and be placed in __init__.py. "
        )

    component_class, component_class_name = None, None
    for _cls in component_class_defs:
        base_class_names = {b.id for b in _cls.bases}
        if BASE_COMPONENT_CLASS_NAME in base_class_names:
            component_class = _cls
            component_class_name = _cls.name
            break

    if (
        component_class_name is None
        or BASE_COMPONENT_CLASS_NAME not in base_class_names
    ):
        raise ValueError(
            f"Classes in {main_class} must inherit {BASE_COMPONENT_CLASS_NAME}!"
        )

    keywords = ",".join(
        [f'"{kw.arg}": {ast.unparse(kw.value)}' for kw in component_class.keywords]
    )
    keywords = re.sub(r"(?<!\w)\'|\'(?!\w)", '"', keywords)
    keywords = re.sub(r"DataType\.(\w+)", r'"\1"', keywords)
    keywords = re.sub(r"ComponentGroup\.(\w+)", r'"\1"', keywords)
    keywords = re.sub(r":\s?(None)", r':"\1"', keywords)
    keywords = json.loads("{" + keywords + "}")

    _component_description = keywords.pop("component_description", "")

    keywords.pop("component_group")

    component_data = dict()
    try:
        component_data["name"] = keywords.pop("component_name")
        # component_data["class_name"] = component_class_name
        component_data["description"] = _component_description
        # component_data["group"] = keywords.pop("component_group")
        component_data["inputs types"] = json.dumps(keywords.pop("input_types"))
        component_data["output type"] = keywords.pop("output_type")
        component_data["configuration parameters"] = list(keywords.keys())

    except KeyError as e:
        raise ValueError(
            f"Failed to parse component at {main_class}! One or more expected attributes may be missing. Details: {str(e)}"
        )

    return component_data


def generate_components_json(component_path: str):
    component_dir = os.path.basename(component_path)
    component_name = component_dir.replace("_", "-")
    config = {
        "name": component_name,
        "location": "https://github.com/lunarbase-labs/lunarverse",
        "subdirectory": component_dir
    }
    return config


if __name__ == "__main__":
    main_doc = ""
    for component_dir in os.listdir(".."):
        if component_dir.startswith("."):
            continue
        if component_dir.startswith("venv"):
            continue

        if component_dir.startswith("utils"):
            continue

        if component_dir.startswith("LICENSES"):
            continue

        component_name = component_dir
        component_dir = f"../{component_dir}"
        if not os.path.isdir(component_dir):
            continue

        # if os.path.isfile(f"{component_dir}/README.md"):
        #     readme_path = f"/Users/alexbogatu/lunar/docs/main-docs/lunar.github.io/docs/all_components/{component_name}"
        #     os.makedirs(readme_path, exist_ok=True)
        #     shutil.copy(
        #         f"{component_dir}/README.md", f"{readme_path}/{component_name}.md"
        #     )
        # print(component_dir)
        config = generate_components_json(component_dir)
        print(f"{config},")
        # component = generate_component_readme(component_dir)
        # _desc = component["description"].split("\n")[0].split(".")[0]
        # main_doc = (
        #     main_doc
        #     + f"| [{component['name']}](./all_components/{component_name}/{component_name}.md) | {_desc} |\n"
        # )

        # readme = generate_readme(
        #     context=json.dumps(component),
        #     api_key="18f5fa86c73d463183690228a6ad1480",
        #     endpoint="https://lunarchatgpt.openai.azure.com/",
        #     deployment="lunar-chatgpt-4o",
        #     version="2024-02-01",
        #     max_tokens=500,
        # )
        # if len(readme) > 0:
        #     with open(f"{component_dir}/README.md", "w") as f:
        #         f.write(readme)
        # print(readme)

        # print("=====================")

    print(main_doc)

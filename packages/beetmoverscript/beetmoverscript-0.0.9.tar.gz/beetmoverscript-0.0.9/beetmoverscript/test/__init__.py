from beetmoverscript.utils import load_json


def get_fake_valid_config():
    return load_json(path="beetmoverscript/test/fake_config.json")


def get_fake_valid_task():
    return load_json(path="beetmoverscript/test/test_work_dir/task.json")


def get_fake_balrog_props(fake_context):
    return load_json(path="beetmoverscript/test/fake_balrog_props.json")

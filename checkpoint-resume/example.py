"""
Checkpoint + Resume example.
"""

from implementation import CheckpointStore, ResumableRunner


def step_1(data: dict):
    data["a"] = 1
    return data


def step_2(data: dict):
    if not data.get("_already_failed"):
        data["_already_failed"] = True
        raise RuntimeError("Simulated interruption on step 2")
    data["b"] = 2
    return data


def step_3(data: dict):
    data["c"] = data["a"] + data["b"]
    return data


def main():
    store = CheckpointStore(".checkpoints/demo.json")
    runner = ResumableRunner("demo_task", [step_1, step_2, step_3], store)

    first = runner.run(initial_data={})
    print("first run:", first.status, first.step_index, first.error)

    second = runner.run()
    print("second run:", second.status, second.step_index, second.error)
    print("final data:", second.data)


if __name__ == "__main__":
    main()

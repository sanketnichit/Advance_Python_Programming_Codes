"""Python Garbage Collection: Research and Manual Control

This practical demonstrates reference counting, cyclic garbage collection,
collection settings, memory usage, and timing with Python's gc module.

Run: python garbage_collection.py
No third-party packages are required.
"""

import gc
import sys
import time
import tracemalloc
import weakref


def show_heading(title):
    """Print a heading for each experiment."""
    print(f"\n{'=' * 8} {title} {'=' * 8}")


class Node:
    """A small object used to make object destruction visible."""

    def __init__(self, name):
        self.name = name
        self.other = None

    def __del__(self):
        print(f"   [__del__] {self.name} was destroyed")


def experiment_1_reference_counting():
    show_heading("1. REFERENCE COUNTING")

    first = Node("A")
    print("Reference count of A:", sys.getrefcount(first))

    second = first
    print("After second = first:", sys.getrefcount(first))

    del first
    print("After deleting first:", sys.getrefcount(second))

    print("Deleting the last reference...")
    del second
    print("The object is destroyed immediately when its reference count reaches zero.")


def experiment_2_reference_cycle():
    show_heading("2. REFERENCE CYCLE AND MANUAL COLLECTION")

    gc.collect()
    was_enabled = gc.isenabled()
    gc.disable()

    try:
        print("Automatic garbage collection enabled?", gc.isenabled())

        x = Node("X")
        y = Node("Y")
        x.other = y
        y.other = x

        del x, y
        print("Both names were deleted. The two objects still refer to each other.")

        found = gc.collect()
        print("Objects found by gc.collect():", found)
    finally:
        if was_enabled:
            gc.enable()
        else:
            gc.disable()


def experiment_3_collection_information():
    show_heading("3. THRESHOLDS, COUNTS AND STATISTICS")

    print("Python version:", sys.version.split()[0])
    print("Collection thresholds:", gc.get_threshold())
    print("Current generation counts:", gc.get_count())

    print("\nCollection statistics:")
    for generation, stats in enumerate(gc.get_stats()):
        print(
            f"Generation {generation}: "
            f"collections={stats['collections']}, "
            f"collected={stats['collected']}, "
            f"uncollectable={stats['uncollectable']}"
        )


def experiment_4_automatic_collection():
    show_heading("4. AUTOMATIC COLLECTION WITH CALLBACKS")

    if not gc.isenabled():
        gc.enable()

    old_thresholds = gc.get_threshold()
    events = []

    def collection_watcher(phase, info):
        """Save details when a garbage-collection run finishes."""
        if phase == "stop":
            events.append((info.get("generation"), info.get("collected")))

    gc.collect()
    gc.callbacks.append(collection_watcher)

    try:
        gc.set_threshold(50, 5, 5)

        for _ in range(300):
            first = []
            second = []
            first.append(second)
            second.append(first)

        print("Temporary cycles created: 300")
        print("Automatic collections observed:", len(events))
        print("First few (generation, objects collected):", events[:5])
    finally:
        gc.set_threshold(*old_thresholds)
        if collection_watcher in gc.callbacks:
            gc.callbacks.remove(collection_watcher)
        gc.collect()


def experiment_5_generations():
    show_heading("5. GENERATIONAL COLLECTION")

    gc.collect()

    keeper = Node("Long-lived object")
    keeper.other = keeper

    print(
        "Tracked objects before collect(0):",
        [len(gc.get_objects(generation)) for generation in range(3)],
    )

    gc.collect(0)
    print(
        "Tracked objects after collect(0):",
        [len(gc.get_objects(generation)) for generation in range(3)],
    )

    gc.collect(1)
    print(
        "Tracked objects after collect(1):",
        [len(gc.get_objects(generation)) for generation in range(3)],
    )

    print("Objects that survive younger-generation collections can be promoted.")
    keeper.other = None
    del keeper


def experiment_6_memory_usage():
    show_heading("6. MEMORY USED BY UNREACHABLE CYCLES")

    gc.collect()
    was_enabled = gc.isenabled()
    gc.disable()

    tracemalloc.start()
    try:
        starting_memory = tracemalloc.get_traced_memory()[0]

        for _ in range(20000):
            first = {}
            second = {}
            first["other"] = second
            second["other"] = first

        del first, second

        memory_before = tracemalloc.get_traced_memory()[0] - starting_memory
        collected = gc.collect()
        memory_after = tracemalloc.get_traced_memory()[0] - starting_memory

        print(f"Memory held before collection: {memory_before / 1024:.1f} KiB")
        print("Objects found by gc.collect():", collected)
        print(f"Memory after collection:       {memory_after / 1024:.1f} KiB")
    finally:
        tracemalloc.stop()
        if was_enabled:
            gc.enable()
        else:
            gc.disable()


def experiment_7_debug_saveall():
    show_heading("7. DEBUG_SAVEALL")

    gc.collect()
    old_debug_flags = gc.get_debug()
    old_garbage_length = len(gc.garbage)

    try:
        gc.set_debug(old_debug_flags | gc.DEBUG_SAVEALL)

        first = ["first object"]
        second = ["second object"]
        first.append(second)
        second.append(first)
        del first, second

        found = gc.collect()
        saved_objects = gc.garbage[old_garbage_length:]

        print("Objects found during collection:", found)
        print("Objects saved in gc.garbage:", len(saved_objects))
        print("Saved object types:", [type(obj).__name__ for obj in saved_objects])
    finally:
        gc.set_debug(old_debug_flags)
        # Remove only objects added by this experiment.
        del gc.garbage[old_garbage_length:]
        gc.collect()


def experiment_8_tracking_and_weak_references():
    show_heading("8. TRACKED OBJECTS AND WEAK REFERENCES")

    samples = [
        ("Integer", 10),
        ("String", "Python"),
        ("List", [1, 2, 3]),
        ("Empty dictionary", {}),
        ("Dictionary with list", {"numbers": [1, 2]}),
        ("Tuple of integers", (1, 2, 3)),
        ("Node object", Node("Tracked node")),
    ]

    for label, obj in samples:
        print(f"{label:<22} tracked by gc? {gc.is_tracked(obj)}")

    item = Node("Weak reference object")
    reference = weakref.ref(item)
    print("Weak reference alive?", reference() is not None)

    del item
    print("After deleting the object, weak reference alive?", reference() is not None)


def experiment_9_freeze():
    show_heading("9. FREEZE AND UNFREEZE")

    gc.collect()
    print("Frozen objects before freeze():", gc.get_freeze_count())

    gc.freeze()
    print("Frozen objects after freeze(): ", gc.get_freeze_count())

    gc.unfreeze()
    print("Frozen objects after unfreeze():", gc.get_freeze_count())


def allocation_work(number_of_items=200000):
    """Create many small lists for a simple allocation-heavy timing test."""
    values = []
    for number in range(number_of_items):
        values.append([number])
    return len(values)


def experiment_10_timing():
    show_heading("10. TIME WITH AUTOMATIC GC ENABLED AND DISABLED")

    original_state = gc.isenabled()
    timings = {}

    try:
        for label, enable_gc in (("Enabled", True), ("Disabled", False)):
            gc.enable()
            gc.collect()

            if enable_gc:
                gc.enable()
            else:
                gc.disable()

            start_time = time.perf_counter()
            total = allocation_work()
            elapsed = time.perf_counter() - start_time
            timings[label] = elapsed

            print(f"Garbage collection {label.lower():<8}: {elapsed * 1000:.2f} ms")
            print("Lists created:", total)
    finally:
        if original_state:
            gc.enable()
        else:
            gc.disable()

    if timings["Disabled"] < timings["Enabled"]:
        print("In this run, disabling automatic collection was faster.")
    elif timings["Disabled"] > timings["Enabled"]:
        print("In this run, enabling automatic collection was faster.")
    else:
        print("Both runs took approximately the same time.")

    print("Timing can change with the computer and Python version.")


def main():
    print("PYTHON GARBAGE COLLECTION PRACTICAL")
    print("Python version:", sys.version.split()[0])

    experiment_1_reference_counting()
    experiment_2_reference_cycle()
    experiment_3_collection_information()
    experiment_4_automatic_collection()
    experiment_5_generations()
    experiment_6_memory_usage()
    experiment_7_debug_saveall()
    experiment_8_tracking_and_weak_references()
    experiment_9_freeze()
    experiment_10_timing()

    print("\nConclusion: Reference counting frees objects when their reference count")
    print("reaches zero. The cyclic garbage collector finds unreachable cycles.")
    print("The gc module allows programmers to inspect and control this process.")


if __name__ == "__main__":
    main()

import threading

from .memory_cache import MemoryCache


def test_simple_cache():
    cache = MemoryCache()

    assert cache.get("empty_key") is None

    cache.put("key1", "foo")
    assert cache.get("key1") == "foo"

    cache.put("key2", 1.1)
    assert cache.get("key2") == 1.1

    cache.delete("key2")

    assert cache.get("key2") is None


def test_race_condition():
    cache = MemoryCache()
    key = "any_key"

    def put_key():
        cache.put(key, "any_val")
        val = cache.get(key)
        cache.put(key, f"updated-value: {val}")

    def update_key():
        cache.put(key, "any_val_update")

    thread1 = threading.Thread(target=put_key)
    thread2 = threading.Thread(target=update_key)

    thread1.start()
    thread2.start()

    thread1.join()
    thread2.join()

    assert cache.get(key) == "any_val_update"

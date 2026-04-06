import functools
from collections.abc import Callable
from typing import ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def pw_trace(name: str | None = None) -> Callable[[Callable[P, R]], Callable[P, R]]:
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @functools.wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if not args:
                return func(*args, **kwargs)

            instance = args[0]
            page = getattr(instance, "page", None)
            if page is None:
                return func(*args, **kwargs)

            group_name = name or f"{instance.__class__.__name__}.{func.__name__}"

            try:
                page.context.tracing.group(group_name)
            except Exception:
                return func(*args, **kwargs)

            try:
                return func(*args, **kwargs)
            finally:
                try:
                    page.context.tracing.group_end()
                except Exception:
                    pass

        return wrapper

    return decorator

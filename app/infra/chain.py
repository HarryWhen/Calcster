from typing import Callable, Generic, Optional, ParamSpec, Self, TypeVar, override

Req = ParamSpec("Req")
Res = TypeVar("Res")


class Chain(Generic[Req, Res]):
    def __init__(
        self,
        *handlers: Callable[Req, Optional[Res]],
    ) -> None:
        self._handlers = handlers

    def __call__(self, *args: Req.args, **kwargs: Req.kwargs) -> Optional[Res]:
        for handler in self._handlers:
            if res := handler(*args, **kwargs):
                return res
        return None

    def __or__(self, other: Callable[Req, Optional[Res]]) -> Self:
        return self.__class__(*self._handlers, other)


class ChainWithDefaultHandler(Chain[Req, Res]):
    def __init__(
        self,
        default_handler: Callable[Req, Res],
        *handlers: Callable[Req, Optional[Res]],
    ) -> None:
        super().__init__(*handlers)
        self._default_handler = default_handler

    @override
    def __call__(self, *args: Req.args, **kwargs: Req.kwargs) -> Res:
        if res := super().__call__(*args, **kwargs):
            return res
        return self._default_handler(*args, **kwargs)

    @override
    def __or__(self, other: Callable[Req, Optional[Res]]) -> Self:
        return self.__class__(self._default_handler, *self._handlers, other)

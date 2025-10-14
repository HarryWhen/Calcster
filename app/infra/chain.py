from typing import Callable, Optional, ParamSpec, Protocol, Self, TypeVar

Req = ParamSpec("Req")
Res = TypeVar("Res")


class ChainLike(Protocol[Req, Res]):
    def __call__(self, *args: Req.args, **kwargs: Req.kwargs) -> Res: ...

    def __or__(self, other: Callable[Req, Optional[Res]]) -> Self: ...


class Chain(ChainLike[Req, Optional[Res]]):
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


class ChainWithDefaultHandler(ChainLike[Req, Res]):
    def __init__(
        self,
        *,
        default_handler: Callable[Req, Res],
        chain: Optional[Chain[Req, Res]] = None,
    ) -> None:
        self._chain = chain or Chain()
        self._default_handler = default_handler

    def __call__(self, *args: Req.args, **kwargs: Req.kwargs) -> Res:
        return self._chain(*args, **kwargs) or self._default_handler(*args, **kwargs)

    def __or__(self, other: Callable[Req, Optional[Res]]) -> Self:
        return self.__class__(
            default_handler=self._default_handler,
            chain=self._chain | other,
        )

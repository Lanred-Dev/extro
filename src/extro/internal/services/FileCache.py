import pyray
from typing import TYPE_CHECKING, Generic, TypeVar, Callable

CacheFileType = TypeVar("CacheFileType")
FileType = TypeVar("FileType")

if TYPE_CHECKING:
    LoaderFunction = Callable[[str], CacheFileType]
    UnloaderFunction = Callable[[CacheFileType], None]
    CloneLoaderFunction = Callable[[CacheFileType], FileType]


class Cache(Generic[CacheFileType, FileType]):
    __slots__ = ("_cache", "_users_map", "_loader", "_unloader", "_clone_loader")

    _cache: dict[str, CacheFileType]
    _users_map: dict[str, int]
    _loader: "LoaderFunction"
    _unloader: "UnloaderFunction"
    _clone_loader: "CloneLoaderFunction | None"

    def __init__(
        self,
        loader: "LoaderFunction",
        unloader: "UnloaderFunction",
        clone_loader: "CloneLoaderFunction | None" = None,
    ):
        self._cache = {}
        self._users_map = {}
        self._loader = loader
        self._unloader = unloader
        self._clone_loader = clone_loader

    def load(self, path: str) -> FileType:
        # If there is no clone loader then `FileType` is the same as `CacheFileType` (at least should be)
        if path in self._cache:
            if self._clone_loader:
                return self._clone_loader(self._cache[path])

            self._users_map[path] += 1
            return self._cache[path]  # type: ignore

        resource: CacheFileType = self._loader(path)
        self._cache[path] = resource
        self._users_map[path] = 1
        return resource  # type: ignore

    def unload(self, path: str):
        if path not in self._cache:
            return

        self._users_map[path] -= 1

        if self._users_map[path] <= 0:
            self._unloader(self._cache[path])
            del self._cache[path]
            del self._users_map[path]


audio_cache = Cache[pyray.Wave, pyray.Sound](
    pyray.load_wave, pyray.unload_wave, pyray.load_sound_from_wave
)

texture_cache = Cache[pyray.Texture, pyray.Texture](
    pyray.load_texture, pyray.unload_texture
)

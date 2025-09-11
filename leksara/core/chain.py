"""ReviewChain runner and pipeline executor.

Fitur utama:
1. Eksekusi berurutan: patterns -> functions.
2. Setiap step boleh berupa callable langsung atau tuple (callable, {kwargs}).
3. Bisa dipakai fungsional (``run_pipeline`` / ``Leksara``) atau OOP (``ReviewChain``).
4. Opsi benchmark=True mengembalikan metrik waktu per step & total.

Contoh cepat:
    from leksara.core.chain import run_pipeline
    from leksara.functions.cleaner.basic import case_normal, remove_punctuation
    data = ["Halo GAN!!!", "Produk BAGUS???"]
    pipe = {"patterns": [], "functions": [case_normal, remove_punctuation]}
    cleaned = run_pipeline(data, pipe)

Catatan: Default pipeline (jika None) menggunakan subset fungsi dasar
yang tersedia (remove_tags -> case_normal -> remove_whitespace) bila dapat diimpor.
"""

# ReviewChain runner dan executor pipeline
from __future__ import annotations

from typing import Callable, Iterable, Dict, Any, Union, Tuple, List, Optional
from dataclasses import dataclass
from time import perf_counter

try:
    import pandas as pd  # type: ignore
except Exception:  # pragma: no cover
    pd = None  # type: ignore

TextFn = Callable[[str], str]
Step = Union[TextFn, Tuple[TextFn, Dict[str, Any]]]


# ---------------------------- utils ----------------------------
def _normalize_steps(steps: Optional[Iterable[Step]]) -> List[TextFn]:
    """Konversi step menjadi callable murni, simpan nama step utk pelaporan."""
    out: List[TextFn] = []
    if not steps:
        return out
    for s in steps:
        if callable(s):
            fn = s
            setattr(fn, "__leksara_name__", getattr(fn, "__name__", repr(fn)))
            out.append(fn)
        elif isinstance(s, tuple) and len(s) == 2 and callable(s[0]) and isinstance(s[1], dict):
            fn, kwargs = s
            name = getattr(fn, "__name__", repr(fn))
            def wrapped(x: str, _fn=fn, _kw=kwargs):
                return _fn(x, **_kw)
            setattr(wrapped, "__leksara_name__", name)
            out.append(wrapped)
        else:
            raise TypeError("Step pipeline harus callable atau (callable, dict kwargs).")
    return out


def _compose(funcs: Iterable[TextFn]) -> TextFn:
    funcs = list(funcs)
    def _f(x: str) -> str:
        for fn in funcs:
            x = fn(x)
        return x
    return _f


def _default_pipeline() -> Dict[str, List[Step]]:
    """Pipeline default sederhana bila user tak memberi pipeline."""
    patterns: List[Step] = []
    functions: List[Step] = []
    try:
        from ..functions.cleaner.basic import remove_tags, case_normal, remove_whitespace  # type: ignore
        functions.extend([remove_tags, case_normal, remove_whitespace])
    except Exception:
        # jika fungsi dasar belum tersedia, pakai pipeline kosong
        pass
    return {"patterns": patterns, "functions": functions}


# ------------------------ functional API -----------------------
def leksara(
    data,  # pd.Series | Iterable[str] (annotation dilonggarkan agar pd opsional)
    pipeline: Optional[Dict[str, Iterable[Step]]] = None,
    *,
    benchmark: bool = False,
):
    """Eksekusi pipeline: patterns → functions.

    Args:
        data: pd.Series atau iterable of str
        pipeline: {"patterns": [...], "functions": [...]} (optional)
        benchmark: jika True kembalikan (hasil, metrics)
    """
    if pipeline is None:
        pipeline = _default_pipeline()

    patterns = _normalize_steps(pipeline.get("patterns", []))
    functions = _normalize_steps(pipeline.get("functions", []))
    steps_all = [*patterns, *functions]
    fn = _compose(steps_all)

    # timing agregat per step
    timings_map: Dict[str, float] = {}

    def _run_steps_with_timing(x: str) -> str:
        y = x
        for step in steps_all:
            if not benchmark:
                y = step(y)
            else:
                t0 = perf_counter()
                y = step(y)
                dt = perf_counter() - t0
                name = getattr(step, "__leksara_name__", getattr(step, "__name__", repr(step)))
                timings_map[name] = timings_map.get(name, 0.0) + dt
        return y

    def _apply_one(v: Any) -> Any:  # type: ignore[valid-type]
        return _run_steps_with_timing(v) if isinstance(v, str) else v

    # dukung iterable biasa tanpa pandas
    if pd is not None and isinstance(data, pd.Series):
        out = data.apply(_apply_one)
    else:
        # asumsikan iterable of str
        out = [_apply_one(v) for v in data]

    if benchmark:
        total = sum(timings_map.values())
        metrics = {
            "n_steps": len(steps_all),
            "total_time_sec": total,
            "per_step": sorted(timings_map.items(), key=lambda kv: kv[1], reverse=True),
        }
        return out, metrics
    return out


def run_pipeline(
    data,
    pipeline: Optional[Dict[str, Iterable[Step]]] = None,
    *,
    benchmark: bool = False,
):
    return Leksara(data, pipeline=pipeline, benchmark=benchmark)


# -------------------------- OOP API ----------------------------
@dataclass
class ReviewChain:
    """Wrapper OOP untuk pipeline teks."""
    patterns: List[Step]
    functions: List[Step]

    @classmethod
    def from_steps(
        cls,
        *,
        patterns: Optional[Iterable[Step]] = None,
        functions: Optional[Iterable[Step]] = None,
    ) -> "ReviewChain":
        if patterns is None and functions is None:
            pipe = _default_pipeline()
            patterns = pipe["patterns"]
            functions = pipe["functions"]
        return cls(list(patterns or []), list(functions or []))

    def _build_callable(self) -> TextFn:
        return _compose([*_normalize_steps(self.patterns), *_normalize_steps(self.functions)])

    def process_text(self, text: str) -> str:
        return self._build_callable()(text)

    def run_on_series(self, series, *, benchmark: bool = False):
        pipe = {"patterns": self.patterns, "functions": self.functions}
        return run_pipeline(series, pipeline=pipe, benchmark=benchmark)

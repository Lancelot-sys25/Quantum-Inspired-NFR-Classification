"""Download the exact public datasets used by the experiments."""

from __future__ import annotations

import hashlib
import urllib.request
from pathlib import Path


DATASETS = (
    (
        "PROMISE-relabeled-NICE.csv",
        "https://zenodo.org/api/records/14590935/files/"
        "PROMISE-relabeled-NICE.csv/content",
        "87acb2172bc6273b8e04c55b4de8bf090cb0a9980b9d23010b20af88245f2642",
    ),
    (
        "PROMISE_exp.arff",
        "https://raw.githubusercontent.com/AleksandarMitrevski/"
        "se-requirements-classification/master/0-datasets/PROMISE_exp/"
        "PROMISE_exp.arff",
        "7475c2904648912ef08bd1b6149f505f7ce6ab26ee9b187c2ddee28d1af97d75",
    ),
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def download(name: str, url: str, expected_hash: str, output_dir: Path) -> None:
    destination = output_dir / name
    if destination.exists() and sha256(destination) == expected_hash:
        print(f"Verified existing file: {destination}")
        return

    temporary = destination.with_suffix(destination.suffix + ".download")
    request = urllib.request.Request(
        url, headers={"User-Agent": "Quantum-Inspired-NFR-Artifact/1.0"}
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            temporary.write_bytes(response.read())

        actual_hash = sha256(temporary)
        if actual_hash != expected_hash:
            raise RuntimeError(
                f"SHA-256 mismatch for {name}: expected {expected_hash}, "
                f"received {actual_hash}"
            )
        temporary.replace(destination)
        print(f"Downloaded and verified: {destination}")
    finally:
        temporary.unlink(missing_ok=True)


def main() -> None:
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)
    for dataset in DATASETS:
        download(*dataset, output_dir)


if __name__ == "__main__":
    main()

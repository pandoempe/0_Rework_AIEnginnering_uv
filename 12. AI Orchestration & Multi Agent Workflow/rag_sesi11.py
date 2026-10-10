"""
Sesi 12 — jembatan ke sistem RAG dari Sesi 11
==============================================

Modul kecil ini memuat index FAISS dan potongan dokumen yang sudah Anda bangun
di Sesi 11, lalu menyediakan satu fungsi saja:

    from rag_sesi11 import cari
    potongan = cari("masa tunggu klaim rawat inap", k=3)

Tujuannya supaya Sesi 12 tidak perlu membangun ulang RAG dari nol. Yang kita
bangun hari ini adalah alur di atasnya, bukan retrieval-nya.

Prasyarat:
    pip install google-genai python-dotenv numpy faiss-cpu
    file .env berisi GEMINI_API_KEY
    index_lindungiku.faiss dan potongan.json dari Sesi 11
"""

import json
import os
import pathlib

import faiss
import numpy as np
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL_EMBED = "gemini-embedding-001"
DIMENSI = 768


def akar_sesi():
    # Folder yang memuat index_lindungiku.faiss, entah folder ini atau induknya.
    for p in (pathlib.Path("."), pathlib.Path(".."), pathlib.Path("../..")):
        if (p / "index_lindungiku.faiss").is_file():
            return p.resolve()
    raise SystemExit(
        "index_lindungiku.faiss tidak ditemukan.\n"
        "Jalankan notebook dari folder Sesi 12, atau salin index dan potongan.json\n"
        "dari folder Sesi 11 Anda. Baca Troubleshooting bagian A."
    )


AKAR = akar_sesi()
BERKAS_INDEX = AKAR / "index_lindungiku.faiss"
BERKAS_POTONGAN = AKAR / "potongan.json"

index = faiss.read_index(str(BERKAS_INDEX))
potongan = json.loads(BERKAS_POTONGAN.read_text(encoding="utf-8"))

assert index.ntotal == len(potongan), (
    f"index berisi {index.ntotal} vector, potongan.json berisi {len(potongan)} "
    "potongan. Keduanya harus sama. Bangun ulang dari notebook Sesi 11."
)

_key = os.getenv("GEMINI_API_KEY")
if not _key:
    raise SystemExit("GEMINI_API_KEY tidak ditemukan. Periksa file .env.")

client = genai.Client(api_key=_key)


def normalisasi(v):
    panjang = np.linalg.norm(v, axis=1, keepdims=True)
    panjang[panjang == 0] = 1e-12
    return v / panjang


def _embed_pertanyaan(teks):
    # task_type untuk pertanyaan berbeda dari task_type untuk dokumen.
    # Tertukar tidak memunculkan error, hanya membuat hasil pencarian melemah.
    resp = client.models.embed_content(
        model=MODEL_EMBED,
        contents=[teks],
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=DIMENSI,
        ),
    )
    v = np.array([e.values for e in resp.embeddings], dtype="float32")
    return normalisasi(v)


def cari(pertanyaan, k=3):
    """Kembalikan k potongan paling relevan dari knowledge base Sesi 11.

    Setiap potongan adalah dict dengan kunci 'teks' dan 'sumber'.
    """
    q = _embed_pertanyaan(pertanyaan)
    skor, baris = index.search(q, k)
    hasil = []
    for nilai, i in zip(skor[0], baris[0]):
        item = dict(potongan[i])
        item["skor"] = float(nilai)
        hasil.append(item)
    return hasil


def konteks(pertanyaan, k=3):
    """Gabungkan k potongan teratas menjadi satu blok teks siap pakai."""
    return "\n\n".join(p["teks"] for p in cari(pertanyaan, k))


if __name__ == "__main__":
    print(f"index  : {BERKAS_INDEX}")
    print(f"vector : {index.ntotal}")
    for p in cari("masa tunggu klaim rawat inap", k=3):
        print(f"\n[{p['skor']:.3f}] {p['sumber']}")
        print(p["teks"][:160].replace("\n", " "))

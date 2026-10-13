Objective dari use case (apa yang ingin diselesaikan).
Membuat sistem Chat LLM menggunakan RAG untuk mencari informasi yang relevan di knowledge base dan menggunakan API LLM untuk menjawab pertanyaan user menggunakan knowledge yang relevan.

Sumber dan struktur knowledge base yang digunakan.
Database frequenly ask question (faq) dengan feature aq_id,category,question,answer.
data ini di econding untuk disimpan dalam bentuk vectorized di FAISS.

Batasan atau asumsi yang digunakan (misal: sistem hanya menjawab berdasarkan FAQ yang tersedia).
Sistem hanya menjawab berdasarkan data yang tersedia dari knowledge base, pada system prompt sudah di insert template untuk menjawab jika knowledge yang dibutuhkan untuk menjawab pertanyaan tidak ada di dalam sistem RAG.


Deskripsi singkat problem statement dan knowledge base.
Membuat sistem Chat LLM menggunakan RAG untuk mencari informasi yang relevan di knowledge base dan menggunakan API LLM untuk menjawab pertanyaan user menggunakan knowledge yang relevan.

Penjelasan alur sistem (ingest → embed → store → retrieve → generate).
Ingest :
1. Membaca database "ecommerce_faq_knowledge_base.csv"
2. Mengekstrak feature yang dibutuhkan lalu di buat list untuk selanjutnya dilakukan Embeddings.
Embed:
Melakukan Embedding data, merubah data menjadi data vektor (angka).
Store:
Menyimpan vektor kedalam database FAISS
Retreive:
1. Sistem mendapatkan input pertanyaan dari customer.
2. Pertanyaan dilakukan embedding menjadi vektor.
3. Melakukan semantic search dengan result 3 informasi yang konteksnya paling dekat dengan pertanyaan (k=3)
Generate:
1. Informasi yang didapatkan pada proses retrieve di insert kedalam system prompt beserta pertanyaan dari user.
2. Prompt dikirimkan ke LLM lewat API.
3. Sistem mendapatkan respon jawaban dan ditampilkan ke user.

Hasil pengujian query beserta analisis relevansi.
Telah dilakukan pengujian 5 pertanyaan :
1. "apakah jumlah stock valid?",
2. "bagaimana cara mengembalikan barang yang rusak?",
3. "apakah ada promo untuk pembelian pertama?",
4. "berapa lama waktu pengiriman ke luar negeri?",
5. "apakah bisa mengubah alamat pengiriman setelah order?"
pertanyaan no 4 tidak ada di knowledge base dan sistem meminta user untuk mengkontak Service Center (sesuai yang diperintahkan).
Pertanyaan lain jawabannya sudah sesuai.

Keterbatasan sistem yang ditemukan.
Knowledge terbatas pada informasi yang terdapat di RAG, perlu dilakukan update dan maintanance informasi yang tersimpan di RAG.

Cara menjalankan notebook/script.
1. Pastikan sudah membuat file .env didalam folder project dan mengisi "API_KEY_OPENROUTER = <isi api key open router anda>"
2. Buka "starter_notebook_semantic_search.ipynb"
3. Sesuaikan pertanyaan pada section 7 dan 8
4. Select Run All
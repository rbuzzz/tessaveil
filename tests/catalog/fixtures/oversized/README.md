The loader tests create sparse files exceeding the 1 MiB record and 16 MiB
word-list limits at runtime. This fixture directory records that case without
checking large binary padding into the repository.

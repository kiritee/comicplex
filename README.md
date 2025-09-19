# ComicPlex


🚀 *Plex for your comics — scan, enrich, and organize your digital collection.*


![License](https://img.shields.io/github/license/kiritee/comicplex)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![Build](https://img.shields.io/github/actions/workflow/status/kiritee/comicplex/ci.yml?branch=main&label=build)
![Coverage](https://img.shields.io/codecov/c/github/kiritee/comicplex?label=coverage)
![Issues](https://img.shields.io/github/issues/kiritee/comicplex)


**ComicPlex** is a sleek Python-powered tool that:


1. **Scans** your folders for `.cbz`, `.cbr`, `.pdf`, and other comic files.
2. **Parses** messy filenames into series, volume, issue, year.
3. **Enriches** issues with metadata from ComicVine — writer, artist, publisher, characters, arcs.
4. **Stores** your library in a local SQLite database.
5. **Builds smart reading views** by story arc, character, creator, or event using symlinks.


✨ Think of it as **Plex for comics** — automatic, organized, and future-proof.


## Quickstart
```bash
pip install -e .
export COMICVINE_API_KEY=your_key_here
comicplex scan ~/Comics --db ./data/catalog.db
comicplex enrich --db ./data/catalog.db
comicplex tag --db ./data/catalog.db
comicplex build-views --db ./data/catalog.db --views-root ./ReadingViews
```


## Notes
- Filenames aren’t consistent. Parser uses multiple heuristics + fuzzy matching.
- Windows: symlinks may require admin/developer mode.
- This is an MVP — extend the filename patterns and metadata mappers as needed.


## Roadmap
- [ ] Add character/team/event tagging from ComicVine
- [ ] Support `.comicinfo.xml` metadata inside CBZ
- [ ] Smarter story-arc view generation
- [ ] Web UI for browsing your library
- [ ] Dockerized deployment


## Contributing
PRs are welcome! For major changes, please open an issue first to discuss what you’d like to change.


## License
[MIT](LICENSE)
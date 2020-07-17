# ib_scraper
[InterviewBit](https://interviewbit.com) problems scraper and my notes 

#### Requirements
- install pandoc
	- `convert.py` uses `pandoc` to convert html to markdown.
- install mkdocs
	- `mkdocs` is not required but can be used to generate site using md files.

#### Doc generation
Run following commands
- `mkdocs new doc_dir`
- `python convert.py problems doc_dir/docs`
- `cd doc_dir`
- `mkdocs build`
	- `mkdocs build` will create a directory `site` in `doc_dir` containing the HTML doc for the problems.

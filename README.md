# ib_scraper
[InterviewBit](https://interviewbit.com) problems scraper and my notes 

### Requirements
- install pandoc
	- `convert.py` uses `pandoc` to convert html to markdown.
- install mkdocs and mkdocs-material
	- `pip install mkdocs`
	- `pip install mkdocs-material`
	- `mkdocs` is not required but can be used to generate site using md files.
- install pypandoc
	- `pip install pypandoc` python wrapper to pandoc.

### Doc generation
Run following commands
- `mkdocs new doc_dir`
- `python combine.py problems doc_dir/docs`
- `cd doc_dir`
- `mkdocs build`
	- `mkdocs build` will create a directory `site` in `doc_dir` containing the HTML doc for the problems.

### Notes addition
Save your notes on a problem in markdown format. To put your notes under the problem directory run `store_md.py` .

**Usage:**
- meta : `python store_md.py meta`
- store : `python store_md.py store category prob_slug notes.md`
	- `https://www.interviewbit.com/problems/reverse-bits/` has problem slug `reverse-bits`.

Refer category map given below or you can set your own category abbreviations *meta* argument to `store_md.py` .
Problem banner with problem link will be added by `store_md.py`.

**Category Map:**
- `arr` : arrays
- `bin_srch` : binary search
- `bit` : bit manipulation
- `btrack` : backtracking
- `dp` : dynamic programming
- `graph` : graphs
- `greedy` : greedy
- `hash` : hashing
- `heap_map` : heaps and maps
- `link_lt` : linked lists
- `math` : math
- `stk_q` : stacks and queues
- `str` : strings
- `tc` : time complexity
- `tree` : trees
- `two_ptr` : two pointers
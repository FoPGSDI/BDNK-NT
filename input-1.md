* from https://wxu26.github.io/writings/claude_for_research.html extract two md files for templates, using these as guiding principles 

**central task**
* translate the research paper to latex + bibtex format, in physics review D format: @NT-Disk.pdf is a research paper by Novikov and Thorne in pdf format, each page is rotated to the left; each page contains two subpages (similar to a book format)
* first call the plan mode, deploying 28 agents (each agent looking at 1-2 pages), converge on the convension for mathematical expression 
* turn on translate mode, deploying 28 agents (each agent translate 1-2 page), each agent should have its own tex file and bib file
* final agent merge to one tex and bib file, then compile this
* in translate mode, deploying 10 agents (each agent translate 1-2 page, randomly sampled), each agent should have its own tex file and bib file (in check folder); compare the results to the original translation; do this twice
* final agent check and finalize

**FilesAndLinks**
* @NT-Disk.pdf is the original paper
* https://github.com/FoPGSDI/BDNK-NT is the git repo

**Commit-Priciples**
* each subagents commit individually
* one commit should be finalized after each stage
* the progress of each subagent should be documented in md files, the final converged convension should be documented in one md files, the stage progress should be documented in one md files according to the original guideline; these should be shown in progress folder
* we should have stage-wise research diaries and final report for human read

**Managing-Skill**
* from https://wxu26.github.io/writings/claude_for_research.html extract two md files for templates, using these as guiding principles, use these two md directly, modify them to fit the tasks below and keep track of the progress

**central task**
* central target: read through the paper, generate three mark down files for mathematical non-step skipping derivations, and numerical implementations, and tests results and test suits/designs
* read through the research paper in latex + bibtex format @paper.tex and @paper.bbl
* first call (plan mode): deploying one agents, converge on the convension for mathematical expression; one agent for mathematical non-step skipping derivations; one agent for numerical implementations; one agent for tests results and test suits/designs
* based on the plan proceed as follows:
* second call (editting mode): deploying one agents, converge on the convension for mathematical expression; one agent for mathematical non-step skipping derivations; one agent for numerical implementations; one agent for tests results and test suits/designs; simultaneously deploy 6 agents for each pdf plots, add the descriptions and implementation/numerical should-be-awared issues in md files
* in editting mode, deploying 11 agents to repeat the task and double check
* final agent check and finalize the results
* check the python numerical implementation and generated results with the original numerical results, this can be split to 6 agents if no logic dependence exist, iterate till fully consistent with original results
* final agent check and finalize the results

**FilesAndLinks**
* @/arXiv-2509.15303v1/Paper.tex and @/arXiv-2509.15303v1/fluids.bib is the original paper tex
* https://github.com/FoPGSDI/BDNK-NT is the git repo, BDNK-NS branch

**Commit-Priciples**
* cycle progress documentation: commit and push after one cycle ends 
* stage progress documentation: commit and push after one stage ends 
* each subagents commit individually
* one commit should be finalized after each stage
* the progress of each subagent should be documented in md files, the final converged convension should be documented in one md files, the stage progress should be documented in one md files according to the original guideline; these should be shown in progress folder
* we should have stage-wise research diaries and final report for human read